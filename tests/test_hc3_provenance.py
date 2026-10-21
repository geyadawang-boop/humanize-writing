# -*- coding: utf-8 -*-
"""Offline source-integrity tests using temporary synthetic HC3 inputs only."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


spec = importlib.util.spec_from_file_location(
    "hc3_builder_under_test", Path(__file__).with_name("build_hc3_corpus.py")
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.raw = self.root / "raw"
        self.raw.mkdir()
        self.dest = self.root / "corpus"
        self.data = {
            "a.jsonl": (json.dumps({"human_answers": ["甲文"]}, ensure_ascii=False) + "\n").encode("utf-8"),
            "b.jsonl": (json.dumps({"chatgpt_answers": ["乙文"]}, ensure_ascii=False) + "\n").encode("utf-8"),
        }
        self.expected = {name: hashlib.sha256(data).hexdigest() for name, data in self.data.items()}
        for name, data in self.data.items():
            (self.raw / name).write_bytes(data)
        self.plan = [
            ("a_%02d.md", "a.jsonl", "human_answers", 1, 3, 1),
            ("b_%02d.md", "b.jsonl", "chatgpt_answers", 1, 3, 1),
        ]

    def run_build(self, expected=None):
        with mock.patch.multiple(
            builder, PLAN=self.plan, SRC_SHA=self.expected if expected is None else expected
        ), mock.patch.object(
            builder.urllib.request, "urlopen", side_effect=AssertionError("Network forbidden in provenance tests")
        ), contextlib.redirect_stdout(io.StringIO()):
            return builder.build(self.raw, self.dest)

    def test_matching_sources_write_expected_samples(self):
        self.assertEqual(self.run_build(), 2)
        self.assertEqual((self.dest / "a_01.md").read_bytes(), "甲文\n".encode("utf-8"))
        self.assertEqual((self.dest / "b_01.md").read_bytes(), "乙文\n".encode("utf-8"))

    def test_mismatch_rejects_before_creating_destination(self):
        expected = dict(self.expected)
        expected["b.jsonl"] = hashlib.sha256(self.data["b.jsonl"] + b" ").hexdigest()
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch for b.jsonl"):
            self.run_build(expected)
        self.assertFalse(self.dest.exists())

    def test_later_mismatch_preserves_existing_corpus_without_partial_write(self):
        self.dest.mkdir()
        sentinel = self.dest / "a_01.md"
        sentinel.write_bytes(b"existing frozen sample")
        before = {p.name: p.read_bytes() for p in self.dest.iterdir()}
        (self.raw / "b.jsonl").write_bytes(self.data["b.jsonl"] + b" ")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch for b.jsonl"):
            self.run_build()
        self.assertEqual({p.name: p.read_bytes() for p in self.dest.iterdir()}, before)

    def test_matching_first_sixteen_digest_characters_is_insufficient(self):
        actual = self.expected["a.jsonl"]
        changed = actual[:-1] + ("0" if actual[-1] != "0" else "1")
        self.assertEqual(changed[:16], actual[:16])
        with mock.patch.object(builder, "SRC_SHA", {"a.jsonl": changed}):
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                builder.verify_source("a.jsonl", self.data["a.jsonl"])

    def test_missing_registration_rejects_before_destination_creation(self):
        with self.assertRaisesRegex(ValueError, "No valid registered SHA-256 for HC3 source b.jsonl"):
            self.run_build({"a.jsonl": self.expected["a.jsonl"]})
        self.assertFalse(self.dest.exists())

    def test_malformed_registration_is_rejected(self):
        for invalid in (None, "", "a" * 16, "z" * 64):
            with self.subTest(expected=invalid), mock.patch.object(builder, "SRC_SHA", {"a.jsonl": invalid}):
                with self.assertRaisesRegex(ValueError, "No valid registered SHA-256"):
                    builder.verify_source("a.jsonl", self.data["a.jsonl"])

    def test_parses_verified_bytes_without_rereading_cache(self):
        (self.raw / "a.jsonl").write_bytes(b"not the verified data")
        with mock.patch.object(builder, "fetch", side_effect=lambda name, raw: self.data[name]):
            self.assertEqual(self.run_build(), 2)
        self.assertEqual((self.dest / "a_01.md").read_text(encoding="utf-8"), "甲文\n")


if __name__ == "__main__":
    unittest.main()
