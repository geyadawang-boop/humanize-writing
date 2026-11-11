"""运行：python -B -m unittest discover -s tests -p test_writing_project.py -v

自包含临时项目。真实短段落只验证操作闭环，不代表长篇文学质量评测。
"""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import writing_project as wp


NOVEL_BODIES = (
    '# 第一章 借灯\n\n小满赶到渡口时，父亲的渡船已经离岸。灯塔暗着，雾里只剩一声短笛。'
    '她从值班室找出旧油灯，却发现灯芯湿透了。她拆下母亲补在袖口的棉线，拧成新的灯芯。'
    '火苗立起来，她没有向河面挥手，而是沿石阶爬向灯塔。\n',
    '# 第二章 归岸\n\n小满把油灯举进灯塔的玻璃罩，火光在雾里旋开。半个时辰后，渡船擦着石堤靠岸。'
    '父亲先摸了摸她烧黑的袖口，才接过缆绳。她说以后值夜要备两根灯芯。'
    '天亮时，两个人把新灯芯收进防水盒；母亲留下的那根线已经烧完了。\n',
)
SCREEN_BODIES = (
    '# SC001 外景 渡口 夜\n\n雾压在水面。小满冲到石堤边，只看见一条绷紧的空缆绳。'
    '灯塔不亮。她拧开旧油灯，抽出湿灯芯，停了停，拆下袖口的棉线。\n'
    '小满：再等我一下。\n她捧着火苗跑上台阶。\n',
    '# SC002 内景 灯塔 夜\n\n小满把油灯推进玻璃罩。光穿过浓雾。窗外传来船壳擦过石堤的声音。'
    '父亲推门进来，握住她烧破的袖口。\n父亲：这回轮到我跟着你的灯走了。\n'
    '小满把两根新灯芯放进铁盒，合上盖。\n',
)


