"""Behavioral regressions from the 2026-09-26 read-only audit; no frozen-corpus tuning."""
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

lint = load("audit_lint", ROOT / "scripts/ai_smell_lint.py")
blind = load("audit_blind", ROOT / "tests/blindtest.py")
measure = load("audit_measure_helpers", ROOT / "tests/measurement_helpers.py")
builder = load("audit_cred_builder", ROOT / "tests/build_cred_corpus.py")
CN = "这份记录保存了车间设备的检验过程工人先核对仪表编号再检查接线位置每次送电前必须确认电源已经切断检验完成以后技术员将读数抄入登记表并签上姓名班长收到表格后将结果与上次记录比较发现异常便暂停设备使用等待维修人员到场处理随后复查保护开关和接地电阻最后保存当天的记录供下次检验参考"
EN = ("The robust valve passed the bench test. The note gives a nuanced account of the leak. Pressure is crucial to the procedure. The spring was pivotal in the repair. "
      + "On day 1 the technician opened the cabinet and checked the cable before recording the reading in the book. The operator closed the door and waited for the inspector to finish the check. " * 4)
TECH = "这套闭环控制装置用于调节电机转速，编号为1。传感器采集转速后，将测量值送回控制器，控制器根据误差调节电压。闭环稳定性由系统极点决定，检验时需要记录阶跃响应和稳态误差。闭环带宽决定设备跟踪指令的能力。程序读取缓冲区之前检查地址对齐，结构体的地址对齐要求由编译器和处理器共同确定，强制取消地址对齐可能增加访存次数。维修人员应保存原始测量结果，再比较调整前后的曲线。"

def messages(result):
    return [m for w, m in result[0] if w]

def cli(args, text=""):
    return subprocess.run([sys.executable, "-B", str(ROOT / "scripts/ai_smell_lint.py"), *args],
                          input=text, capture_output=True, text=True, encoding="utf-8", timeout=10)

