"""File-contract checks only; semantic routing needs independent task evaluation."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = (
    'SKILL.md', 'README.md', 'references/routing.md',
    'references/genre-router.md', 'references/editing-workflow.md',
    'references/novel-workflow.md', 'references/screenplay-workflow.md',
    'references/project-workflow.md', 'references/knowledge-map.md',
    'references/material-intake.md', 'references/novel-craft.md',
    'references/longform-revision.md',
    'references/by-genre.md',
    'references/chinese-screenplay-format.md', 'references/content-boundaries.md',
    'references/campus-youth-craft.md', 'references/china-screen-content-boundaries.md',
    'references/quick-reference.md', 'references/deai-techniques.md',
    'references/writing-workflow.md', 'templates/README.md',
    'references/style-craft.md', 'references/style-spectrum-craft.md',
    'references/research-basis.md', 'references/source-evidence.md',
    'templates/quality-review.md',
)


class SkillStructureTests(unittest.TestCase):
    def test_active_local_links_resolve_inside_skill(self):
        errors = []
        for relative in ACTIVE:
            source = ROOT / relative
            if not source.is_file():
                errors.append(f'{relative}: missing active resource')
                continue
            content = source.read_text(encoding='utf-8')
            for raw in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', content):
                target = raw.split(' "', 1)[0].strip('<> ')
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                target = unquote(target.split('#', 1)[0])
                if not target:
                    continue
                resolved = (source.parent / target).resolve()
                if not resolved.is_relative_to(ROOT.resolve()) or not resolved.exists():
                    errors.append(f'{relative} -> {target}')
        self.assertEqual(errors, [], '\n'.join(errors))

    def test_package_text_uses_utf8_lf(self):
        errors = []
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file() or path.suffix not in ('.md', '.py'):
                continue
            data = path.read_bytes()
            relative = path.relative_to(ROOT).as_posix()
            if data.startswith(bytes([239, 187, 191])) or bytes([13]) in data:
                errors.append(relative + ': BOM or non-LF line ending')
            try:
                data.decode('utf-8')
            except UnicodeDecodeError:
                errors.append(relative + ': invalid UTF-8')
        self.assertEqual(errors, [], chr(10).join(errors))

    def test_core_resources_are_utf8_without_bom_or_nul(self):
        for relative in ACTIVE:
            with self.subTest(file=relative):
                data = (ROOT / relative).read_bytes()
                self.assertFalse(data.startswith(b'\xef\xbb\xbf'))
                self.assertNotIn(b'\0', data)
                self.assertTrue(data.decode('utf-8').strip())


if __name__ == '__main__':
    unittest.main()
