# -*- coding: utf-8 -*-
"""证据索引：41 条规则都必须能指回外部证据或声明“无计分”。

本测试守住四件事：
1. 索引覆盖台账里的每一条规则，且类型一致；
2. `evidence_ids` 全部能在 detection-evidence.md 里找到对应编号；
3. 计分规则必须有证据或实测，状态行必须为 0 权重、无证据需求；
4. 台账里的实测登记必须与 rule-measurements.json 的实际测量结果一一对应。
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT / "references" / "rule-ledger.json").read_text(encoding="utf-8"))
INDEX = json.loads((ROOT / "references" / "evidence-index.json").read_text(encoding="utf-8"))
EVIDENCE_TEXT = (ROOT / "references" / "detection-evidence.md").read_text(encoding="utf-8")
KNOWN_IDS = set(re.findall(r"\| *E(\d\d) *\|", EVIDENCE_TEXT)) | set(re.findall(r"\bE(\d\d)\b", EVIDENCE_TEXT))
KNOWN_IDS = {"E" + i for i in KNOWN_IDS}

LEDGER_TAGS = [r["tag"] for r in LEDGER["rules"]]
INDEX_TAGS = [r["tag"] for r in INDEX["rules"]]


class CoverageTest(unittest.TestCase):
    def test_index_version(self):
        self.assertEqual(INDEX["version"], "0.60")
        self.assertEqual(INDEX["evidence_base"], "references/detection-evidence.md")

    def test_every_rule_indexed_once(self):
        self.assertEqual(len(INDEX_TAGS), len(set(INDEX_TAGS))
                         , "证据索引里有重复标签")
        self.assertEqual(set(INDEX_TAGS), set(LEDGER_TAGS))
        self.assertEqual(len(INDEX_TAGS), 41)

    def test_kind_matches_ledger(self):
        ledger_kind = {r["tag"]: r["kind"] for r in LEDGER["rules"]}
        for row in INDEX["rules"]:
            self.assertEqual(row["kind"], ledger_kind[row["tag"]], row["tag"])


class EvidenceReferenceTest(unittest.TestCase):
    def test_ids_exist_in_evidence_doc(self):
        for row in INDEX["rules"]:
            for eid in row["evidence_ids"]:
                self.assertIn(eid, KNOWN_IDS, "%s 引用了不存在的 %s" % (row["tag"], eid))

    def test_weighted_rules_have_evidence(self):
        for row in INDEX["rules"]:
            if row["kind"] == "weighted":
                self.assertTrue(row["evidence_ids"],
                                "%s 是加权规则，却没有证据编号" % row["tag"])
            if row["kind"] == "status":
                self.assertEqual(row["evidence_ids"], [],
                                 "%s 是状态行，只做测量说明，不绑定证据" % row["tag"])

    def test_rationale_non_empty(self):
        for row in INDEX["rules"]:
            self.assertTrue(row["rationale"].strip(), row["tag"])

    def test_measured_only_where_ledger_has_it(self):
        ledger_measured = {r["tag"] for r in LEDGER["rules"] if r.get("measured_v060")}
        index_measured = {r["tag"] for r in INDEX["rules"] if r.get("measured_v060")}
        self.assertEqual(index_measured, ledger_measured)
        self.assertLessEqual(len(index_measured), 41)

    def test_measured_matches_rule_measurement_output(self):
        """台账实测必须来自当前 evidence_measure.py 的输出，不能留旧口径。"""
        measured = json.loads(
            (ROOT / "references" / "rule-measurements.json").read_text(encoding="utf-8")
        )["rules"]
        ledger_measured = {r["tag"].strip("[]") for r in LEDGER["rules"] if r.get("measured_v060")}
        self.assertEqual(ledger_measured, set(measured))


if __name__ == "__main__":
    unittest.main()
