# -*- coding: utf-8 -*-
"""ai_rate.py — 可校准的“AI 参与度”参考评分（humanize-writing skill v0.60）

它做什么：
    用 31 个可解释的汉语写作特征，在冻结的同题配对语料上训练一个逻辑回归，
    用 Platt 校准把原始分数映射为 0–1 的参考值，并给出逐特征贡献与适用边界。

它不做什么：
    - 不鉴定作者身份，不回答“这段是不是 AI 写的”；
    - 不预测知网、Turnitin、GPTZero、朱雀等外部产品的分数；
    - 不对训练分布之外的长文、诗歌、剧本、公文给出可信概率（会显式警告）。

用法：
    python -B scripts/ai_rate.py train --corpora corpora/pairs --out models/zh_hc3_logreg_v1.json
    python -B scripts/ai_rate.py eval --model models/zh_hc3_logreg_v1.json
    python -B scripts/ai_rate.py predict 稿子.md
    python -B scripts/ai_rate.py predict 稿子.md --json --genre fiction
    python -B scripts/ai_rate.py explain        # 打印特征清单与证据编号
"""

import argparse
import hashlib
import json
import math
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import features as F  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MIN_CJK = 100
MAX_WINDOWS = 8
WINDOW_SIZE = 320

# 分数带：只用于报告语言，不是身份判定阈值
BANDS = ((0.35, "偏低"), (0.65, "不确定"), (1.01, "偏高"))

TRAINING_DOMAIN = "中文问答/百科体（HC3-Chinese，ChatGPT 2022 年回答）"

MODEL_NOTE = (
    "校准对象是“同题配对的中文问答文本”，不是通用写作。"
    "跨体裁、跨模型、跨长度时分数会偏移；不得据此判定作者或预测外部检测结果。"
)


def cjk_len(t):
    return F.cjk_count(t)


def band_of(score):
    for edge, name in BANDS:
        if score < edge:
            return name
    return "偏高"


# ---------------------------------------------------------------- 数据加载

def load_pairs(directory):
    """读取 hc3_*.jsonl，返回 {split: [(human, ai, domain, id)]}。"""
    out = {}
    for name in ("train", "cal", "test"):
        path = os.path.join(directory, "hc3_%s.jsonl" % name)
        rows = []
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    r = json.loads(line)
                    rows.append((r["human"], r["ai"], r.get("domain", ""), r["id"]))
        out[name] = rows
    return out


def build_xy(rows):
    X, y, groups = [], [], []
    for human, ai, domain, pid in rows:
        X.append(F.vector(human))
        y.append(0)
        groups.append(pid)
        X.append(F.vector(ai))
        y.append(1)
        groups.append(pid)
    return X, y, groups


# ---------------------------------------------------------------- 数学工具

def sigmoid(z):
    if z < -60:
        return 0.0
    if z > 60:
        return 1.0
    return 1.0 / (1.0 + math.exp(-z))


def standardize_fit(X):
    n = len(X[0])
    mu = [sum(row[j] for row in X) / float(len(X)) for j in range(n)]
    sd = []
    for j in range(n):
        var = sum((row[j] - mu[j]) ** 2 for row in X) / float(len(X))
        sd.append(math.sqrt(var) or 1.0)
    return mu, sd


def standardize_apply(row, mu, sd):
    return [(row[j] - mu[j]) / sd[j] for j in range(len(row))]


def fit_logreg(X, y, epochs=260, lr=0.09, l2=0.008, seed=11):
    """全批量梯度下降的 L2 逻辑回归；类别已等量，不需加权。"""
    mu, sd = standardize_fit(X)
    Z = [standardize_apply(row, mu, sd) for row in X]
    n = len(Z[0])
    w = [0.0] * n
    b = 0.0
    for ep in range(epochs):
        gw = [0.0] * n
        gb = 0.0
        for row, label in zip(Z, y):
            p = sigmoid(sum(wi * xi for wi, xi in zip(w, row)) + b)
            g = p - label
            for j in range(n):
                gw[j] += g * row[j]
            gb += g
        scale = lr / float(len(Z))
        for j in range(n):
            w[j] -= scale * gw[j] + lr * l2 * w[j]
        b -= scale * gb
    return {"mu": mu, "sd": sd, "w": w, "b": b}


