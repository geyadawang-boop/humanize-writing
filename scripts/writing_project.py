#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可续写的小说/剧本项目记录器；stdlib only，不生成正文、不证明文学品质。

退出码：0 操作成功/指定范围检查通过；1 内容未齐、过期或未通过；
2 参数、路径、状态格式、台账结构错误。status 的 0 仅表示已成功显示状态。
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath

STATE_FILE = 'project-state.json'
SCHEMA = 1
TEMPLATES = Path(__file__).resolve().parent.parent / 'templates'
STAGES = {'planning', 'drafting', 'revising', 'paused', 'complete'}
UNIT_STATES = {'planned', 'drafted', 'revised'}
ENDING_IDS = {'main-conflict', 'protagonist-arc', 'aftermath'}
NOVEL_FILES = {
    'story-bible.md': 'story-bible.md',
    'volume-outline.md': 'volume-outline.md',
    **{f'ledger/{name}.md': f'{name}.md' for name in (
        'character-sheet', 'world-rules', 'foreshadowing-ledger',
        'power-ledger', 'outline-changelog', 'chapter-progress')},
}
SCREENPLAY_FILES = {
    'screenplay-bible.md': 'screenplay-bible.md',
    'scene-list.md': 'screenplay-scene-list.md',
    'episode-outline.md': 'screenplay-episode-outline.md',
}


class ProjectError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest_json(value):
    return digest_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(',', ':')).encode('utf-8'))


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def inside(root, relative):
    """Reject absolute paths, traversal, Windows drive/ADS names and symlink escapes."""
    if not text_value(relative) or '\\' in relative or ':' in relative:
        raise ProjectError(f'必须使用项目内 POSIX 相对路径：{relative!r}')
    path = PurePosixPath(relative)
    if path.is_absolute() or PureWindowsPath(relative).drive or '..' in path.parts:
        raise ProjectError(f'路径越界：{relative!r}')
    result = (root / path).resolve()
    try:
        result.relative_to(root.resolve())
    except ValueError as exc:
        raise ProjectError(f'路径/链接指向项目外：{relative!r}') from exc
    if result == root.resolve():
        raise ProjectError('文件路径不能是项目根目录')
    return result


def read_text(root, relative):
    path = inside(root, relative)
    if not path.is_file():
        raise ProjectError(f'文件缺失：{relative}')
    try:
        return path.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        raise ProjectError(f'无法读取 UTF-8 文件 {relative}: {exc}') from exc


def read_json(root, relative):
    try:
        return json.loads(read_text(root, relative))
    except json.JSONDecodeError as exc:
        raise ProjectError(f'JSON 格式错误 {relative}: {exc}') from exc


def create_text(root, relative, text):
    path = inside(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)


