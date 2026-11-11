#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check novel-project ledgers without treating missing evidence as a pass.

Usage: python -B ledger_check.py PROJECT --current-chapter N --current-volume M [--final]
Exit codes: 0 = checks completed without RED (YELLOW is still possible);
1 = RED findings; 2 = invalid/incomplete inputs or usage (takes priority over RED).
Numerical defaults are configurable editorial heuristics, not literary laws.
"""
import argparse
import os
import re
import sys
import tempfile
import unicodedata

SHORT_TERM_MAX_GAP = 15
MID_TERM_MAX_GAP = 50
MID_WAKE_MAX_GAP = 100  # 2 x assumed 50-chapter volumes; configure for the project.
LONG_FERMENT_MAX_GAP = 50
OVERDUE_HARD = 5
OVERDUE_RATIO = 0.20
POWER_LAG_RED = 2
OUTLINE_GAP = 30
QUESTIONS_HARD = 5
CURVE_WINDOW = 4
CURVE_HIGH, CURVE_LOW = 8, 3
DEFAULT_THRESHOLDS = {
    'short_gap': SHORT_TERM_MAX_GAP, 'mid_gap': MID_TERM_MAX_GAP,
    'mid_wake_gap': MID_WAKE_MAX_GAP, 'long_wake_gap': LONG_FERMENT_MAX_GAP,
    'overdue_hard': OVERDUE_HARD, 'overdue_ratio': OVERDUE_RATIO,
    'power_lag_red': POWER_LAG_RED, 'outline_gap': OUTLINE_GAP,
    'questions_hard': QUESTIONS_HARD, 'curve_window': CURVE_WINDOW,
    'curve_high': CURVE_HIGH, 'curve_low': CURVE_LOW,
}
CN_NUM = dict(zip('零〇一二两三四五六七八九', [0, 0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9]))
NUMBER = r'(?:[0-9]+|[零〇一二两三四五六七八九十百千]+)'
EMPTY = {'', '-', '—', '–', '无', '暂无', '待定', '未定'}
PLACEHOLDERS = EMPTY | {'待填', '待补', '待处理', '以后再说', '具体原因', '原因',
                        '处置说明', 'TBD', 'TODO', '待确认', '待核实', 'N/A', 'NA'}


def chinese_number(value):
    if value.isdigit():
        return int(value)
    total, digit = 0, 0
    for char in value:
        if char in CN_NUM:
            digit = CN_NUM[char]
        elif char in '十百千':
            total += (digit or 1) * {'十': 10, '百': 100, '千': 1000}[char]
            digit = 0
        else:
            return None
    return total + digit


def parse_chapter(value):
    """Parse one positive chapter/volume number; reject ranges and arbitrary digits."""
    value = str(value).strip() if value is not None else ''
    direct = re.fullmatch(r'(?:第\s*)?(' + NUMBER + r')\s*(?:章|卷)?', value)
    if direct:
        number = chinese_number(direct.group(1))
        return number if number and number > 0 else None
    matches = re.findall(r'第\s*(' + NUMBER + r')\s*[章卷]', value)
    if len(matches) == 1 and not re.search(r'[-–—~～至到]\s*(?:第\s*)?' + NUMBER, value):
        return chinese_number(matches[0]) or None
    return None


def parse_deadline(value):
    """A planned range ends at its upper bound; a scalar uses that chapter."""
    value = value.strip()
    match = re.fullmatch(r'(?:第\s*)?(' + NUMBER + r')\s*章?\s*[-–—~～至到]\s*'
                         r'(?:第\s*)?(' + NUMBER + r')\s*章?', value)
    if match:
        first, last = map(chinese_number, match.groups())
        return last if 0 < first <= last else None
    return parse_chapter(value)


def _cells(line):
    # A literal pipe in a Markdown cell must be escaped as \|.
    value = line.strip()
    if value.startswith('|'):
        value = value[1:]
    if value.endswith('|') and not value.endswith('\\|'):
        value = value[:-1]
    return [cell.strip().replace('\\|', '|') for cell in re.split(r'(?<!\\)\|', value)]


def parse_tables(text):
    """Return Markdown tables, preserving physical line numbers for diagnostics."""
    tables, lines, index, fence = [], text.splitlines(), 0, None
    while index < len(lines):
        stripped = lines[index].strip()
        marker = re.match(r'^(`{3,}|~{3,})', stripped)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            index += 1
            continue
        if fence is None and stripped.startswith('|') and index + 1 < len(lines):
            separators = _cells(lines[index + 1])
            if separators and all(re.fullmatch(r':?-{3,}:?', cell) for cell in separators):
                header = _cells(stripped)
                table = {'header': header, 'rows': [], 'lines': [], 'line': index + 1,
                         'separator_count': len(separators)}
                index += 2
                while index < len(lines) and '|' in lines[index] and lines[index].strip():
                    table['rows'].append(_cells(lines[index]))
                    table['lines'].append(index + 1)
                    index += 1
                tables.append(table)
                continue
        index += 1
    return tables


def _normal_header(value):
    """Normalize presentation only; never infer roles from substrings."""
    value = unicodedata.normalize('NFKC', str(value).strip())
    for marker in ('**', '__', chr(96)):
        if value.startswith(marker) and value.endswith(marker) and len(value) > 2 * len(marker):
            value = value[len(marker):-len(marker)].strip()
    return re.sub(r'\s+', '', value).casefold()


# Deliberately finite aliases. In particular, a first/planned/actual recovery
# chapter is not the chapter identifier of a progress row.
HEADER_ALIASES = {
    '章': ('章', '章号', '章节', '章节号', '章节编号'),
    '伏笔ID': ('伏笔ID', '伏笔编号'),
    '周期': ('周期',),
    '埋设章节': ('埋设章节', '埋设章', '埋设章号', '埋设章节号'),
    '发酵记录': ('发酵记录',),
    '预计回收章节': ('预计回收章节', '预计回收章', '预计回收章号',
                     '预计回收章节号', '计划回收章节', '计划回收章'),
    '状态': ('状态',),
    '角色名': ('角色名', '角色姓名'),
    '上次更新卷': ('上次更新卷', '上次更新卷号', '上次更新卷次'),
    '生效卷': ('生效卷', '生效卷号', '生效卷次'),
    '适用状态': ('适用状态',),
    '当前章数': ('当前章数', '当前章', '当前章节', '当前章号'),
    '调整方向': ('调整方向',),
    '疑问': ('疑问',),
    '抛出章': ('抛出章', '抛出章节', '抛出章号'),
    '情绪强度': ('情绪强度',),
    '处置说明': ('处置说明',),
    '处置决定': ('处置决定',),
}
_HEADER_ROLES = {_normal_header(alias): role
                 for role, aliases in HEADER_ALIASES.items() for alias in aliases}


def _header_role(value):
    value = _normal_header(value)
    if value in _HEADER_ROLES:
        return _HEADER_ROLES[value]
    # Keep existing template annotations, but not arbitrary chapter qualifiers
    # or an incompatible rating scale that would silently change the numbers.
    annotation = re.fullmatch(r'(状态|周期|适用状态)\([^()]+\)', value)
    if annotation:
        return annotation.group(1)
    if re.fullmatch(r'情绪强度(?:1[-–—~至]10分?|\(1[-–—~至]10分?\))', value):
        return '情绪强度'
    return None


def _columns_for(table, needle):
    role = _header_role(needle)
    return [index for index, head in enumerate(table['header'])
            if (_header_role(head) == role if role is not None
                else _normal_header(head) == _normal_header(needle))]


def find_table(tables, needles, min_hits=1):
    """Rank exact semantic roles; callers must validate completeness and uniqueness."""
    ranked = [(sum(bool(_columns_for(t, needle)) for needle in needles), t) for t in tables]
    candidates = [item for item in ranked if item[0] >= max(min_hits, 1)]
    return max(candidates, key=lambda item: item[0])[1] if candidates else None


def col_of(table, needle):
    matches = _columns_for(table, needle)
    return matches[0] if len(matches) == 1 else None


def decode_bytes(data):
    """按 BOM 与常见中文编码解码；行尾统一为 LF，顺序与 ai_smell_lint 保持一致。"""
    text = None
    for bom, enc in ((b"\xff\xfe\x00\x00", "utf-32"), (b"\x00\x00\xfe\xff", "utf-32"),
                     (b"\xff\xfe", "utf-16"), (b"\xfe\xff", "utf-16")):
        if data.startswith(bom):
            text = data.decode(enc)
            break
    if text is None:
        for enc in ("utf-8-sig", "gbk"):
            try:
                text = data.decode(enc)
                break
            except UnicodeDecodeError:
                continue
    if text is None:
        text = data.decode("utf-8", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read(path):
    with open(path, 'rb') as handle:
        return decode_bytes(handle.read())


def _without_fenced_code(content):
    output, fence = [], None
    for line in content.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            output.append(line)
    return '\n'.join(output)


class Report:
    def __init__(self):
        self.red, self.yellow, self.ok, self.warn = [], [], [], []
        self.thresholds = dict(DEFAULT_THRESHOLDS)

    @property
    def exit_code(self):
        return 2 if self.warn else 1 if self.red else 0

    @property
    def complete(self):
        return not self.warn

    def add(self, level, code, message):
        bucket = {'RED': self.red, 'YELLOW': self.yellow, 'OK': self.ok, 'WARN': self.warn}[level]
        entry = f'[{code}] {message}'
        if entry not in bucket:
            bucket.append(entry)

    def dump(self):
        for level, entries in [('RED', self.red), ('YELLOW', self.yellow),
                               ('WARN', self.warn), ('OK', self.ok)]:
            for entry in entries:
                print(f'{level:6} {entry}')
        status = '检查不完整' if self.warn else '存在红线' if self.red else '有黄线待审' if self.yellow else '已查项未见预警'
        print(f'—— {status}；红线 {len(self.red)} / 黄线 {len(self.yellow)} / '
              f'输入问题 {len(self.warn)} / 通过 {len(self.ok)}；退出码 {self.exit_code}')


def _load_table(rep, path, key, code, required, allow_none=True):
    try:
        content = read(path)
    except (OSError, UnicodeError) as error:
        rep.add('WARN', code, f'{path} 无法读取：{error}')
        return None
    tables = parse_tables(content)
    candidate = find_table(tables, required)
    declarations_content = _without_fenced_code(content)
    declaration = re.findall(
        r'^\s*<!--\s*ledger-check:\s*' + re.escape(key) +
        r'\s*=\s*(none|not-applicable)\s*;\s*reason\s*=\s*(.+?)\s*-->\s*$', declarations_content, re.M)
    if declaration:
        if len(declaration) != 1 or not allow_none:
            rep.add('WARN', code, f'{key} 的免检声明重复或不适用于此检查')
            return None
        mode, reason = declaration[0]
        expected = 'not-applicable' if key == 'power' else 'none'
        has_rows = any(any(cell.strip() for cell in row) for t in tables
                       if any(_columns_for(t, needle) for needle in required)
                       for row in t['rows'])
        if mode != expected or reason.strip() in PLACEHOLDERS:
            rep.add('WARN', code, f'{key} 免检声明须使用 {expected} 并填写具体原因')
        elif has_rows:
            rep.add('WARN', code, f'{key} 声明无记录/不适用，但表中仍有数据或占位行；请核对')
        else:
            rep.add('OK', code, f'{key} 已明确声明 {mode}：{reason}')
            return None
    elif re.search(r'<!--\s*ledger-check:\s*' + re.escape(key) + r'\s*=', declarations_content):
        rep.add('WARN', code, f'{key} 免检声明格式错误；需附 reason=具体原因')
    if not candidate:
        rep.add('WARN', code, f'{path} 未识别台账表（需列：{" / ".join(required)}）')
        return None
    missing = [needle for needle in required if not _columns_for(candidate, needle)]
    roles = dict.fromkeys(_header_role(head) for head in candidate['header'])
    duplicate = [role for role in roles
                 if role is not None and len(_columns_for(candidate, role)) > 1]
    if missing or duplicate or candidate['separator_count'] != len(candidate['header']):
        rep.add('WARN', code, f'{path} 第 {candidate["line"]} 行表头错误；'
                f'缺列={missing}，重复列={duplicate}，表头/分隔列数须相等')
        return None
    complete_tables = [t for t in tables if all(_columns_for(t, needle) for needle in required)]
    if len(complete_tables) != 1:
        rep.add('WARN', code, f'{path} 有多张同类表，无法确定唯一事实台账；请合并')
        return None
    return candidate


def _rows(rep, table, code):
    rows = []
    for line, row in zip(table['lines'], table['rows']):
        if len(row) != len(table['header']):
            rep.add('WARN', code, f'第 {line} 行有 {len(row)} 列，表头为 {len(table["header"])} 列；未将错位行计为有效数据')
        elif any(cell.strip() for cell in row):
            rows.append((line, row))
    if not rows:
        rep.add('WARN', code, '台账没有有效数据行；空表/空白占位不等于检查通过，确实无记录时需明确声明')
    return rows


def _state(value, choices):
    for choice in sorted(choices, key=len, reverse=True):
        if re.match(re.escape(choice) + r'(?:$|[\s：（(])', value.strip()):
            return choice
    return None


def _cell(table, row, needle, default=''):
    index = col_of(table, needle)
    return row[index] if index is not None else default


def _reason(state, table, row):
    note = _cell(table, row, '处置说明') or _cell(table, row, '处置决定')
    if note.strip() not in PLACEHOLDERS:
        return note.strip()
    match = re.search(r'[:：（(]\s*(.+?)\s*[）)]?$', state)
    reason = match.group(1).strip(' ()（）') if match else ''
    return reason if reason not in PLACEHOLDERS else ''


def _thresholds(rep, overrides):
    result = dict(DEFAULT_THRESHOLDS)
    if overrides is not None:
        if not isinstance(overrides, dict):
            rep.add('WARN', 'CONFIG', 'thresholds 必须为字典')
            return None
        unknown = set(overrides) - set(result)
        if unknown:
            rep.add('WARN', 'CONFIG', f'未知阈值：{sorted(unknown)}')
            return None
        result.update(overrides)
    for key, value in result.items():
        valid = (not isinstance(value, bool) and isinstance(value, (int, float))
                 and 0 <= value <= 1) if key == 'overdue_ratio' else (
                     type(value) is int and value >= (0 if key in {'overdue_hard', 'questions_hard'} else 1))
        if not valid:
            rep.add('WARN', 'CONFIG', f'{key} 阈值无效：{value!r}')
    numeric_curve = all(type(result[k]) is int for k in ('curve_low', 'curve_high'))
    if not numeric_curve or not (1 <= result['curve_low'] < result['curve_high'] <= 10):
        rep.add('WARN', 'CONFIG', '情绪阈值须满足 1 <= curve_low < curve_high <= 10')
    if isinstance(result['curve_window'], int) and result['curve_window'] < 2:
        rep.add('WARN', 'CONFIG', 'curve_window 至少为 2')
    return None if rep.warn else result


def check_foreshadowing(rep, ledger, cur_ch, thresholds=None, final=False):
    """Explicit plans win; deadline and memory-refresh clocks are independent.

    Source: novel-craft 黄金时间窗口/超计划章节; foreshadowing-craft 总账.
    An unplanned mid-term default of 50 and refresh default of 100 are configurable
    chapter proxies, not an assertion that every volume has 50 chapters.
    """
    cfg = thresholds or rep.thresholds
    before = len(rep.warn)
    table = _load_table(rep, os.path.join(ledger, 'foreshadowing-ledger.md'), 'foreshadowing',
                        'F-LEDGER', ['伏笔ID', '周期', '埋设章节', '发酵记录', '预计回收章节', '状态'])
    if table is None:
        return
    rows = _rows(rep, table, 'F-ROW')
    if cur_ch is None:
        rep.add('WARN', 'F-CONTEXT', '缺 --current-chapter，无法判断已生效/未来条目及回收/唤醒时间')
    active, overdue, refresh, seen, planned = [], [], [], set(), 0
    closed = {'已回收', '已废弃', '留续作', '已取消'}
    not_active = {'计划中', '未埋设', '待埋设', '未生效'}
    states = closed | not_active | {'未发酵', '发酵中', '已埋设', '未回收', '待回收', '逾期'}
    for line, row in rows:
        fid, state_text = _cell(table, row, '伏笔ID'), _cell(table, row, '状态')
        if not fid or fid in seen:
            rep.add('WARN', 'F-ID', f'第 {line} 行伏笔ID为空或重复：{fid!r}')
            continue
        seen.add(fid)
        state = _state(state_text, states)
        cycle = _state(_cell(table, row, '周期'), {'短期', '中期', '长期'})
        plant = parse_chapter(_cell(table, row, '埋设章节'))
        if state is None or cycle is None or plant is None:
            rep.add('WARN', 'F-PARSE', f'{fid} 第 {line} 行的状态/周期/埋设章节无效或仍是占位符')
            continue
        raw_plan = _cell(table, row, '预计回收章节')
        due = None if raw_plan in EMPTY else parse_deadline(raw_plan)
        if raw_plan not in EMPTY and due is None:
            rep.add('WARN', 'F-PLAN', f'{fid} 预计回收章节无法解析：{raw_plan!r}；未使用默认值掩盖错值')
        if due is not None and due < plant:
            rep.add('WARN', 'F-ORDER', f'{fid} 预计回收第{due}章早于埋设第{plant}章')
        ferment = []
        raw_ferment = _cell(table, row, '发酵记录')
        if raw_ferment not in EMPTY:
            for item in re.split(r'[,，、;；]|<br\s*/?>', raw_ferment):
                if not item.strip():
                    continue
                number = parse_chapter(item.strip())
                if number is None:
                    rep.add('WARN', 'F-FERMENT-PARSE', f'{fid} 发酵记录无法解析：{item!r}')
                elif number < plant or (cur_ch is not None and number > cur_ch):
                    rep.add('WARN', 'F-FERMENT-TIME', f'{fid} 发酵第{number}章早于埋设或晚于当前章，未用于抵消断档')
                else:
                    ferment.append(number)
        future = cur_ch is not None and plant > cur_ch
        if future and state in closed - {'已取消'}:
            rep.add('WARN', 'F-TIME', f'{fid} 埋设第{plant}章尚未到达，却已标为 {state}')
        reason = _reason(state_text, table, row)
        if final:
            if state not in closed:
                rep.add('RED', 'X-DANGLE', f'完结未闭合：{fid}（{state_text}）；计划回收/未来埋设不能冒充已完成处置')
            elif state in {'已废弃', '留续作', '已取消'} and not reason:
                rep.add('RED', 'X-DISPOSITION', f'{fid} 仅标 {state}，缺处置说明；需解释读者承诺如何收束或后续承接')
        if state in closed:
            continue
        if future or state in not_active:
            planned += 1
            if not future and cur_ch is not None:
                rep.add('YELLOW', 'F-NOT-ACTIVE', f'{fid} 计划埋设章已到但仍标 {state}；请对照正文确认，未计入已生效分母')
            continue
        active.append(fid)
        if cur_ch is None:
            continue
        if raw_plan in EMPTY:
            fallback = cfg['short_gap'] if cycle == '短期' else cfg['mid_gap'] if cycle == '中期' else None
            due = plant + fallback if fallback is not None else None
            detail = f'暂按埋后 {fallback} 章作审计窗口' if fallback is not None else '长期伏笔须人工确定高潮前的兑现点'
            rep.add('YELLOW', 'F-NO-PLAN', f'{fid} 未填预计回收章；{detail}，不视为普适写作期限')
        if due is not None and cur_ch > due:
            overdue.append(fid)
            origin = '项目计划' if raw_plan not in EMPTY else '默认审计窗口'
            rep.add('YELLOW', 'F-OVERDUE', f'{fid} 超 {origin} 第{due}章 {cur_ch - due}章（{cycle}，第{plant}章埋）')
        if cycle in {'中期', '长期'}:
            last = max([plant] + ferment)
            window = cfg['mid_wake_gap'] if cycle == '中期' else cfg['long_wake_gap']
            if cur_ch - last > window:
                refresh.append(fid)
                rep.add('YELLOW', 'F-FERMENT', f'{fid} 距上次埋设/发酵第{last}章已 {cur_ch - last}章，'
                        f'超过本次 {window}章唤醒窗口；补发酵不等于完成回收')
    if overdue and len(overdue) > cfg['overdue_hard']:
        rep.add('RED', 'F-HARD', f'逾期 {len(overdue)} 项 > {cfg["overdue_hard"]}；请逐条审查计划与处置')
    if overdue and active and len(overdue) / len(active) > cfg['overdue_ratio']:
        rep.add('RED', 'F-RATIO', f'已生效未处置伏笔中逾期 {len(overdue)}/{len(active)} '
                f'({len(overdue) / len(active):.0%}) > {cfg["overdue_ratio"]:.0%}；未来/未埋设/已处置行不计分母')
    if rows and len(rep.warn) == before and not overdue and not refresh:
        rep.add('OK', 'F-LEDGER', f'已生效未处置 {len(active)} 条，未生效 {planned} 条；未见逾期/唤醒断档（不等于正文质量认证）')
    if final and rows and len(rep.warn) == before and not any('[X-DANGLE]' in s or '[X-DISPOSITION]' in s for s in rep.red):
        rep.add('OK', 'X-FINAL', '伏笔台账逐行有终态处置；仍需人工核对正文是否实际兑现')


def check_power(rep, ledger, cur_vol, thresholds=None):
    """Classify lag per applicable row; one severe lag never promotes another row."""
    cfg = thresholds or rep.thresholds
    before = len(rep.warn)
    table = _load_table(rep, os.path.join(ledger, 'power-ledger.md'), 'power',
                        'P-LEDGER', ['角色名', '上次更新卷'])
    if table is None:
        return
    rows = _rows(rep, table, 'P-ROW')
    if cur_vol is None:
        rep.add('WARN', 'P-CONTEXT', '适用战力表却缺 --current-volume，无法检查更新断档')
    stale, applicable, planned, seen = 0, 0, 0, set()
    inactive = {'未登场', '计划中', '未生效', '不适用', '已退出', '退场', '死亡'}
    active = {'适用', '在场', '活跃', '当前', '生效'}
    for line, row in rows:
        name = _cell(table, row, '角色名')
        if not name or name in seen:
            rep.add('WARN', 'P-NAME', f'第 {line} 行角色名为空或重复：{name!r}')
            continue
        seen.add(name)
        raw_state = _cell(table, row, '适用状态', _cell(table, row, '状态', '适用'))
        state = _state(raw_state, active | inactive)
        if state is None:
            rep.add('WARN', 'P-STATE', f'{name} 适用状态无效：{raw_state!r}')
            continue
        raw_start = _cell(table, row, '生效卷')
        start = None if raw_start in EMPTY else parse_chapter(raw_start)
        if raw_start not in EMPTY and start is None:
            rep.add('WARN', 'P-START', f'{name} 生效卷无法解析：{raw_start!r}')
            continue
        if state in inactive or (start is not None and cur_vol is not None and start > cur_vol):
            planned += 1
            continue
        updated = parse_chapter(_cell(table, row, '上次更新卷'))
        if updated is None:
            rep.add('WARN', 'P-PARSE', f'{name} 上次更新卷无效或仍是占位符')
            continue
        applicable += 1
        if cur_vol is None:
            continue
        lag = cur_vol - updated
        if lag < 0:
            rep.add('WARN', 'P-FUTURE', f'{name} 上次更新第{updated}卷晚于当前第{cur_vol}卷，不能据此判同步')
        elif lag >= 1:
            stale += 1
            rep.add('RED' if lag >= cfg['power_lag_red'] else 'YELLOW', 'P-STALE',
                    f'{name} 上次更新第{updated}卷，落后 {lag} 卷；按角色逐行审计')
    if rows and len(rep.warn) == before and not stale:
        rep.add('OK', 'P-LEDGER', f'当前卷适用 {applicable} 行无更新断档；未生效/不适用 {planned} 行未计入')


def check_outline(rep, ledger, cur_ch, thresholds=None):
    cfg = thresholds or rep.thresholds
    before = len(rep.warn)
    table = _load_table(rep, os.path.join(ledger, 'outline-changelog.md'), 'outline',
                        'O-LEDGER', ['当前章数', '调整方向'])
    if table is None:
        return
    rows, chapters = _rows(rep, table, 'O-ROW'), []
    if cur_ch is None:
        rep.add('WARN', 'O-CONTEXT', '缺 --current-chapter，无法检查大纲调整记录时间')
    for line, row in rows:
        chapter = parse_chapter(_cell(table, row, '当前章数'))
        if chapter is None:
            rep.add('WARN', 'O-PARSE', f'第 {line} 行当前章数无效')
        elif cur_ch is not None and chapter > cur_ch:
            rep.add('WARN', 'O-FUTURE', f'第 {line} 行调整记录在未来第{chapter}章，未作为最近完成记录')
        else:
            chapters.append(chapter)
    if chapters and cur_ch is not None:
        last = max(chapters)
        if cur_ch - last > cfg['outline_gap']:
            rep.add('YELLOW', 'O-GAP', f'距最近调整第{last}章已 {cur_ch - last}章；请确认是否有未记偏离，按纲推进可说明后保持原纲')
        elif len(rep.warn) == before:
            rep.add('OK', 'O-GAP', f'最近已发生的大纲调整记录在第{last}章（按章号而非表格行序）')


def check_questions(rep, root, cur_ch, thresholds=None, final=False):
    cfg = thresholds or rep.thresholds
    before = len(rep.warn)
    table = _load_table(rep, os.path.join(root, 'story-bible.md'), 'questions',
                        'Q-BIBLE', ['疑问', '抛出章', '状态'])
    if table is None:
        return
    rows, pending, seen, future_count = _rows(rep, table, 'Q-ROW'), [], set(), 0
    if cur_ch is None:
        rep.add('WARN', 'Q-CONTEXT', '缺 --current-chapter，无法区分已抛出和未来计划疑问')
    closed = {'已答', '已解决', '永不答'}
    planned = {'计划中', '未抛出', '待抛出', '未生效', '已取消'}
    for line, row in rows:
        question, raw_state = _cell(table, row, '疑问'), _cell(table, row, '状态')
        state = _state(raw_state, closed | planned | {'延迟', '未答', '待答', '挂起', '未解决'})
        chapter = parse_chapter(_cell(table, row, '抛出章'))
        if not question or question in seen or state is None or chapter is None:
            rep.add('WARN', 'Q-PARSE', f'第 {line} 行疑问为空/重复，或状态/抛出章无法解析')
            continue
        seen.add(question)
        future = cur_ch is not None and chapter > cur_ch
        if future and state in closed:
            rep.add('WARN', 'Q-FUTURE', f'{question} 尚未到抛出章却已标 {state}')
        if final and state not in closed | {'已取消'}:
            rep.add('RED', 'X-QUESTION', f'完结仍有未处置疑问：{question}（{state}）；延迟或未来计划不能算已答')
        if final and state in {'永不答', '已取消'} and not _reason(raw_state, table, row):
            rep.add('RED', 'X-QDISPOSITION', f'{question} 标 {state} 但无处置说明，请说明留白或取消的依据')
        if state in closed | {'已取消'}:
            continue
        if future or state in planned:
            future_count += 1
            continue
        pending.append(question)
    if len(pending) > cfg['questions_hard']:
        for question in pending:
            rep.add('YELLOW', 'Q-PEND', f'已抛出未答：{question}')
        rep.add('RED', 'Q-HARD', f'已抛出未答 {len(pending)} 个 > {cfg["questions_hard"]}；延迟仍占读者注意力，需实际回应或有依据地处置')
    elif len(pending) >= 3:
        for question in pending:
            rep.add('YELLOW', 'Q-PEND', f'已抛出未答：{question}；安排回应')
    elif rows and len(rep.warn) == before:
        rep.add('OK', 'Q-BIBLE', f'已抛出未答 {len(pending)} 个；未来/未抛出 {future_count} 个未计入当前负担')


def check_curve(rep, ledger, cur_ch=None, thresholds=None):
    cfg = thresholds or rep.thresholds
    before = len(rep.warn)
    table = _load_table(rep, os.path.join(ledger, 'chapter-progress.md'), 'curve',
                        'C-LEDGER', ['章', '情绪强度'], allow_none=False)
    if table is None:
        return
    rows, scores, seen = _rows(rep, table, 'C-ROW'), [], set()
    if cur_ch is None:
        rep.add('WARN', 'C-CONTEXT', '缺 --current-chapter，无法确定已完成章节的情绪窗口')
    for line, row in rows:
        chapter = parse_chapter(_cell(table, row, '章'))
        if chapter is None or chapter in seen:
            rep.add('WARN', 'C-CHAPTER', f'第 {line} 行章号无效或重复')
            continue
        seen.add(chapter)
        if cur_ch is not None and chapter > cur_ch:
            continue
        raw_state = _cell(table, row, '状态')
        if raw_state and _state(raw_state, {'计划中', '待写', '未生效'}):
            rep.add('WARN', 'C-NOT-WRITTEN', f'第{chapter}章在当前章范围内却尚未写成，不能按计划分数审计正文')
            continue
        raw_score = _cell(table, row, '情绪强度')
        match = re.fullmatch(r'(10|[1-9])(?:\s*分|\s*/\s*10)?', raw_score)
        if not match:
            rep.add('WARN', 'C-SCORE', f'第{chapter}章情绪强度须为 1–10，收到 {raw_score!r}')
            continue
        scores.append((chapter, int(match.group(1))))
    if cur_ch is None:
        return
    if not scores:
        rep.add('WARN', 'C-NO-COMPLETED', f'截至当前第{cur_ch}章没有有效的已完成章节记录；未来计划不能替代正文进度')
        return
    scores.sort()
    window = cfg['curve_window']
    tail = scores[-window:]
    if tail[-1][0] != cur_ch:
        rep.add('WARN', 'C-CURRENT', f'当前第{cur_ch}章缺有效情绪记录，最新有效记录为第{tail[-1][0]}章')
    if any(right[0] != left[0] + 1 for left, right in zip(tail, tail[1:])):
        rep.add('WARN', 'C-GAP', f'最近记录章号不连续：{[ch for ch, _ in tail]}；不能宣称连续 {window}章')
        return
    if len(rep.warn) != before:
        return
    if len(tail) < window:
        rep.add('OK', 'C-SAMPLE', f'当前仅 {len(tail)} 个连续有效章节，不足 {window}章预警窗口；未判定曲线健康')
    elif all(score >= cfg['curve_high'] for _, score in tail):
        rep.add('YELLOW', 'C-HIGH', f'最近 {window}个已完成连续章节情绪均 >= {cfg["curve_high"]}：{tail}；人工检查是否需要喘息')
    elif all(score <= cfg['curve_low'] for _, score in tail):
        rep.add('YELLOW', 'C-LOW', f'最近 {window}个已完成连续章节情绪均 <= {cfg["curve_low"]}：{tail}；人工检查是否缺少改变处境的事件')
    else:
        rep.add('OK', 'C-CURVE', f'近 {window}章未命中高/低同区阈值：{tail}；不代表所有章节有起伏')


def check_final(rep, ledger, cur_ch=None):
    """Compatibility entry point; run_checks integrates final checking once."""
    check_foreshadowing(rep, ledger, cur_ch, final=True)


def run_checks(root, cur_ch=None, cur_vol=None, final=False, thresholds=None):
    """Return Report; callers can inspect red/yellow/ok/warn, complete, exit_code."""
    rep = Report()
    cfg = _thresholds(rep, thresholds)
    if cfg is None:
        return rep
    rep.thresholds = cfg
    for name, value in [('current-chapter', cur_ch), ('current-volume', cur_vol)]:
        if value is not None and (type(value) is not int or value < 1):
            rep.add('WARN', 'CONTEXT', f'{name} 必须是正整数或 None，收到 {value!r}')
    if rep.warn:
        return rep
    if not os.path.isdir(root):
        rep.add('WARN', 'IO', f'项目目录不存在：{root}')
        return rep
    ledger = os.path.join(root, 'ledger')
    check_foreshadowing(rep, ledger, cur_ch, cfg, final)
    check_power(rep, ledger, cur_vol, cfg)
    check_outline(rep, ledger, cur_ch, cfg)
    check_questions(rep, root, cur_ch, cfg, final)
    check_curve(rep, ledger, cur_ch, cfg)
    return rep


def demo():
    """Deliberately red fixture: API and CLI still return 1 when detection succeeds."""
    with tempfile.TemporaryDirectory() as root:
        os.makedirs(os.path.join(root, 'ledger'))
        header = '| 伏笔ID | 内容 | 类型 | 周期 | 埋设章节 | 发酵记录 | 预计回收章节 | 重要性 | 状态 |\n'
        separator = '|---|---|---|---|---|---|---|---|---|\n'
        rows = ''.join(f'| F-{n} | 示例 | 剧情 | 中期 | 第{n}章 | 无 | 第30章 | ★ | 未发酵 |\n' for n in range(1, 7))
        rows += '| F-7 | 长线 | 剧情 | 长期 | 第1章 | 第10章 | 第100章 | ★ | 发酵中 |\n'
        files = {
            'ledger/foreshadowing-ledger.md': header + separator + rows,
            'ledger/power-ledger.md': '| 角色名 | 上次更新卷 |\n|---|---|\n| 甲 | 第1卷 |\n| 乙 | 第2卷 |\n',
            'ledger/outline-changelog.md': '| 当前章数 | 调整方向 |\n|---|---|\n| 第40章 | 改支线 |\n',
            'story-bible.md': '| 疑问 | 抛出章 | 状态 |\n|---|---|---|\n' +
                ''.join(f'| Q{n} | 第{n}章 | 延迟 |\n' for n in range(1, 7)),
            'ledger/chapter-progress.md': '| 章 | 情绪强度 |\n|---|---|\n' +
                ''.join(f'| {n} | 9 |\n' for n in range(81, 85)),
        }
        for relative, content in files.items():
            with open(os.path.join(root, relative), 'w', encoding='utf-8', newline='\n') as handle:
                handle.write(content)
        rep = run_checks(root, 84, 3, True)
        rep.dump()
        codes = ' '.join(rep.red + rep.yellow)
        expected = ['F-HARD', 'F-RATIO', 'F-OVERDUE', 'F-FERMENT', 'P-STALE',
                    'O-GAP', 'Q-HARD', 'C-HIGH', 'X-DANGLE']
        missing = [code for code in expected if code not in codes]
        if missing or rep.warn or rep.exit_code != 1:
            print('DEMO FAIL', missing, rep.warn)
            return 2
        print('DEMO PASS：预设九类预警均命中；示例含红线，退出码按约定为 1')
        return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_root', nargs='?')
    parser.add_argument('--current-chapter', type=int)
    parser.add_argument('--current-volume', type=int)
    parser.add_argument('--final', action='store_true', help='审计伏笔与疑问是否已有明确终态处置')
    parser.add_argument('--demo', action='store_true')
    for key, default in DEFAULT_THRESHOLDS.items():
        parser.add_argument('--' + key.replace('_', '-'), dest=key,
                            type=float if key == 'overdue_ratio' else int,
                            help=f'可覆盖的项目审计阈值，默认 {default}')
    args = parser.parse_args()
    if args.demo:
        return demo()
    if not args.project_root:
        parser.error('需要 project_root 或 --demo')
    cfg = {key: getattr(args, key) for key in DEFAULT_THRESHOLDS if getattr(args, key) is not None}
    rep = run_checks(args.project_root, args.current_chapter, args.current_volume, args.final, cfg)
    rep.dump()
    if rep.warn:
        print('WARN 表示检查不完整，不得据此宣布台账健康或作品已完结。修正输入后重跑。')
    return rep.exit_code


if __name__ == '__main__':
    sys.exit(main())
