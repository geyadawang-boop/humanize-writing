"""Every knowledge document must be reachable from SKILL.md by real markdown links.

The existing structure test only checks that links *inside* listed files resolve; it cannot see a
document that nothing links to. That blind spot was found in v0.49: four references files were only
ever mentioned as plain filenames, so no navigation path reached them.
"""
from pathlib import Path
import re
import unittest
from collections import deque

ROOT = Path(__file__).resolve().parents[1]
START = ROOT / 'SKILL.md'
LINK = re.compile(r'\[[^\]\n]*\]\(([^)\n]+)\)')

# Knowledge documents the entry chain must reach. Corpora, templates and self-descriptive
# READMEs are excluded: they are read by path from scripts/tests, not by navigation.
SKIP_NAMES = {'README.md', 'SKILL.md', 'SOURCES.md', 'MANIFEST.md', 'CALIB.md', 'SAMPLES.md'}


def links_from(path):
    text = path.read_text(encoding='utf-8')
    out = []
    for raw in LINK.findall(text):
        target = raw.split(' "', 1)[0].strip('<> ').split('#')[0]
        if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        resolved = (path.parent / target).resolve()
        if resolved.suffix == '.md' and resolved.exists():
            out.append(resolved)
    return out


def reachable():
    seen, queue = {START}, deque([START])
    while queue:
        current = queue.popleft()
        for nxt in links_from(current):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


class LinkReachabilityTests(unittest.TestCase):
    def test_start_file_exists(self):
        self.assertTrue(START.is_file(), 'SKILL.md entry point missing')

    def test_every_knowledge_document_is_reachable_from_skill(self):
        got = reachable()
        expected = [p for p in (ROOT / 'references').glob('*.md') if p.name not in SKIP_NAMES]
        self.assertGreater(len(expected), 40, 'reference set shrank unexpectedly; re-check this list')
        missing = sorted(p.name for p in expected if p.resolve() not in got)
        self.assertEqual(
            missing, [],
            '这些知识文档没有任何指向它的 markdown 链接，从 SKILL.md 走不到：' + ', '.join(missing))

    def test_navigation_is_layered_not_one_flat_index(self):
        """Some documents must be reached through another document, not all dumped onto SKILL.md."""
        parent, queue = {START: None}, deque([START])
        while queue:
            current = queue.popleft()
            for nxt in links_from(current):
                if nxt not in parent:
                    parent[nxt] = current
                    queue.append(nxt)

        def depth(path):
            n, cur = 0, path
            while parent.get(cur) is not None:
                n += 1
                cur = parent[cur]
            return n

        deep = [p for p in parent if p != START and depth(p) >= 2]
        self.assertGreaterEqual(
            len(deep), 10,
            '可达集合几乎全部直挂在入口上，说明按需加载的分层结构被压平了')


if __name__ == '__main__':
    unittest.main()
