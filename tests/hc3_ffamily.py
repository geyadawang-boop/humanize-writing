# -*- coding: utf-8 -*-
"""F 族（语域 / 事实密度层）候选信号的 dev/eval 测量（v0.25）。

v0.24 结论（research-basis.md §十六）：现有特征族在第三方语料上 AUC 0.68–0.83、
不存在可用操作点；后续方向登记为「语义层/事实层特征」。本脚本把该方向做成可测量：

  · dev / eval 双切分，均与冻结的 tests/corpus_hc3/ 60 篇互不相交（原始顺序确定性抽取，
    前 40 字键去重后顺序跳过已用键；eval 同时跳过 dev 已消费键）；dev 用于设计与调权，
    eval 只允许跑一次（--eval）。
  · F 候选特征逐项 AUC（law / baike 两域），组合惩罚加在 v0.24 lint 原始分之上复算
    （含短文本密度归一，与 evaluate() 同式）。

数字纪律：F 权重与阈值只在 dev 上定稿；eval 结果一旦打印即为终值，不得回头改权重。

用法：
    python tests/hc3_ffamily.py            # dev 测量（可反复）
    python tests/hc3_ffamily.py --eval     # eval 终测（只允许跑一次）
"""
import argparse
import hashlib
import importlib.util
import pathlib
import re
import statistics
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bhc = load_mod("build_hc3_corpus", pathlib.Path(__file__).resolve().parent / "build_hc3_corpus.py")
lint = load_mod("ai_smell_lint", ROOT / "scripts" / "ai_smell_lint.py")

SPLITS = {
    "dev": [
        ("law.jsonl", "chatgpt_answers", 100, 199, 12),
        ("law.jsonl", "human_answers", 100, 199, 12),
        ("baike.jsonl", "chatgpt_answers", 200, 300, 20),
        ("baike.jsonl", "human_answers", 200, 300, 20),
    ],
    "eval": [
        ("law.jsonl", "chatgpt_answers", 100, 199, 12),
        ("law.jsonl", "human_answers", 100, 199, 12),
        ("baike.jsonl", "chatgpt_answers", 200, 300, 24),
        ("baike.jsonl", "human_answers", 200, 300, 24),
    ],
}
DOM = {
    ("law.jsonl", "chatgpt_answers"): "law",
    ("law.jsonl", "human_answers"): "law",
    ("baike.jsonl", "chatgpt_answers"): "baike",
    ("baike.jsonl", "human_answers"): "baike",
}

EXT_ANCHOR = re.compile(
    r"\d+(?:\.\d+)?%?"
    r"|[一二三四五六七八九十百千万亿两半零]{1,4}(?:元|万|亿|年|月|日|条|款|项|次|个|件|倍|折|岁|斤|米|字|篇|页|人|家|天|小时|分钟)"
    r"|第[一二三四五六七八九十百零\d]{1,4}[条款项章]"
    r"|《[^《》\n]{2,24}》"
    r"|[“「][^”」\n]{2,30}[”」]"
    r"|[\u4e00-\u9fff]{2,6}(?:省|市|县|村|镇|区|路|街|法院|律师事务所|大学|学院|公司|银行|医院)"
)
HEDGES = (
    "一般来说", "一般而言", "通常", "往往", "或许", "一般情况下", "相对而言",
    "在一定程度上", "需要根据", "因人而异", "视情况", "大体上", "多数情况",
    "大多数情况", "综合来看", "总体而言", "整体而言", "具体而言",
)
ADVICE = (
    "建议您", "建议咨询", "建议向", "建议及时", "应当", "务必", "请注意",
    "需要注意的是", "可以考虑", "最好",
)
PARTICLE = re.compile(r"(?:吧|呢|嘛|呗|哦|呀|啦|啊|哈|哟)[。！？!?\n]|哈{2,}")
LIST_PREFIX = re.compile(r"^\s*(?:[0-9]{1,2}[\.、]|[①②③④⑤⑥⑦⑧⑨⑩])", re.M)

F_RULES = [
    ("advice", ">=", 2.0, 5),
    ("nin", ">=", 2.5, 5),
]


