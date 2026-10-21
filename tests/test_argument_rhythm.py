"""Regression checks for v0.41 observations; semantic quality needs text review."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rhythm_lint", ROOT / "scripts/ai_smell_lint.py")
LINT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(LINT)
CONTEXT = ("九月二十日工作人员到仓库核对借用登记，确认封面上的姓名和归还日期。"
           "旧表格放在靠窗的抽屉里，新表格由值班人员保管，登记内容需要与原件核对后再录入。"
           "当天尚未核对的物件留在架上，负责人将在周四下午通知借用人到场。") * 2


class ArgumentRhythmTests(unittest.TestCase):
    def tagged(self, text, tag, genre="general"):
        issues, status, _ = LINT.evaluate(text, genre)
        self.assertEqual(status, "ok")
        return [(w, m) for w, m in issues if m.startswith(tag)]

    def test_no_short_sentence_quota_penalty(self):
        observations = self.tagged(CONTEXT, "[短句]")
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0][0], 0)

    def test_many_short_sentences_are_not_a_quality_pass(self):
        text = "他走进屋。她抬起头。雨还在下。门没有关。灯还亮着。" * 8
        observations = self.tagged(text, "[短句]")
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0][0], 0)
        self.assertNotIn("✓", observations[0][1])

    def test_factual_corrections_are_located_without_count_penalty(self):
        text = "通知写的不是周五，而是周四。要交的不是复印件，而是原件。" + CONTEXT
        observations = self.tagged(text, "[对照句式]")
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0][0], 0)
        self.assertFalse(any(w and "不是…而是…" in m for w, m in LINT.evaluate(text)[0]))

    def test_character_claim_is_not_automatically_a_semantic_verdict(self):
        text = "她说：你要的不是解释，而是认错。他答：我要的不是面子，而是实话。" + CONTEXT
        observations = self.tagged(text, "[对照句式]", "fiction")
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0][0], 0)

    def test_other_repeated_patterns_still_produce_existing_signal(self):
        text = "不仅核对日期，还要核对姓名。不仅检查原件，还要记录编号。不仅整理表格，还要保存凭证。" + CONTEXT
        issues, status, _ = LINT.evaluate(text)
        self.assertEqual(status, "ok")
        self.assertTrue(any(w == 5 and "不仅…还/更…" in m for w, m in issues))

    def test_genre_gates_remain_effective(self):
        for genre in ("tech", "academic", "official", "law"):
            with self.subTest(genre=genre):
                self.assertEqual(self.tagged(CONTEXT, "[短句]", genre), [])

    def test_insufficient_text_still_not_evaluated(self):
        self.assertEqual(LINT.evaluate("他停下。她回头。")[1], "short")

    def test_cli_version_is_explicit_and_source_is_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "sample.md"
            original = CONTEXT.encode("utf-8")
            source.write_bytes(original)
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/ai_smell_lint.py"),
                                     "--json", str(source)], capture_output=True, text=True,
                                    encoding="utf-8", timeout=15)
            self.assertIn(result.returncode, (0, 1))
            data = json.loads(result.stdout)[0]
            self.assertEqual(data["ruleset_version"], "0.43")
            self.assertEqual(data["score_kind"], "static_style_heuristic")
            self.assertIs(data["is_ai_probability"], False)
            self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