def raw_scores(model, X):
    return [
        sum(wi * xi for wi, xi in zip(model["w"], standardize_apply(row, model["mu"], model["sd"])))
        + model["b"]
        for row in X
    ]


def auc(y, scores):
    """Mann–Whitney U 形式的 AUC，处理并列。"""
    pairs = sorted(zip(scores, y))
    ranks = [0.0] * len(pairs)
    i = 0
    while i < len(pairs):
        j = i
        while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
            j += 1
        avg = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    n1 = sum(1 for _, lab in pairs if lab == 1)
    n0 = len(pairs) - n1
    if not n1 or not n0:
        return 0.5
    s = sum(r for r, (_, lab) in zip(ranks, pairs) if lab == 1)
    return (s - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def eer(y, scores):
    """等错误率：FPR 与 FNR 最接近时的错误率。"""
    pairs = sorted(zip(scores, y), reverse=True)
    n1 = sum(y)
    n0 = len(y) - n1
    tp = fp = 0
    best = 1.0
    for s, lab in pairs:
        if lab == 1:
            tp += 1
        else:
            fp += 1
        fpr = fp / float(n0 or 1)
        fnr = (n1 - tp) / float(n1 or 1)
        best = min(best, max(fpr, fnr))
    return best


def brier(y, p):
    return sum((pi - yi) ** 2 for pi, yi in zip(p, y)) / float(len(y))


def log_loss(y, p):
    eps = 1e-9
    return -sum(
        yi * math.log(max(pi, eps)) + (1 - yi) * math.log(max(1 - pi, eps))
        for yi, pi in zip(y, p)
    ) / float(len(y))


def bootstrap_auc(y, scores, groups, iters=200, seed=7):
    """按 pair 重抽样（人类与 AI 成对进出），避免把同题两条当独立样本。"""
    rng = random.Random(seed)
    uniq = sorted(set(groups))
    by_group = {}
    for g, lab, sc in zip(groups, y, scores):
        by_group.setdefault(g, []).append((lab, sc))
    vals = []
    for _ in range(iters):
        picked = [rng.choice(uniq) for _ in range(len(uniq))]
        yy, ss = [], []
        for g in picked:
            for lab, sc in by_group[g]:
                yy.append(lab)
                ss.append(sc)
        vals.append(auc(yy, ss))
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def fit_platt(model, X, y):
    """在校准集上拟合 a*score+b，再做逻辑压缩。"""
    s = raw_scores(model, X)
    a, c = 1.0, 0.0
    for _ in range(400):
        ga = gc = 0.0
        for si, yi in zip(s, y):
            p = sigmoid(a * si + c)
            ga += (p - yi) * si
            gc += (p - yi)
        a -= 0.02 * ga / len(y)
        c -= 0.02 * gc / len(y)
    return a, c


def calibrated(model, X):
    a, c = model["platt"]["a"], model["platt"]["b"]
    return [sigmoid(a * s + c) for s in raw_scores(model, X)]


def calibration_table(y, p, bins=10):
    out = []
    for i in range(bins):
        lo, hi = i / float(bins), (i + 1) / float(bins)
        sel = [pi for pi, yi in zip(p, y) if (lo <= pi < hi or (i == bins - 1 and pi == hi))]
        yy = [yi for pi, yi in zip(p, y) if (lo <= pi < hi or (i == bins - 1 and pi == hi))]
        if sel:
            out.append({
                "bin": "%.1f–%.1f" % (lo, hi),
                "n": len(sel),
                "mean_predicted": round(sum(sel) / len(sel), 3),
                "observed_ai_rate": round(sum(yy) / len(yy), 3),
            })
    return out


# ---------------------------------------------------------------- 训练

def train(corpora_dir, out_path, epochs=260, seed=11):
    data = load_pairs(corpora_dir)
    for split in ("train", "cal", "test"):
        if not data.get(split):
            raise SystemExit("缺少 %s 切分：先运行 scripts/corpus_build.py" % split)
    Xtr, ytr, _ = build_xy(data["train"])
    Xcal, ycal, _ = build_xy(data["cal"])
    Xte, yte, gte = build_xy(data["test"])

    model = fit_logreg(Xtr, ytr, epochs=epochs, seed=seed)
    a, c = fit_platt({"w": model["w"], "b": model["b"], "mu": model["mu"], "sd": model["sd"]},
                     Xcal, ycal)
    model["platt"] = {"a": round(a, 4), "b": round(c, 4)}

    p_tr = calibrated(model, Xtr)
    p_cal = calibrated(model, Xcal)
    p_te = calibrated(model, Xte)
    lo, hi = bootstrap_auc(yte, p_te, gte)

    metrics = {
        "train": {
            "n_pairs": len(data["train"]),
            "auc": round(auc(ytr, p_tr), 4),
            "brier": round(brier(ytr, p_tr), 4),
        },
        "cal": {
            "n_pairs": len(data["cal"]),
            "auc": round(auc(ycal, p_cal), 4),
            "brier": round(brier(ycal, p_cal), 4),
        },
        "test": {
            "n_pairs": len(data["test"]),
            "auc": round(auc(yte, p_te), 4),
            "auc_ci95": [round(lo, 4), round(hi, 4)],
            "eer": round(eer(yte, p_te), 4),
            "brier": round(brier(yte, p_te), 4),
            "log_loss": round(log_loss(yte, p_te), 4),
            "accuracy_at_0.5": round(
                sum(1 for pi, yi in zip(p_te, yte) if (pi >= 0.5) == (yi == 1)) / float(len(yte)), 4
            ),
        },
    }

    model.update({
        "tool": "ai_rate",
        "skill_version": "0.60",
        "model_name": "zh-hc3-logreg-v1",
        "trained_at": "2026-11-12",
        "training_domain": TRAINING_DOMAIN,
        "feature_names": F.FEATURE_NAMES,
        "feature_specs": F.FEATURE_SPECS,
        "metrics": metrics,
        "calibration_table": calibration_table(yte, p_te),
        "corpora": {
            "dir": os.path.relpath(corpora_dir, ROOT).replace(os.sep, "/"),
            "train_pairs": len(data["train"]),
            "cal_pairs": len(data["cal"]),
            "test_pairs": len(data["test"]),
        },
        "note": MODEL_NOTE,
    })

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(model, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("模型已写入 %s" % out_path)
    print("train AUC %.3f / cal AUC %.3f / test AUC %.3f（95%% CI %.3f–%.3f）" % (
        metrics["train"]["auc"], metrics["cal"]["auc"],
        metrics["test"]["auc"], lo, hi))
    print("test EER %.3f · Brier %.3f · 0.5 阈值准确率 %.3f" % (
        metrics["test"]["eer"], metrics["test"]["brier"], metrics["test"]["accuracy_at_0.5"]))
    return model


# ---------------------------------------------------------------- 预测

def load_model(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _contributions(model, vec):
    z = standardize_apply(vec, model["mu"], model["sd"])
    items = []
    for name, zi, wi in zip(model["feature_names"], z, model["w"]):
        spec = model["feature_specs"].get(name, {})
        items.append({
            "name": name,
            "label": spec.get("label", name),
            "value": round(vec[model["feature_names"].index(name)], 3),
            "z": round(zi, 2),
            "weight": round(wi, 3),
            "contribution": round(zi * wi, 3),
            "prior_direction": spec.get("direction", 0),
            "evidence": spec.get("evidence", []),
        })
    return items


def ood_warnings(model, text, vec, genre=None):
    warns = []
    chars = cjk_len(text)
    if genre:
        warns.append(
            "已声明文体「%s」，但模型训练分布是%s；跨体裁分数仅供参考。" % (genre, TRAINING_DOMAIN)
        )
    big = [n for n, v in zip(model["feature_names"], vec)
           if abs((v - model["mu"][model["feature_names"].index(n)]) /
                  model["sd"][model["feature_names"].index(n)]) > 4.0]
    if len(big) >= 6:
        warns.append(
            "有 %d 个特征落在训练分布 4 个标准差之外（如 %s），属于分布外样本，分数不可信。"
            % (len(big), "、".join(big[:4]))
        )
    if chars < 300:
        warns.append("文本仅 %d 个汉字，特征不稳定；建议 ≥300 字再参考。" % chars)
    if re.search(r"(?m)^\s*(第[一二三四五六七八九十百]+[章节回幕场]|[一二三四五六七八九十]+、)", text):
        warns.append("检测到章节/条款编号，结构类特征可能被体裁格式主导。")
    return warns


def predict_text(model, text, genre=None):
    chars = cjk_len(text)
    if chars < MIN_CJK:
        return {
            "tool": "ai_rate",
            "status": "insufficient",
            "chars": chars,
            "message": "有效汉字 %d 个，少于 %d，不评分。换更长片段，或改用 ai_smell_lint.py 的定位结果。" % (chars, MIN_CJK),
            "is_authorship_judgment": False,
        }
    segs = [text] if chars <= 1400 else [w[1] for w in F.windows(text, size=WINDOW_SIZE, max_windows=MAX_WINDOWS)]
    scores = []
    all_vecs = []
    for seg in segs:
        vec = F.vector(seg)
        all_vecs.append(vec)
        scores.append(calibrated(model, [vec])[0])
    scores_sorted = sorted(scores)
    median = scores_sorted[len(scores_sorted) // 2]
    p25 = scores_sorted[int(0.25 * (len(scores_sorted) - 1))]
    p75 = scores_sorted[int(0.75 * (len(scores_sorted) - 1))]
    full_vec = F.vector(text)
    contrib = sorted(_contributions(model, full_vec), key=lambda x: abs(x["contribution"]), reverse=True)[:8]
    warns = ood_warnings(model, text, full_vec, genre)
    if len(segs) > 1:
        warns.append("分数取分窗中位数，而特征贡献按整篇向量计算；两者口径不同，贡献只用于定位句子。")
    return {
        "tool": "ai_rate",
        "status": "ok",
        "model": model["model_name"],
        "chars": chars,
        "windows": len(segs),
        "score": round(median, 3),
        "score_iqr": [round(p25, 3), round(p75, 3)],
        "band": band_of(median),
        "window_scores": [round(s, 3) for s in scores],
        "top_features": contrib,
        "warnings": warns,
        "is_authorship_judgment": False,
        "note": "0–1 是训练分布内的校准参考值，不是“AI 生成概率”，不能用于判定作者。",
    }


def read_text(path):
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            with open(path, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise SystemExit("无法解码：%s（支持 UTF-8 / GB18030）" % path)


def format_report(r):
    if r.get("status") != "ok":
        return r.get("message", "无法评分")
    lines = [
        "参考值 %.2f（%s；窗口 %d，IQR %.2f–%.2f）" % (
            r["score"], r["band"], r["windows"], r["score_iqr"][0], r["score_iqr"][1]),
        "训练分布：中文问答/百科体；跨体裁会偏移。此值不是作者判定，也不预测外部检测分数。",
    ]
    if r["windows"] > 1:
        lines.append("分窗：%s" % ", ".join("%.2f" % s for s in r["window_scores"]))
    lines.append("主要贡献（绝对值排序，正=偏 AI 侧，负=偏人写侧）：")
    for it in r["top_features"]:
        lines.append("  %+.2f  %s（实测 %.2f）·证据 %s" % (
            it["contribution"], it["label"], it["value"], ",".join(it["evidence"]) or "—"))
    for w in r["warnings"]:
        lines.append("注意：" + w)
    return "\n".join(lines)


# ---------------------------------------------------------------- 外部评估

def eval_external(model, classic_dir, cred_dir, calib_dir):
    rows = []
    if classic_dir and os.path.isdir(classic_dir):
        scores = []
        for fn in sorted(os.listdir(classic_dir)):
            if not fn.endswith(".md") or fn.upper().startswith("SOURCES"):
                continue
            t = read_text(os.path.join(classic_dir, fn))
            if cjk_len(t) < MIN_CJK:
                continue
            scores.append((fn, calibrated(model, [F.vector(t)])[0]))
        if scores:
            mean = sum(s for _, s in scores) / len(scores)
            flagged = [n for n, s in scores if s >= 0.5]
            rows.append({
                "set": "公版人写文本（鲁迅/朱自清等，非训练域）",
                "n": len(scores),
                "mean_score": round(mean, 3),
                "flagged_at_0.5": flagged,
            })
    if cred_dir and os.path.isdir(cred_dir):
        human_files = sorted(f for f in os.listdir(cred_dir) if f.startswith("human_"))
        ai_files = sorted(f for f in os.listdir(cred_dir) if f.startswith("ai_"))
        hs = [calibrated(model, [F.vector(read_text(os.path.join(cred_dir, f)))])[0]
              for f in human_files if cjk_len(read_text(os.path.join(cred_dir, f))) >= MIN_CJK]
        as_ = [calibrated(model, [F.vector(read_text(os.path.join(cred_dir, f)))])[0]
               for f in ai_files if cjk_len(read_text(os.path.join(cred_dir, f))) >= MIN_CJK]
        if hs and as_:
            y = [0] * len(hs) + [1] * len(as_)
            rows.append({
                "set": "C-ReD 中文配对（学术/评论/作文，跨语料）",
                "n": len(hs) + len(as_),
                "human_n": len(hs),
                "ai_n": len(as_),
                "auc": round(auc(y, hs + as_), 4),
            })
    if calib_dir and os.path.isdir(calib_dir):
        scores = []
        for fn in sorted(os.listdir(calib_dir)):
            if fn.endswith(".md") and not fn.upper().startswith("CALIB"):
                t = read_text(os.path.join(calib_dir, fn))
                if cjk_len(t) >= MIN_CJK:
                    scores.append((fn, calibrated(model, [F.vector(t)])[0]))
        if scores:
            rows.append({
                "set": "项目内 AI 校准样本（多文体）",
                "n": len(scores),
                "mean_score": round(sum(s for _, s in scores) / len(scores), 3),
                "min_score": round(min(s for _, s in scores), 3),
            })
    return rows


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="可校准的 AI 参与度参考评分")
    sub = ap.add_subparsers(dest="cmd")

    t = sub.add_parser("train", help="在 corpora/pairs 上训练并写模型")
    t.add_argument("--corpora", default=os.path.join(ROOT, "corpora", "pairs"))
    t.add_argument("--out", default=os.path.join(ROOT, "models", "zh_hc3_logreg_v1.json"))

    p = sub.add_parser("predict", help="给文本打分")
    p.add_argument("paths", nargs="+")
    p.add_argument("--model", default=os.path.join(ROOT, "models", "zh_hc3_logreg_v1.json"))
    p.add_argument("--genre", default=None, help="声明文体（仅用于提示跨域风险）")
    p.add_argument("--json", action="store_true")

    e = sub.add_parser("eval", help="在项目内外部集上评估")
    e.add_argument("--model", default=os.path.join(ROOT, "models", "zh_hc3_logreg_v1.json"))
    e.add_argument("--classic", default=os.path.join(ROOT, "tests", "corpus_classic"))
    e.add_argument("--cred", default=os.path.join(ROOT, "tests", "corpus_cred"))
    e.add_argument("--calib", default=os.path.join(ROOT, "tests", "corpus_ai_calib"))

    sub.add_parser("explain", help="打印特征清单")

    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help()
        return 2

    if args.cmd == "train":
        train(args.corpora, args.out)
        return 0

    if args.cmd == "explain":
        for name in F.FEATURE_NAMES:
            spec = F.FEATURE_SPECS[name]
            print("%-24s %-30s 先验%+d  证据:%s" % (
                name, spec["label"], spec["direction"], ",".join(spec["evidence"]) or "—"))
        return 0

    model = load_model(args.model)

    if args.cmd == "eval":
        rows = eval_external(model, args.classic, args.cred, args.calib)
        print("外部集评估（模型 %s）" % model["model_name"])
        for r in rows:
            print(" - %s" % json.dumps(r, ensure_ascii=False))
        print("注意：这些数字只说明该模型在这些文件上的表现，不构成通用能力证明。")
        return 0

    if args.cmd == "predict":
        results = []
        for path in args.paths:
            if os.path.isdir(path):
                for fn in sorted(os.listdir(path)):
                    if fn.endswith((".md", ".txt")):
                        full = os.path.join(path, fn)
                        results.append((full, predict_text(model, read_text(full), args.genre)))
            else:
                results.append((path, predict_text(model, read_text(path), args.genre)))
        if args.json:
            print(json.dumps({
                "model": model["model_name"],
                "results": [{"path": p, "result": r} for p, r in results],
            }, ensure_ascii=False, indent=2))
        else:
            for path, res in results:
                print("\n== %s" % path)
                print(format_report(res))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