def feats(text):
    body = lint.strip_markdown(text)
    total = lint.chinese_len(body)
    k = 300.0 / total if total else 0.0
    return {
        "cur_anchor": len(lint.ANCHOR_RE.findall(body)) * k,
        "ext_anchor": len(EXT_ANCHOR.findall(body)) * k,
        "hedge": sum(body.count(w) for w in HEDGES) * k,
        "advice": sum(body.count(w) for w in ADVICE) * k,
        "nin": body.count("您") * k,
        "wo": body.count("我") * k,
        "particle": len(PARTICLE.findall(body)) * k,
        "list": len(LIST_PREFIX.findall(body)) * k,
    }


def f_penalty(text):
    f = feats(text)
    p, hits = 0, []
    for name, op, thr, w in F_RULES:
        v = f[name]
        ok = v < thr if op == "<" else v >= thr
        if ok:
            p += w
            hits.append(name)
    return p, hits


def combined_score(text):
    issues, status = lint.check(text, genre="general")
    pen, hits = f_penalty(text)
    english = sum(w for w, m in issues if m.startswith(lint.ENGLISH_ISSUE_TAGS))
    chinese = sum(w for w, m in issues if not m.startswith(lint.ENGLISH_ISSUE_TAGS)) + pen
    body = lint.strip_markdown(text)
    units = lint.chinese_len(body) + lint.ascii_word_len(body)
    if status == "ok" and chinese > 0 and lint.MIXED_MIN_UNITS <= units < lint.SCORE_NORM_CHARS:
        chinese = round(chinese * lint.SCORE_NORM_CHARS / units)
    return min(100, english + chinese), status, hits


def base_score(text):
    return lint.evaluate(text, genre="general")[2]


def auc(a, h):
    gt = eq = tot = 0
    for x in a:
        for y in h:
            tot += 1
            if x > y:
                gt += 1
            elif x == y:
                eq += 1
    return (gt + 0.5 * eq) / tot if tot else float("nan")


def tradeoff(ai, hu, line):
    print("  阈值   召回TPR   误报FPR")
    for t in (20, 25, 30, 35, 39, 40, 45, 50):
        tpr = sum(1 for s in ai if s > t) / len(ai)
        fpr = sum(1 for s in hu if s > t) / len(hu)
        mark = "  <- 当前判定线" if t == line else ""
        print("  %-6d %-9.2f %-9.2f%s" % (t, tpr, fpr, mark))


def bucket(recs, field, lo, hi, skip, n):
    seen = set(skip)
    out = []
    for r in recs:
        for a in (r.get(field) or []):
            t = bhc.clean(a)
            if not (lo <= bhc.cn_len(t) <= hi):
                continue
            key = t[:40]
            if key in seen:
                continue
            seen.add(key)
            out.append(t)
            if len(out) >= n:
                return out, seen
    return out, seen


def load_records():
    raw_dir = pathlib.Path(tempfile.gettempdir()) / "hc3_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    recs = {}
    src_names = {p[1] for p in bhc.PLAN} | {p[0] for p in SPLITS["dev"] + SPLITS["eval"]}
    for fname in sorted(src_names):
        data = bhc.fetch(fname, raw_dir)
        got = hashlib.sha256(data).hexdigest()
        if got != bhc.SRC_SHA.get(fname, got):
            print("!! %s sha256 与登记不符：%s" % (fname, got))
            return None
        recs[fname] = bhc.load(raw_dir / fname)
    return recs


def frozen_keys(recs):
    tree = ROOT / "tests" / "corpus_hc3"
    frozen = {}
    bad = 0
    for pattern, fname, field, lo, hi, n in bhc.PLAN:
        texts, seen = bucket(recs[fname], field, lo, hi, set(), n)
        frozen[(fname, field, lo, hi)] = seen
        files = sorted(tree.glob(pattern.replace("%02d", "*")))
        if len(files) != len(texts):
            bad += abs(len(files) - len(texts))
        for p, t in zip(files, texts):
            if p.read_text(encoding="utf-8").strip() != t.strip():
                bad += 1
    return frozen, bad


