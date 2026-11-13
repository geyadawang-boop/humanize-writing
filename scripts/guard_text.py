# -*- coding: utf-8 -*-
"""guard_text.py — 受保护内容机械比对（humanize-writing skill）

用法:
    python -B scripts/guard_text.py 改前.md 改后.md
    python -B scripts/guard_text.py 改前.md 改后.md --json
    python -B scripts/guard_text.py 改前.md 改后.md --strict
    python -B scripts/guard_text.py 改前.md 改后.md --allow 允许例外.json

比对 frontmatter、围栏代码、行内代码、链接目标、标题层级、表格结构、
有序列表条目数与显式 ID。只报告可机械识别的结构变化，不判断事实、
语义、文学质量或作者身份；未列出不等于未改动。

默认报告式：即使有 hard 项也返回 0；--strict 时存在未登记的 hard 项
才返回 1。退出码 2 表示输入或参数错误。
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_smell_lint as lint  # noqa: E402

FENCE_RE = re.compile(
    r"^[ \t]{0,3}(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^\n]*)\n"
    r"(?P<body>.*?)^[ \t]{0,3}(?P=fence)[ \t]*$",
    re.M | re.S,
)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---[ \t]*(?:\n|$)", re.S)
INLINE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M)
LINK_RE = re.compile(r"\]\(([^)\n]*)\)")
REF_LINK_RE = re.compile(r"^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*(\S+)", re.M)
HTML_URL_RE = re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
ID_RE = re.compile(r"<[^>\n]*\bid\s*=\s*[\"']([^\"']+)[\"'][^>\n]*>", re.I)
TABLE_LINE_RE = re.compile(r"^[ \t]*\|.*\|[ \t]*$")
ORDERED_RE = re.compile(r"^[ \t]*(\d+)[.)][ \t]+(.+?)[ \t]*$")


def _line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def _blank_spans(text, spans):
    """用空格遮罩区间，保留换行，避免代码内容被后续结构正则误抽。"""
    chars = list(text)
    for start, end in spans:
        for i in range(start, end):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def _normalize_space(value):
    return re.sub(r"[ \t\u3000]+", " ", value).strip()


def _link_target(raw):
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        raw = raw[1:raw.index(">")]
    else:
        raw = re.split(r"[ \t]+[\"']", raw, 1)[0]
    raw = raw.split("#", 1)[0]
    return raw.strip()


def _yaml_keys(raw):
    keys = {}
    lines = raw.splitlines()
    for line in lines[1:-1]:
        m = re.match(r"^([A-Za-z0-9_-]+)[ \t]*:[ \t]*(.*)$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    return keys


def _table_cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def _tables(masked):
    lines = masked.split("\n")
    out, i = [], 0
    while i < len(lines):
        if not TABLE_LINE_RE.match(lines[i]):
            i += 1
            continue
        start = i
        rows = []
        while i < len(lines) and TABLE_LINE_RE.match(lines[i]):
            rows.append(_table_cells(lines[i]))
            i += 1
        out.append({"line": start + 1, "rows": rows})
    return out


def _ordered_lists(masked):
    lines = masked.split("\n")
    out, i = [], 0
    while i < len(lines):
        if not ORDERED_RE.match(lines[i]):
            i += 1
            continue
        start = i
        items = []
        while i < len(lines):
            m = ORDERED_RE.match(lines[i])
            if not m:
                break
            items.append({
                "number": int(m.group(1)),
                "text": _normalize_space(m.group(2)),
                "line": i + 1,
            })
            i += 1
        out.append({"line": start + 1, "items": items})
    return out


def _extract(text):
    frontmatter = {"status": "absent", "raw": None, "keys": {}, "line": 1}
    spans = []
    match = FRONTMATTER_RE.match(text)
    if match:
        raw = match.group(0).rstrip("\n")
        frontmatter = {
            "status": "present",
            "raw": raw,
            "keys": _yaml_keys(raw),
            "line": 1,
        }
        spans.append((0, match.end()))
    elif text.startswith("---\n"):
        frontmatter = {"status": "unclosed", "raw": None, "keys": {}, "line": 1}

    code_blocks = []
    for m in FENCE_RE.finditer(text):
        code_blocks.append({
            "value": (m.group("info").strip(), m.group("body").rstrip("\n")),
            "info": m.group("info").strip(),
            "line": _line_of(text, m.start()),
        })
        spans.append((m.start(), m.end()))
    masked = _blank_spans(text, spans)

    inline_code, inline_spans = [], []
    for m in INLINE_RE.finditer(masked):
        inline_code.append({"value": m.group(2), "line": _line_of(masked, m.start())})
        inline_spans.append((m.start(), m.end()))
    masked = _blank_spans(masked, inline_spans)

    headings = []
    for m in HEADING_RE.finditer(masked):
        headings.append({
            "level": len(m.group(1)),
            "text": _normalize_space(m.group(2)),
            "line": _line_of(masked, m.start()),
        })

    link_targets = []
    for m in LINK_RE.finditer(masked):
        target = _link_target(m.group(1))
        if target:
            link_targets.append({"value": target, "line": _line_of(masked, m.start())})
    for m in REF_LINK_RE.finditer(masked):
        target = _link_target(m.group(1))
        if target:
            link_targets.append({"value": target, "line": _line_of(masked, m.start())})
    for m in HTML_URL_RE.finditer(masked):
        target = _link_target(m.group(1))
        if target:
            link_targets.append({"value": target, "line": _line_of(masked, m.start())})

    return {
        "frontmatter": frontmatter,
        "code_blocks": code_blocks,
        "inline_code": inline_code,
        "headings": headings,
        "link_targets": link_targets,
        "tables": _tables(masked),
        "ordered_lists": _ordered_lists(masked),
        "explicit_ids": [
            {"value": m.group(1), "line": _line_of(masked, m.start())}
            for m in ID_RE.finditer(masked)
        ],
    }


def _missing(before_items, after_items, key):
    after_counts = Counter(key(item) for item in after_items)
    lost = []
    for item in before_items:
        value = key(item)
        if after_counts[value] > 0:
            after_counts[value] -= 1
        else:
            lost.append(item)
    return lost


def _added(before_items, after_items, key):
    before_counts = Counter(key(item) for item in before_items)
    new = []
    for item in after_items:
        value = key(item)
        if before_counts[value] > 0:
            before_counts[value] -= 1
        else:
            new.append(item)
    return new


def _compare_frontmatter(before, after):
    hard, added = [], []
    payload = {"status": before["status"], "keys_removed": [], "keys_added": [], "keys_changed": []}
    b_status, a_status = before["status"], after["status"]
    if b_status == "unclosed" or a_status == "unclosed":
        hard.append({
            "kind": "frontmatter",
            "detail": "frontmatter 未闭合",
            "line_before": 1,
        })
        return hard, added, payload
    if b_status == "absent" and a_status == "absent":
        return hard, added, payload
    if b_status == "present" and a_status == "absent":
        hard.append({
            "kind": "frontmatter",
            "detail": "frontmatter 丢失",
            "line_before": 1,
        })
        payload["status"] = "lost"
        payload["keys_removed"] = sorted(before["keys"])
        return hard, added, payload
    if b_status == "absent" and a_status == "present":
        added.append({
            "kind": "frontmatter",
            "detail": "新增 frontmatter",
            "line_after": 1,
        })
        payload["status"] = "added"
        return hard, added, payload
    if before["raw"] == after["raw"]:
        payload["status"] = "same"
        return hard, added, payload

    b_keys, a_keys = before["keys"], after["keys"]
    removed = sorted(set(b_keys) - set(a_keys))
    new_keys = sorted(set(a_keys) - set(b_keys))
    changed = sorted(k for k in set(b_keys) & set(a_keys) if b_keys[k] != a_keys[k])
    payload.update({
        "status": "changed",
        "keys_removed": removed,
        "keys_added": new_keys,
        "keys_changed": changed,
    })
    parts = []
    if removed:
        parts.append("删除键 " + "、".join(removed))
    if new_keys:
        parts.append("新增键 " + "、".join(new_keys))
    if changed:
        parts.append("修改键 " + "、".join(changed))
    detail = "frontmatter 改变"
    if parts:
        detail += "：" + "；".join(parts)
    hard.append({"kind": "frontmatter", "detail": detail, "line_before": 1})
    return hard, added, payload


def _compare_headings(before, after):
    hard, soft, added = [], [], []
    payload = {"lost": [], "level_changed": [], "reordered": []}
    by_text = {}
    for index, heading in enumerate(after):
        by_text.setdefault(heading["text"], []).append(index)
    used = set()
    matched_indices = []
    for heading in before:
        candidates = [i for i in by_text.get(heading["text"], []) if i not in used]
        if not candidates:
            hard.append({
                "kind": "heading",
                "detail": "标题丢失：%s" % heading["text"],
                "line_before": heading["line"],
            })
            payload["lost"].append(heading["text"])
            continue
        index = candidates[0]
        used.add(index)
        matched_indices.append(index)
        if after[index]["level"] != heading["level"]:
            hard.append({
                "kind": "heading",
                "detail": "标题层级改变：%s（H%d → H%d）" % (
                    heading["text"], heading["level"], after[index]["level"]),
                "line_before": heading["line"],
                "line_after": after[index]["line"],
            })
            payload["level_changed"].append({
                "text": heading["text"],
                "before": heading["level"],
                "after": after[index]["level"],
            })
    if matched_indices != sorted(matched_indices):
        soft.append({
            "kind": "heading_order",
            "detail": "标题顺序变化（标题仍存在，未丢失）",
            "line_before": before[0]["line"] if before else None,
        })
        payload["reordered"] = [h["text"] for h in before]
    for index, heading in enumerate(after):
        if index not in used:
            added.append({
                "kind": "heading",
                "detail": "新增标题：%s" % heading["text"],
                "line_after": heading["line"],
            })
    return hard, soft, added, payload


def _compare_tables(before, after):
    hard, soft, added = [], [], []
    payload = []
    for index in range(min(len(before), len(after))):
        old, new = before[index], after[index]
        old_cols = len(old["rows"][0]) if old["rows"] else 0
        new_cols = len(new["rows"][0]) if new["rows"] else 0
        status = "ok"
        if old_cols != new_cols:
            status = "columns_changed"
            hard.append({
                "kind": "table",
                "detail": "第 %d 个表格列数改变：%d → %d" % (index + 1, old_cols, new_cols),
                "line_before": old["line"],
                "line_after": new["line"],
            })
        if len(old["rows"]) > len(new["rows"]):
            status = "row_lost"
            hard.append({
                "kind": "table",
                "detail": "第 %d 个表格行数减少：%d → %d" % (
                    index + 1, len(old["rows"]), len(new["rows"])),
                "line_before": old["line"],
                "line_after": new["line"],
            })
        elif len(old["rows"]) < len(new["rows"]):
            status = "added_rows"
            added.append({
                "kind": "table",
                "detail": "第 %d 个表格新增 %d 行" % (
                    index + 1, len(new["rows"]) - len(old["rows"])),
                "line_after": new["line"],
            })
        elif old["rows"] != new["rows"] and status == "ok":
            status = "cells_changed"
            soft.append({
                "kind": "table_cells",
                "detail": "第 %d 个表格单元格文本变化（行数未变）" % (index + 1),
                "line_before": old["line"],
                "line_after": new["line"],
            })
        payload.append({
            "index": index + 1,
            "rows_before": len(old["rows"]),
            "rows_after": len(new["rows"]),
            "columns_before": old_cols,
            "columns_after": new_cols,
            "status": status,
        })
    if len(before) > len(after):
        hard.append({
            "kind": "table",
            "detail": "表格数量减少：%d → %d" % (len(before), len(after)),
            "line_before": before[len(after)]["line"],
        })
    elif len(before) < len(after):
        added.append({
            "kind": "table",
            "detail": "新增 %d 个表格" % (len(after) - len(before)),
            "line_after": after[len(before)]["line"],
        })
    return hard, soft, added, payload


def _compare_ordered(before, after):
    hard, soft, added = [], [], []
    payload = []
    for index in range(min(len(before), len(after))):
        old, new = before[index], after[index]
        status = "ok"
        if len(old["items"]) > len(new["items"]):
            status = "items_lost"
            hard.append({
                "kind": "ordered_list",
                "detail": "第 %d 个有序列表条目减少：%d → %d" % (
                    index + 1, len(old["items"]), len(new["items"])),
                "line_before": old["line"],
                "line_after": new["line"],
            })
        elif len(old["items"]) < len(new["items"]):
            status = "added_items"
            added.append({
                "kind": "ordered_list",
                "detail": "第 %d 个有序列表新增 %d 条" % (
                    index + 1, len(new["items"]) - len(old["items"])),
                "line_after": new["line"],
            })
        old_texts = [item["text"] for item in old["items"]]
        new_texts = [item["text"] for item in new["items"]]
        if len(old_texts) == len(new_texts) and old_texts != new_texts:
            if status == "ok":
                status = "text_changed"
            soft.append({
                "kind": "ordered_list_text",
                "detail": "第 %d 个有序列表条目文本变化（条目数未变）" % (index + 1),
                "line_before": old["line"],
                "line_after": new["line"],
            })
        payload.append({
            "index": index + 1,
            "items_before": len(old["items"]),
            "items_after": len(new["items"]),
            "status": status,
        })
    if len(before) > len(after):
        hard.append({
            "kind": "ordered_list",
            "detail": "有序列表数量减少：%d → %d" % (len(before), len(after)),
            "line_before": before[len(after)]["line"],
        })
    elif len(before) < len(after):
        added.append({
            "kind": "ordered_list",
            "detail": "新增 %d 个有序列表" % (len(after) - len(before)),
            "line_after": after[len(before)]["line"],
        })
    return hard, soft, added, payload


def compare(before_text, after_text):
    before = _extract(before_text)
    after = _extract(after_text)
    hard, soft, added = [], [], []

    part_hard, part_added, fm_payload = _compare_frontmatter(
        before["frontmatter"], after["frontmatter"])
    hard.extend(part_hard)
    added.extend(part_added)

    part_hard, part_soft, part_added, head_payload = _compare_headings(
        before["headings"], after["headings"])
    hard.extend(part_hard)
    soft.extend(part_soft)
    added.extend(part_added)

    code_lost = _missing(before["code_blocks"], after["code_blocks"], key=lambda x: x["value"])
    for item in code_lost:
        hard.append({
            "kind": "code_block",
            "detail": "围栏代码块丢失或内容改变（%s）" % (item["info"] or "无语言标记"),
            "line_before": item["line"],
        })
    code_new = _added(before["code_blocks"], after["code_blocks"], key=lambda x: x["value"])
    for item in code_new:
        added.append({
            "kind": "code_block",
            "detail": "新增或改写后的代码块（%s）" % (item["info"] or "无语言标记"),
            "line_after": item["line"],
        })

    inline_lost = _missing(before["inline_code"], after["inline_code"], key=lambda x: x["value"])
    for item in inline_lost:
        hard.append({
            "kind": "inline_code",
            "detail": "行内代码丢失：%s" % item["value"][:80],
            "line_before": item["line"],
        })
    inline_new = _added(before["inline_code"], after["inline_code"], key=lambda x: x["value"])
    for item in inline_new:
        added.append({
            "kind": "inline_code",
            "detail": "新增或改写后的行内代码：%s" % item["value"][:80],
            "line_after": item["line"],
        })

    link_lost = _missing(before["link_targets"], after["link_targets"], key=lambda x: x["value"])
    for item in link_lost:
        hard.append({
            "kind": "link_target",
            "detail": "链接目标丢失：%s" % item["value"],
            "line_before": item["line"],
        })
    link_new = _added(before["link_targets"], after["link_targets"], key=lambda x: x["value"])
    for item in link_new:
        added.append({
            "kind": "link_target",
            "detail": "新增链接目标：%s" % item["value"],
            "line_after": item["line"],
        })

    id_lost = _missing(before["explicit_ids"], after["explicit_ids"], key=lambda x: x["value"])
    for item in id_lost:
        hard.append({
            "kind": "explicit_id",
            "detail": "显式 ID 丢失：%s" % item["value"],
            "line_before": item["line"],
        })
    id_new = _added(before["explicit_ids"], after["explicit_ids"], key=lambda x: x["value"])
    for item in id_new:
        added.append({
            "kind": "explicit_id",
            "detail": "新增显式 ID：%s" % item["value"],
            "line_after": item["line"],
        })

    part_hard, part_soft, part_added, table_payload = _compare_tables(
        before["tables"], after["tables"])
    hard.extend(part_hard)
    soft.extend(part_soft)
    added.extend(part_added)

    part_hard, part_soft, part_added, ordered_payload = _compare_ordered(
        before["ordered_lists"], after["ordered_lists"])
    hard.extend(part_hard)
    soft.extend(part_soft)
    added.extend(part_added)

    def brief_code(item):
        return "%s（第 %d 行）" % (item["info"] or "无语言标记", item["line"])

    return {
        "tool": "guard_text",
        "status": "changed" if hard else "ok",
        "summary": {
            "hard": len(hard),
            "soft": len(soft),
            "added": len(added),
            "allowed": 0,
        },
        "frontmatter": fm_payload,
        "protected": {
            "code_blocks": {
                "lost": [brief_code(item) for item in code_lost],
                "added": [brief_code(item) for item in code_new],
            },
            "inline_code": {
                "lost": [item["value"][:80] for item in inline_lost],
                "added": [item["value"][:80] for item in inline_new],
            },
            "link_targets": {
                "lost": [item["value"] for item in link_lost],
                "added": [item["value"] for item in link_new],
            },
            "headings": head_payload,
            "tables": table_payload,
            "ordered_lists": ordered_payload,
            "explicit_ids": {
                "lost": [item["value"] for item in id_lost],
                "added": [item["value"] for item in id_new],
            },
        },
        "hard": hard,
        "soft": soft,
        "added": added,
        "note": "只比对可机械识别的结构，不判断事实、语义与作者身份；未列出不等于未改动。",
    }


def _apply_allow(hard, rules):
    allowed, kept = [], []
    for item in hard:
        match = None
        for rule in rules:
            if not isinstance(rule, dict) or rule.get("kind") != item["kind"]:
                continue
            value = str(rule.get("value", ""))
            if value and value not in item.get("detail", ""):
                continue
            match = rule
            break
        if match is None:
            kept.append(item)
        else:
            entry = dict(item)
            entry["allowed"] = str(match.get("reason", ""))
            allowed.append(entry)
    return kept, allowed


def _truncate(value, limit=100):
    value = str(value)
    return value if len(value) <= limit else value[:limit] + "…"


def format_text(result):
    lines = []
    summary = result["summary"]
    if not result["hard"] and not result["soft"] and not result["added"]:
        lines.append("受保护内容：未发现丢失或结构改变。")
    else:
        head = "受保护内容：丢失/改变 %d 项、观察 %d 项、新增 %d 项" % (
            summary["hard"], summary["soft"], summary["added"])
        if summary["allowed"]:
            head += "（已登记例外 %d 项）" % summary["allowed"]
        lines.append(head)
        for item in result["hard"]:
            lines.append("  [hard] %s 第 %s 行：%s" % (
                item["kind"], item.get("line_before", "?"), _truncate(item["detail"])))
        for item in result["soft"]:
            lines.append("  [soft] %s 第 %s 行：%s" % (
                item["kind"], item.get("line_before", "?"), _truncate(item["detail"])))
        for item in result["added"]:
            lines.append("  [add]  %s 第 %s 行：%s" % (
                item["kind"], item.get("line_after", "?"), _truncate(item["detail"])))
    lines.append(result["note"])
    return "\n".join(lines)


def load_allow(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rules = data.get("allow") if isinstance(data, dict) else data
    if not isinstance(rules, list):
        raise ValueError("allow 文件需要 {\"allow\": [...]} 或直接给数组")
    return rules


def main(argv=None):
    ap = argparse.ArgumentParser(description="受保护内容机械比对")
    ap.add_argument("before", help="改前文本")
    ap.add_argument("after", help="改后文本")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="存在未登记 hard 项时返回 1")
    ap.add_argument("--allow", help="允许例外 JSON：{\"allow\": [{\"kind\":…, \"value\":…, \"reason\":…}]}")
    args = ap.parse_args(argv)

    try:
        before_text = lint.read_text(args.before)
        after_text = lint.read_text(args.after)
    except (OSError, UnicodeError) as exc:
        print("无法读取输入: %s" % exc, file=sys.stderr)
        return 2

    rules = []
    if args.allow:
        try:
            rules = load_allow(args.allow)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print("无法读取 allow 文件: %s" % exc, file=sys.stderr)
            return 2

    result = compare(before_text, after_text)
    if rules:
        result["hard"], allowed = _apply_allow(result["hard"], rules)
        result["summary"]["hard"] = len(result["hard"])
        result["summary"]["allowed"] = len(allowed)
        result["allowed"] = allowed
        result["status"] = "changed" if result["hard"] else "ok"

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))

    if args.strict and result["hard"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
