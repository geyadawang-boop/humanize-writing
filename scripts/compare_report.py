# -*- coding: utf-8 -*-
"""compare_report.py — 改前/改后对比报告（humanize-writing skill）

用法:
    python scripts/compare_report.py 改前.md 改后.md
    python scripts/compare_report.py 改前.md 改后.md --format html --out 报告.html
    python scripts/compare_report.py 改前.md 改后.md --genre academic --language zh
    python scripts/compare_report.py 改前.md 改后.md --semantic 判读.json

同一规则集分别评改前、改后两稿，输出一份对比报告：
    一、指标前后对比（分数、加权命中合计、条目数、字数、句数、段数、平均句长）
    二、改前命中分级清单（加权项 / 零权重观察，逐条标注改后是否仍命中）
    三、逐段对照（删除用删除线，新增用粗体或 <ins>）
    四、语义候选与人工判读（可选 --semantic 合并判读 JSON）
    五、受保护内容核对（frontmatter/代码/链接/标题/表格/ID 的机械比对）

分数口径与 ai_smell_lint.py 完全一致：只表示本规则集的加权命中，不判作者身份、
文学质量或外部检测结果；两稿分数之差也不能单独证明改稿收益，仍要按问题逐条核读。
"""
import argparse
import difflib
import html
import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_smell_lint as lint  # noqa: E402
import guard_text as guard  # noqa: E402

STATUS_TAGS = ("[概览]", "[genre]", "[短文本]")
DEFAULT_OUT = "改前改后对比报告"


def tag_of(message):
    m = re.match(r"^(\[[^\]]+\])", message)
    return m.group(1) if m else message[:12]


def profile(text, genre, language):
    """与 lint 同一口径评估一遍，并取出报告需要的派生量。"""
    issues, status, score = lint.evaluate(text, genre, language,
                                          fingerprint=True, candidates=True)
    body = lint.strip_markdown(text)
    lens = [lint.chinese_len(s) for s in lint.sentences(body)]
    weighted = [(w, m) for w, m in issues if w]
    observed = [(w, m) for w, m in issues if not w and tag_of(m) not in STATUS_TAGS]
    return {
        "score": score,
        "status": status,
        "label": lint.label_of(score, status),
        "chars": lint.chinese_len(body),
        "sentences": len(lens),
        "paragraphs": len(lint.paragraphs(body)),
        "mean_len": (sum(lens) / float(len(lens))) if lens else 0.0,
        "weight_total": sum(w for w, _ in weighted),
        "weighted_n": len(weighted),
        "weighted": weighted,
        "observed": observed,
        "issues": issues,
    }


def metric_rows(before, after):
    rows = [
        ("静态写作线索分", "score", "low", 0),
        ("加权命中合计", "weight_total", "low", 0),
        ("加权命中条目", "weighted_n", "low", 0),
        ("有效中文字", "chars", None, 0),
        ("句数", "sentences", None, 0),
        ("段数", "paragraphs", None, 0),
        ("平均句长", "mean_len", None, 1),
    ]
    out = []
    for label, key, better, digits in rows:
        old, new = before[key], after[key]
        delta = new - old
        judgement = ""
        if better == "low" and delta:
            judgement = "改善" if delta < 0 else "变差"
        out.append((label, old, new, delta, digits, judgement))
    return out


def _num(value, digits):
    return ("%." + str(digits) + "f") % value


def after_state(before_item, after):
    """同一标签在改后稿里的状态：已消失 / 仍命中（权重变化）。"""
    tag, weight = before_item
    hit = next((w for w, m in after["issues"] if tag_of(m) == tag), None)
    if hit is None:
        return "已消失"
    if hit != weight:
        return "仍命中（权重 %s → %s）" % (weight, hit)
    return "仍命中"


