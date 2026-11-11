# -*- coding: utf-8 -*-
"""用本项目自带的同题配对语料锁住权重方向：规则降权/保留必须与数据一致。

配对方式：corpus_hc3 的 human_*/ai_* 同名配对；corpus_cred 的 human_主题_序号 与
ai_主题_模型_序号 配对。判据只看方向，不追求显著：样本量小，δ 只用于排除反方向。
"""
import importlib.util
import json
from pathlib import Path
import re
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("direction_lint", ROOT / "scripts" / "ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)
LEDGER = json.loads((ROOT / "references" / "rule-ledger.json").read_text(encoding="utf-8"))


def body_of(path):
    return LINT.strip_markdown(path.read_text(encoding="utf-8-sig"))


def count_density(text):
    body = body_of(text)
    total = LINT.chinese_len(body) or 1
    return {w: body.count(w) * 1000.0 / total for w in LINT.ROAD_WORDS + LINT.STRONG_WORDS}


def hc3_pairs():
    base = ROOT / "tests" / "corpus_hc3"
    humans = {p.name.replace("human_", ""): p for p in base.glob("human_*.md")}
    ais = {p.name.replace("ai_", ""): p for p in base.glob("ai_*.md")}
    return [(humans[k], ais[k]) for k in sorted(set(humans) & set(ais))]


def cred_pairs():
    base = ROOT / "tests" / "corpus_cred"
    humans, ais = {}, {}
    for p in base.glob("human_*.md"):
        m = re.fullmatch(r"human_(.+?)_(\d+)\.md", p.name)
        if m:
            humans[(m.group(1), m.group(2))] = p
    for p in base.glob("ai_*.md"):
        m = re.fullmatch(r"ai_(.+?)_([a-z0-9]+)_(\d+)\.md", p.name)
        if m:
            ais[(m.group(1), m.group(3))] = p
    return [(humans[k], ais[k]) for k in sorted(set(humans) & set(ais))]


def mean(values):
    return statistics.mean(values) if values else 0.0


class CorpusDirectionTests(unittest.TestCase):
    def test_pairs_are_actually_present(self):
        self.assertEqual(len(hc3_pairs()), 12, "hc3 同题配对不应为空")
        self.assertEqual(len(cred_pairs()), 30, "cred 同题配对不应为空")

    def test_road_words_are_not_denser_in_ai(self):
        pairs = [(count_density(h), count_density(a)) for h, a in cred_pairs()]
        human = mean([sum(d[w] for w in LINT.ROAD_WORDS) for d, _ in pairs])
        machine = mean([sum(d[w] for w in LINT.ROAD_WORDS) for _, d in pairs])
        self.assertGreaterEqual(human, machine,
                                "cred 配对语料里路标词人类不更少（%.2f vs %.2f），降权方向必须保持"
                                % (human, machine))
        self.assertEqual(next(r for r in LEDGER["rules"] if r["tag"] == "[路标词]")["kind"], "observation")

    def test_strong_words_lean_ai_enough_to_keep_weight(self):
        pairs = [(count_density(h), count_density(a)) for h, a in cred_pairs()]
        human = mean([sum(d[w] for w in LINT.STRONG_WORDS) for d, _ in pairs])
        machine = mean([sum(d[w] for w in LINT.STRONG_WORDS) for _, d in pairs])
        self.assertGreaterEqual(machine, human,
                                "AI 词在 cred 上应不低于人类（%.2f vs %.2f），否则应降权" % (machine, human))
        self.assertEqual(next(r for r in LEDGER["rules"] if r["tag"] == "[AI 词]")["kind"], "weighted")

    def test_paragraph_start_repetition_leans_ai(self):
        def hits(path):
            body = body_of(path)
            if LINT.chinese_len(body) < LINT.MIN_CHARS:
                return 0
            starts = [p[:3] for p in LINT.raw_paragraphs(body)]
            return 1 if max((starts.count(s) for s in set(starts)), default=0) >= 3 else 0
        pairs = hc3_pairs()
        self.assertGreaterEqual(sum(hits(a) for _, a in pairs), sum(hits(h) for h, _ in pairs),
                                "hc3 配对上段首重复应偏 AI，否则应降权")
        self.assertEqual(next(r for r in LEDGER["rules"] if r["tag"] == "[段落开头]")["kind"], "weighted")

    def test_translationese_family_has_no_stable_direction(self):
        """整族在两套语料上方向相反，因此只允许零权重。"""
        def density(path):
            body = body_of(path)
            total = LINT.chinese_len(body) or 1
            hits = sum(len(rx.findall(body)) for _, rx in LINT.TRANSLATIONESE)
            return hits * 1000.0 / total

        hc3_diff = mean([a - h for h, a in ((density(x), density(y)) for x, y in hc3_pairs())])
        cred_diff = mean([a - h for h, a in ((density(x), density(y)) for x, y in cred_pairs())])
        self.assertLess(hc3_diff * cred_diff, 0,
                        "两套语料方向必须相反才允许零权重（hc3 %+.2f / cred %+.2f）"
                        % (hc3_diff, cred_diff))
        rule = next(r for r in LEDGER["rules"] if r["tag"] == "[翻译腔]")
        self.assertEqual(rule["kind"], "observation")
        self.assertTrue(str(rule["weight"]).startswith("0"))

    def test_isomorphism_leans_ai_but_human_classics_also_trigger(self):
        def density(path):
            runs2, _, total = LINT.isomorphism_runs(body_of(path))
            return len(runs2) * 100.0 / total if total else 0.0

        cred_diff = mean([a - h for h, a in ((density(x), density(y)) for x, y in cred_pairs())])
        self.assertGreater(cred_diff, 0.0, "cred 上两句同构应偏 AI（实得 %+.2f）" % cred_diff)
        classic = max(density(p) for p in (ROOT / "tests" / "corpus_classic").glob("*.md"))
        self.assertGreater(classic, 4.0,
                           "人类经典同样高频触发（实测最高 %.1f 组/百句），所以只能零权重" % classic)
        rule = next(r for r in LEDGER["rules"] if r["tag"] == "[相邻同构]")
        self.assertEqual(rule["kind"], "observation")
        self.assertTrue(str(rule["weight"]).startswith("0"))

    def test_worst_case_direction_is_not_reversed(self):
        """整篇加权分不得出现"人类显著更高"的反向；否则整套权重失去意义。

        v0.59 把词表单次命中改为零权重后，cred（多为 100–600 字短文）原先 +1.00 的
        差距几乎全部来自单词单次命中，实测回落到 -0.07；hc3 的正向由 +1.58 升到 +2.83。
        词表方向现在由 hc3 与「不同套话种类」簇承担，cred 只保留容差窗口（不足一个
        8 分条目的 2/30），并要求两套配对合并后仍为正。
        """
        cred = [(LINT.evaluate(h.read_text(encoding="utf-8-sig"))[2],
                 LINT.evaluate(a.read_text(encoding="utf-8-sig"))[2]) for h, a in cred_pairs()]
        hc3 = [(LINT.evaluate(h.read_text(encoding="utf-8-sig"))[2],
                LINT.evaluate(a.read_text(encoding="utf-8-sig"))[2]) for h, a in hc3_pairs()]
        cred_diff = mean([a - h for h, a in cred])
        hc3_diff = mean([a - h for h, a in hc3])
        pooled = (sum(a - h for h, a in cred) + sum(a - h for h, a in hc3)) / (len(cred) + len(hc3))
        self.assertGreater(hc3_diff, 0.0,
                           "hc3 上 AI 平均分应高于人类（v0.59 实测 +2.83），实得 %.2f" % hc3_diff)
        self.assertGreater(cred_diff, -0.5,
                           "cred 短文上不得出现明显反向（不足 2 个 8 分条目），实得 %.2f" % cred_diff)
        self.assertGreater(pooled, 0.0,
                           "两套配对合并后 AI 平均分必须更高，实得 %.2f" % pooled)


if __name__ == "__main__":
    unittest.main()
