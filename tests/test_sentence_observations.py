"""Sentence statistics are observations, not a reward for punctuation changes.

Text probes are synthetic; passing them does not validate literary quality.
"""
import importlib.util
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sentence_observation_lint", ROOT / "scripts/ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)

PROBES = {
    "even_observation": {
        "baseline": "九月二十日，林舟把归还的图书逐本放回靠窗的书架。值班的阿姨翻开借阅登记，核对封面内侧写着的姓名。走廊里的学生排到门口，手上都拿着待盖章的卡片。隔壁教室传来拖动桌子的声音，窗台的玻璃杯轻轻晃动。林舟把空纸箱移到墙边，给等候的学生腾出一条通道。阿姨指着登记表上的空栏，请他补上昨天借书的时间。他从书包里取出收据，照着上面的日期填写借阅记录。下课铃响过以后，门口只剩两名正在翻找卡片的学生。",
        "punctuation_only": "九月二十日，林舟把归还的图书逐本放回靠窗的书架。值班的阿姨翻开借阅登记，核对封面内侧写着的姓名，走廊里的学生排到门口，手上都拿着待盖章的卡片，隔壁教室传来拖动桌子的声音，窗台的玻璃杯轻轻晃动，林舟把空纸箱移到墙边，给等候的学生腾出一条通道。阿姨指着登记表上的空栏，请他补上昨天借书的时间。他从书包里取出收据，照着上面的日期填写借阅记录。下课铃响过以后，门口只剩两名正在翻找卡片的学生。",
        "date_fragment": "九月二十日。林舟把归还的图书逐本放回靠窗的书架。值班的阿姨翻开借阅登记，核对封面内侧写着的姓名。走廊里的学生排到门口，手上都拿着待盖章的卡片。隔壁教室传来拖动桌子的声音，窗台的玻璃杯轻轻晃动。林舟把空纸箱移到墙边，给等候的学生腾出一条通道。阿姨指着登记表上的空栏，请他补上昨天借书的时间。他从书包里取出收据，照着上面的日期填写借阅记录。下课铃响过以后，门口只剩两名正在翻找卡片的学生。"
    },
    "functional_short_beats": {
        "baseline": "九月二十日。警铃响了。楼梯口有烟。值班员喊停。前面的人停住。后面还在挤。她抬起手。让孩子靠墙。别往里面走。门打不开。窗边有人喊。这边能出去。她回头数人。还差一个孩子。小林在桌下。书包卡住了。先把包放下。小林松了手。她拉住他的袖子。两人走到门口。楼下有人接应。担架放平了。孩子们靠在一起。值班员点完人数。又点了一遍。没有人落下。她放下手。手指还在抖。",
        "punctuation_only": "九月二十日。警铃响了。楼梯口有烟。值班员喊停。前面的人停住，后面还在挤，她抬起手，让孩子靠墙，别往里面走，门打不开，窗边有人喊，这边能出去，她回头数人，还差一个孩子，小林在桌下。书包卡住了。先把包放下。小林松了手。她拉住他的袖子。两人走到门口。楼下有人接应。担架放平了。孩子们靠在一起。值班员点完人数。又点了一遍。没有人落下。她放下手。手指还在抖。"
    },
    "four_sentence_gate": {
        "baseline": "九月二十日上午，林舟在靠窗的桌上找到借阅登记，封面还夹着阿姨留下的便条。便条上写着昨天没有归还的几本书，每本后面都列有班级和姓名，字迹没有涂改。他先照名单核对柜子里的图书，再把已经找到的书放到一边，登记表暂时没有修改。等值班阿姨回来以后，两人又检查了一遍日期，才把核对完的借阅记录录入电脑。",
        "punctuation_only": "九月二十日上午，林舟在靠窗的桌上找到借阅登记，封面还夹着阿姨留下的便条，便条上写着昨天没有归还的几本书，每本后面都列有班级和姓名，字迹没有涂改。他先照名单核对柜子里的图书，再把已经找到的书放到一边，登记表暂时没有修改。等值班阿姨回来以后，两人又检查了一遍日期，才把核对完的借阅记录录入电脑。"
    },
    "real_corrections_and_other_pattern_control": {
        "baseline": "九月二十日核对通知时，她发现集合的时间不是周五，而是周四。清单要求带来的不是复印件，而是原件，需要在现场核对后归还。工作人员不仅核对日期，还要核对姓名，避免把两个班的登记混在一起。当天不仅检查借阅记录，还要保存凭证，已经归还的书要单独登记。交接时不仅整理表格，还要说明空栏，接班人员才能找到没有确认的项目。她把两个日期圈出来，等同学看过原件以后，再抄到新的通知纸上。",
        "punctuation_only": "九月二十日核对通知时，她发现集合的时间不是周五，而是周四。清单要求带来的不是复印件，而是原件，需要在现场核对后归还。工作人员不仅核对日期，还要核对姓名，避免把两个班的登记混在一起，当天不仅检查借阅记录，还要保存凭证，已经归还的书要单独登记，交接时不仅整理表格，还要说明空栏，接班人员才能找到没有确认的项目。她把两个日期圈出来，等同学看过原件以后，再抄到新的通知纸上。"
    }
}


