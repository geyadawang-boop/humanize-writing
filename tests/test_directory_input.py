# -*- coding: utf-8 -*-
"""目录输入：递归收纯文本、逐文件报告 + 汇总、退出码语义，且单文件行为不变。"""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dir_lint", ROOT / "scripts" / "ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)

HUMAN_TEXT = (ROOT / "tests" / "samples" / "human_like.md").read_text(encoding="utf-8-sig")
FAIL_TEXT = (ROOT / "tests" / "samples" / "ai_heavy.md").read_text(encoding="utf-8-sig") * 3


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = LINT.main(argv)
    return code, out.getvalue(), err.getvalue()


class DirectoryInputTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        (self.base / "a.md").write_text(FAIL_TEXT, encoding="utf-8")
        sub = self.base / "sub"
        sub.mkdir()
        (sub / "b.md").write_text(HUMAN_TEXT, encoding="utf-8")
        (sub / "c.txt").write_text(HUMAN_TEXT, encoding="utf-8")
        (self.base / "d.png").write_bytes(b"\x89PNG\r\n")
        hidden = self.base / ".hidden"
        hidden.mkdir()
        (hidden / "e.md").write_text(FAIL_TEXT, encoding="utf-8")
        (self.base / "__pycache__").mkdir()
        (self.base / "__pycache__" / "f.md").write_text(FAIL_TEXT, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_recurses_text_files_and_summarises(self):
        code, out, _ = run([str(self.base)])
        self.assertEqual(code, 1, "目录内有超阈值文件时应以 1 退出")
        self.assertIn("a.md", out)
        self.assertIn("b.md", out)
        self.assertIn("c.txt", out)
        self.assertNotIn("d.png", out)
        self.assertNotIn("e.md", out, "隐藏目录不应被采样")
        self.assertNotIn("f.md", out, "__pycache__ 不应被采样")
        self.assertIn("目录汇总：3 个文件", out)
        self.assertIn("超阈值 1", out)

    def test_json_mode_lists_each_path(self):
        code, out, _ = run([str(self.base), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(out)
        self.assertEqual(len(data), 3)
        self.assertTrue(all("path" in item for item in data))
        self.assertEqual([Path(item["path"]).name for item in data], ["a.md", "b.md", "c.txt"])

    def test_empty_directory_is_an_input_error(self):
        empty = self.base / "empty"
        empty.mkdir()
        code, out, err = run([str(empty)])
        self.assertEqual(code, 2)
        self.assertIn("没有可读", err)
        self.assertEqual(out.strip(), "")

    def test_single_file_output_stays_unchanged(self):
        code, out, _ = run([str(self.base / "a.md")])
        self.assertEqual(code, 1)
        self.assertNotIn("目录汇总", out)
        self.assertIn("=== ", out)

    def test_directory_with_only_clean_files_exits_zero(self):
        clean = self.base / "clean"
        clean.mkdir()
        (clean / "ok.md").write_text(HUMAN_TEXT, encoding="utf-8")
        code, out, _ = run([str(clean)])
        self.assertEqual(code, 0)
        self.assertIn("未超阈值 1", out)


if __name__ == "__main__":
    unittest.main()
