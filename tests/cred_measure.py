# -*- coding: utf-8 -*-
"""第三方语料分离度测量（v0.26，只测不调）。

对两组新落库语料跑 lint：
  · tests/corpus_cred/    C-ReD 抽样 360 篇（3 域 × 30 human + 9 生成器 × 10 AI），
                          测**多模型泛化**（claude/deepseek/doubao/gemini/gpt/qwen 九家）
  · tests/corpus_classic/ 民国公版真人文本 11 篇（仅人写正样本），
                          测**跨时代误报**（当代检测器对民国白话/文言的表现）

用途是**测量**，不是调参：本脚本不写入任何权重，不改任何阈值、词表或规则。
来源与抽样协议见各目录 SOURCES.md。
用法：python tests/cred_measure.py
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ai_smell_lint", ROOT / "scripts" / "ai_smell_lint.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)

helper_spec = importlib.util.spec_from_file_location("measurement_helpers", ROOT / "tests" / "measurement_helpers.py")
measure = importlib.util.module_from_spec(helper_spec)
helper_spec.loader.exec_module(measure)


D_CRED = ROOT / "tests" / "corpus_cred"
D_CLASSIC = ROOT / "tests" / "corpus_classic"

# C-ReD 域 → lint 门控（见 corpus_cred/SOURCES.md 门控映射）
CRED = {
    "composition": "fiction",
    "film": "general",
    "paper": "academic",
}
GENS = ("claude35haiku", "deepseekr1", "deepseekv3", "doubao15pro",
        "gemini25flash", "gpt35turbo", "gpt4o", "qwen25", "qwen3")


def score_of(p, genre):
    _, status, score = lint.evaluate(p.read_text(encoding="utf-8"), genre=genre)
    return score if status == "ok" else None


def auc(a, h):
    return measure.auc(a, h)


def stat_line(tag, scores):
    return tag + " " + measure.describe(scores, lint.PASS_LINE)


def section_cred():
    print("A. C-ReD 历史冻结语料回归（探索性来源对照，不鉴定作者）")
    if not any(D_CRED.glob("human_*.md")):
        print("   样本未随仓库分发（上游未声明许可证）；重建："
              "python -B tests/build_cred_corpus.py --repo <C-ReD 目录>")
        return
    pooled_ai, pooled_hu = [], []
    for dom, gate in CRED.items():
        hg = measure.collect(sorted(D_CRED.glob("human_cred%s_*.md" % dom)), gate, lint.evaluate)
        hu = hg["scores"]
        pooled_hu.extend(hu)
        print()
        print("-- 域 %s -> %s -- human %s；coverage %s" % (
            dom, gate, stat_line("human", hu), measure.coverage_text(hg)))
        dom_ai = []
        for g in GENS:
            ag = measure.collect(sorted(D_CRED.glob("ai_cred%s_%s_*.md" % (dom, g))), gate, lint.evaluate)
            ai = ag["scores"]
            dom_ai.extend(ai)
            print("   %-14s %s；coverage %s" % (g, stat_line("AI", ai), measure.coverage_text(ag)))
        pooled_ai.extend(dom_ai)
        print("   域内合并 %s | AUC %s" % (stat_line("AI", dom_ai), measure.fmt(auc(dom_ai, hu), 3)))
    print()
    print("三域合并：%s" % stat_line("AI", pooled_ai))
    print("          %s | AUC %s" % (stat_line("human", pooled_hu), measure.fmt(auc(pooled_ai, pooled_hu), 3)))
    print("阈值  可判定子集TPR  可判定子集FPR")
    for t in (20, 25, 30, 35, 39, 40, 45):
        print("%-5d %-14s %s" % (t,
            measure.fmt(measure.rate(sum(s > t for s in pooled_ai), len(pooled_ai))),
            measure.fmt(measure.rate(sum(s > t for s in pooled_hu), len(pooled_hu)))))


def classic_gate(name):
    if name.startswith(("prose_", "fiction_")):
        return "fiction"
    if name.startswith("speech_"):
        return "speech"
    if name.startswith("law_"):
        return "law"
    raise ValueError(name)


def section_classic():
    print()
    print("B. 历史公版标签文本回归，仅本次样本；不外推作者身份")
    files = sorted(p for p in D_CLASSIC.glob("*.md") if p.name != "SOURCES.md")
    fp = assessed = 0
    for p in files:
        g = classic_gate(p.name)
        issues, status, score = lint.evaluate(p.read_text(encoding="utf-8"), genre=g)
        deduct = [m for w, m in issues if w]
        assessed += status == "ok"
        fp += status == "ok" and score > lint.PASS_LINE
        print("  %-36s genre=%-8s score=%3d %s%s" % (
            p.name, g, score, lint.label_of(score, status),
            "" if not deduct else "  线索: " + "; ".join(deduct)))
    print("coverage %d/%d=%s；弃判%d；可判定子集超线 %d/%d=%s" % (
        assessed, len(files), measure.fmt(measure.rate(assessed, len(files))), len(files)-assessed,
        fp, assessed, measure.fmt(measure.rate(fp, assessed))))
    print("局限：历史语域、节选及来源登记限制；本次重跑不是新的独立盲测，不据此调参。")


def main():
    print("第三方语料分离度测量（v0.26：corpus_cred + corpus_classic）")
    print("阈值 PASS_LINE=%d  GOOD_LINE=%d" % (lint.PASS_LINE, lint.GOOD_LINE))
    section_cred()
    section_classic()
    print("\n本测量不写入权重：可分性不足时调参只是拟合噪声。"
          "见 corpus_cred/SOURCES.md、corpus_classic/SOURCES.md 与 research-basis.md。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
