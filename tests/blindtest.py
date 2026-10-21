# -*- coding: utf-8 -*-
"""t13 历史冻结语料回归（保留脚本旧名）：真人语料（标签=人写，期望低分）对比 LLM 同文体对照样本（标签=AI，期望高分）。

每篇按各自文体门控跑 lint；仅将自身静态阈值 PASS_LINE 用作探索性的来源标签对照。
这不将静态分数解释为作者身份或 AI 概率；已消费样本重跑不是新的独立盲测。

运行:
    python tests/blindtest.py

输出: 门控/general 得分、coverage、可判定子集混淆矩阵与P/R/FPR/FNR；零分母显示N/A。
局限: 每类 n=4，AI 样本与 lint 同源（tests/corpus_ai/SAMPLES.md），
指标仅作方向性参考，不构成对泛化性能的估计。
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ai_smell_lint", ROOT / "scripts" / "ai_smell_lint.py"
)
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)

# (genre, 文件名)，标签=人写（负样本），与 tests/corpus/SOURCES.md 对应
HUMAN = [
    ("law", "law_gongbao_hongxiufeng.md"),
    ("email", "email_liangdishu.md"),
    ("speech", "speech_wen_yiduo_zuihou.md"),
    ("fiction", "fiction_kong_yiji.md"),
]
# 标签=AI（正样本），与 tests/corpus_ai/SAMPLES.md 对应
AI = [
    ("law", "ai_law_memo.md"),
    ("email", "ai_email_reply.md"),
    ("speech", "ai_speech_ceremony.md"),
    ("fiction", "ai_fiction_excerpt.md"),
]


def run_all(rows, d, gated=True):
    out = []
    for genre, name in rows:
        text = (d / name).read_text(encoding="utf-8")
        g = genre if gated else "general"
        issues, status, score = lint.evaluate(text, genre=g)
        deduct = [m for w, m in issues if w]
        out.append((name, g, status, score, deduct))
    return out


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def fmt_rate(value):
    return "N/A" if value is None else "%.2f" % value


def coverage(rows):
    assessed = sum(st == "ok" for _, _, st, _, _ in rows)
    return {"total": len(rows), "assessed": assessed,
            "abstained": len(rows) - assessed, "rate": ratio(assessed, len(rows))}


def metrics(ai_rows, human_rows, thr):
    """只对可判定子集计算探索性阈值指标；弃判另报 coverage。"""
    ai = [s for _, _, st, s, _ in ai_rows if st == "ok"]
    human = [s for _, _, st, s, _ in human_rows if st == "ok"]
    tp = sum(s > thr for s in ai)
    fn = len(ai) - tp
    fp = sum(s > thr for s in human)
    tn = len(human) - fp
    return (tp, fn, tn, fp, ratio(tp, tp + fp), ratio(tp, tp + fn),
            ratio(fp, fp + tn), ratio(fn, fn + tp))


def show(rows):
    for name, genre, status, score, deduct in rows:
        print("  %-30s genre=%-8s score=%3d %s%s" % (
            name, genre, score, lint.label_of(score, status),
            "" if not deduct else "  扣分: " + "; ".join(deduct)))


def block(title, ai_rows, human_rows, thr):
    print(title)
    print("[来源标签 human · 历史对照]")
    show(human_rows)
    print("[来源标签 AI · 历史对照]")
    show(ai_rows)
    for name, rows in (("AI", ai_rows), ("human", human_rows)):
        c = coverage(rows)
        print("覆盖率 %s: %d/%d = %s；弃判 %d" % (
            name, c["assessed"], c["total"], fmt_rate(c["rate"]), c["abstained"]))
    tp, fn, tn, fp, p, r, fpr, fnr = metrics(ai_rows, human_rows, thr)
    print("可判定子集混淆矩阵: TP=%d FN=%d TN=%d FP=%d" % (tp, fn, tn, fp))
    print("探索性指标 P=%s  R=%s  FPR=%s  FNR=%s（分母为0显示N/A）"
          % tuple(fmt_rate(v) for v in (p, r, fpr, fnr)))


def main():
    thr = lint.PASS_LINE
    d_h = ROOT / "tests" / "corpus"
    d_a = ROOT / "tests" / "corpus_ai"
    print("历史冻结语料回归（静态阈值 PASS_LINE=%d；探索性来源对照，不鉴定作者）" % thr)
    block("\n== A. 门控模式：每篇按各自文体门控（lint 实际使用方式）==",
          run_all(AI, d_a), run_all(HUMAN, d_h), thr)
    block("\n== B. general 模式：不知文体时的默认检测（门控代价对照）==",
          run_all(AI, d_a, gated=False), run_all(HUMAN, d_h, gated=False), thr)
    print("\n局限：AI 样本与 lint 同源（同一开发线生成），每类仅 4 篇；这些语料已参与开发或回归，不是新独立盲测，"
          "指标仅作方向性参考（tests/corpus_ai/SAMPLES.md）。\n"
          "B 列仅作门控代价呈现，不改变判定；据此调参 = 用测试集刷分，禁止。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