def paragraphs_of(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def inline_diff(old, new, mode):
    """字符级对照：删除标红、新增标绿；md 用删除线/粗体，html 用 del/ins。"""
    sm = difflib.SequenceMatcher(None, old, new)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        a, b = old[i1:i2], new[j1:j2]
        if tag == "equal":
            out.append(html.escape(a) if mode == "html" else a)
            continue
        if mode == "html":
            if a:
                out.append('<del>%s</del>' % html.escape(a))
            if b:
                out.append('<ins>%s</ins>' % html.escape(b))
        else:
            if a:
                out.append("~~%s~~" % a)
            if b:
                out.append("**%s**" % b)
    return "".join(out)


def diff_blocks(before_text, after_text):
    """段落级 opcodes；改写段配对做字符级对照。返回 [(kind, payload)]。"""
    a, b = paragraphs_of(before_text), paragraphs_of(after_text)
    sm = difflib.SequenceMatcher(None, a, b)
    blocks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "delete":
            blocks.extend(("del", [x]) for x in a[i1:i2])
        elif tag == "insert":
            blocks.extend(("add", [x]) for x in b[j1:j2])
        else:
            n = max(i2 - i1, j2 - j1)
            for k in range(n):
                old = a[i1 + k] if i1 + k < i2 else ""
                new = b[j1 + k] if j1 + k < j2 else ""
                if old and new:
                    # 相似度过低说明两段本来就不是同一段，硬做字符对照会把整段涂花；
                    # 这种情况退回「删一段 + 增一段」。
                    ratio = difflib.SequenceMatcher(None, old, new).quick_ratio()
                    if ratio >= 0.5:
                        blocks.append(("mod", (old, new)))
                    else:
                        blocks.append(("del", [old]))
                        blocks.append(("add", [new]))
                elif old:
                    blocks.append(("del", [old]))
                else:
                    blocks.append(("add", [new]))
    return blocks


def change_summary(before_text, after_text):
    blocks = diff_blocks(before_text, after_text)
    return {
        "modified": sum(1 for k, _ in blocks if k == "mod"),
        "added": sum(1 for k, _ in blocks if k == "add"),
        "deleted": sum(1 for k, _ in blocks if k == "del"),
    }


def load_semantic(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data.get("judgments") if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError("语义判读 JSON 需要 {\"judgments\": [...]} 或直接给数组")
    out = []
    for item in items:
        if not isinstance(item, dict) or not item.get("candidate"):
            raise ValueError("每条判读至少需要 candidate 字段")
        out.append({
            "candidate": str(item["candidate"]),
            "verdict": str(item.get("verdict", "")),
            "note": str(item.get("note", "")),
        })
    return out


def _verdict_for(message, semantic):
    """判读按 candidate 与候选行做双向子串匹配；命不中就留空，不猜。"""
    for item in semantic or ():
        if item["candidate"] and (item["candidate"] in message or message.startswith(item["candidate"])):
            return item
    return None


def _md_cell(text):
    return text.replace("|", "\\|")


def protected_result(before_text, after_text):
    """两稿相似度过低时跳过，避免拿无关文本生成大量假警报。"""
    ratio = difflib.SequenceMatcher(None, before_text, after_text).quick_ratio()
    if ratio < 0.3:
        return {"skipped": True, "ratio": ratio}
    return guard.compare(before_text, after_text)


def protected_lead(result):
    if result.get("skipped"):
        return ("两稿相似度过低（%.2f），可能不是同一篇的修订，"
                "跳过受保护内容比对。" % result["ratio"])
    summary = result["summary"]
    if not result["hard"] and not result["soft"]:
        return "受保护内容：未发现丢失或结构改变。"
    return ("受保护内容：丢失/改变 %d 项、观察 %d 项、新增 %d 项；逐条见下。"
            % (summary["hard"], summary["soft"], summary["added"]))


def build_md(before_text, after_text, before, after, name0, name1, semantic, title):
    parts = []
    parts.append("# %s" % title)
    parts.append("")
    parts.append("改前 `%s` → 改后 `%s`。分数口径与 ai_smell_lint 规则集 %s 一致："
                 "只表示本规则集加权命中，不判作者身份、文学质量或外部检测结果；"
                 "分数下降不等于改稿一定变好，须按条目核读。"
                 % (name0, name1, lint.RULESET_VERSION))
    parts.append("")
    verdict = "未变" if before["score"] == after["score"] else (
        "下降 %d" % (before["score"] - after["score"]) if after["score"] < before["score"]
        else "上升 %d" % (after["score"] - before["score"]))
    parts.append("**结论**：静态线索分 %d → %d（%s），加权命中合计 %d → %d。"
                 % (before["score"], after["score"], verdict,
                    before["weight_total"], after["weight_total"]))
    parts.append("")

    parts.append("## 一、指标前后对比")
    parts.append("")
    parts.append("| 指标 | 改前 | 改后 | 变化 |")
    parts.append("| --- | ---: | ---: | --- |")
    for label, old, new, delta, digits, judgement in metric_rows(before, after):
        if delta == 0:
            change = "持平"
        else:
            change = "%+s%s" % (_num(delta, digits), ("（%s）" % judgement) if judgement else "")
        parts.append("| %s | %s | %s | %s |" % (label, _num(old, digits), _num(new, digits), change))
    parts.append("")

    parts.append("## 二、改前命中分级清单")
    parts.append("")
    parts.append("### 加权项（需逐条核读）")
    parts.append("")
    if before["weighted"]:
        for w, m in sorted(before["weighted"], key=lambda x: -x[0]):
            parts.append("- **%d** %s（改后：%s）" % (w, m, after_state((tag_of(m), w), after)))
    else:
        parts.append("- 无加权命中。")
    parts.append("")
    parts.append("### 零权重观察（只标位置，不作改写依据）")
    parts.append("")
    if before["observed"]:
        for _, m in before["observed"]:
            parts.append("- %s" % m)
    else:
        parts.append("- 无观察行。")
    parts.append("")

    summary = change_summary(before_text, after_text)
    parts.append("## 三、逐段对照")
    parts.append("")
    parts.append("~~删除线~~ 为改前文字，**粗体** 为改后文字；未改动段落已省略。"
                 "改写 %d 段、新增 %d 段、删除 %d 段。"
                 % (summary["modified"], summary["added"], summary["deleted"]))
    parts.append("")
    blocks = diff_blocks(before_text, after_text)
    if not blocks:
        parts.append("两稿逐段一致（可能只改了标点或空行）。")
    for kind, payload in blocks:
        if kind == "mod":
            parts.append("> %s" % inline_diff(payload[0], payload[1], "md"))
        elif kind == "del":
            parts.append("> ~~%s~~" % payload[0])
        else:
            parts.append("> **%s**" % payload[0])
        parts.append("")
    parts.append("")

    parts.append("## 四、语义候选与人工判读")
    parts.append("")
    candidates = [m for _, m in after["observed"] if tag_of(m) == "[语义候选]"]
    if semantic:
        parts.append("| 候选 | 判读 | 说明 |")
        parts.append("| --- | --- | --- |")
        for item in semantic:
            parts.append("| %s | %s | %s |" % (_md_cell(item["candidate"]),
                                               _md_cell(item["verdict"]),
                                               _md_cell(item["note"])))
        parts.append("")
    if candidates:
        parts.append("改后稿的语义候选（需要逐条答是/否；候选存在不等于有问题）：")
        parts.append("")
        for m in candidates:
            hit = _verdict_for(m, semantic)
            mark = (" → 判读：%s" % hit["verdict"]) if hit else ""
            parts.append("- %s%s" % (m, mark))
    else:
        parts.append("改后稿没有语义候选行；语义候选只在命中时输出（ai_smell_lint.py --candidates）。")
    parts.append("")

    parts.append("## 五、受保护内容核对")
    parts.append("")
    protected = protected_result(before_text, after_text)
    parts.append(protected_lead(protected))
    parts.append("")
    if not protected.get("skipped"):
        if protected["hard"]:
            parts.append("| 类型 | 位置（改前） | 说明 |")
            parts.append("| --- | ---: | --- |")
            for item in protected["hard"]:
                parts.append("| %s | %s | %s |" % (
                    _md_cell(item["kind"]),
                    item.get("line_before", "-"),
                    _md_cell(item["detail"])))
            parts.append("")
        if protected["soft"]:
            parts.append("观察项（不阻断，需人工判断是否为有意改写）：")
            parts.append("")
            for item in protected["soft"]:
                parts.append("- %s 第 %s 行：%s" % (
                    item["kind"], item.get("line_before", "?"), item["detail"]))
            parts.append("")
    parts.append("机械比对只覆盖可识别结构，不等于事实核读；新增内容不在此判定。")
    parts.append("")
    return "\n".join(parts)


HTML_CSS = """
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
max-width:980px;margin:32px auto;padding:0 20px;line-height:1.75;color:#1f2328}
h1{font-size:24px;border-bottom:2px solid #d0d7de;padding-bottom:8px}
h2{font-size:19px;margin-top:32px;border-bottom:1px solid #eaecef;padding-bottom:4px}
h3{font-size:16px;color:#57606a}
table{border-collapse:collapse;width:100%;margin:12px 0}
th,td{border:1px solid #d0d7de;padding:6px 10px;text-align:left;font-size:14px}
th{background:#f6f8fa}
td:not(:first-child){font-variant-numeric:tabular-nums}
del{background:#ffecec;color:#b42318;text-decoration:line-through}
ins{background:#e8f5ec;color:#0b6b35;text-decoration:none;font-weight:600}
blockquote{margin:8px 0;padding:6px 12px;border-left:3px solid #d0d7de;color:#24292f}
.small{color:#57606a;font-size:13px}
"""


def build_html(before_text, after_text, before, after, name0, name1, semantic, title):
    e = html.escape
    out = []
    out.append("<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">")
    out.append("<title>%s</title><style>%s</style></head><body>" % (e(title), HTML_CSS))
    out.append("<h1>%s</h1>" % e(title))
    out.append('<p class="small">改前 <code>%s</code> → 改后 <code>%s</code>。'
               '分数口径与 ai_smell_lint 规则集 %s 一致：只表示加权命中，'
               '不判作者身份、文学质量或外部检测结果。</p>'
               % (e(name0), e(name1), e(lint.RULESET_VERSION)))
    out.append("<p><strong>结论</strong>：静态线索分 %d → %d，加权命中合计 %d → %d。</p>"
               % (before["score"], after["score"], before["weight_total"], after["weight_total"]))

    out.append("<h2>一、指标前后对比</h2><table><tr><th>指标</th><th>改前</th><th>改后</th><th>变化</th></tr>")
    for label, old, new, delta, digits, judgement in metric_rows(before, after):
        change = "持平" if delta == 0 else "%+s%s" % (
            _num(delta, digits), ("（%s）" % judgement) if judgement else "")
        out.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                   % (e(label), _num(old, digits), _num(new, digits), e(change)))
    out.append("</table>")

    out.append("<h2>二、改前命中分级清单</h2><h3>加权项（需逐条核读）</h3><ul>")
    if before["weighted"]:
        for w, m in sorted(before["weighted"], key=lambda x: -x[0]):
            out.append("<li><strong>%d</strong> %s（改后：%s）</li>"
                       % (w, e(m), e(after_state((tag_of(m), w), after))))
    else:
        out.append("<li>无加权命中。</li>")
    out.append("</ul><h3>零权重观察（只标位置，不作改写依据）</h3><ul>")
    if before["observed"]:
        for _, m in before["observed"]:
            out.append("<li>%s</li>" % e(m))
    else:
        out.append("<li>无观察行。</li>")
    out.append("</ul>")

    summary = change_summary(before_text, after_text)
    out.append("<h2>三、逐段对照</h2>")
    out.append('<p class="small"><del>红底删除</del> 为改前文字，<ins>绿底</ins> 为改后文字；'
               "未改动段落已省略。改写 %d 段、新增 %d 段、删除 %d 段。</p>"
               % (summary["modified"], summary["added"], summary["deleted"]))
    blocks = diff_blocks(before_text, after_text)
    if not blocks:
        out.append("<p>两稿逐段一致（可能只改了标点或空行）。</p>")
    for kind, payload in blocks:
        if kind == "mod":
            body = inline_diff(payload[0], payload[1], "html")
        elif kind == "del":
            body = "<del>%s</del>" % e(payload[0])
        else:
            body = "<ins>%s</ins>" % e(payload[0])
        out.append("<blockquote>%s</blockquote>" % body)

    out.append("<h2>四、语义候选与人工判读</h2>")
    candidates = [m for _, m in after["observed"] if tag_of(m) == "[语义候选]"]
    if semantic:
        out.append("<table><tr><th>候选</th><th>判读</th><th>说明</th></tr>")
        for item in semantic:
            out.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                       % (e(item["candidate"]), e(item["verdict"]), e(item["note"])))
        out.append("</table>")
    if candidates:
        out.append("<p>改后稿的语义候选（需要逐条答是/否；候选存在不等于有问题）：</p><ul>")
        for m in candidates:
            hit = _verdict_for(m, semantic)
            mark = (" → 判读：%s" % e(hit["verdict"])) if hit else ""
            out.append("<li>%s%s</li>" % (e(m), mark))
        out.append("</ul>")
    else:
        out.append("<p>改后稿没有语义候选行。</p>")

    out.append("<h2>五、受保护内容核对</h2>")
    protected = protected_result(before_text, after_text)
    out.append("<p>%s</p>" % e(protected_lead(protected)))
    if not protected.get("skipped"):
        if protected["hard"]:
            out.append("<table><tr><th>类型</th><th>位置（改前）</th><th>说明</th></tr>")
            for item in protected["hard"]:
                out.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    e(item["kind"]),
                    e(str(item.get("line_before", "-"))),
                    e(item["detail"])))
            out.append("</table>")
        if protected["soft"]:
            out.append("<p>观察项（不阻断，需人工判断是否为有意改写）：</p><ul>")
            for item in protected["soft"]:
                out.append("<li>%s 第 %s 行：%s</li>" % (
                    e(item["kind"]),
                    e(str(item.get("line_before", "?"))),
                    e(item["detail"])))
            out.append("</ul>")
    out.append('<p class="small">机械比对只覆盖可识别结构，不等于事实核读；'
               "新增内容不在此判定。</p>")
    out.append("</body></html>")
    return "\n".join(out)