class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'project'

    def tearDown(self):
        self.temp.cleanup()

    def write(self, relative, text):
        path = wp.inside(self.root, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def command(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = wp.main(list(args))
        return code, output.getvalue()

    def healthy(self, kind='novel', reviewed=True):
        state = wp.init_project(self.root, kind, '短篇小说' if kind == 'novel' else 'film', 2, '借灯')
        if kind == 'novel':
            files = {
                'story-bible.md': '# 借灯\n小满要让渡船归岸，父亲从保护者变为接受女儿帮助的人。故事发生在同一夜的渡口与灯塔。\n<!-- ledger-check: questions=none; reason=本短篇的主疑问是渡船能否归岸，已在第二章明确回答，未保留悬念 -->\n',
                'volume-outline.md': '# 全篇大纲\n第一章：小满发现灯塔熄灭，以袖口棉线点灯。第二章：她登塔引航，父亲归岸，二人补足备用灯芯。\n',
                'ledger/character-sheet.md': '# 人物\n小满原以为自己只能等待救援；她用母亲留下的缝线点灯，承担了一次不可逆的损失。父亲接受她的照顾。\n',
                'ledger/world-rules.md': '# 规则\n这是写实渡口；油灯要有干燥灯芯才能持续燃烧。灯塔只能指示航道，不能平息风浪。\n',
                'ledger/foreshadowing-ledger.md': '# 伏笔\n| 伏笔ID | 内容 | 类型 | 周期 | 埋设章节 | 发酵记录 | 预计回收章节 | 重要性 | 状态 |\n|---|---|---|---|---|---|---|---|---|\n| F-001 | 袖口棉线来自母亲 | 道具 | 短期 | 第1章 | 第1章 | 第2章 | 关键 | 已回收 |\n',
                'ledger/power-ledger.md': '# 适用性\n<!-- ledger-check: power=not-applicable; reason=本作品为写实亲情故事，无分级战力体系 -->\n',
                'ledger/outline-changelog.md': '# 计划变化\n<!-- ledger-check: outline=none; reason=本轮两章按定稿大纲完成，没有偏离原计划 -->\n',
                'ledger/chapter-progress.md': '# 进度\n| 章 | 日期 | 字数 | 本章事件 | 章末钩子类型 | 情绪强度 1–10 | 伏笔动作 | 台账更新 ✓ | 备注 |\n|---|---|---|---|---|---|---|---|---|\n| 1 | 2026-09-26 | 110 | 小满以棉线点灯 | 行动未完 | 7 | 埋F-001 | ✓ | 已核对 |\n| 2 | 2026-09-26 | 105 | 渡船归岸，父女备灯芯 | 余韵 | 4 | 收F-001 | ✓ | 已核对 |\n',
            }
            bodies = NOVEL_BODIES
        else:
            files = {
                'screenplay-bible.md': '# 借灯\nproject_id: lamp-film\ntitle: 借灯\nmedium: film\nstructure: standalone\ndeliverable_scope: 两场完整短片剧本\nformat_contract: 中文场号、内外景、地点、时间、动作与具名对白\ncanonical_constraints: 一个夜晚，渡口和灯塔两个空间，没有超自然救援。\nending_contract: 父亲归岸，小满的主动选择得到回应。\n',
                'scene-list.md': '# 场景清单\n| scene_id | episode_id | setting | time | participants | goal | obstacle | action_turn | exit_state | duration_estimate | status | draft_path |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n| SC001 | N/A | 渡口 | 夜 | 小满 | 点灯 | 灯芯潮湿 | 拆袖口棉线 | 举灯登塔 | 1分钟 | drafted | manuscript/SC001.md |\n| SC002 | N/A | 灯塔 | 夜 | 小满、父亲 | 引航 | 浓雾 | 灯亮船归 | 两人备灯芯 | 1分钟 | drafted | manuscript/SC002.md |\n',
                'episode-outline.md': '# 分集适用性\nN/A: standalone：独立短片，不属于分集作品。SC001 是行动建立，SC002 完成主冲突与关系转变。\n',
            }
            bodies = SCREEN_BODIES
        files['session-handoff.md'] = '# 交接\n本轮两单元均已成稿，时间线停在黎明。小满烧掉了袖口棉线，父亲平安归岸。下一步全篇核读代价是否成立。没有新增未处置承诺。\n'
        ending = {'ending_note': '灯火带来归航；母亲的线被消耗，父女以备灯芯承接这次选择。', 'promises': [
            {'id': key, 'promise': promise, 'disposition': 'resolved', 'units': [state['units'][1]['id']], 'reason': reason}
            for key, promise, reason in (
                ('main-conflict', '渡船是否归岸', '正文明确写船靠岸、父亲出现'),
                ('protagonist-arc', '小满是否从等待转为行动', '她付出棉线的代价并主动登塔'),
                ('aftermath', '危机之后二人如何生活', '二人补足备用灯芯，改变以后值夜的做法'))]}
        files['ending.json'] = json.dumps(ending, ensure_ascii=False, indent=2)
        for relative, text in files.items():
            self.write(relative, text)
        for unit, body in zip(state['units'], bodies):
            self.write(unit['file'], body)
            unit['status'] = 'revised'
            unit['summary'] = '小满发现熄灯并决定付出代价' if unit['sequence'] == 1 else '灯亮引船归岸，父女关系发生改变'
        state['stage'] = 'revising'
        state['checkpoint'] = {**wp.snapshot(self.root, state), 'at': wp.now()}
        wp.save_state(self.root, state)
        if reviewed:
            self.add_reviews(state)
        return wp.load_state(self.root)

    def add_reviews(self, state):
        self.write('reviews/reader.md', '# 测试夹具的具名评阅\n第一单元把困难压缩在湿灯芯上，袖口棉线是可见代价；第二单元父亲的动作回应了小满的选择。场景时间连续，终局三项在第二单元落地。此评阅只用于测试记录流程，不声称经过真实出版评审。\n')
        for scope in [u['id'] for u in state['units']] + ['final']:
            wp.record_review(self.root, state, scope, '测试夹具辅助评阅', 'reviews/reader.md', 'pass', 'assisted')
        wp.save_state(self.root, state)

    def test_empty_project_cannot_complete(self):
        wp.init_project(self.root, 'novel', '短篇小说', 2, '空项目')
        code, _ = self.command('check', str(self.root), '--final')
        self.assertNotEqual(code, 0)
        code, _ = self.command('complete', str(self.root))
        self.assertNotEqual(code, 0)
        self.assertIsNone(wp.load_state(self.root)['completion'])

    def test_complete_micro_novel_and_verify(self):
        self.healthy()
        code, output = self.command('complete', str(self.root))
        self.assertEqual(code, 0, output)
        code, output = self.command('check', str(self.root), '--final')
        self.assertEqual(code, 0, output)

    def test_complete_micro_screenplay_and_verify(self):
        self.healthy('screenplay')
        code, output = self.command('complete', str(self.root))
        self.assertEqual(code, 0, output)
        self.assertEqual(wp.load_state(self.root)['stage'], 'complete')

    def test_body_edit_invalidates_checkpoint_reviews_and_completion(self):
        self.healthy()
        self.assertEqual(self.command('complete', str(self.root))[0], 0)
        self.write('manuscript/CH002.md', NOVEL_BODIES[1] + '\n父亲又说了一句话。\n')
        code, output = self.command('check', str(self.root), '--final')
        self.assertEqual(code, 1, output)
        self.assertIn('旧', output)
        self.assertIn('评阅过期', output)

    def test_ledger_only_edit_invalidates_completion(self):
        self.healthy()
        self.assertEqual(self.command('complete', str(self.root))[0], 0)
        path = self.root / 'ledger/world-rules.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n雾在黎明后逐渐消散。\n', encoding='utf-8')
        code, output = self.command('check', str(self.root), '--final')
        self.assertEqual(code, 1, output)
        self.assertIn('评阅过期', output)

    def test_missing_or_unreviewed_unit_fails(self):
        state = self.healthy(reviewed=False)
        self.assertEqual(wp.inspect_project(self.root, state, final=True)['exit_code'], 1)
        (self.root / 'manuscript/CH002.md').unlink()
        report = wp.inspect_project(self.root, state, final=True)
        self.assertTrue(any('正文文件缺失' in e for e in report['errors']))

    def test_pause_resume_and_reopen_preserve_prose(self):
        self.healthy()
        before = (self.root / 'manuscript/CH001.md').read_bytes()
        self.assertEqual(self.command('pause', str(self.root), '--next', '核读父亲对白')[0], 0)
        self.assertEqual(wp.load_state(self.root)['stage'], 'paused')
        self.assertEqual(self.command('resume', str(self.root), '--next', '先读交接单再核读对白')[0], 0)
        self.assertEqual(self.command('complete', str(self.root))[0], 0)
        self.assertEqual(self.command('reopen', str(self.root), '--next', '修订结尾余韵')[0], 0)
        state = wp.load_state(self.root)
        self.assertIsNone(state['completion'])
        self.assertNotIn('final', state['reviews'])
        self.assertIn('CH001', state['reviews'])
        self.assertEqual(before, (self.root / 'manuscript/CH001.md').read_bytes())
        self.assertNotEqual(self.command('complete', str(self.root))[0], 0)

    def test_reopen_requires_completed_project(self):
        state = self.healthy()
        before = state.copy()
        code, output = self.command('reopen', str(self.root), '--next', '误重开')
        self.assertEqual(code, 2, output)
        self.assertIn('尚未登记完结', output)
        self.assertEqual(wp.load_state(self.root)['stage'], before['stage'])
        self.assertEqual(self.command('pause', str(self.root), '--next', '暂停核读')[0], 0)
        code, output = self.command('reopen', str(self.root), '--next', '暂停下误重开')
        self.assertEqual(code, 2, output)
        self.assertEqual(wp.load_state(self.root)['stage'], 'paused')

    def test_gbk_support_file_is_decoded(self):
        """项目文件被存成 GBK 时，读取应返回正文，而不是抛编码错误。"""
        wp.init_project(self.root, 'novel', '短篇小说', 2, '借灯')
        path = wp.inside(self.root, 'story-bible.md')
        path.write_bytes('小满要在天亮前点亮灯塔。'.encode('gbk'))
        self.assertEqual(wp.read_text(self.root, 'story-bible.md'), '小满要在天亮前点亮灯塔。')

    def test_init_never_overwrites_existing_content(self):
        self.root.mkdir()
        self.write('keep.md', '用户的既有文稿')
        with self.assertRaises(wp.ProjectError):
            wp.init_project(self.root, 'novel', 'novel', 1, '误覆盖')
        self.assertEqual((self.root / 'keep.md').read_text(encoding='utf-8'), '用户的既有文稿')

    def test_path_traversal_absolute_and_drive_paths_rejected(self):
        for path in ('../outside.md', '/outside.md', 'C:/outside.md', 'ledger/../../outside.md', 'x:stream', 'a\\b.md'):
            with self.subTest(path=path), self.assertRaises(wp.ProjectError):
                wp.inside(self.root, path)

    def test_duplicate_and_unregistered_manuscripts_rejected(self):
        state = self.healthy('screenplay')
        self.write('manuscript/SC999.md', '她站在河边。')
        report = wp.inspect_project(self.root, state, final=True)
        self.assertTrue(any('未纳入计划' in e for e in report['errors']))
        state['units'][1]['file'] = state['units'][0]['file']
        with self.assertRaises(wp.ProjectError):
            wp.validate_state(self.root, state)

    def test_scope_shortening_requires_record_and_retains_removed_prose(self):
        state = self.healthy()
        bad = json.loads(json.dumps(state))
        bad['project']['target_units'] = 1
        bad['units'] = bad['units'][:1]
        with self.assertRaises(wp.ProjectError):
            wp.validate_state(self.root, bad)
        code, output = self.command('resize', str(self.root), '--units', '1', '--reason', '把两章合为一章，需重写并重做终局映射')
        self.assertEqual(code, 0, output)
        self.assertTrue((self.root / 'manuscript/CH002.md').exists())
        self.assertEqual(len(wp.load_state(self.root)['scope_changes']), 1)
        self.assertNotEqual(self.command('complete', str(self.root))[0], 0)
        self.assertEqual(self.command('resize', str(self.root), '--units', '2', '--reason', '复核后恢复独立第二章')[0], 0)
        self.assertEqual(len(wp.load_state(self.root)['units']), 2)

    def test_open_ending_cannot_hide_unresolved_main_conflict(self):
        state = self.healthy('screenplay')
        ending = wp.read_json(self.root, 'ending.json')
        ending['promises'][0]['disposition'] = 'intentional-open'
        self.write('ending.json', json.dumps(ending, ensure_ascii=False))
        self.assertTrue(any('核心收尾' in e for e in wp.ending_errors(self.root, state)))

    def test_review_evidence_edit_invalidates_review(self):
        state = self.healthy('screenplay')
        self.write('reviews/reader.md', '改成另一份评阅后需要重新登记。')
        report = wp.inspect_project(self.root, state, final=True)
        self.assertTrue(any('评阅证据为空或已改变' in e for e in report['errors']))

    def test_assisted_final_completes_with_honest_completion_level(self):
        self.healthy('screenplay')
        code, output = self.command('complete', str(self.root))
        self.assertEqual(code, 0, output)
        self.assertIn('未经过独立人工评阅', output)
        completion = wp.load_state(self.root)['completion']
        self.assertEqual(completion['review_source'], 'assisted')
        self.assertEqual(completion['completion_level'], 'assisted_draft_complete')

    def test_human_source_record_interface_only(self):
        state = self.healthy('screenplay')
        wp.record_review(self.root, state, 'final', '接口字段样例（非真实人工验收）',
                         'reviews/reader.md', 'pass', 'human')
        self.assertEqual(state['reviews']['final']['source'], 'human')

    def test_episode_requires_each_scene_body(self):
        state = wp.init_project(self.root, 'screenplay', 'screen_series', 1, '借灯第一集', 'episode')
        unit = state['units'][0]
        unit['scenes'] = [
            {'id': 'E01-S01', 'summary': '点灯', 'marker': '# E01-S01'},
            {'id': 'E01-S02', 'summary': '引航归岸', 'marker': '# E01-S02'}]
        self.write('scene-list.md', '# 场景\n| scene_id | episode_id | setting | time | participants | goal | obstacle | action_turn | exit_state | duration_estimate | status | draft_path |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n| E01-S01 | EP001 | 渡口 | 夜 | 小满 | 点灯 | 湿灯芯 | 拆袖口线 | 火亮 | 1分钟 | drafted | manuscript/EP001.md |\n| E01-S02 | EP001 | 灯塔 | 夜 | 小满、父亲 | 引航 | 雾 | 归岸 | 备灯芯 | 1分钟 | drafted | manuscript/EP001.md |\n')
        self.write('episode-outline.md', '# 分集\n| episode_id | local_goal | entry_state | A_B_threads | turns | local_payoff | season_delta | hook_payoff_link | estimated_duration | scene_ids | status |\n|---|---|---|---|---|---|---|---|---|---|---|\n| EP001 | 归岸 | 失联 | 点灯与成长 | 自主引航 | 船归 | 父女互信 | 本集闭合 | 2分钟 | E01-S01,E01-S02 | drafted |\n')
        self.write(unit['file'], '# E01-S01\n她把线捻成灯芯，划亮火柴。\n# E01-S02\n')
        errors = wp.screenplay_errors(self.root, state, final=True)
        self.assertTrue(any('只有场标' in e for e in errors))
        for editorial_text in (
                '<!-- 下一场使用 # E01-S02，待写归航 -->',
                '> 提示：下一场使用 # E01-S02',
                '本场的道具上写着“# E01-S02”。',
                '<!--\n# E01-S02\n这只是注释中的假正文。\n-->'):
            self.write(unit['file'], '# E01-S01\n她点亮灯芯。\n' + editorial_text + '\n# E01-S02\n')
            errors = wp.screenplay_errors(self.root, state, final=True)
            self.assertTrue(any('E01-S02 只有场标' in e for e in errors), (editorial_text, errors))
        self.write(unit['file'], '# E01-S01\n她点亮灯芯。\n~~~markdown\n# E01-S02\n这是示例，不是第二场正文。\n~~~\n')
        errors = wp.screenplay_errors(self.root, state, final=True)
        self.assertTrue(any('独立场标行' in e for e in errors), errors)
        self.write(unit['file'], '# E01-S01\n她点亮灯芯。\n# E01-S02\n~~~markdown\n这只是正文位置里的代码示例。\n~~~\n')
        self.assertTrue(any('E01-S02 只有场标' in e for e in wp.screenplay_errors(self.root, state, final=True)))
        self.write(unit['file'], '# E01-S01\n她把线捻成灯芯，划亮火柴。\n# E01-S02\n渡船归岸，父亲扶住门框看着她。\n')
        self.assertEqual(wp.screenplay_errors(self.root, state, final=True), [])
        episode_table = wp.read_text(self.root, 'episode-outline.md')
        for prefix, suffix in (('~~~markdown\n', '\n~~~'), ('<!--\n', '\n-->')):
            self.write('episode-outline.md', prefix + episode_table + suffix)
            with self.assertRaises(wp.ProjectError):
                wp.screenplay_errors(self.root, state, final=True)
        self.write('episode-outline.md', episode_table)
        self.assertEqual(wp.screenplay_errors(self.root, state, final=True), [])

    def test_manuscript_placeholder_is_not_content(self):
        for value in ('', '# 第一章\n', '<正文>', 'TODO', '待填写', '...',
                      '~~~markdown\n这一段是代码围栏中的示例。\n~~~',
                      '<!--\n注释中的说明也不是正文。\n-->'):
            self.assertFalse(wp.has_content(value), value)
        self.assertTrue(wp.has_content('她合上灯罩，火光映亮了父亲的脸。'))

    def test_next_chapter_and_handoff_preserve_unchanged_unit_review(self):
        state = wp.init_project(self.root, 'novel', '短篇小说', 2, '逐章测试')
        unit = state['units'][0]
        unit['summary'] = '小满决定点灯引航'
        unit['status'] = 'drafted'
        self.write(unit['file'], NOVEL_BODIES[0])
        self.write('reviews/ch1.md', '第一章的小满付出了袖口棉线，行动因果明确；核读了她点灯登塔的完整段落。')
        state['checkpoint'] = wp.snapshot(self.root, state)
        wp.record_review(self.root, state, unit['id'], '辅助评阅夹具', 'reviews/ch1.md', 'pass', 'assisted')
        state['units'][1]['summary'] = '船归岸，父女备灯芯'
        state['units'][1]['status'] = 'drafted'
        self.write(state['units'][1]['file'], NOVEL_BODIES[1])
        self.write('ledger/chapter-progress.md', '第一章点灯、第二章引航与归岸，已同步进度。')
        self.write('session-handoff.md', '第二章成稿，父亲已经归岸，下一步核读结尾。')
        state['checkpoint'] = wp.snapshot(self.root, state)
        self.assertEqual(wp.review_errors(self.root, state, unit['id'], wp.snapshot(self.root, state)), [])
        self.write(unit['file'], NOVEL_BODIES[0] + '她又拿出了一根备用灯芯。')
        self.assertTrue(any('评阅过期' in e for e in wp.review_errors(self.root, state, unit['id'], wp.snapshot(self.root, state))))

    def test_explicit_dependency_edit_invalidates_only_dependent_unit(self):
        state = self.healthy('screenplay', reviewed=False)
        state['units'][0]['depends_on'] = ['screenplay-bible.md']
        state['checkpoint'] = wp.snapshot(self.root, state)
        self.add_reviews(state)
        self.write('screenplay-bible.md', wp.read_text(self.root, 'screenplay-bible.md') + '\n故事时间改为清晨。')
        snap = wp.snapshot(self.root, state)
        self.assertTrue(wp.review_errors(self.root, state, 'SC001', snap))
        self.assertEqual(wp.review_errors(self.root, state, 'SC002', snap), [])
        self.assertTrue(wp.review_errors(self.root, state, 'final', snap))

    def test_scene_id_in_instructions_is_not_a_scene_record(self):
        state = self.healthy('screenplay', reviewed=False)
        self.write('scene-list.md', '# 说明\nSC001 和 SC002 是示例 ID，不是已写的场景表。')
        with self.assertRaises(wp.ProjectError):
            wp.screenplay_errors(self.root, state, final=True)

    def test_project_ledger_thresholds_persist_and_expire_final_review(self):
        state = self.healthy(reviewed=False)
        state['project']['ledger_thresholds'] = {'short_gap': 20, 'curve_window': 3}
        state['checkpoint'] = wp.snapshot(self.root, state)
        self.add_reviews(state)
        report = wp.inspect_project(self.root, state, final=True)
        self.assertEqual(report['exit_code'], 0, report)
        self.assertEqual(wp.load_state(self.root)['project']['ledger_thresholds']['short_gap'], 20)
        state['project']['ledger_thresholds']['short_gap'] = 25
        snap = wp.snapshot(self.root, state)
        self.assertTrue(wp.review_errors(self.root, state, 'final', snap))
        self.assertEqual(wp.review_errors(self.root, state, 'CH001', snap), [])
        state['project']['ledger_thresholds']['unknown_window'] = 4
        self.assertEqual(wp.inspect_project(self.root, state, final=True)['exit_code'], 2)

    def test_cli_help_is_utf8_even_under_legacy_output_setting(self):
        environment = dict(os.environ)
        environment['PYTHONIOENCODING'] = 'cp1252'
        result = subprocess.run([sys.executable, '-B', str(Path(wp.__file__)), '--help'],
                                capture_output=True, env=environment, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = result.stdout.decode('utf-8')
        self.assertIn('可续写的小说/剧本项目记录器', output)

    def test_progress_requires_all_written_chapters_not_only_latest_or_future(self):
        state = self.healthy(reviewed=False)
        for rows, message in (('| 2 | 4 |\n', '漏记'), ('| 3 | 5 |\n', '范围外')):
            with self.subTest(rows=rows):
                self.write('ledger/chapter-progress.md', '| 章 | 情绪强度 |\n|---|---|\n' + rows)
                for final in (False, True):
                    errors = wp.novel_progress_errors(self.root, state, final=final)
                    self.assertTrue(any(message in value for value in errors), errors)
                state['checkpoint'] = wp.snapshot(self.root, state)
                wp.save_state(self.root, state)
                code, output = self.command('check', str(self.root), '--final')
                self.assertNotEqual(code, 0, output)
                code, output = self.command('complete', str(self.root))
                self.assertNotEqual(code, 0, output)
                self.assertNotEqual(wp.load_state(self.root)['stage'], 'complete')
        self.write('ledger/chapter-progress.md', '| 章 | 情绪强度 |\n|---|---|\n| 1 | 7 |\n| 2 | 4 |\n')
        self.assertEqual(wp.novel_progress_errors(self.root, state, final=True), [])

    def test_progress_current_checks_written_subset_without_inventing_future_completion(self):
        state = self.healthy(reviewed=False)
        state['units'][1]['status'] = 'planned'
        self.write(state['units'][1]['file'], '# 第二章\n')
        self.write('ledger/chapter-progress.md', '| 章 | 情绪强度 |\n|---|---|\n| 1 | 7 |\n')
        self.assertEqual(wp.novel_progress_errors(self.root, state, final=False), [])
        self.assertTrue(wp.novel_progress_errors(self.root, state, final=True))

    def test_template_placeholder_rows_are_not_completion_records(self):
        state = wp.init_project(self.root, 'novel', '短篇小说', 2, '借灯')
        self.write('ledger/chapter-progress.md',
                   '| 章 | 日期 | 字数 | 本章事件 | 章末钩子类型 | 情绪强度 1–10 | 伏笔动作 | 台账更新 ✓ | 备注 |\n'
                   '|---|---|---|---|---|---|---|---|---|\n'
                   '| 1 |  |  |  |  |  |  |  |  |\n'
                   '| 2 |  |  |  |  |  |  |  |  |\n')
        self.assertEqual(wp.novel_progress_errors(self.root, state, final=False), [])
        errors = wp.novel_progress_errors(self.root, state, final=True)
        self.assertTrue(any('漏记' in value for value in errors), errors)
        self.assertFalse(any('记为完成' in value for value in errors), errors)

    def test_fenced_or_commented_scene_tables_are_not_canonical_records(self):
        state = self.healthy('screenplay', reviewed=False)
        table = wp.read_text(self.root, 'scene-list.md')
        for prefix, suffix in (('```markdown\n', '\n```'),
                               ('~~~~markdown\n', '\n~~~~'), ('<!--\n', '\n-->')):
            with self.subTest(prefix=prefix):
                self.write('scene-list.md', prefix + table + suffix)
                with self.assertRaises(wp.ProjectError):
                    wp.screenplay_errors(self.root, state, final=True)
                self.assertNotEqual(self.command('complete', str(self.root))[0], 0)
        self.write('scene-list.md', '~~~markdown\n' + table + '\n~~~\n\n' + table)
        self.assertEqual(wp.screenplay_errors(self.root, state, final=True), [])

    def test_unframed_table_rows_are_parsed_including_unplanned_extra_scene(self):
        state = self.healthy('screenplay', reviewed=False)
        table = wp.read_text(self.root, 'scene-list.md')
        unframed = '\n'.join(line.strip('|') if '|' in line else line for line in table.splitlines()) + '\n'
        self.write('scene-list.md', unframed)
        self.assertEqual(wp.screenplay_errors(self.root, state, final=True), [])
        self.write('scene-list.md', table + 'SC003 | N/A | 河岸 | 晨 | 小满 | 告别 | 涨潮 | 解缆 | 离岸 | 1分钟 | planned | manuscript/SC003.md\n')
        errors = wp.screenplay_errors(self.root, state, final=True)
        self.assertTrue(any('SC003 未列入' in value for value in errors), errors)
        self.assertNotEqual(self.command('complete', str(self.root))[0], 0)

    def test_malformed_checkpoint_returns_controlled_input_error(self):
        state = self.healthy(reviewed=False)
        state['checkpoint'] = 'pending'
        wp.save_state(self.root, state)
        code, output = self.command('review', str(self.root), '--scope', 'CH001',
                                    '--reviewer', '辅助评阅', '--source', 'assisted',
                                    '--evidence', 'reviews/reader.md', '--verdict', 'pass')
        self.assertEqual(code, 2, output)
        self.assertIn('checkpoint 必须是对象', output)


if __name__ == '__main__':
    unittest.main()
