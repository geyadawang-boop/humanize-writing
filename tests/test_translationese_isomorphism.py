# -*- coding: utf-8 -*-
"""v0.54 新增两条观察：[翻译腔] 与 [相邻同构] 只计数、恒零权重，且不误伤分行文本。"""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("obs_lint", ROOT / "scripts" / "ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)


def tag_of(message):
    return message.split("]", 1)[0] + "]"


TRANSLATIONESE_TEXT = (
    "值得注意的是，这类流程在某种程度上被认为是效率提升的关键。"
    "当团队需要在较短的时间内完成更多任务的时候，往往会先进行一轮评估，并且在此基础上作出调整。"
    "对于一线人员来说，这样的改变在某种程度上减少了重复劳动，但是如果缺少配套说明的话，"
    "也很容易带来新的困惑。因此，需要指出的是，流程本身并不能代替判断，"
    "并且需要在实践中不断校正，使得各项安排能够真正落到具体的人身上。"
)

PLAIN_TEXT = (
    "傍晚他把水壶放上灶台，等水开。窗外有人在搬东西，木箱刮过水泥地，声音很长。"
    "他数了三遍抽屉里的螺丝，还是少一颗。母亲打电话来问周末回不回去，他说回。"
    "水开了，他掀开壶盖，热气扑到眼镜上，什么也看不见，就那么站了一会儿。"
)

ISO_TEXT = (
    "交接在每天傍晚进行。"
    "团队先把原始记录整理成表格，再把表格交给复核人逐项核对。"
    "复核人先比对日期与签名，再把疑点写成清单交给值班主管。"
    "值班主管先确认清单的次序，再把结论抄进当日的交接记录。"
    "末尾那句不参与统计，只用来补足篇幅，顺便让段落看起来像真的。"
)

FIG_TEXT = (
    "交接在每天傍晚进行。"
    "团队先把原始记录整理成表格，像收拾一间乱屋子，再把表格交给复核人逐项核对。"
    "复核人先比对日期与签名，再把疑点写成清单交给值班主管。"
    "值班主管先确认清单的次序，再把结论抄进当日的交接记录。"
)

POEM_TEXT = "\n".join([
    "我把窗打开", "风进来", "帘子动了一下", "像谁在门外站着", "又走了",
    "桌上那杯水", "还是温的", "我没喝", "也没倒掉", "就那么放着",
    "天慢慢黑了", "楼下的猫叫了一声", "我抬头", "什么也没看见", "又低下头",
])


class TranslationeseTests(unittest.TestCase):
    def test_counts_markers_but_never_scores(self):
        # 用两倍长度越过短文本归一化门槛，这样分数应等于加权项之和，便于断言零权重
        issues, _, score = LINT.evaluate(TRANSLATIONESE_TEXT * 2)
        self.assertFalse([m for _, m in issues if tag_of(m) == "[短文本]"])
        lines = [(w, m) for w, m in issues if tag_of(m) == "[翻译腔]"]
        self.assertEqual(len(lines), 2, "命中时应输出计数行 + 证据行")
        self.assertTrue(all(w == 0 for w, _ in lines))
        self.assertRegex(lines[0][1], r"标记合计 \d+ 处（\d+\.\d+/千字）")
        self.assertIn("方向相反", lines[1][1])
        weighted = sum(w for w, _ in issues if w)
        self.assertEqual(score, weighted)

    def test_plain_narrative_reports_nothing(self):
        issues, _, _ = LINT.evaluate(PLAIN_TEXT)
        self.assertEqual([m for _, m in issues if tag_of(m) == "[翻译腔]"], [])

    def test_every_family_is_a_compiled_pattern(self):
        self.assertGreaterEqual(len(LINT.TRANSLATIONESE), 15)
        for name, rx in LINT.TRANSLATIONESE:
            self.assertTrue(name, "每个族都要有名字，便于报告定位")
            self.assertIsInstance(rx, type(LINT.SENT_SPLIT))


class IsomorphismTests(unittest.TestCase):
    def test_three_sentence_run_is_counted_with_positions(self):
        runs2, runs3, total = LINT.isomorphism_runs(ISO_TEXT)
        self.assertEqual(len(runs2), 2, "三句同款应产生两处两句组")
        self.assertEqual(len(runs3), 1)
        self.assertGreaterEqual(total, 4)
        self.assertTrue(all(p.startswith("第1段第") for p in runs2 + runs3))

    def test_observation_lines_are_zero_weight(self):
        issues, _, score = LINT.evaluate(ISO_TEXT)
        lines = [(w, m) for w, m in issues if tag_of(m) == "[相邻同构]"]
        self.assertGreaterEqual(len(lines), 2)
        self.assertTrue(all(w == 0 for w, _ in lines))
        self.assertIn("不计分", lines[-1][1])
        self.assertEqual(score, sum(w for w, _ in issues if w))

    def test_figurative_sentence_breaks_the_run(self):
        runs2, _, _ = LINT.isomorphism_runs(FIG_TEXT)
        self.assertEqual(len(runs2), 0, "带比喻的并列是修辞，不参与同构计数")

    def test_line_broken_text_is_skipped(self):
        self.assertEqual(LINT.isomorphism_runs(POEM_TEXT), ([], [], 0))

    def test_classical_prose_is_not_scored_by_these_tags(self):
        path = ROOT / "tests" / "corpus_classic" / "prose_zhuziqing_hetangyuese.md"
        issues, _, score = LINT.evaluate(path.read_text(encoding="utf-8-sig"))
        new_tags = [w for w, m in issues if tag_of(m) in ("[翻译腔]", "[相邻同构]")]
        self.assertTrue(all(w == 0 for w in new_tags))
        self.assertEqual(score, sum(w for w, _ in issues if w))
        runs2, _, total = LINT.isomorphism_runs(LINT.strip_markdown(path.read_text(encoding="utf-8-sig")))
        self.assertGreater(len(runs2), 0, "经典散文同样会触发，这正是它不计分的原因")
        self.assertGreater(total, 0)


if __name__ == "__main__":
    unittest.main()