class CliBehavior(unittest.TestCase):
    def test_help(self):
        r = cli(["--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("--language", r.stdout)
        self.assertNotIn("Traceback", r.stderr)

    def test_unknown_option_is_controlled(self):
        r = cli(["--not-a-real-option"])
        self.assertEqual(r.returncode, 2)
        self.assertIn("未知参数", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_missing_file_is_controlled(self):
        r = cli([str(ROOT / "tests/__audit_definitely_missing_input__.md")])
        self.assertEqual(r.returncode, 2)
        self.assertIn("无法读取输入", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_language_argument_errors(self):
        for args in (["--language"], ["--language", "spanish"]):
            with self.subTest(args=args):
                r = cli(args)
                self.assertEqual(r.returncode, 2)
                self.assertNotIn("Traceback", r.stderr)

    def test_json_preserves_static_not_identity_contract(self):
        r = cli(["--json", "--language", "en", "-"], EN)
        data = json.loads(r.stdout)[0]
        self.assertEqual(data["score_kind"], "static_style_heuristic")
        self.assertIs(data["is_ai_probability"], False)
        self.assertIs(data["language_is_verified"], False)
        self.assertEqual(data["language"], "en")

class LanguageAndScore(unittest.TestCase):
    def test_mixed_99_to_100_keeps_identical_english_signal_score(self):
        left = lint.evaluate(EN + CN[:99], "tech", "mixed")
        right = lint.evaluate(EN + CN[:100], "tech", "mixed")
        self.assertEqual((left[1], right[1]), ("ok", "ok"))
        self.assertEqual(left[2], right[2])
        self.assertEqual(left[2], lint.evaluate(EN, "tech", "en")[2])

    def test_chinese_keyword_does_not_appear_only_after_100(self):
        en = "The inspector recorded the reading on day 1. " * 40
        prefix = "闭环" + CN
        results = [lint.evaluate(en + prefix[:n], "tech", "mixed") for n in (99, 100)]
        self.assertEqual(results[0][2], results[1][2])
        for r in results:
            self.assertTrue(any("闭环" in m for m in messages(r)))

    def test_declared_english_minimum(self):
        self.assertEqual(lint.evaluate("valve " * 99, language="en")[1], "short")
        self.assertEqual(lint.evaluate("valve " * 100, language="en")[1], "ok")

    def test_declared_mixed_minimum(self):
        self.assertEqual(lint.evaluate(CN[:50] + " valve" * 49, language="mixed")[1], "short")
        self.assertEqual(lint.evaluate(CN[:50] + " valve" * 50, language="mixed")[1], "ok")

    def test_spanish_ascii_is_not_automatically_english(self):
        text = "El equipo reviso el informe antes de cerrar la puerta y entregar las llaves al encargado. " * 8
        r = lint.evaluate(text)
        self.assertEqual(r[1], "limited")
        all_messages = " ".join(m for _, m in r[0])
        self.assertIn("语言未确认", all_messages)
        self.assertNotIn("[英文模式]", all_messages)

    def test_cyrillic_is_unsupported_not_short(self):
        r = lint.evaluate("Рабочие проверили приборы перед началом работы и записали результаты измерений в журнал. " * 20)
        self.assertEqual(r[1], "unsupported")
        self.assertTrue(any("不支持" in m for _, m in r[0]))

    def test_auto_latin_cli_abstains(self):
        r = cli(["--json", "-"], EN)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(json.loads(r.stdout)[0]["status"], "limited")

    def test_explicit_english_is_declared_not_verified(self):
        r = lint.evaluate(EN, language="en")
        self.assertEqual(r[1], "ok")
        self.assertTrue(any("调用者声明" in m for _, m in r[0]))

    def test_technical_word_advice_preserves_meaning(self):
        r = lint.evaluate(TECH, "tech")
        weighted = [(w,m) for w,m in r[0] if w and ("闭环" in m or "对齐" in m)]
        self.assertEqual(len(weighted), 2)
        self.assertEqual([w for w,_ in weighted], [12,12])
        for _, message in weighted:
            self.assertIn("专业术语", message)
            self.assertIn("保留", message)
            self.assertNotIn("→ 删除", message)

class EndingAndGenre(unittest.TestCase):
    def test_short_actual_final_summary_is_seen(self):
        r = lint.evaluate(CN + "记录编号1。" + chr(10)*2 + "总而言之。")
        self.assertTrue(any(m.startswith("[总结式结尾]") for m in messages(r)))

    def test_summary_in_previous_long_paragraph_is_not_final(self):
        r = lint.evaluate("总而言之，" + CN + "记录编号1。" + chr(10)*2 + "明天再谈。")
        self.assertFalse(any(m.startswith("[总结式结尾]") for m in messages(r)))

    def test_known_signoffs_do_not_hide_short_body_ending(self):
        text = CN + "编号1。" + chr(10)*2 + "总而言之。" + chr(10)*2 + "此致" + chr(10)*2 + "敬礼"
        self.assertTrue(any(m.startswith("[总结式结尾]") for m in messages(lint.evaluate(text))))

    def test_english_tech_honors_summary_gate(self):
        text = EN + chr(10)*2 + "In conclusion, the valve is ready."
        general = messages(lint.evaluate(text, "general", "en"))
        tech = messages(lint.evaluate(text, "tech", "en"))
        self.assertTrue(any(m.startswith("[英文总结式结尾]") for m in general))
        self.assertFalse(any(m.startswith("[英文总结式结尾]") for m in tech))

    def test_mixed_tech_honors_same_gate(self):
        text = EN + CN[:99] + chr(10)*2 + "In conclusion, the valve is ready."
        general = messages(lint.evaluate(text, "general", "mixed"))
        tech = messages(lint.evaluate(text, "tech", "mixed"))
        self.assertTrue(any(m.startswith("[英文总结式结尾]") for m in general))
        self.assertFalse(any(m.startswith("[英文总结式结尾]") for m in tech))

    def test_english_previous_paragraph_is_not_final_summary(self):
        text = EN + chr(10)*2 + "In conclusion, the valve is ready." + chr(10)*2 + "We will test it tomorrow."
        r = lint.evaluate(text, language="en")
        self.assertFalse(any(m.startswith("[英文总结式结尾]") for m in messages(r)))

class MeasurementBehavior(unittest.TestCase):
    def test_ffamily_zero_penalty_uses_current_normalization(self):
        ffamily = load("audit_hc3_ffamily", ROOT / "tests/hc3_ffamily.py")
        text = EN + CN[:100]
        self.assertEqual(ffamily.f_penalty(text)[0], 0)
        self.assertEqual(ffamily.combined_score(text)[0], lint.evaluate(text)[2])

    def test_all_abstained_is_not_true_negative_or_false_negative(self):
        rows = [("sample", "general", "short", 0, [])]
        self.assertEqual(blind.metrics(rows, rows, 40), (0,0,0,0,None,None,None,None))
        self.assertEqual(blind.coverage(rows)["rate"], 0)
        self.assertEqual(blind.coverage(rows)["abstained"], 1)

    def test_partial_coverage_uses_assessed_denominators(self):
        ai = [("known", "general", "ok", 80, []), ("unknown", "general", "limited", 0, [])]
        hu = [("known", "general", "ok", 0, []), ("unknown", "general", "unsupported", 0, [])]
        self.assertEqual(blind.metrics(ai, hu, 40), (1,0,1,0,1,1,0,0))
        self.assertEqual(blind.coverage(ai)["rate"], 0.5)
        self.assertEqual(blind.coverage(hu)["rate"], 0.5)

    def test_empty_denominators_are_na(self):
        self.assertIsNone(blind.coverage([])["rate"])
        self.assertEqual(blind.fmt_rate(None), "N/A")
        self.assertIsNone(measure.auc([], [1]))
        self.assertEqual(measure.fmt(measure.rate(0,0)), "N/A")

    def test_measure_collect_excludes_unknown_status(self):
        paths = [SimpleNamespace(read_text=lambda encoding, value=value: value) for value in ("known", "short", "limited")]
        def evaluate(text, genre):
            return [], "ok" if text=="known" else text, 45 if text=="known" else 0
        group = measure.collect(paths, "general", evaluate)
        self.assertEqual(group["scores"], [45])
        self.assertEqual((group["assessed"],group["abstained"]), (1,2))
        self.assertAlmostEqual(group["coverage"], 1/3)

    def test_auc_does_not_preclude_a_specific_operating_point(self):
        ai, human = [100]*8 + [0]*2, [50]*10
        self.assertEqual(measure.auc(ai,human), 0.8)
        self.assertEqual(measure.rate(sum(x>75 for x in ai),len(ai)), 0.8)
        self.assertEqual(measure.rate(sum(x>75 for x in human),len(human)), 0.0)

    def test_builder_reports_source_pool_and_picked_medians_separately(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root/"sources"
            domain = src/"composition"
            domain.mkdir(parents=True)
            for suffix, rows in (("human",[(1,"甲"*100),(2,"乙"*200),(3,"丙"*600),(4,"丁"*700)]),
                                 ("stub",[(1,"戊"*400),(2,"己"*500)])):
                with (domain/("CReD_composition_"+suffix+".csv")).open("w",encoding="utf-8",newline="") as handle:
                    writer = csv.writer(handle)
                    writer.writerow(["id","text"])
                    writer.writerows(rows)
            capture = io.StringIO()
            with mock.patch.multiple(builder,SRC=src,OUT=root/"output",DOMAINS={"composition":"fiction"},
                                     GEN_SHORT={"stub":"stub"},HUMAN_TARGET=2,AI_TARGET=2), contextlib.redirect_stdout(capture):
                builder.main()
            output = capture.getvalue()
            self.assertIn("source_pool_n=4", output)
            self.assertIn("source_pool_median=400.0", output)
            self.assertIn("picked_human_median=150.0", output)
            self.assertIn("ai_window=[300, 900]", output)
            self.assertIn("picked_median=450.0", output)
            self.assertEqual(len(list((root/"output").glob("human_*.md"))), 2)

if __name__ == "__main__":
    unittest.main()
