"""真实任务评测集的结构守卫：用例必须指向真实文档，且达到最低覆盖。

语义路由是否选对不在 unittest 里判断；这里只防止用例腐烂成失效链接或空壳。
"""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'tests' / 'eval'
SPEC = importlib.util.spec_from_file_location('validate_eval', EVAL / 'validate_eval.py')
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class EvalSetTests(unittest.TestCase):
    def test_routing_cases_are_valid(self):
        errors = VALIDATOR.validate_routing(VALIDATOR.load_cases('routing_cases.json'))
        self.assertEqual(errors, [], '\n'.join(errors))

    def test_revision_cases_are_valid(self):
        errors = VALIDATOR.validate_revision(VALIDATOR.load_cases('revision_cases.json'))
        self.assertEqual(errors, [], '\n'.join(errors))

    def test_drift_cases_are_valid(self):
        errors = VALIDATOR.validate_drift(VALIDATOR.load_cases('drift_cases.json'))
        self.assertEqual(errors, [], '\n'.join(errors))

    def test_fidelity_cases_are_valid(self):
        errors = VALIDATOR.validate_fidelity(
            VALIDATOR.load_cases('fidelity_cases.json'))
        self.assertEqual(errors, [], '\n'.join(errors))

    def test_eval_files_use_utf8_without_crlf(self):
        for path in sorted(EVAL.iterdir()):
            if path.suffix not in ('.md', '.py', '.json', '.csv'):
                continue
            with self.subTest(file=path.name):
                data = path.read_bytes()
                self.assertFalse(data.startswith(b'\xef\xbb\xbf'), f'{path.name}: BOM')
                self.assertNotIn(b'\r', data, f'{path.name}: CRLF')
                data.decode('utf-8')


if __name__ == '__main__':
    unittest.main()
