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
    'references/academic-craft.md', 'references/thesis-craft.md',
    'references/argumentative-craft.md', 'references/speech-craft.md',
    'references/poetry-craft.md', 'references/prose-flow-craft.md',
    'references/argument-and-rhythm.md',
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
                try:
                    resolved.relative_to(ROOT.resolve())
                except ValueError:
                    errors.append(f'{relative} -> {target}')
                    continue
                if not resolved.exists():
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


    def test_skill_and_readme_versions_agree(self):
        """版本号曾多次手工同步；这里把 SKILL 元数据、README 标题与最新版本节绑在一起。"""
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        match = re.search(r"version:\s*'([0-9]+\.[0-9]+)'", skill)
        self.assertIsNotNone(match, 'SKILL.md 缺少 metadata.version')
        version = match.group(1)
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        head = "\n".join(readme.splitlines()[:10])
        self.assertIn(version, head, 'README 顶部（标题或元数据表）未写当前版本')
        sections = re.findall(r'^## v([0-9]+\.[0-9]+)', readme, re.M)
        if not sections:
            changelog = ROOT / 'CHANGELOG.md'
            if changelog.is_file():
                sections = re.findall(r'^## ([0-9]+\.[0-9]+)', changelog.read_text(encoding='utf-8'), re.M)
        self.assertEqual(sections[0], version, '最新版本记录必须就是当前版本')
        self.assertEqual(sections, sorted(sections, key=lambda v: tuple(map(int, v.split('.'))), reverse=True),
                         '版本记录必须按版本号降序排列')


if __name__ == '__main__':
    unittest.main()
