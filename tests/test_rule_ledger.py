# -*- coding: utf-8 -*-
"""规则台账：单一事实源驱动「每条规则都能自主触发、权重与声明一致」。

台账 references/rule-ledger.json 为数据源；本测试负责三件事：
1. 每条规则用自带的探针必须命中，加权规则必须有正权重，观察/状态行必须为零；
2. 源码里存在的标签不得游离于台账之外（新增规则未登记即失败）；
3. 文体门控、版本号、冻结分数在台账、源码、文档之间保持一致。
"""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ledger_lint", ROOT / "scripts" / "ai_smell_lint.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)

LEDGER = json.loads((ROOT / "references" / "rule-ledger.json").read_text(encoding="utf-8"))
RULES = LEDGER["rules"]
BY_TAG = {r["tag"]: r for r in RULES}
TAG_RE = re.compile(r"^(\[[^\]]+\])")


def run(rule):
    p = rule["probe"]
    return LINT.evaluate(p["text"], p["genre"], p["language"],
                         p["fingerprint"], p["candidates"])


def tags_of(issues):
    found = set()
    for _, message in issues:
        m = TAG_RE.match(message)
        if m:
            found.add(m.group(1))
    return found


class LedgerContractTests(unittest.TestCase):
    def test_versions_agree_across_ledger_code_and_docs(self):
        self.assertEqual(LEDGER["ruleset_version"], LINT.RULESET_VERSION)
        skill = re.search(r"version:\s*'([^']+)'",
                          (ROOT / "SKILL.md").read_text(encoding="utf-8")).group(1)
        self.assertEqual(LEDGER["skill_version"], skill)
        self.assertIn("v" + skill, (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("## " + skill, (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_genre_skips_match_code(self):
        expected = {k: list(v) for k, v in LINT.GENRE_SKIPS.items()}
        self.assertEqual(LEDGER["genre_skips"], expected)

    def test_tags_are_unique_and_well_formed(self):
        tags = [r["tag"] for r in RULES]
        self.assertEqual(len(tags), len(set(tags)), "台账存在重复标签")
        for r in RULES:
            self.assertRegex(r["tag"], r"^\[[^\]]+\]$")
            self.assertIn(r["kind"], ("weighted", "observation", "status"))
            self.assertTrue(r["weight"] and r["evidence"])

    def test_every_rule_probe_actually_fires(self):
        missing = []
        for rule in RULES:
            issues, _, _ = run(rule)
            if rule["tag"] not in tags_of(issues):
                missing.append(rule["tag"])
        self.assertEqual(missing, [], "以下规则的探针未能自主触发: %s" % missing)

    def test_weighted_rules_carry_weight_observations_never_do(self):
        wrong = []
        for rule in RULES:
            issues, _, _ = run(rule)
            hits = [w for w, m in issues if m.startswith(rule["tag"])]
            if rule["kind"] == "weighted" and not any(w > 0 for w in hits):
                wrong.append((rule["tag"], "加权规则无正权重", hits))
            if rule["kind"] != "weighted" and any(w != 0 for w in hits):
                wrong.append((rule["tag"], "观察/状态行应按零权重", hits))
        self.assertEqual(wrong, [])

    def test_observation_rules_stay_zero_across_all_probes(self):
        leaks = []
        observations = [r["tag"] for r in RULES if r["kind"] == "observation"]
        for rule in RULES:
            issues, _, _ = run(rule)
            for tag in observations:
                for w, m in issues:
                    if m.startswith(tag) and w:
                        leaks.append((rule["tag"], tag, w))
        self.assertEqual(leaks, [], "观察行出现正权重: %s" % leaks)

    def test_no_unregistered_tag_is_emitted(self):
        emitted, bad = set(), []
        for rule in RULES:
            issues, _, _ = run(rule)
            found = tags_of(issues)
            emitted |= found
            bad.extend(sorted(found - set(BY_TAG)))
        self.assertEqual(bad, [], "探针产生未登记标签: %s" % sorted(set(bad)))
        self.assertEqual(emitted, set(BY_TAG), "台账中有规则未被任何探针覆盖")

    def test_genre_skips_actually_disable_the_rule(self):
        failing = []
        for genre, skips in LEDGER["genre_skips"].items():
            for name in skips:
                tag = "[%s]" % name
                rule = BY_TAG.get(tag)
                if not rule:
                    continue  # 段落均匀不是独立标签
                issues, _, _ = run(rule)
                text = rule["probe"]["text"]
                gated, _, _ = LINT.evaluate(text, genre, rule["probe"]["language"],
                                            rule["probe"]["fingerprint"], rule["probe"]["candidates"])
                if tag in tags_of(gated):
                    failing.append((genre, tag))
        self.assertEqual(failing, [], "文体门控未生效: %s" % failing)

    def test_genre_line_is_linked_to_gating(self):
        rule = BY_TAG["[段落开头]"]
        issues, _, _ = LINT.evaluate(rule["probe"]["text"], "tech", rule["probe"]["language"])
        self.assertIn("[genre]", tags_of(issues))
        self.assertNotIn("[段落开头]", tags_of(issues))


if __name__ == "__main__":
    unittest.main()
