# -*- coding: utf-8 -*-
"""第三方语料分离度测量（v0.24）。

对 tests/corpus_hc3/ 的 60 篇第三方样本跑 lint，输出：
  · 分组分数统计（分 law / general 门控）
  · 各域 AUC（AI 分数 > 人类分数的概率）
  · 阈值—召回—误报权衡表

用途是**测量**，不是调参：本脚本不写入任何权重。
用法：python tests/hc3_measure.py
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


D = ROOT / "tests" / "corpus_hc3"
DOMAINS = {
    "law": ("ai_hc3law_m_*.md", "human_hc3law_*.md"),
    "baike": ("ai_hc3baike_*.md", "human_hc3baike_*.md"),
}
GENRES = ("law", "general")


def score_of(p, genre):
    _, status, score = lint.evaluate(p.read_text(encoding="utf-8"), genre=genre)
    return score if status == "ok" else None


def auc(a, h):
    return measure.auc(a, h)


def main():
    print("HC3 历史冻结语料回归；探索性来源对照，不鉴定作者")
    print("静态阈值 PASS_LINE=%d GOOD_LINE=%d" % (lint.PASS_LINE, lint.GOOD_LINE))
    for genre in GENRES:
        print()
        print("门控 --genre %s" % genre)
        pooled_ai, pooled_human = [], []
        for dom, (ai_pat, hu_pat) in DOMAINS.items():
            ag = measure.collect(sorted(D.glob(ai_pat)), genre, lint.evaluate)
            hg = measure.collect(sorted(D.glob(hu_pat)), genre, lint.evaluate)
            ai, hu = ag["scores"], hg["scores"]
            pooled_ai.extend(ai)
            pooled_human.extend(hu)
            print("  %s | AI %s | human %s | AUC %s" % (
                dom, measure.describe(ai, lint.PASS_LINE), measure.describe(hu, lint.PASS_LINE), measure.fmt(auc(ai, hu), 3)))
            print("  coverage: AI %s；human %s" % (measure.coverage_text(ag), measure.coverage_text(hg)))
        print("  合并 AI %s | human %s | AUC %s" % (
            measure.describe(pooled_ai, lint.PASS_LINE), measure.describe(pooled_human, lint.PASS_LINE),
            measure.fmt(auc(pooled_ai, pooled_human), 3)))
        print("  阈值  可判定子集TPR  可判定子集FPR")
        for t in (20, 25, 30, 35, 39, 40, 45):
            tpr = measure.rate(sum(s > t for s in pooled_ai), len(pooled_ai))
            fpr = measure.rate(sum(s > t for s in pooled_human), len(pooled_human))
            print("  %-5d %-14s %s" % (t, measure.fmt(tpr), measure.fmt(fpr)))
    print("AUC 汇总排序，不单独决定可用操作点；须依据实际阈值曲线和预先指定的TPR/FPR要求判断。")
    print("分母为0显示N/A；弃判不计TN或FN。历史数据重跑不是新的独立盲测，不据此调权重。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
