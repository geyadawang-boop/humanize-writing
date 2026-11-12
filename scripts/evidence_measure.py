# -*- coding: utf-8 -*-
"""evidence_measure.py — 在冻结语料上测量每条规则与每个特征的区分力

用法：
    python -B scripts/evidence_measure.py                 # 测量并写 JSON
    python -B scripts/evidence_measure.py --update-ledger # 同时把实测值写进规则台账

输出：
    references/feature-evidence.json   特征级：δ、AUC、分域 δ
    references/rule-measurements.json  规则级：人类/AI 每千字加权命中

口径：
- δ = 2*AUC - 1，AUC 为“人类文本取值高于 AI 文本”的概率；正号表示人类侧更高。
- 规则按 ai_smell_lint.py 的实际输出统计，权重取该规则在 lint 中的返回值。
- 语料是中文问答体（HC3-Chinese），测量结果只在该分布内成立。
"""

import argparse
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import features as F  # noqa: E402
import ai_smell_lint as L  # noqa: E402

CORPORA = os.path.join(ROOT, "corpora", "pairs")
OUT_FEATURE = os.path.join(ROOT, "references", "feature-evidence.json")
OUT_RULE = os.path.join(ROOT, "references", "rule-measurements.json")
LEDGER = os.path.join(ROOT, "references", "rule-ledger.json")

DOMAINS = ("baike", "open_qa", "finance", "law", "nlpcc_dbqa")


def load_all():
    rows = []
    for split in ("train", "cal", "test"):
        path = os.path.join(CORPORA, "hc3_%s.jsonl" % split)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    r["split"] = split
                    rows.append(r)
    return rows


