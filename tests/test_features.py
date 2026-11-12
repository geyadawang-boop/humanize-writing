# -*- coding: utf-8 -*-
"""特征层：31 个特征的定义、数值稳定性与证据绑定。

这层是整个可解释评分器的基础。测试目标不是“分数对不对”，而是：
1. 特征清单与向量顺序一致，不会错位；
2. 每条特征都有标签、方向、证据与说明，不能出现无出处的特征；
3. 明显不同的文本在对应特征上确实分开；
4. 空文本、极短文本不崩，窗口切分有上界。
"""
import importlib.util
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("hw_features", ROOT / "scripts" / "features.py")
F = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(F)

LONG = "他推开门，屋里没有人。" * 3 + "桌上那盏灯还亮着，灯芯烧得只剩一小截，火苗贴着玻璃壁抖。" * 2
SHORT = "下雨了。走吧。"
PARA = ("第一段写清楚一件事的来龙去脉，句子有长有短，读起来不费劲。"
        "第二段接着往下说，中间插一句短的。"
        "第三段收住，不再重复前面说过的话。")


class FeatureSpecTest(unittest.TestCase):
    def test_count_is_31(self):
        self.assertEqual(len(F.FEATURE_SPECS), 31)

    def test_every_spec_is_complete(self):
        for name, spec in F.FEATURE_SPECS.items():
            self.assertIsInstance(name, str)
            self.assertTrue(spec.get("label"), name)
            self.assertIn(spec.get("direction"), (-1, 0, 1), name)
            self.assertTrue(spec.get("note"), name)
            ev = spec.get("evidence")
            self.assertIsInstance(ev, list, name)
            self.assertTrue(ev, "%s 没有证据编号" % name)

    def test_vector_order_matches_specs(self):
        vec = F.vector(PARA)
        self.assertEqual(len(vec), len(F.FEATURE_SPECS))
        keys = list(F.FEATURE_SPECS.keys())
        self.assertEqual(keys, list(F.extract(PARA).keys()))

    def test_all_values_finite(self):
        for text in (PARA, LONG, SHORT, ""):
            for name, v in F.extract(text).items():
                self.assertFalse(math.isnan(v), name)
                self.assertFalse(math.isinf(v), name)


class FeatureBehaviourTest(unittest.TestCase):
    def test_short_sentences_lower_mean(self):
        self.assertLess(F.extract(SHORT)["sent_len_mean"],
                        F.extract(LONG)["sent_len_mean"])

    def test_multi_paragraph_text_has_paragraph_signal(self):
        two = F.extract(PARA + "\n\n" + "短的一段。")
        self.assertGreater(two["para_len_mean"], 0)
        self.assertGreater(two["para_len_sd"], 0)

    def test_empty_text_does_not_crash(self):
        out = F.extract("")
        self.assertEqual(len(out), 31)
        self.assertEqual(out["sent_len_mean"], 0.0)

    def test_vector_is_deterministic(self):
        self.assertEqual(F.vector(PARA), F.vector(PARA))


class WindowTest(unittest.TestCase):
    def test_short_text_single_window(self):
        wins = F.windows(PARA)
        self.assertEqual(len(wins), 1)
        self.assertIn("第一段", wins[0][1])

    def test_long_text_window_cap(self):
        wins = F.windows(PARA * 40, size=320, max_windows=8)
        self.assertLessEqual(len(wins), 8)
        self.assertGreater(len(wins), 1)
        for _, seg in wins:
            self.assertGreater(len(seg), 0)


if __name__ == "__main__":
    unittest.main()
