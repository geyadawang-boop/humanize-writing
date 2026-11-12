# -*- coding: utf-8 -*-
"""随包语料：manifest 与文件必须互相对得上。

语料一旦与 manifest 脱节，校准报告里的 AUC 就没有意义。本测试校验：
1. 文件存在、sha256 与 manifest 一致；
2. 声明条数等于实际行数，域计数与行数吻合；
3. 不携带上游 prompt（question），不夹带隐私串；
4. 许可、来源、切分规则都有登记。
"""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "corpora" / "manifest.json"
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
PRIVACY_RE = re.compile(r"(https?://|www\.|\b[\w.+-]+@[\w-]+\.\w+|1[3-9]\d{9})")


def rows_of(split):
    path = ROOT / MANIFEST["splits"][split]["path"]
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


class ManifestIntegrityTest(unittest.TestCase):
    def test_version_and_source(self):
        self.assertEqual(MANIFEST["version"], "0.60")
        src = MANIFEST["source"]
        self.assertEqual(src["license"], "CC BY-SA 4.0")
        self.assertTrue(src["license_url"].startswith("https://creativecommons.org/"))
        self.assertEqual(src["upstream_sha256"], src["expected_sha256"])
        self.assertTrue(src["sha_matches_expected"])

    def test_sha256_matches_files(self):
        for name, info in MANIFEST["splits"].items():
            path = ROOT / info["path"]
            self.assertTrue(path.exists(), name)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, info["sha256"], name)

    def test_declared_counts_match_rows(self):
        total = 0
        for name, info in MANIFEST["splits"].items():
            rows = rows_of(name)
            self.assertEqual(len(rows), info["pairs"], name)
            total += len(rows)
        self.assertEqual(total, MANIFEST["totals"]["pairs"])

    def test_domain_counts_match_rows(self):
        for name, counts in MANIFEST["domain_counts"].items():
            actual = {}
            for row in rows_of(name):
                actual[row["domain"]] = actual.get(row["domain"], 0) + 1
            self.assertEqual(actual, counts, name)

    def test_splits_are_disjoint(self):
        ids = {name: {r["id"] for r in rows_of(name)} for name in MANIFEST["splits"]}
        self.assertFalse(ids["train"] & ids["cal"])
        self.assertFalse(ids["train"] & ids["test"])
        self.assertFalse(ids["cal"] & ids["test"])


class RowContractTest(unittest.TestCase):
    def test_fields_present(self):
        rows = rows_of("test")
        for row in rows[:50]:
            for field in MANIFEST["fields"]:
                self.assertIn(field, row)
            self.assertEqual(row["license"], "CC BY-SA 4.0")
            self.assertGreaterEqual(row["human_len"], MANIFEST["filters"]["min_cjk"])

    def test_no_prompt_carried(self):
        for row in rows_of("test")[:50]:
            self.assertNotIn("question", row)
            self.assertNotIn("prompt", row)

    def test_no_privacy_strings(self):
        for row in rows_of("test")[:100]:
            for side in ("human", "ai"):
                self.assertIsNone(PRIVACY_RE.search(row[side]), side)

    def test_excluded_domains_absent(self):
        excluded = set(MANIFEST["filters"]["excluded_domains"])
        for name in MANIFEST["splits"]:
            self.assertFalse({r["domain"] for r in rows_of(name)} & excluded, name)

    def test_length_cap(self):
        cap = MANIFEST["filters"]["max_cjk"] + 100  # 句末收口允许少量超出
        for row in rows_of("test"):
            self.assertLessEqual(row["human_len"], cap)
            self.assertLessEqual(row["ai_len"], cap)


if __name__ == "__main__":
    unittest.main()