class SentenceObservationTests(unittest.TestCase):
    def observation(self, text, genre="fiction"):
        issues, status, score = LINT.evaluate(text, genre)
        self.assertEqual(status, "ok")
        return [(w, m) for w, m in issues if m.startswith("[句长]")], issues, score

    def assert_neutral(self, text):
        observations, _, _ = self.observation(text)
        self.assertEqual(len(observations), 1)
        weight, message = observations[0]
        self.assertEqual(weight, 0)
        self.assertIn("仅观察", message)
        self.assertNotIn("✓", message)
        return message

    def test_uniform_long_sentences_have_no_penalty(self):
        self.assert_neutral(PROBES["even_observation"]["baseline"])

    def test_uniform_short_sentences_have_no_penalty(self):
        self.assert_neutral("他先停下。他才回头。她也停下。她又回头。" * 8)

    def test_midrange_variance_is_also_neutral(self):
        text = PROBES["even_observation"]["baseline"].replace("九月二十日，", "九月二十日。", 1)
        lengths = [LINT.chinese_len(s) for s in LINT.sentences(LINT.strip_markdown(text))]
        self.assertGreaterEqual(statistics.pstdev(lengths), 4)
        self.assertLess(statistics.pstdev(lengths), 7)
        self.assert_neutral(text)

    def test_high_variance_is_not_a_quality_pass(self):
        text = PROBES["even_observation"]["punctuation_only"]
        lengths = [LINT.chinese_len(s) for s in LINT.sentences(LINT.strip_markdown(text))]
        self.assertGreaterEqual(statistics.pstdev(lengths), 7)
        self.assert_neutral(text)

    def test_punctuation_only_changes_cannot_earn_variance_discount(self):
        for name, variants in PROBES.items():
            with self.subTest(case=name):
                before, after = variants["baseline"], variants["punctuation_only"]
                han = lambda text: "".join(c for c in text if "\u4e00" <= c <= "\u9fff")
                self.assertEqual(han(before), han(after))
                _, old_issues, old_score = self.observation(before)
                _, new_issues, new_score = self.observation(after)
                self.assertEqual([(w, m) for w, m in old_issues if w],
                                 [(w, m) for w, m in new_issues if w])
                self.assertEqual(old_score, new_score)

    def test_four_to_three_sentence_gate_does_not_change_score(self):
        variants = PROBES["four_sentence_gate"]
        before, _, old_score = self.observation(variants["baseline"])
        after, _, new_score = self.observation(variants["punctuation_only"])
        self.assertEqual(len(LINT.sentences(variants["baseline"])), 4)
        self.assertEqual(len(LINT.sentences(variants["punctuation_only"])), 3)
        self.assertEqual(len(before), 1)
        self.assertEqual(after, [])
        self.assertEqual(old_score, new_score)

    def test_genre_gates_keep_their_existing_scope(self):
        text = PROBES["even_observation"]["baseline"]
        for genre in LINT.GENRES:
            with self.subTest(genre=genre):
                observations, _, _ = self.observation(text, genre)
                if genre in ("tech", "academic", "official"):
                    self.assertEqual(observations, [])
                else:
                    self.assertEqual(len(observations), 1)
                    self.assertEqual(observations[0][0], 0)

    def test_other_weighted_signal_and_normalization_remain(self):
        for text in PROBES["real_corrections_and_other_pattern_control"].values():
            with self.subTest(text=text[:30]):
                _, issues, score = self.observation(text)
                weighted = [(w, m) for w, m in issues if w]
                self.assertEqual(len(weighted), 1)
                self.assertEqual(weighted[0][0], 5)
                self.assertIn("不仅…还/更…", weighted[0][1])
                self.assertEqual(score, round(5 * 300 / 165))
                self.assertTrue(any(w == 0 and m.startswith("[对照句式]") for w, m in issues))


if __name__ == "__main__":
    unittest.main()
