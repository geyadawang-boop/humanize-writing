"""v0.52 的三项观察档：X 级否决计数、字符指纹、语义候选。

三者都是零权重：不得改变分数、status 或退出码，也不得提供“应该改”的依据。
X 级的证据来自外部同题配对复测，本项目语料未复测；测试只锁定“不计分、明确不改”
这一行为契约，不认证任何外部结论。
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("v052_lint", ROOT / "scripts" / "ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)

BODY = ("九月二十日工作人员到仓库核对借用登记，确认封面上的姓名和归还日期。"
        "旧表格放在靠窗的抽屉里，新表格由值班人员保管，登记内容需要与原件核对后再录入。"
        "负责人将在周四下午通知借用人到场。") * 2

CANDIDATES = (
    BODY + "\n\n"
    "因此，工作人员重新整理了抽屉里的表格。\n\n"
    "所以，登记顺序也做了调整。\n\n"
    "与此同时，值班人员开始核对新的名单。\n\n"
    "核心问题是：哪一份表格才算原件？\n\n"
    "她提升了核对速度，也优化了登记流程。\n\n"
    "今天天气很好。明天天气很好。后天天气很好。\n"
)


def messages(issues, tag):
    return [(w, m) for w, m in issues if m.startswith(tag)]


class VetoTests(unittest.TestCase):
    def test_veto_counts_are_listed_but_never_weighted(self):
        text = "## 一、背景\n\n" + BODY + "\n\n这意味着旧表不再使用。\n"
        issues, status, _ = LINT.evaluate(text)
        self.assertEqual(status, "ok")
        veto = messages(issues, "[X 级]")
        self.assertTrue(veto)
        self.assertTrue(all(w == 0 for w, _ in veto), "X 级只计数，不得携带权重")
        joined = " ".join(m for _, m in veto)
        self.assertIn("序数词小标题", joined)
        self.assertIn("这意味着", joined)
        self.assertIn("不改", joined)
        self.assertIn("不计分", joined)

    def test_plain_prose_has_no_veto_block(self):
        issues, _, _ = LINT.evaluate(BODY)
        self.assertEqual(messages(issues, "[X 级]"), [])

    def test_veto_never_changes_score(self):
        plain = LINT.evaluate(BODY)
        with_veto = LINT.evaluate("## 一、背景\n\n" + BODY + "\n\n这意味着旧表不再使用。\n")
        self.assertEqual(plain[2], with_veto[2], "X 级计数不得参与计分")


class FingerprintTests(unittest.TestCase):
    TEXT = BODY + "他说：“好。”——然后走了；桌上放着书、笔、纸。"

    def test_off_by_default(self):
        issues, _, _ = LINT.evaluate(BODY)
        self.assertEqual(messages(issues, "[X 指纹]"), [])

    def test_reports_raw_counts_without_targets(self):
        issues, status, _ = LINT.evaluate(self.TEXT, fingerprint=True)
        self.assertEqual(status, "ok")
        lines = messages(issues, "[X 指纹]")
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(w == 0 for w, _ in lines))
        data, boundary = lines[0][1], lines[1][1]
        self.assertIn("破折号 1 处", data)
        self.assertIn("引号 1 对", data)
        self.assertIn("分号 1 处", data)
        self.assertIn("顿号 2 处", data)
        self.assertIn("句长中位", data)
        self.assertIn("不能反推本篇来源", boundary)
        self.assertIn("不计分", boundary)

    def test_fingerprint_does_not_change_score_or_status(self):
        left = LINT.evaluate(self.TEXT)
        right = LINT.evaluate(self.TEXT, fingerprint=True)
        self.assertEqual((left[1], left[2]), (right[1], right[2]))

    def test_short_sample_reports_no_ratio(self):
        issues, status, _ = LINT.evaluate("他停下。她回头。", fingerprint=True)
        self.assertEqual(status, "short")
        lines = messages(issues, "[X 指纹]")
        self.assertEqual(len(lines), 1)
        self.assertIn("不足", lines[0][1])
        self.assertIn("不报数据", lines[0][1])
        self.assertEqual(lines[0][0], 0)


class CandidateTests(unittest.TestCase):
    def test_off_by_default(self):
        issues, _, _ = LINT.evaluate(CANDIDATES)
        self.assertEqual(messages(issues, "[语义候选]"), [])

    def test_four_families_are_located_with_zero_weight(self):
        issues, status, _ = LINT.evaluate(CANDIDATES, candidates=True)
        self.assertEqual(status, "ok")
        lines = messages(issues, "[语义候选]")
        self.assertTrue(all(w == 0 for w, _ in lines), "候选不得携带权重")
        joined = " ".join(m for _, m in lines)
        self.assertIn("段间衔接接口", joined)
        self.assertIn("结论提示冒号", joined)
        self.assertIn("同义重命名", joined)
        self.assertIn("等长三连", joined)
        self.assertIn("不构成改写理由", joined)

    def test_long_runs_are_sampled_not_dumped(self):
        text = BODY + "\n\n" + "\n\n".join("结论：这是第%d条记录。" % i for i in range(1, 11))
        issues, _, _ = LINT.evaluate(text, candidates=True)
        line = next(m for _, m in issues if m.startswith("[语义候选] 结论提示冒号"))
        self.assertIn("结论提示冒号 10 处", line)
        self.assertEqual(line.count("」「"), 2, "抽样最多展示三条")

    def test_candidates_do_not_change_score(self):
        left = LINT.evaluate(CANDIDATES)
        right = LINT.evaluate(CANDIDATES, candidates=True)
        self.assertEqual((left[1], left[2]), (right[1], right[2]))

    def test_three_equal_sentences_are_only_a_position_hint(self):
        text = BODY + "今天天气很好。明天天气很好。后天天气很好。"
        issues, _, _ = LINT.evaluate(text, candidates=True)
        line = next(m for _, m in issues if m.startswith("[语义候选] 等长三连"))
        self.assertIn("等长不等于骨架同构", line)
        self.assertIn("不加罚", line)


class CliObservationFlags(unittest.TestCase):
    def run_cli(self, args):
        return subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / "ai_smell_lint.py"), *args],
                              input=CANDIDATES, capture_output=True, text=True,
                              encoding="utf-8", timeout=15)

    def test_help_mentions_both_flags(self):
        result = self.run_cli(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("--fingerprint", result.stdout)
        self.assertIn("--candidates", result.stdout)

    def test_all_flag_turns_on_both_observation_layers(self):
        result = self.run_cli(["--all", "-"])
        self.assertIn("[X 指纹]", result.stdout)
        self.assertIn("[语义候选]", result.stdout)

    def test_flags_do_not_change_exit_code_and_stay_json(self):
        plain = self.run_cli(["--json", "-"])
        flagged = self.run_cli(["--json", "--fingerprint", "--candidates", "-"])
        self.assertEqual(plain.returncode, flagged.returncode)
        data = json.loads(flagged.stdout)[0]
        self.assertEqual(data["score_kind"], "static_style_heuristic")
        self.assertIs(data["is_ai_probability"], False)
        self.assertEqual(data["score"], json.loads(plain.stdout)[0]["score"])
        tags = " ".join(item["message"] for item in data["issues"])
        self.assertIn("[X 指纹]", tags)
        self.assertIn("[语义候选]", tags)
        self.assertTrue(all(item["weight"] == 0 for item in data["issues"]
                            if item["message"].startswith(("[X 级]", "[X 指纹]", "[语义候选]"))))


if __name__ == "__main__":
    unittest.main()