def auc(hs, as_):
    pairs = sorted([(v, 0) for v in hs] + [(v, 1) for v in as_])
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
    n1 = len(hs)
    n0 = len(as_)
    if not n1 or not n0:
        return 0.5
    s = sum(r for r, (_, lab) in zip(ranks, pairs) if lab == 0)
    return (s - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def feature_evidence(rows):
    names = F.FEATURE_NAMES
    per = {n: {"human": [], "ai": []} for n in names}
    per_domain = {d: {n: {"human": [], "ai": []} for n in names} for d in DOMAINS}
    for r in rows:
        fh = F.extract(r["human"])
        fa = F.extract(r["ai"])
        for n in names:
            per[n]["human"].append(fh[n])
            per[n]["ai"].append(fa[n])
            if r["domain"] in per_domain:
                per_domain[r["domain"]][n]["human"].append(fh[n])
                per_domain[r["domain"]][n]["ai"].append(fa[n])

    out = {}
    for n in names:
        h, a = per[n]["human"], per[n]["ai"]
        A = auc(h, a)
        out[n] = {
            "label": F.FEATURE_SPECS[n]["label"],
            "human_median": round(statistics.median(h), 2),
            "ai_median": round(statistics.median(a), 2),
            "delta": round(2 * A - 1, 3),
            "auc": round(A, 3),
            "per_domain_delta": {
                d: (round(2 * auc(v["human"], v["ai"]) - 1, 2) if len(v["human"]) >= 30 else None)
                for d, v in ((d, per_domain[d][n]) for d in DOMAINS)
            },
        }
    return out


def rule_evidence(rows):
    """按“有多少篇触发该规则”统计命中率，避免零权重规则被算成 0。

    输出每条规则：
      human_rate / ai_rate：触发该规则的文本占比（%）
      diff_pp：AI 侧命中率减人类侧（百分点），正=AI 更多
      mean_weight：触发时的平均权重
    """
    tags = {}
    totals = {"human": 0, "ai": 0}
    for r in rows:
        for label in ("human", "ai"):
            text = r[label]
            issues, status = L.check(text, genre="general", language="zh")
            if status not in ("ok", "limited"):
                continue
            totals[label] += 1
            seen = {}
            for weight, msg in issues:
                m = msg.strip()
                if not m.startswith("["):
                    continue
                tag = m[1:m.find("]")] if "]" in m else m
                if tag not in seen or weight > seen[tag]:
                    seen[tag] = weight
            for tag, weight in seen.items():
                rec = tags.setdefault(tag, {"h": 0, "a": 0, "wh": [], "wa": []})
                if label == "human":
                    rec["h"] += 1
                    rec["wh"].append(weight)
                else:
                    rec["a"] += 1
                    rec["wa"].append(weight)
    out = {}
    for tag, rec in tags.items():
        nh = totals["human"] or 1
        na = totals["ai"] or 1
        if nh < 100 or na < 100:
            continue
        if rec["h"] + rec["a"] < 20:
            continue
        hr = 100.0 * rec["h"] / nh
        ar = 100.0 * rec["a"] / na
        if hr > 90 and ar > 90:
            continue  # 纯观察行，两侧都出现，不具区分力
        out[tag] = {
            "human_rate_pct": round(hr, 1),
            "ai_rate_pct": round(ar, 1),
            "diff_pp": round(ar - hr, 1),
            "human_hits": rec["h"],
            "ai_hits": rec["a"],
            "mean_weight_human": round(statistics.mean(rec["wh"]), 1) if rec["wh"] else 0,
            "mean_weight_ai": round(statistics.mean(rec["wa"]), 1) if rec["wa"] else 0,
            "n_human": nh,
            "n_ai": na,
        }
    return out


def update_ledger(rules):
    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    matched = 0
    for rule in ledger["rules"]:
        tag = rule.get("tag") or ""
        key = tag[1:-1] if tag.startswith("[") and tag.endswith("]") else tag
        m = rules.get(key)
        if not m:
            # 本轮未达到测量门槛（样本少或两侧都高频）：删掉旧值，避免台账混用两代口径
            rule.pop("measured_v060", None)
            continue
        matched += 1
        diff = m["diff_pp"]
        if diff >= 5:
            verdict = "AI 侧命中率更高（方向与本规则一致）"
        elif diff <= -5:
            verdict = "人类侧命中率更高（方向与本规则相反）"
        else:
            verdict = "两侧命中率相差 <5 个百分点（不足以支撑该规则）"
        rule["measured_v060"] = {
            "corpus": "HC3-Chinese 中文问答体（随包 5203 对）",
            "human_rate_pct": m["human_rate_pct"],
            "ai_rate_pct": m["ai_rate_pct"],
            "diff_pp": diff,
            "mean_weight_human": m["mean_weight_human"],
            "mean_weight_ai": m["mean_weight_ai"],
            "verdict": verdict,
        }
    ledger["measurement"] = {
        "script": "scripts/evidence_measure.py",
        "corpus": "corpora/pairs（HC3-Chinese 子集，5203 对）",
        "metric": "触发该规则的文本占比（%），diff_pp = AI 侧 - 人类侧",
        "updated": "2026-11-12",
        "matched_rules": matched,
        "note": "本轮只登记实测，不改权重与阈值；ruleset_version 因此保持不变。",
    }
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("规则台账已更新：%d 条规则写入 measured_v060" % matched)


def main(argv=None):
    ap = argparse.ArgumentParser(description="测量冻结语料上的规则与特征区分力")
    ap.add_argument("--update-ledger", action="store_true")
    args = ap.parse_args(argv)

    rows = load_all()
    if len(rows) < 500:
        raise SystemExit("语料不足，先运行 scripts/corpus_build.py")
    print("语料 %d 对；开始测量特征…" % len(rows))
    feats = feature_evidence(rows)
    print("开始测量规则（逐篇跑 lint，约需 1–2 分钟）…")
    rules = rule_evidence(rows)

    with open(OUT_FEATURE, "w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "corpus": "corpora/pairs（HC3-Chinese 子集）",
            "pairs": len(rows),
            "delta_definition": "2*AUC-1，正号=人类侧取值更高",
            "features": feats,
        }, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(OUT_RULE, "w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "corpus": "corpora/pairs（HC3-Chinese 子集）",
            "pairs": len(rows),
            "metric": "触发该规则的文本占比（%）；diff_pp = AI 侧 - 人类侧",
            "rules": rules,
        }, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("\n特征区分力（|δ| 前 12）：")
    for n, v in sorted(feats.items(), key=lambda kv: -abs(kv[1]["delta"]))[:12]:
        print("  %-24s δ=%+.2f 人%.2f/AI%.2f" % (n, v["delta"], v["human_median"], v["ai_median"]))
    print("\n规则命中率差异（|diff| 前 12）：")
    for t, v in sorted(rules.items(), key=lambda kv: -abs(kv[1]["diff_pp"]))[:12]:
        print("  %-16s 人%5.1f%% / AI%5.1f%%  diff=%+.1fpp  触发 %d/%d" % (
            t, v["human_rate_pct"], v["ai_rate_pct"], v["diff_pp"], v["human_hits"], v["ai_hits"]))
    bad = [t for t, v in rules.items() if v["diff_pp"] <= -5]
    print("\n方向与本规则相反（人类侧命中更多）：" + ("、".join(bad) if bad else "无"))

    if args.update_ledger:
        update_ledger(rules)
    return 0


if __name__ == "__main__":
    sys.exit(main())
