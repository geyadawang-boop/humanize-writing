# -*- coding: utf-8 -*-
"""改前改后对比报告：指标表、分级清单、标红对照、语义判读合并与错误码。"""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cmp_report", ROOT / "scripts" / "compare_report.py")
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)

AI_TEXT = (ROOT / "tests" / "samples" / "ai_heavy.md").read_text(encoding="utf-8-sig")
HUMAN_TEXT = (ROOT / "tests" / "samples" / "human_like.md").read_text(encoding="utf-8-sig")


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = REPORT.main(argv)
    return code, out.getvalue(), err.getvalue()


class CompareReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.before = self.base / "before.md"
        self.after = self.base / "after.md"
        self.before.write_text(AI_TEXT, encoding="utf-8")
        self.after.write_text(HUMAN_TEXT, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, *extra, fmt="md"):
        out = self.base / ("report." + fmt)
        code, stdout, stderr = run([str(self.before), str(self.after),
                                    "--format", fmt, "--out", str(out)] + list(extra))
        return code, out, stdout, stderr

    def test_markdown_report_has_metrics_and_grades(self):
        code, out, stdout, _ = self.build()
        self.assertEqual(code, 0)
        self.assertIn("报告 →", stdout)
        text = out.read_text(encoding="utf-8")
        self.assertIn("## 一、指标前后对比", text)
        self.assertIn("静态写作线索分", text)
        self.assertIn("| 24 | 0 |", text)
        self.assertIn("## 二、改前命中分级清单", text)
        self.assertIn("### 加权项（需逐条核读）", text)
        self.assertIn("改后：已消失", text)
        self.assertIn("## 三、逐段对照", text)
        self.assertIn("~~现代社会中", text)
        self.assertIn("## 四、语义候选与人工判读", text)

    def test_html_report_marks_deletions_and_insertions(self):
        code, out, _, _ = self.build(fmt="html")
        self.assertEqual(code, 0)
        text = out.read_text(encoding="utf-8")
        self.assertIn("<del>", text)
        self.assertIn("<ins>", text)
        self.assertIn("静态写作线索分", text)
        self.assertNotIn("<script>", text)

    def test_unrelated_paragraphs_are_not_inline_mixed(self):
        """相似度过低的段落不许硬做字符对照，必须拆成删一段 + 增一段。"""
        blocks = REPORT.diff_blocks("甲" * 200 + "，乙。", "丙" * 200 + "，丁。")
        self.assertEqual([k for k, _ in blocks], ["del", "add"])

    def test_similar_paragraph_is_inline_diffed(self):
        blocks = REPORT.diff_blocks("他走进屋子，把外套挂在门边。",
                                    "他走进屋子，把外套搭在门边。")
        self.assertEqual([k for k, _ in blocks], ["mod"])
        self.assertIn("~~", blocks[0][1][0] + "~~")

    def test_semantic_json_is_merged(self):
        sem = self.base / "sem.json"
        sem.write_text(json.dumps({"judgments": [
            {"candidate": "同义重命名", "verdict": "确认", "note": "同一实体换了说法"}
        ]}, ensure_ascii=False), encoding="utf-8")
        code, out, _, _ = self.build("--semantic", str(sem))
        self.assertEqual(code, 0)
        text = out.read_text(encoding="utf-8")
        self.assertIn("| 候选 | 判读 | 说明 |", text)
        self.assertIn("同义重命名 | 确认", text)

    def test_bad_inputs_return_two(self):
        code, _, err = run([str(self.before), str(self.base / "missing.md")])
        self.assertEqual(code, 2)
        self.assertIn("无法读取", err)
        bad = self.base / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        code, _, err = run([str(self.before), str(self.after), "--semantic", str(bad)])
        self.assertEqual(code, 2)
        self.assertIn("语义判读", err)

    def test_unknown_genre_returns_two(self):
        code, _, err = run([str(self.before), str(self.after), "--genre", "poetry"])
        self.assertEqual(code, 2)
        self.assertIn("未知 --genre", err)


if __name__ == "__main__":
    unittest.main()
