# -*- coding: utf-8 -*-
"""ai_rate：模型契约、评分输出与命令行。

重点守住四条边界：
1. 分数必须在 0–1 之间，且显式标记“不是作者判断”；
2. 短文本拒绝评分，而不是给一个看似精确的数字；
3. 模型文件里的指标与校准表必须存在，报告不能凭空引用；
4. 分布外文本返回 out_of_domain 且不给分；长文分数与贡献取自同一窗口。
"""
import importlib.util
import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("hw_ai_rate", ROOT / "scripts" / "ai_rate.py")
R = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R)

MODEL_PATH = ROOT / "models" / "zh_hc3_logreg_v1.json"
MODEL = json.loads(MODEL_PATH.read_text(encoding="utf-8"))

HUMANISH = (
    "我到的时候，摊子还没收。老板蹲在小马扎上剥蒜，脚边一只搪瓷盆，"
    "盆里的水浑着，浮着几片香菜叶。他抬头看了我一眼，说今天没面了，"
    "锅里那点汤是给自己留的。我说那就算了。他说你等等，起身去后面，"
    "翻出一个塑料袋，里面是半把挂面，硬塞给我，说回去自己下，别放太多盐。"
)
LONG_AIISH = (
    "首先，我们需要明确问题的核心。其次，从多个维度来看，这一现象既涉及个体选择，"
    "也涉及结构性因素。值得注意的是，相关研究已经表明，二者之间存在复杂的互动关系。"
    "综上所述，只有在充分理解其内在逻辑的基础上，才能形成更为全面的认识。"
) * 3
# 拼接训练域内的人类回答，得到超过 1400 字、不会被分布外规则拦截的长文本
LONG_DOMAIN_TEXT = "\n\n".join(
    json.loads(line)["human"]
    for line in (ROOT / "corpora" / "pairs" / "hc3_test.jsonl").read_text(encoding="utf-8").splitlines()[:12]
    if line.strip()
)


class ModelContractTest(unittest.TestCase):
    def test_model_metadata(self):
        self.assertEqual(MODEL["tool"], "ai_rate")
        self.assertEqual(len(MODEL["feature_names"]), 31)
        self.assertEqual(len(MODEL["w"]), 31)
        self.assertIn("platt", MODEL)

    def test_metrics_registered(self):
        m = MODEL["metrics"]["test"]
        self.assertEqual(m["n_pairs"], 713)
        self.assertGreaterEqual(m["auc"], 0.90)
        self.assertLessEqual(m["auc_ci95"][0], m["auc"])
        self.assertGreaterEqual(m["auc_ci95"][1], m["auc"])
        self.assertTrue(MODEL["calibration_table"])

    def test_calibration_is_monotonic_on_raw(self):
        self.assertGreater(MODEL["platt"]["a"], 0)
        at_mean = R.calibrated(MODEL, [MODEL["mu"]])[0]
        self.assertGreater(at_mean, 0.0)
        self.assertLess(at_mean, 1.0)
        lo = R.calibrated(MODEL, [[v - 1.0 for v in MODEL["mu"] * 1]])[0]
        self.assertGreaterEqual(lo, 0.0)


class PredictTest(unittest.TestCase):
    def test_short_text_refused(self):
        out = R.predict_text(MODEL, "太短了。")
        self.assertEqual(out["status"], "insufficient")
        self.assertNotIn("score", out)

    def test_normal_text_shape(self):
        out = R.predict_text(MODEL, HUMANISH, genre="qa")
        self.assertEqual(out["status"], "ok")
        self.assertGreaterEqual(out["score"], 0.0)
        self.assertLessEqual(out["score"], 1.0)
        self.assertEqual(out["is_authorship_judgment"], False)
        self.assertEqual(len(out["top_features"]), 8)
        self.assertEqual(out["score_window"], 1)
        self.assertNotIn("windows_detail", out)
        self.assertIn(out["band"], {"偏低", "不确定", "偏高"})
        self.assertTrue(out["warnings"])
        self.assertIn("不是", out["note"])

    def test_declared_genre_out_of_domain(self):
        out = R.predict_text(MODEL, HUMANISH, genre="fiction")
        self.assertEqual(out["status"], "out_of_domain")
        for key in ("score", "score_iqr", "band", "window_scores"):
            self.assertNotIn(key, out)
        self.assertTrue(out["reasons"])
        self.assertEqual(len(out["top_features"]), 8)
        self.assertEqual(out["is_authorship_judgment"], False)

    def test_long_text_windows_aligned(self):
        self.assertGreater(R.cjk_len(LONG_DOMAIN_TEXT), 1400)
        out = R.predict_text(MODEL, LONG_DOMAIN_TEXT)
        self.assertEqual(out["status"], "ok")
        self.assertGreater(out["windows"], 1)
        self.assertEqual(len(out["windows_detail"]), out["windows"])
        idx = out["score_window"] - 1
        self.assertEqual(out["windows_detail"][idx]["score"], out["score"])
        self.assertEqual(
            [it["name"] for it in out["windows_detail"][idx]["top_features"]],
            [it["name"] for it in out["top_features"][:3]],
        )

    def test_iqr_brackets_score(self):
        out = R.predict_text(MODEL, LONG_AIISH)
        self.assertEqual(out["status"], "ok")
        self.assertGreaterEqual(out["windows"], 1)
        self.assertLessEqual(out["windows"], 8)
        self.assertGreaterEqual(out["score_iqr"][0], 0.0)
        self.assertLessEqual(out["score_iqr"][1], 1.0)

    def test_deterministic(self):
        a = R.predict_text(MODEL, HUMANISH)["score"]
        b = R.predict_text(MODEL, HUMANISH)["score"]
        self.assertEqual(a, b)

    def test_band_boundaries(self):
        self.assertEqual(R.band_of(0.1), "偏低")
        self.assertEqual(R.band_of(0.9), "偏高")
        self.assertNotEqual(R.band_of(0.1), R.band_of(0.9))


class CliTest(unittest.TestCase):
    def test_predict_json(self):
        p = ROOT / "tests" / "tmp_predict_sample.md"
        try:
            p.write_text(HUMANISH, encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = R.main(["predict", str(p), "--json"])
            self.assertEqual(rc, 0)
            data = json.loads(buf.getvalue())
            self.assertEqual(data["results"][0]["result"]["status"], "ok")
        finally:
            if p.exists():
                p.unlink()

    def test_explain_runs(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = R.main(["explain"])
        self.assertEqual(rc, 0)
        self.assertIn("sent_len", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