def read(path):
    # 与 ai_smell_lint 共用解码顺序（UTF-8 / GBK / UTF-16 与 UTF-32 BOM），
    # 避免同一稿能 lint 却在对比报告里报“无法读取”。
    return lint.read_text(str(path))


def main(argv=None):
    ap = argparse.ArgumentParser(description="改前/改后对比报告")
    ap.add_argument("before", help="改前文本")
    ap.add_argument("after", help="改后文本")
    ap.add_argument("--genre", default="general", help="文体：%s" % "/".join(lint.GENRES))
    ap.add_argument("--language", default="auto", help="auto/zh/en/mixed")
    ap.add_argument("--format", choices=("md", "html"), default="md")
    ap.add_argument("--out", help="输出路径；默认 %s.md/.html" % DEFAULT_OUT)
    ap.add_argument("--semantic", help="人工判读 JSON：{\"judgments\": [{\"candidate\":…}]}")
    ap.add_argument("--title", default="改前改后对比报告")
    args = ap.parse_args(argv)

    if args.genre not in lint.GENRES:
        print("未知 --genre: %s（可选: %s）" % (args.genre, "/".join(lint.GENRES)), file=sys.stderr)
        return 2
    if args.language not in lint.LANGUAGES:
        print("未知 --language: %s（可选: %s）"
              % (args.language, "/".join(lint.LANGUAGES)), file=sys.stderr)
        return 2
    try:
        before_text, after_text = read(args.before), read(args.after)
    except (OSError, UnicodeError) as exc:
        print("无法读取输入: %s" % exc, file=sys.stderr)
        return 2
    try:
        semantic = load_semantic(args.semantic) if args.semantic else None
    except (OSError, ValueError) as exc:
        print("无法读取语义判读 JSON: %s" % exc, file=sys.stderr)
        return 2

    before = profile(before_text, args.genre, args.language)
    after = profile(after_text, args.genre, args.language)
    if args.format == "html":
        page = build_html(before_text, after_text, before, after,
                          args.before, args.after, semantic, args.title)
    else:
        page = build_md(before_text, after_text, before, after,
                        args.before, args.after, semantic, args.title)
    out = args.out or ("%s.%s" % (DEFAULT_OUT, args.format))
    Path(out).write_text(page, encoding="utf-8")
    print("报告 → %s（分数 %d → %d，加权命中 %d → %d）"
          % (out, before["score"], after["score"], before["weight_total"], after["weight_total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
