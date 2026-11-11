"""Paragraph layout and regex anchors must not reward cosmetic changes.

Synthetic probes test tool behavior, not literary quality or AI authorship.
"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("paragraph_anchor_lint", ROOT / "scripts/ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)

PARAS = [
    "她把落满灰的布袋放到桌边，解开已经打结的绳子，先从外层取出裹着棉布的杯子。",
    "杯口缺了细小的瓷片，手指碰过去有些扎，她便转着杯身寻找对应的裂纹，没有继续用力。",
    "柜门被地毯挡住，她用脚把翘起的边角压平，再扶着门板缓缓拉开，露出放在底层的木盒。",
    "盒盖上的绒布已经褪色，贴近铰链的地方还留着深色折痕，她扶住盖子，把杯子平放进去。",
    "屋外传来推车经过的声音，轮子碾过门槛时轻轻磕响，她侧耳听着，手上的动作停了下来。",
    "等声音走远，她重新拢好垫布，把绳子收到盒底，合盖时留出缝隙，避免压到裂开的杯口。"
]

CONTEXT = "".join(PARAS)
BALANCED = "\n\n".join(PARAS)
UNBALANCED = "\n\n".join([PARAS[0], PARAS[1], "".join(PARAS[2:])])


class ParagraphAnchorObservationTests(unittest.TestCase):
    def result(self, text, genre="fiction"):
        issues, status, score = LINT.evaluate(text, genre)
        self.assertEqual(status, "ok")
        return issues, score

    def neutral(self, text, tag, genre="fiction"):
        issues, _ = self.result(text, genre)
        hits = [(w, m) for w, m in issues if m.startswith(tag)]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][0], 0)
        self.assertIn("仅观察", hits[0][1])
        self.assertNotIn("✓", hits[0][1])
        return hits[0][1]

    def test_balanced_paragraphs_have_no_penalty(self):
        lens = [LINT.chinese_len(p) for p in LINT.paragraphs(BALANCED)]
        self.assertLess(max(lens), 2 * min(lens))
        self.neutral(BALANCED, "[段落]")

    def test_uneven_paragraphs_do_not_receive_quality_approval(self):
        lens = [LINT.chinese_len(p) for p in LINT.paragraphs(UNBALANCED)]
        self.assertGreaterEqual(max(lens), 2 * min(lens))
        self.neutral(UNBALANCED, "[段落]")

    def test_rebreaking_same_characters_and_punctuation_has_no_layout_discount(self):
        self.assertEqual(BALANCED.replace("\n", ""), UNBALANCED.replace("\n", ""))
        a, sa = self.result(BALANCED)
        b, sb = self.result(UNBALANCED)
        self.assertEqual([(w, m) for w, m in a if w], [(w, m) for w, m in b if w])
        self.assertEqual(sa, sb)

    def test_two_paragraph_gate_and_short_paragraph_filter_preserved(self):
        two = "\n\n".join(["".join(PARAS[:3]), "".join(PARAS[3:])])
        with_short = two + "\n\n她停住。"
        self.assertEqual(len(LINT.paragraphs(with_short)), 2)
        issues, score = self.result(two)
        self.assertTrue(any(m.startswith("[段落]") and "<3" in m for _, m in issues))
        self.assertEqual(score, self.result(BALANCED)[1])

    def test_genre_gates_preserved(self):
        for genre in LINT.GENRES:
            with self.subTest(genre=genre):
                issues, _ = self.result(BALANCED, genre)
                if genre in ("tech", "academic", "official"):
                    self.assertTrue(any(m.startswith("[段落]") and "跳过" in m for _, m in issues))
                else:
                    self.neutral(BALANCED, "[段落]", genre)
                self.neutral(BALANCED, "[锚点]", genre)

    def test_other_paragraph_start_signal_remains(self):
        text = "\n\n".join("她整理好杯子，" + p for p in PARAS)
        issues, _ = self.result(text, "general")
        self.assertTrue(any(w == 5 and m.startswith("[段落开头]") for w, m in issues))
        self.assertFalse(any(w and m.startswith("[段落开头]") for w, m in self.result(text, "fiction")[0]))

    def test_concrete_actions_with_zero_regex_anchors_are_not_penalized(self):
        self.assertEqual(LINT.ANCHOR_RE.findall(CONTEXT), [])
        self.neutral(CONTEXT, "[锚点]")

    def test_unrelated_numbers_and_places_cannot_earn_anchor_discount(self):
        padded = CONTEXT + "北京，2026，上海，42。"
        self.assertGreater(len(LINT.ANCHOR_RE.findall(padded)), 0)
        self.neutral(padded, "[锚点]")
        self.assertEqual(self.result(CONTEXT)[1], self.result(padded)[1])

    def test_equivalent_quantity_notation_has_no_anchor_score_advantage(self):
        chinese = "她取出两把剪刀。" + CONTEXT
        arabic = "她取出2把剪刀。" + CONTEXT
        self.assertEqual(LINT.ANCHOR_RE.findall(chinese), [])
        self.assertTrue(LINT.ANCHOR_RE.findall(arabic))
        self.neutral(chinese, "[锚点]")
        self.neutral(arabic, "[锚点]")
        self.assertEqual(self.result(chinese)[1], self.result(arabic)[1])

    def test_anchor_observation_does_not_disable_independent_word_signal(self):
        # v0.59：单次命中只定位；同一词 ≥2 次才计分（min(12, 4×2)=8）。
        text = CONTEXT + "这部分确实不可或缺。那部分同样不可或缺。"
        issues, score = self.result(text)
        weighted = [(w, m) for w, m in issues if w]
        self.assertEqual(len(weighted), 1)
        self.assertEqual(weighted[0][0], 8)
        self.assertIn("不可或缺", weighted[0][1])
        units = LINT.chinese_len(LINT.strip_markdown(text)) + LINT.ascii_word_len(LINT.strip_markdown(text))
        self.assertEqual(score, round(8 * 300 / units) if units < 300 else 8)

    def test_short_input_is_still_unassessed(self):
        issues, status, _ = LINT.evaluate("北京，2把剪刀。")
        self.assertEqual(status, "short")
        self.assertFalse(any(m.startswith("[锚点]") for _, m in issues))


if __name__ == "__main__":
    unittest.main()