def save_state(root, state):
    """Only this declared state file is replaced; manuscript files are never overwritten."""
    dest = inside(root, STATE_FILE)
    temp = inside(root, '.project-state.json.tmp')
    if temp.exists():
        raise ProjectError('存在未处理的 .project-state.json.tmp；先核对并移走它')
    with temp.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(state, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    temp.replace(dest)


def visible_markdown_lines(text):
    """Blank out comments/fenced examples while preserving line positions."""
    output, fence, in_comment = [], None, False
    for raw in text.splitlines():
        if fence is not None:
            char, count = fence
            if re.fullmatch(r'\s*' + re.escape(char) + '{' + str(count) + r',}\s*', raw):
                fence = None
            output.append('')
            continue
        fragments, cursor = [], 0
        while cursor < len(raw):
            if in_comment:
                end = raw.find('-->', cursor)
                if end < 0:
                    break
                in_comment = False
                cursor = end + 3
            else:
                start = raw.find('<!--', cursor)
                if start < 0:
                    fragments.append(raw[cursor:])
                    break
                fragments.append(raw[cursor:start])
                in_comment = True
                cursor = start + 4
        line = ''.join(fragments)
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match.group(1)
            fence = (token[0], len(token))
            output.append('')
        else:
            output.append(line)
    return output


def has_content(text):
    """Reject obvious empty/template-only bodies, not a length/quality score."""
    lines = []
    for line in visible_markdown_lines(text):
        clean = line.strip()
        if not clean or clean.startswith(('#', '>', '```', '|')):
            continue
        clean = re.sub(r'^[-*]\s*(?:\[[ xX]\])?\s*', '', clean)
        if re.fullmatch(r'[\s\-_*{}<>（）()\[\].…]+', clean):
            continue
        if re.fullmatch(r'(?:TODO|TBD|待填写|待补充|待写|正文|示例|placeholder|在此写.*|\{.*?\}|<.*?>)[。.!！]?', clean, re.I):
            continue
        lines.append(clean)
    return bool(lines)


def required_files(state):
    return NOVEL_FILES if state['project']['kind'] == 'novel' else SCREENPLAY_FILES


def validate_state(root, state):
    if not isinstance(state, dict) or state.get('schema_version') != SCHEMA:
        raise ProjectError('不支持的 project-state schema_version')
    project = state.get('project')
    if not isinstance(project, dict) or project.get('kind') not in ('novel', 'screenplay'):
        raise ProjectError('project.kind 必须是 novel 或 screenplay')
    if not all(text_value(project.get(k)) for k in ('title', 'format', 'unit_type')):
        raise ProjectError('project 缺少 title/format/unit_type')
    allowed = {'chapter'} if project['kind'] == 'novel' else {'scene', 'episode'}
    if project['unit_type'] not in allowed:
        raise ProjectError(f'unit_type 应属于 {sorted(allowed)}')
    for key in ('target_units', 'initial_target_units', 'current_volume'):
        if type(project.get(key)) is not int or project[key] < 1:
            raise ProjectError(f'project.{key} 必须是正整数')
    if state.get('stage') not in STAGES or not text_value(state.get('next_step')):
        raise ProjectError('stage 无效或 next_step 为空')
    units = state.get('units')
    if not isinstance(units, list) or len(units) != project['target_units']:
        raise ProjectError('units 数量与 target_units 不一致；用 resize 留下改纲原因')
    seen_ids, seen_paths = set(), set()
    for index, unit in enumerate(units, 1):
        if not isinstance(unit, dict):
            raise ProjectError('units 条目必须是对象')
        uid = unit.get('id')
        if not text_value(uid) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', uid) or uid in seen_ids:
            raise ProjectError(f'重复/无效 unit id：{uid!r}')
        path = inside(root, unit.get('file'))
        if not unit['file'].startswith('manuscript/') or path.suffix not in ('.md', '.txt'):
            raise ProjectError('正文必须是 manuscript/ 内的 .md 或 .txt 文件')
        normalized = str(path).casefold()
        if normalized in seen_paths or unit.get('sequence') != index:
            raise ProjectError('正文路径重复或 sequence 未连续排列')
        if unit.get('status') not in UNIT_STATES or not isinstance(unit.get('summary'), str):
            raise ProjectError(f'{uid} status/summary 无效')
        if not isinstance(unit.get('scenes', []), list):
            raise ProjectError(f'{uid}.scenes 必须是列表')
        dependencies = unit.get('depends_on', [])
        if not isinstance(dependencies, list):
            raise ProjectError(f'{uid}.depends_on 必须是相对文件路径列表')
        for relative in dependencies:
            inside(root, relative)
        seen_ids.add(uid)
        seen_paths.add(normalized)
    expected = project['initial_target_units']
    history = state.get('scope_changes', [])
    if not isinstance(history, list):
        raise ProjectError('scope_changes 必须是列表')
    for event in history:
        if (not isinstance(event, dict) or event.get('from') != expected
                or type(event.get('to')) is not int or event['to'] < 1
                or not text_value(event.get('reason'))):
            raise ProjectError('计划变更链无效；缩减/扩展计划必须说明原因')
        expected = event['to']
    if expected != project['target_units']:
        raise ProjectError('target_units 被直接改动；请恢复并用 resize 记录变更')
    support = state.get('support_files')
    minimum = set(required_files(state)) | {'ending.json', 'session-handoff.md'}
    if not isinstance(support, list) or not minimum.issubset(set(support)):
        raise ProjectError('support_files 缺少该文体必需文件')
    for relative in support:
        inside(root, relative)
    if len(support) != len(set(support)):
        raise ProjectError('support_files 出现重复路径')
    if not isinstance(state.get('reviews'), dict) or not isinstance(state.get('template_hashes'), dict):
        raise ProjectError('reviews/template_hashes 格式错误')
    checkpoint = state.get('checkpoint')
    if checkpoint is not None and not isinstance(checkpoint, dict):
        raise ProjectError('checkpoint 必须是对象或 null；请使用 checkpoint 命令生成')
    if isinstance(checkpoint, dict):
        if not isinstance(checkpoint.get('fingerprint'), str) or not isinstance(checkpoint.get('files'), dict):
            raise ProjectError('checkpoint 缺少 fingerprint/files；请使用 checkpoint 命令生成')
    if not isinstance(state.get('retired_units'), list):
        raise ProjectError('retired_units 格式错误')
    for unit in state['retired_units']:
        if not isinstance(unit, dict):
            raise ProjectError('retired_units 条目错误')
        inside(root, unit.get('file'))
    for record in state['reviews'].values():
        if not isinstance(record, dict):
            raise ProjectError('review 记录必须是对象')
        inside(root, record.get('evidence'))
    return state


def load_state(root):
    return validate_state(root, read_json(root, STATE_FILE))


def snapshot(root, state):
    files = {}
    dependencies = [relative for unit in state['units'] for relative in unit.get('depends_on', [])]
    for relative in sorted(set(state['support_files'] + [u['file'] for u in state['units']] + dependencies)):
        path = inside(root, relative)
        files[relative] = digest_bytes(path.read_bytes()) if path.is_file() else None
    core = {key: state[key] for key in ('project', 'units', 'support_files', 'scope_changes')}
    return {'fingerprint': digest_json({'state': core, 'files': files}), 'files': files}


def review_fingerprint(root, state, scope, snap):
    if scope == 'final':
        return snap['fingerprint']
    unit = unit_record(state, scope)
    paths = sorted(set([unit['file']] + unit.get('depends_on', [])))
    files = {}
    for relative in paths:
        path = inside(root, relative)
        files[relative] = digest_bytes(path.read_bytes()) if path.is_file() else None
    contract = {key: state['project'][key] for key in ('kind', 'format', 'unit_type')}
    return digest_json({'contract': contract, 'unit': unit, 'files': files})


def invalidate(state):
    state['completion'] = None
    if state['stage'] == 'complete':
        state['stage'] = 'revising'


def assert_editable(state):
    if state['stage'] == 'complete':
        raise ProjectError('项目已登记完结；先用 reopen 重开，再修订/续写')


def unit_record(state, uid):
    for unit in state['units']:
        if unit['id'] == uid:
            return unit
    raise ProjectError(f'未知单元：{uid}')


def new_unit(state, sequence):
    prefix = {'chapter': 'CH', 'scene': 'SC', 'episode': 'EP'}[state['project']['unit_type']]
    uid = f'{prefix}{sequence:03d}'
    return {'id': uid, 'sequence': sequence, 'title': '', 'summary': '',
            'file': f'manuscript/{uid}.md', 'status': 'planned', 'scenes': [], 'depends_on': []}


def init_project(root, kind, format_name, units, title, unit_type=None):
    if units < 1:
        raise ProjectError('--units 必须大于零')
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise ProjectError('init 只接受不存在的目录或空目录，禁止覆盖既有项目')
    unit_type = unit_type or ('chapter' if kind == 'novel' else 'scene')
    if unit_type not in ({'chapter'} if kind == 'novel' else {'scene', 'episode'}):
        raise ProjectError('kind 与 unit-type 不相容')
    source = NOVEL_FILES if kind == 'novel' else SCREENPLAY_FILES
    texts = {}
    for relative, template in source.items():
        path = TEMPLATES / template
        if not path.is_file():
            raise ProjectError(f'缺少安装模板：{path}')
        texts[relative] = path.read_text(encoding='utf-8-sig')
    for name in ('session-handoff.md', 'quality-review.md'):
        texts[name] = (TEMPLATES / name).read_text(encoding='utf-8-sig')
    ending = {'ending_note': '', 'promises': [
        {'id': key, 'promise': label, 'disposition': 'open', 'units': [], 'reason': ''}
        for key, label in (('main-conflict', '主冲突'), ('protagonist-arc', '主人公选择与变化'),
                           ('aftermath', '结局后果与余韵'))]}
    texts['ending.json'] = json.dumps(ending, ensure_ascii=False, indent=2) + '\n'
    state = {
        'schema_version': SCHEMA,
        'project': {'title': title, 'kind': kind, 'format': format_name,
                    'unit_type': unit_type, 'initial_target_units': units,
                    'target_units': units, 'current_volume': 1, 'ledger_thresholds': {}},
        'stage': 'planning', 'next_step': '完成立项、文体契约、逐单元计划及故事圣经，再写第一单元。',
        'units': [], 'retired_units': [], 'scope_changes': [],
        'support_files': list(source) + ['ending.json', 'session-handoff.md'],
        'template_hashes': {name: digest_bytes(value.encode('utf-8')) for name, value in texts.items()},
        'checkpoint': None, 'reviews': {}, 'completion': None,
        'created_at': now(), 'updated_at': now(),
    }
    state['units'] = [new_unit(state, i) for i in range(1, units + 1)]
    validate_state(root, state)
    root.mkdir(parents=True, exist_ok=True)
    for relative, text in texts.items():
        create_text(root, relative, text)
    for unit in state['units']:
        create_text(root, unit['file'], f"# {unit['id']}\n\n<!-- 此处写本单元正文；注释和标题不算正文。 -->\n")
    create_text(root, STATE_FILE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    return state


def review_errors(root, state, scope, snap):
    record = state['reviews'].get(scope)
    if not record:
        return [f'{scope} 没有评阅记录']
    errors = []
    if record.get('verdict') != 'pass':
        errors.append(f'{scope} 评阅结论未通过')
    if record.get('fingerprint') != review_fingerprint(root, state, scope, snap):
        errors.append(f'{scope} 评阅过期：本单元正文/计划/显式依赖或全篇终审范围已改变')
    if not text_value(record.get('reviewer')) or record.get('source') not in ('human', 'assisted'):
        errors.append(f'{scope} 评阅人/评阅来源无效')
    evidence = inside(root, record.get('evidence'))
    if not evidence.is_file():
        errors.append(f'{scope} 评阅证据缺失')
    elif (digest_bytes(evidence.read_bytes()) != record.get('evidence_hash')
          or not has_content(read_text(root, record['evidence']))):
        errors.append(f'{scope} 评阅证据为空或已改变，请重新评阅')
    return errors


def ending_errors(root, state):
    ending = read_json(root, 'ending.json')
    if not isinstance(ending, dict) or not isinstance(ending.get('promises'), list):
        raise ProjectError('ending.json 应包含 ending_note 和 promises 列表')
    errors, ids = [], set()
    active = {u['id'] for u in state['units']}
    if not text_value(ending.get('ending_note')):
        errors.append('收尾说明 ending_note 未填写')
    for item in ending['promises']:
        if not isinstance(item, dict) or not text_value(item.get('id')):
            raise ProjectError('终局条目缺少 id')
        if item['id'] in ids:
            raise ProjectError('终局条目 id 重复')
        ids.add(item['id'])
        if not text_value(item.get('promise')) or not text_value(item.get('reason')):
            errors.append(f"收尾 {item['id']} 缺承诺内容/处置理由")
        disposition = item.get('disposition')
        if disposition not in ('resolved', 'intentional-open', 'removed'):
            errors.append(f"收尾 {item['id']} 未处置")
        if item['id'] in ENDING_IDS and disposition != 'resolved':
            errors.append(f"核心收尾 {item['id']} 必须落地；开放结局也要写清本篇作出的选择/后果")
        refs = item.get('units')
        if not isinstance(refs, list) or not refs or any(ref not in active for ref in refs):
            errors.append(f"收尾 {item['id']} 缺有效正文单元证据")
    if not ENDING_IDS.issubset(ids):
        errors.append('收尾缺主冲突/人物弧光/余韵三项中的至少一项')
    return errors


def markdown_cells(line):
    value = line.strip()
    if value.startswith('|'):
        value = value[1:]
    if value.endswith('|') and not value.endswith('\\|'):
        value = value[:-1]
    return [cell.strip().replace('\\|', '|') for cell in re.split(r'(?<!\\)\|', value)]


def markdown_records(text, fields, label):
    """Parse the canonical table, never count IDs mentioned in instructions."""
    lines = visible_markdown_lines(text)
    result = None
    for index, line in enumerate(lines[:-1]):
        if '|' not in line:
            continue
        header = [cell.strip('`') for cell in markdown_cells(line)]
        if not set(fields).issubset(header):
            continue
        separators = markdown_cells(lines[index + 1])
        if not separators or not all(re.fullmatch(r':?-{3,}:?', cell) for cell in separators):
            continue
        if len(separators) != len(header) or len(header) != len(set(header)):
            raise ProjectError(f'{label} 表头重复或分隔行列数不匹配')
        if result is not None:
            raise ProjectError(f'{label} 出现多份同类表，无法确定权威清单')
        result = []
        for data in lines[index + 2:]:
            if not data.strip() or '|' not in data:
                break
            row = markdown_cells(data)
            if len(row) != len(header):
                raise ProjectError(f'{label} 表格行列数不匹配')
            result.append(dict(zip(header, row)))
    if result is None:
        raise ProjectError(f'{label} 缺少规范表头：{", ".join(fields)}')
    return result


def novel_progress_errors(root, state, final=False):
    """Cross-check completed chapter records against actual in-scope prose."""
    import ledger_check
    rows = markdown_records(read_text(root, 'ledger/chapter-progress.md'), ('章',),
                            'ledger/chapter-progress.md')
    recorded = set()
    for row in rows:
        chapter = ledger_check.parse_chapter(row['章'])
        if chapter is None:
            raise ProjectError('章节进度表含无法解析或重复的已完成章号')
        if not any(value.strip() for key, value in row.items() if key != '章'):
            continue  # 模板占位行：只有章号、其余全空，不算完成记录
        if chapter in recorded:
            raise ProjectError('章节进度表含无法解析或重复的已完成章号')
        recorded.add(chapter)
    written = {u['sequence'] for u in state['units'] if u['status'] in ('drafted', 'revised')
               and inside(root, u['file']).is_file() and has_content(read_text(root, u['file']))}
    expected = {u['sequence'] for u in state['units']} if final else written
    errors = []
    missing = sorted(expected - recorded)
    extra = sorted(recorded - written)
    if missing:
        errors.append(f'章节进度表漏记已写/应完成章节：{missing}')
    if extra:
        errors.append(f'章节进度表把未实际写成或范围外章节记为完成：{extra}')
    return errors


def screenplay_errors(root, state, final):
    errors = []
    scene_fields = ('scene_id', 'episode_id', 'setting', 'time', 'participants', 'goal',
                    'obstacle', 'action_turn', 'exit_state', 'duration_estimate', 'status', 'draft_path')
    rows = markdown_records(read_text(root, 'scene-list.md'), scene_fields, 'scene-list.md')
    expected, episode_scenes = {}, {}
    for unit in state['units']:
        uid = unit['id']
        if state['project']['unit_type'] == 'scene':
            expected[uid] = unit
            continue
        scenes = unit.get('scenes', [])
        episode_scenes[uid] = []
        if not scenes:
            errors.append(f'{uid} 未登记本集 scenes；无法验证逐场覆盖')
        body = read_text(root, unit['file']) if inside(root, unit['file']).is_file() else ''
        body_lines = visible_markdown_lines(body)
        markers = set()
        scene_positions = []
        for scene in scenes:
            if not isinstance(scene, dict) or not all(text_value(scene.get(k)) for k in ('id', 'summary', 'marker')):
                raise ProjectError(f'{uid}.scenes 需 id/summary/marker')
            sid, marker = scene['id'], scene['marker']
            if sid in expected or marker in markers:
                raise ProjectError(f'重复 scene id 或场标：{sid}')
            expected[sid] = unit
            markers.add(marker)
            episode_scenes[uid].append(sid)
            positions = [index for index, line in enumerate(body_lines) if line == marker]
            if len(positions) != 1:
                errors.append(f'{uid} 正文需要且仅需一个独立场标行：{marker}')
            else:
                scene_positions.append((positions[0], sid))
        if final:
            ordered = sorted(scene_positions)
            for index, (start, sid) in enumerate(ordered):
                end = ordered[index + 1][0] if index + 1 < len(ordered) else len(body_lines)
                if not has_content('\n'.join(body_lines[start + 1:end])):
                    errors.append(f'{sid} 只有场标，没有动作/对白正文')
    seen, mapped_episodes = set(), {}
    for row in rows:
        sid = row['scene_id']
        if not text_value(sid) or sid in seen:
            raise ProjectError('场景表存在空白或重复 scene_id')
        seen.add(sid)
        if sid not in expected:
            errors.append(f'场景 {sid} 未列入当前正文计划，不能漏写或自动丢弃')
            continue
        unit = expected[sid]
        for field in scene_fields:
            value = row[field]
            if not text_value(value) or re.fullmatch(r'(TODO|TBD|待填写|待补充|\{.*?\}|<.*?>)', value, re.I):
                errors.append(f'场景 {sid} 的 {field} 未填写')
        inside(root, row['draft_path'])
        if row['draft_path'] != unit['file']:
            errors.append(f'场景 {sid} 的 draft_path 与正文计划不一致')
        if row['status'] not in ('drafted', 'revised', 'reviewed'):
            errors.append(f'场景 {sid} 尚未记录为成稿/修订')
        eid = row['episode_id']
        if state['project']['unit_type'] == 'episode' and eid != unit['id']:
            errors.append(f'场景 {sid} 的 episode_id 与单元所属集不一致')
        if eid not in ('N/A', 'NA', 'standalone'):
            mapped_episodes.setdefault(eid, []).append(sid)
    for sid in set(expected) - seen:
        errors.append(f'{sid} 未覆盖在场景表 scene-list.md')
    episode_text = '\n'.join(visible_markdown_lines(read_text(root, 'episode-outline.md')))
    expected_episodes = episode_scenes or mapped_episodes
    if not expected_episodes:
        if not re.search(r'N/A\s*[:：]\s*standalone', episode_text, re.I):
            errors.append('独立作品的 episode-outline.md 需明确 N/A: standalone 并写理由')
    else:
        fields = ('episode_id', 'local_goal', 'entry_state', 'A_B_threads', 'turns',
                  'local_payoff', 'season_delta', 'hook_payoff_link', 'estimated_duration', 'scene_ids', 'status')
        episodes = markdown_records(episode_text, fields, 'episode-outline.md')
        found = set()
        for row in episodes:
            eid = row['episode_id']
            if not text_value(eid) or eid in found:
                raise ProjectError('分集表存在空白或重复 episode_id')
            found.add(eid)
            if eid not in expected_episodes:
                errors.append(f'分集 {eid} 没有范围内场次正文')
                continue
            listed = set(re.split(r'[,，、;；\s]+', row['scene_ids'].strip()))
            if listed != set(expected_episodes[eid]):
                errors.append(f'分集 {eid} 的 scene_ids 与场景计划不一致')
            for field in fields:
                if not text_value(row[field]):
                    errors.append(f'分集 {eid} 的 {field} 未填写')
            if row['status'] not in ('drafted', 'revised', 'reviewed'):
                errors.append(f'分集 {eid} 尚未记录为成稿/修订')
        if found != set(expected_episodes):
            errors.append('分集表未完整覆盖计划内所有集')
    return errors


def inspect_project(root, state, final=False, require_reviews=True):
    root = root.resolve()
    snap = snapshot(root, state)
    errors, structural, warnings = [], [], []
    checkpoint = state.get('checkpoint')
    if not isinstance(checkpoint, dict) or checkpoint.get('fingerprint') != snap['fingerprint']:
        errors.append('没有当前 checkpoint，或正文/计划/台账已改动；先同步后再评阅')
    for unit in state['units']:
        uid, relative = unit['id'], unit['file']
        if not text_value(unit.get('summary')):
            errors.append(f'{uid} 未填写因果性单元计划 summary')
        path = inside(root, relative)
        if not path.is_file():
            errors.append(f'{uid} 正文文件缺失：{relative}')
        elif not has_content(read_text(root, relative)):
            errors.append(f'{uid} 正文为空/仅有标题或占位符')
        if unit['status'] == 'planned':
            errors.append(f'{uid} 尚未记录为 drafted/revised')
        if final and require_reviews:
            errors.extend(review_errors(root, state, uid, snap))
    active_paths = {str(inside(root, u['file'])).casefold() for u in state['units']}
    retired_paths = {str(inside(root, u['file'])).casefold() for u in state['retired_units']}
    manuscript = inside(root, 'manuscript')
    if manuscript.exists():
        for path in manuscript.rglob('*'):
            if path.is_file() and path.suffix.lower() in ('.md', '.txt'):
                relative = path.relative_to(root).as_posix()
                normalized = str(inside(root, relative)).casefold()
                if normalized not in active_paths | retired_paths:
                    errors.append(f'正文未纳入计划或有遗漏：{relative}')
    for relative in state['support_files']:
        path = inside(root, relative)
        if not path.is_file():
            structural.append(f'必需项目文件缺失：{relative}')
        elif digest_bytes(path.read_bytes()) == state['template_hashes'].get(relative):
            errors.append(f'项目文件仍是未填写模板：{relative}')
        elif not path.read_text(encoding='utf-8-sig').strip():
            errors.append(f'项目文件为空：{relative}')
    for unit in state['units']:
        for relative in unit.get('depends_on', []):
            if not inside(root, relative).is_file():
                structural.append(f'{unit["id"]} 的显式依赖文件缺失：{relative}')
    if not structural:
        try:
            if state['project']['kind'] == 'novel':
                import ledger_check
                written = [u['sequence'] for u in state['units'] if u['status'] != 'planned'
                           and inside(root, u['file']).is_file()
                           and has_content(read_text(root, u['file']))]
                rep = ledger_check.run_checks(
                    str(root), cur_ch=max(written) if written else None,
                    cur_vol=state['project']['current_volume'], final=final,
                    thresholds=state['project'].get('ledger_thresholds'))
                errors.extend(rep.red)
                structural.extend(rep.warn)
                warnings.extend(rep.yellow)
                errors.extend(novel_progress_errors(root, state, final=final))
            else:
                errors.extend(screenplay_errors(root, state, final))
            if final:
                errors.extend(ending_errors(root, state))
        except (ValueError, OSError, KeyError, TypeError) as exc:
            structural.append(f'项目依赖检查失败：{exc}')
    if final and require_reviews:
        errors.extend(review_errors(root, state, 'final', snap))
    completion = state.get('completion')
    if state['stage'] == 'complete':
        current_seal = digest_json({'fingerprint': snap['fingerprint'], 'reviews': state['reviews']})
        if not isinstance(completion, dict) or completion.get('seal') != current_seal:
            errors.append('原完结登记已失效，请 reopen 后重新核读、checkpoint、review、complete')
    return {'errors': errors, 'structural_errors': structural, 'warnings': warnings,
            'snapshot': snap, 'exit_code': 2 if structural else (1 if errors else 0)}


def record_review(root, state, scope, reviewer, evidence, verdict, source):
    assert_editable(state)
    if scope != 'final':
        unit_record(state, scope)
    snap = snapshot(root, state)
    if not isinstance(state.get('checkpoint'), dict) or state['checkpoint'].get('fingerprint') != snap['fingerprint']:
        raise ProjectError('先 checkpoint；不能为未同步版本记录评阅')
    if scope != 'final' and not has_content(read_text(root, unit_record(state, scope)['file'])):
        raise ProjectError('空正文不能登记评阅')
    path = inside(root, evidence)
    if not path.is_file() or not has_content(read_text(root, evidence)):
        raise ProjectError('评阅证据必须是项目内有内容的 UTF-8 文本')
    if digest_bytes(path.read_bytes()) == state['template_hashes'].get('quality-review.md'):
        raise ProjectError('未填写的评阅模板不能作通过证据')
    if evidence in state['support_files'] or evidence in [u['file'] for u in state['units']] or evidence == STATE_FILE:
        raise ProjectError('评阅证据须独立于被评阅的正文/台账/状态文件')
    if not text_value(reviewer):
        raise ProjectError('必须填写实际评阅者')
    if scope == 'final' and verdict == 'pass':
        audit = inspect_project(root, state, final=True, require_reviews=False)
        if audit['exit_code']:
            raise ProjectError('最终评阅前仍有内容/结构缺口：' + '; '.join((audit['structural_errors'] + audit['errors'])[:8]))
    state['reviews'][scope] = {'reviewer': reviewer, 'source': source, 'verdict': verdict,
                              'evidence': evidence, 'evidence_hash': digest_bytes(path.read_bytes()),
                              'fingerprint': review_fingerprint(root, state, scope, snap), 'recorded_at': now()}
    invalidate(state)


def resize_project(root, state, target, reason):
    assert_editable(state)
    old = state['project']['target_units']
    if target < 1 or target == old or not text_value(reason):
        raise ProjectError('resize 需不同的正整数目标和具体 --reason')
    if target < old:
        state['retired_units'].extend(copy.deepcopy(state['units'][target:]))
        state['units'] = state['units'][:target]
    else:
        additions = []
        for seq in range(old + 1, target + 1):
            candidate = new_unit(state, seq)
            retired = next((u for u in state['retired_units'] if u['id'] == candidate['id']), None)
            if retired is not None:
                candidate = copy.deepcopy(retired)
            elif inside(root, candidate['file']).exists():
                raise ProjectError(f'新增正文路径已存在且未登记：{candidate["file"]}')
            additions.append(candidate)
        for candidate in additions:
            if not inside(root, candidate['file']).exists():
                create_text(root, candidate['file'], f"# {candidate['id']}\n")
            state['retired_units'] = [u for u in state['retired_units'] if u['id'] != candidate['id']]
        state['units'].extend(additions)
    state['project']['target_units'] = target
    state['scope_changes'].append({'from': old, 'to': target, 'reason': reason.strip(), 'at': now()})
    invalidate(state)


def show(report, state):
    stage = state['stage']
    if stage == 'complete' and report['exit_code']:
        stage += '（旧登记失效，不是有效完结）'
    print(f"{state['project']['title']} | {state['project']['kind']}/{state['project']['format']} | stage={stage}")
    print(f"计划 {len(state['units'])} {state['project']['unit_type']}；下一步：{state['next_step']}")
    completion = state.get('completion')
    if isinstance(completion, dict):
        print(f"完成级别：{completion.get('completion_level', '未记录')}；评阅来源：{completion.get('review_source', '未记录')}")
        if completion.get('review_source') == 'assisted':
            print('评阅边界：未经过独立人工评阅；完成登记不代表可发表。')
    for key, prefix in (('structural_errors', 'ERROR'), ('errors', 'PENDING'), ('warnings', 'WARN')):
        for message in report[key]:
            print(f'{prefix}: {message}')
    print(f"记录检查 exit={report['exit_code']}；机器仅验证内容/记录一致性，不能证明文笔、戏剧效果或事实合规。")


def parser():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='初始化到不存在的/空的项目目录')
    init.add_argument('root', type=Path)
    init.add_argument('--kind', choices=['novel', 'screenplay'], required=True)
    init.add_argument('--format', required=True, dest='format_name')
    init.add_argument('--units', type=int, required=True)
    init.add_argument('--title', default='未命名作品')
    init.add_argument('--unit-type', choices=['chapter', 'scene', 'episode'])
    for name in ('status', 'check', 'complete', 'checkpoint', 'reopen', 'pause', 'resume', 'resize', 'set-unit', 'review'):
        cmd = sub.add_parser(name)
        cmd.add_argument('root', type=Path)
        if name in ('status', 'check'):
            cmd.add_argument('--final', action='store_true')
        if name in ('checkpoint', 'reopen', 'pause', 'resume'):
            cmd.add_argument('--next', required=name in ('reopen', 'pause', 'resume'), dest='next_step')
        if name == 'resize':
            cmd.add_argument('--units', type=int, required=True)
            cmd.add_argument('--reason', required=True)
        if name == 'set-unit':
            cmd.add_argument('unit')
            cmd.add_argument('--summary')
            cmd.add_argument('--title')
            cmd.add_argument('--status', choices=sorted(UNIT_STATES))
        if name == 'review':
            cmd.add_argument('--scope', required=True, help='单元 ID 或 final')
            cmd.add_argument('--reviewer', required=True)
            cmd.add_argument('--source', choices=['human', 'assisted'], required=True)
            cmd.add_argument('--evidence', required=True)
            cmd.add_argument('--verdict', choices=['pass', 'revise'], required=True)
    return ap


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        root = args.root.resolve()
        if args.command == 'init':
            init_project(root, args.kind, args.format_name, args.units, args.title, args.unit_type)
            print(f'已建立未完成项目：{root}；模板和空正文不算完成。')
            return 0
        state = load_state(root)
        command = args.command
        if command in ('status', 'check', 'complete'):
            final = command == 'complete' or args.final or state['stage'] == 'complete'
            report = inspect_project(root, state, final=final)
            show(report, state)
            if command == 'status':
                return 0
            if report['exit_code'] or command == 'check':
                return report['exit_code']
            if state['stage'] == 'paused':
                raise ProjectError('暂停项目先 resume，再 complete')
            state['stage'] = 'complete'
            source = state['reviews']['final']['source']
            level = 'human_review_recorded' if source == 'human' else 'assisted_draft_complete'
            state['next_step'] = '当前范围全稿与所登记来源的评阅已完成；新修订先 reopen。'
            state['completion'] = {'at': now(), 'seal': digest_json({
                'fingerprint': report['snapshot']['fingerprint'], 'reviews': state['reviews']}),
                'review_source': source, 'completion_level': level}
            if source == 'assisted':
                print('已登记完整草稿/辅助终审完成；未经过独立人工评阅，不代表可发表。')
            else:
                print('已登记全稿完成及具名人工评阅记录；工具不独立认证评阅过程或文学品质。')
        elif command == 'checkpoint':
            assert_editable(state)
            invalidate(state)
            state['checkpoint'] = {**snapshot(root, state), 'at': now()}
            if args.next_step:
                state['next_step'] = args.next_step
            if state['stage'] == 'planning':
                state['stage'] = 'drafting'
            print('已同步正文/计划/台账/收尾快照；旧版本评阅不会自动变为有效。')
        elif command == 'review':
            record_review(root, state, args.scope, args.reviewer, args.evidence, args.verdict, args.source)
            print(f'已登记 {args.scope} 的具名评阅；未自动认证其判断。')
        elif command == 'set-unit':
            assert_editable(state)
            unit = unit_record(state, args.unit)
            if args.summary is args.title is args.status is None:
                raise ProjectError('set-unit 至少需要 --summary/--title/--status 之一')
            for field in ('summary', 'title', 'status'):
                value = getattr(args, field)
                if value is not None:
                    unit[field] = value
            invalidate(state)
        elif command == 'resize':
            resize_project(root, state, args.units, args.reason)
        elif command == 'reopen':
            if state['stage'] != 'complete':
                raise ProjectError('项目尚未登记完结，无需重开；暂停项目请用 resume')
            invalidate(state)
            state['stage'] = 'revising'
            state['next_step'] = args.next_step
            state['checkpoint'] = None
            state['reviews'].pop('final', None)
            print('已重开；旧完结与最终评阅已撤销，正文及未变单元的评阅保留。')
        elif command == 'pause':
            assert_editable(state)
            state['resume_stage'] = state['stage'] if state['stage'] != 'paused' else state.get('resume_stage', 'drafting')
            state['stage'] = 'paused'
            state['next_step'] = args.next_step
        elif command == 'resume':
            assert_editable(state)
            if state['stage'] != 'paused':
                raise ProjectError('项目并未暂停')
            state['stage'] = state.pop('resume_stage', 'drafting')
            state['next_step'] = args.next_step
        state['updated_at'] = now()
        validate_state(root, state)
        save_state(root, state)
        return 0
    except (ProjectError, OSError, UnicodeError, TypeError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    # Only the executable entry point owns its streams; importing this module
    # must not alter a host application's or a test runner's output encoding.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='backslashreplace')
    raise SystemExit(main())
