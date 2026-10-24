"""The v0.49 line-break notice is a measurement statement, not a score or exemption.

It exists because a poem whose lines carry no sentence-final punctuation collapses into
one "sentence", so sentence- and paragraph-level checks silently lose their object.
Synthetic probes test tool behavior; they do not certify literary quality or authorship.
"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("line_break_lint", ROOT / "scripts/ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)

# 24 short lines, commas only inside lines, one final period: sentence splitting glues them.
POEM_LINES = [
    "她把落满灰的布袋放到桌边",
    "解开已经打结的绳子",
    "先从外层取出裹着棉布的杯子",
    "杯口缺了细小的瓷片",
    "手指碰过去有些扎",
    "她便转着杯身寻找对应的裂纹",
    "没有继续用力",
    "柜门被地毯挡住",
    "她用脚把翘起的边角压平",
    "再扶着门板缓缓拉开",
    "露出放在底层的木盒",
    "盒盖上的绒布已经褪色",
    "贴近铰链的地方还留着深色折痕",
    "她扶住盖子",
    "把杯子平放进去",
    "屋外传来推车经过的声音",
    "轮子碾过门槛时轻轻磕响",
    "她侧耳听着",
    "手上的动作停了下来",
    "等声音走远",
    "她重新拢好垫布",
    "把绳子收到盒底",
    "合盖时留出缝隙",
    "避免压到裂开的杯口。",
]
POEM = "\n".join(POEM_LINES)
PROSE = " ".join(POEM_LINES)


class LineBreakObservationTests(unittest.TestCase):
    def notice(self, text, genre="general"):
        issues, status, score = LINT.evaluate(text, genre)
        self.assertEqual(status, "ok")
        return [(w, m) for w, m in issues if m.startswith("[分行]")], score, issues

    def test_line_broken_text_reports_collapsed_sentence_count(self):
        hits, score, issues = self.notice(POEM)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][0], 0, "line-break notice must never carry weight")
        overview = next(m for w, m in issues if m.startswith("[概览]"))
        self.assertIn("句", overview)

    def test_same_words_as_prose_gets_no_notice(self):
        hits, score, _ = self.notice(PROSE)
        self.assertEqual(hits, [], "notice must follow line structure, not content")

    def test_notice_does_not_change_score_between_layouts(self):
        poem_hits, poem_score, _ = self.notice(POEM)
        prose_hits, prose_score, _ = self.notice(PROSE)
        self.assertTrue(poem_hits and not prose_hits)
        self.assertEqual(
            [(w, m) for w, m in self.notice(POEM)[2] if w],
            [(w, m) for w, m in self.notice(PROSE)[2] if w],
        )
        self.assertEqual(poem_score, prose_score)

    def test_notice_wording_denies_quality_and_identity_use(self):
        hits, _, _ = self.notice(POEM)
        message = hits[0][1]
        for phrase in ("不计分", "不评价", "不因分行整齐或参差加减分"):
            self.assertIn(phrase, message)

    def test_few_lines_do_not_trigger(self):
        short = "\n".join(POEM_LINES[:6]) + "她停了一下。"
        issues, status, _ = LINT.evaluate(short)
        self.assertFalse(any(m.startswith("[分行]") for _, m in issues), "guard: >=8 lines required")

    def test_notice_survives_genre_gates(self):
        for genre in LINT.GENRES:
            with self.subTest(genre=genre):
                hits, _, _ = self.notice(POEM, genre)
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits[0][0], 0)


class ShortPoemStructureTests(unittest.TestCase):
    """Below MIN_CHARS no score is possible, but line positions are still reportable."""

    JUEJU = "床前明月光，\n疑是地上霜。\n举头望明月，\n低头思故乡。\n"
    REFRAIN = "亚洲铜，亚洲铜\n祖父死在这里，父亲死在这里，我也将死在这里\n你是弱者的根，村中的石头\n亚洲铜，亚洲铜\n风从海上来，吹动我的村庄\n"
    PROSE = ("他合上本子，笔尖在纸面上停了很久，窗外的雨停了又下，下到檐口的水洼漫过上次留下的泥线。\n"
             "他没有再数下去，只是把窗户推开一点，让冷气进来，把桌上那张没有写完的纸压住边角，怕风把墨迹吹糊。\n")

    def assess(self, text):
        return LINT.evaluate(text, "general", "zh")

    def test_short_poem_still_unassessed_but_reports_positions(self):
        issues, status, score = self.assess(self.JUEJU)
        self.assertEqual(status, "short", "短诗的密度分数仍不可用，状态不能偷偷变成可判定")
        self.assertEqual(score, 0)
        notes = [(w, m) for w, m in issues if m.startswith("[分行结构]")]
        self.assertGreaterEqual(len(notes), 3, "四句绝句应给出行数与行长等位置统计")
        self.assertTrue(all(w == 0 for w, _ in notes), "位置统计不得带权重")
        joined = " ".join(m for _, m in notes)
        self.assertIn("不构成诗意或质量判断", joined)
        self.assertIn("无法判定", joined)
        self.assertIn("5、5、5、5", joined, "行长序列要如实报出，供人判断均匀是否有意")

    def test_refrain_lines_are_reported_with_line_numbers(self):
        issues, status, _ = self.assess(self.REFRAIN)
        joined = " ".join(m for w, m in issues if m.startswith("[分行结构]"))
        self.assertIn("第1、4行", joined, "整行原样复现必须给出行号，否则无法核对是否有位移")
        self.assertIn("叠句不设次数上下限", joined)

    def test_short_prose_gets_no_structure_notes(self):
        issues, status, _ = self.assess(self.PROSE)
        self.assertEqual(status, "short")
        self.assertEqual([m for w, m in issues if m.startswith("[分行结构]")], [],
                         "触发条件必须是行末无句末标点的比例，而不是字数少")

    def test_notes_do_not_change_score_or_label(self):
        issues, status, score = self.assess(self.JUEJU)
        self.assertEqual(LINT.label_of(score, status), "无法判定")
        self.assertEqual(sum(w for w, _ in issues), 0, "位置统计不得进分数")


class LongLineStructureTests(unittest.TestCase):
    """v0.51: the same position statistics must survive on the scored path.

    Before this, `[分行结构]` was only reachable below MIN_CHARS, so a 300-character poem
    lost the line-level view exactly where it had enough text to matter.
    """

    CHECKLIST = "\n".join("%d. 检查第%d项的标题层级与链接可达性" % (i, i) for i in range(1, 21))
    SEMICOLON = "山一程；\n水一程；\n身向榆关那畔行；\n夜深千帐灯；\n"
    QUOTED = "他说：“今夜有雪。”\n她说：“明早会停。”\n风从北边来。\n灯还亮着。"

    def notes(self, text):
        return LINT.evaluate(text, "general")

    def test_long_poem_gets_line_positions(self):
        issues, status, _ = self.notes(POEM)
        self.assertEqual(status, "ok")
        notes = [(w, m) for w, m in issues if m.startswith("[分行结构]")]
        self.assertGreaterEqual(len(notes), 3, "长诗也应拿到行数、行长等位置统计")
        self.assertTrue(all(w == 0 for w, _ in notes), "位置统计不得带权重")
        self.assertIn("有效行 24 行", " ".join(m for _, m in notes))

    def test_checklist_is_not_treated_as_verse(self):
        issues, _, _ = self.notes(self.CHECKLIST)
        joined = " ".join(m for _, m in issues)
        self.assertNotIn("[分行]", joined, "清单不是分行文本，不能提示句子层失效")
        self.assertNotIn("[分行结构]", joined, "清单条目不能被报成诗行或韵脚候选")

    def test_semicolon_is_not_a_sentence_end(self):
        issues, _, _ = self.notes(self.SEMICOLON)
        notes = [m for w, m in issues if m.startswith("[分行结构]")]
        self.assertTrue(notes, "分号是句内停顿，四行分号结尾仍属跨行书写")
        self.assertIn("3 处行末没有句末标点", " ".join(notes))

    def test_closing_quote_after_period_still_closes_the_line(self):
        issues, _, _ = self.notes(self.QUOTED)
        self.assertFalse([m for w, m in issues if m.startswith("[分行结构]")],
                         "句号后紧跟收尾引号的行已经闭合，不得计为跨行候选")

    def test_long_line_reference_lists_are_truncated(self):
        verse = "\n".join("我把月光折成纸船放进水里" for _ in range(20))
        issues, _, _ = self.notes(verse)
        joined = " ".join(m for w, m in issues if m.startswith("[分行结构]"))
        self.assertIn("共 20 行", joined, "长清单的行号必须截断并注明总数，不能撑满一行")

    def test_markdown_table_is_not_treated_as_verse(self):
        table = "\n".join([
            "| 项目 | 阈值 | 说明 |",
            "| --- | --- | --- |",
            "| 查重 | 15% | 学科分档 |",
            "| AIGC | 30% | 复检后处理 |",
            "| 盲审 | 10% | 抽样比例 |",
        ])
        issues, _, _ = self.notes(table)
        self.assertFalse([m for w, m in issues if m.startswith("[分行")],
                         "Markdown 表格不是分行韵文，不得报出诗行结构")


if __name__ == "__main__":
    unittest.main()
