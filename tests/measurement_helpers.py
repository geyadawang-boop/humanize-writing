"""Exploratory measurement helpers; unknown inputs are abstentions, never negatives."""
import statistics


def rate(numerator, denominator):
    return numerator / denominator if denominator else None


def fmt(value, digits=2):
    return "N/A" if value is None else format(value, ".%df" % digits)


def auc(ai, human):
    if not ai or not human:
        return None
    return sum((a > h) + 0.5 * (a == h) for a in ai for h in human) / (len(ai) * len(human))


def collect(paths, genre, evaluate):
    scores = []
    total = 0
    for path in paths:
        total += 1
        _, status, score = evaluate(path.read_text(encoding="utf-8"), genre=genre)
        if status == "ok":
            scores.append(score)
    return {"scores": scores, "total": total, "assessed": len(scores),
            "abstained": total - len(scores), "coverage": rate(len(scores), total)}


def coverage_text(group):
    return "%d/%d=%s，弃判%d" % (group["assessed"], group["total"], fmt(group["coverage"]), group["abstained"])


def describe(scores, threshold):
    if not scores:
        return "均分/中位/范围 N/A（可判定样本0；超线率N/A）"
    return "均分 %.1f 中位 %.1f 范围 %d–%d（超线 %d/%d）" % (
        statistics.mean(scores), statistics.median(scores), min(scores), max(scores),
        sum(s > threshold for s in scores), len(scores))