def collect(split, recs, frozen, devused):
    out = {}
    for fname, field, lo, hi, n in SPLITS[split]:
        key = (fname, field, lo, hi)
        skip = set(frozen.get(key, set()))
        if split == "eval":
            skip |= devused.get(key, set())
        texts, _ = bucket(recs[fname], field, lo, hi, skip, n)
        out[(DOM[(fname, field)], "ai" if "chatgpt" in field else "hu")] = texts
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", action="store_true", help="eval 终测（只允许跑一次）")
    args = ap.parse_args()
    split = "eval" if args.eval else "dev"
    recs = load_records()
    if recs is None:
        return 2
    frozen, bad = frozen_keys(recs)
    if bad:
        print("!! 冻结语料与重建不一致 %d 处，中止" % bad)
        return 2
    devused = {}
    for fname, field, lo, hi, n in SPLITS["dev"]:
        key = (fname, field, lo, hi)
        _, seen = bucket(recs[fname], field, lo, hi, set(frozen.get(key, set())), n)
        devused[key] = seen
    data = collect(split, recs, frozen, devused)

    if args.eval:
        print("【eval 终测】此后不得回头改 F_RULES（数字纪律：据此调参=刷分，禁止）")
    else:
        print("【dev 测量】设计与调权在本切分上完成")
    law_ai, law_hu = data[("law", "ai")], data[("law", "hu")]
    bk_ai, bk_hu = data[("baike", "ai")], data[("baike", "hu")]
    print("样本：law %dv%d · baike %dv%d" % (len(law_ai), len(law_hu), len(bk_ai), len(bk_hu)))
    print("冻结语料复验：与树内 60 篇逐字一致 ✓\n" if not bad else "")

    print("== F 候选特征（密度/300字，ai 均分 | hu 均分）==")
    names = list(feats(law_ai[0]).keys())
    for nm in names:
        la = statistics.mean([feats(t)[nm] for t in law_ai])
        lh = statistics.mean([feats(t)[nm] for t in law_hu])
        ba = statistics.mean([feats(t)[nm] for t in bk_ai])
        bh = statistics.mean([feats(t)[nm] for t in bk_hu])
        print("  %-12s law %6.2f | %-6.2f   baike %6.2f | %-6.2f" % (nm, la, lh, ba, bh))

    print("\n== 单特征 AUC（>0.5 = 特征值高偏 AI；<0.5 = 特征值低偏 AI）==")
    for nm in names:
        la = [feats(t)[nm] for t in law_ai]
        lh = [feats(t)[nm] for t in law_hu]
        ba = [feats(t)[nm] for t in bk_ai]
        bh = [feats(t)[nm] for t in bk_hu]
        print("  %-12s law %.3f   baike %.3f   合并 %.3f" % (nm, auc(la, lh), auc(ba, bh), auc(la + ba, lh + bh)))

    print("\n== 基线（v0.24 lint，general 门控）vs 组合（+F 惩罚）==")
    for label, fn in (("基线", base_score), ("组合", lambda t: combined_score(t)[0])):
        la = [fn(t) for t in law_ai]
        lh = [fn(t) for t in law_hu]
        ba = [fn(t) for t in bk_ai]
        bh = [fn(t) for t in bk_hu]
        pa, ph = la + ba, lh + bh
        print("\n[%s] law %.1f/%.1f(max %d/%d)  baike %.1f/%.1f(max %d/%d)  合并 %.1f/%.1f" % (
            label, statistics.mean(la), statistics.mean(lh), max(la), max(lh),
            statistics.mean(ba), statistics.mean(bh), max(ba), max(bh),
            statistics.mean(pa), statistics.mean(ph)))
        print("  AUC  law %.3f  baike %.3f  合并 %.3f" % (auc(la, lh), auc(ba, bh), auc(pa, ph)))
        tradeoff(pa, ph, lint.PASS_LINE)

    if not args.eval:
        print("\n== F 惩罚命中构成（ai / hu 各自平均惩罚分）==")
        for label, group in (("law ai", law_ai), ("law hu", law_hu), ("baike ai", bk_ai), ("baike hu", bk_hu)):
            pens = [f_penalty(t)[0] for t in group]
            hitc = {}
            for t in group:
                for h in f_penalty(t)[1]:
                    hitc[h] = hitc.get(h, 0) + 1
            print("  %-9s mean_pen=%.1f  max=%d  hits=%s" % (
                label, statistics.mean(pens), max(pens), hitc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
