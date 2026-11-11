"""Regression checks for ledger parsing, time semantics and completion gates.
Run: python -B -m unittest discover -s tests -p test_ledger_check.py -v
"""
import importlib.util
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'ledger_check.py'
spec = importlib.util.spec_from_file_location('ledger_check', SCRIPT)
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)
F_HEADERS = ['伏笔ID', '内容', '类型', '周期', '埋设章节', '发酵记录', '预计回收章节', '重要性', '状态']


def table(headers, rows):
    return '| ' + ' | '.join(headers) + ' |\n|' + '|'.join(['---'] * len(headers)) + '|\n' + ''.join(
        '| ' + ' | '.join(map(str, row)) + ' |\n' for row in rows)


def frow(fid='F-1', cycle='短期', plant='第1章', ferment='无', plan='第50章', state='未发酵'):
    return [fid, '信物', '道具', cycle, plant, ferment, plan, '★', state]


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'ledger').mkdir()
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow()]))
        self.write('ledger/power-ledger.md', '<!-- ledger-check: power=not-applicable; reason=本作无分级战力体系 -->\n')
        self.write('ledger/outline-changelog.md', '<!-- ledger-check: outline=none; reason=截至当前章未偏离批准大纲 -->\n')
        self.write('story-bible.md', '<!-- ledger-check: questions=none; reason=正文当前没有悬而未答的问题 -->\n')
        self.progress([17, 18, 19, 20], [4, 6, 5, 7])

    def tearDown(self):
        self.temp.cleanup()

    def write(self, relative, content):
        with (self.root / relative).open('w', encoding='utf-8', newline='\n') as handle:
            handle.write(content)

    def progress(self, chapters, scores):
        self.write('ledger/chapter-progress.md', table(['章', '情绪强度 1–10'], list(zip(chapters, scores))))

    def run_check(self, **kwargs):
        values = {'cur_ch': 20, 'cur_vol': 3}
        values.update(kwargs)
        return ledger.run_checks(str(self.root), **values)

    def assert_code(self, entries, code):
        self.assertTrue(any(f'[{code}]' in item for item in entries), entries)

    def assert_no_code(self, entries, code):
        self.assertFalse(any(f'[{code}]' in item for item in entries), entries)

    def test_known_good_inputs_pass(self):
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 0, rep.warn + rep.red)
        self.assertTrue(rep.complete)

    def test_gbk_ledger_is_decoded(self):
        """Windows 记事本常存 GBK；台账读取不得因编码被判成不可用。"""
        with (self.root / 'ledger' / 'foreshadowing-ledger.md').open('wb') as handle:
            handle.write(table(F_HEADERS, [frow()]).encode('gbk'))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 0, rep.warn + rep.red)
        self.assertTrue(rep.complete)

    def test_only_future_progress_cannot_pass_final(self):
        self.progress([21, 22], [4, 6])
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(state='已回收')]))
        rep = self.run_check(final=True)
        self.assert_code(rep.warn, 'C-NO-COMPLETED')
        self.assertFalse(rep.complete)
        self.assertEqual(rep.exit_code, 2)
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(self.root),
                                 '--current-chapter', '20', '--current-volume', '3', '--final'],
                                capture_output=True, text=True, encoding='utf-8', errors='replace')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_current_pending_progress_is_incomplete(self):
        self.write('ledger/chapter-progress.md', table(['章', '情绪强度', '状态'], [[20, 5, '待写']]))
        rep = self.run_check()
        self.assert_code(rep.warn, 'C-NOT-WRITTEN')
        self.assert_code(rep.warn, 'C-NO-COMPLETED')
        self.assertEqual(rep.exit_code, 2)

    def test_explicit_plan_wins_over_short_age(self):
        rep = self.run_check()
        self.assert_no_code(rep.yellow, 'F-OVERDUE')

    def test_long_term_explicit_plan_can_be_overdue(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(cycle='长期', plan='第10章')]))
        rep = self.run_check()
        self.assert_code(rep.yellow, 'F-OVERDUE')
        self.assert_code(rep.red, 'F-RATIO')

    def test_deadline_is_strictly_after_due_chapter(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(plan='第20章')]))
        self.assert_no_code(self.run_check().yellow, 'F-OVERDUE')

    def test_deadline_range_uses_upper_bound(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(plan='第10–20章')]))
        self.assert_no_code(self.run_check().yellow, 'F-OVERDUE')
        self.assertEqual(ledger.parse_deadline('第20章至第30章'), 30)
        self.assertIsNone(ledger.parse_deadline('第30–20章'))

    def test_missing_plan_uses_configurable_fallback(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(plan='')]))
        self.assert_code(self.run_check().yellow, 'F-OVERDUE')
        rep = self.run_check(thresholds={'short_gap': 30})
        self.assert_no_code(rep.yellow, 'F-OVERDUE')
        self.assert_code(rep.yellow, 'F-NO-PLAN')

    def test_mid_deadline_and_wakeup_are_independent(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(cycle='中期', plan='')]))
        self.progress([57, 58, 59, 60], [4, 6, 5, 7])
        rep = self.run_check(cur_ch=60)
        self.assert_code(rep.yellow, 'F-OVERDUE')
        self.assert_no_code(rep.yellow, 'F-FERMENT')
        rep = self.run_check(cur_ch=60, thresholds={'mid_wake_gap': 40})
        self.assert_code(rep.yellow, 'F-FERMENT')

    def test_wakeup_does_not_erase_overdue(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(cycle='长期', ferment='第19章', plan='第10章')]))
        rep = self.run_check()
        self.assert_code(rep.yellow, 'F-OVERDUE')
        self.assert_no_code(rep.yellow, 'F-FERMENT')

    def test_plan_does_not_erase_wakeup(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(cycle='长期', plan='第200章')]))
        self.progress([57, 58, 59, 60], [4, 6, 5, 7])
        rep = self.run_check(cur_ch=60)
        self.assert_code(rep.yellow, 'F-FERMENT')
        self.assert_no_code(rep.yellow, 'F-OVERDUE')

    def test_future_ferment_cannot_mask_stale(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(cycle='长期', ferment='第100章', plan='第200章')]))
        self.progress([57, 58, 59, 60], [4, 6, 5, 7])
        rep = self.run_check(cur_ch=60)
        self.assertEqual(rep.exit_code, 2)
        self.assert_code(rep.warn, 'F-FERMENT-TIME')
        self.assert_code(rep.yellow, 'F-FERMENT')

    def test_future_and_unplanted_do_not_dilute_ratio(self):
        rows = [frow(plan='第10章')] + [frow(f'F-{i}', plant='第40章', plan='第50章', state='计划中') for i in range(2, 12)]
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, rows))
        rep = self.run_check()
        self.assertTrue(any('1/1' in item for item in rep.red), rep.red)
        self.assertEqual(sum('[F-OVERDUE]' in item for item in rep.yellow), 1)

    def test_unplanted_past_plan_not_counted_as_planted(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(plan='第10章', state='未埋设')]))
        rep = self.run_check()
        self.assert_code(rep.yellow, 'F-NOT-ACTIVE')
        self.assert_no_code(rep.yellow, 'F-OVERDUE')

    def test_power_lag_severity_is_per_row(self):
        self.write('ledger/power-ledger.md', table(['角色名', '上次更新卷'], [['严重', '第1卷'], ['轻微', '第2卷'], ['同步', '第3卷']]))
        rep = self.run_check()
        self.assertTrue(any('严重' in item for item in rep.red))
        self.assertFalse(any('轻微' in item for item in rep.red))
        self.assertTrue(any('轻微' in item for item in rep.yellow))

    def test_power_row_order_does_not_change_severity(self):
        findings = []
        for rows in [[['A', '第1卷'], ['B', '第2卷']], [['B', '第2卷'], ['A', '第1卷']]]:
            self.write('ledger/power-ledger.md', table(['角色名', '上次更新卷'], rows))
            rep = self.run_check()
            findings.append((sorted(rep.red), sorted(rep.yellow)))
        self.assertEqual(*findings)

    def test_future_power_update_is_incomplete(self):
        self.write('ledger/power-ledger.md', table(['角色名', '上次更新卷'], [['甲', '第4卷']]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 2)
        self.assert_code(rep.warn, 'P-FUTURE')
        self.assert_no_code(rep.ok, 'P-LEDGER')

    def test_future_or_inactive_power_rows_excluded(self):
        self.write('ledger/power-ledger.md', table(['角色名', '上次更新卷', '生效卷', '适用状态'],
                   [['已退场', '第1卷', '第1卷', '退场'], ['下卷登场', '', '第4卷', '未登场'], ['当前', '第3卷', '第1卷', '适用']]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 0, rep.warn + rep.red)
        self.assert_no_code(rep.red + rep.yellow, 'P-STALE')

    def test_na_declaration_conflicting_with_data_is_not_green(self):
        self.write('ledger/power-ledger.md', '<!-- ledger-check: power=not-applicable; reason=无战力体系 -->\n' +
                   table(['角色名', '上次更新卷'], [['甲', '第3卷']]))
        self.assertEqual(self.run_check().exit_code, 2)

    def test_missing_files_missing_columns_empty_and_malformed_are_incomplete(self):
        cases = [None, '| 状态 |\n|---|\n| 已回收 |\n', table(F_HEADERS, []),
                 table(F_HEADERS, [[''] * 9]), table(F_HEADERS, [frow()[:-1]]),
                 table(F_HEADERS, [frow() + ['多列']]), table(F_HEADERS, [frow(plant='第X章')]),
                 table(F_HEADERS, [frow(state='')]), table(F_HEADERS, [frow(plan='第X章')])]
        for content in cases:
            with self.subTest(content=content):
                target = self.root / 'ledger' / 'foreshadowing-ledger.md'
                if content is None:
                    target.unlink(missing_ok=True)
                else:
                    self.write('ledger/foreshadowing-ledger.md', content)
                rep = self.run_check()
                self.assertEqual(rep.exit_code, 2, rep.red + rep.warn)
                self.assert_no_code(rep.ok, 'F-LEDGER')

    def test_wrong_column_position_is_supported(self):
        headers = [F_HEADERS[-1]] + F_HEADERS[:-1]
        row = [frow()[-1]] + frow()[:-1]
        self.write('ledger/foreshadowing-ledger.md', table(headers, [row]))
        self.assertEqual(self.run_check().exit_code, 0)

    def test_duplicates_and_ambiguous_tables_fail(self):
        for content in [table(F_HEADERS, [frow(), frow()]), table(F_HEADERS, [frow()]) * 2,
                        table(F_HEADERS + ['状态'], [frow() + ['未发酵']])]:
            self.write('ledger/foreshadowing-ledger.md', content)
            self.assertEqual(self.run_check().exit_code, 2)

    def test_escaped_pipe_in_content_is_preserved(self):
        row = frow()
        row[1] = r'信物\|钥匙'
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [row]))
        self.assertEqual(self.run_check().exit_code, 0)

    def test_fenced_examples_are_not_fact_tables(self):
        self.write('ledger/foreshadowing-ledger.md', '```markdown\n' + table(F_HEADERS, [frow(plan='第3章')]) + '```\n' + table(F_HEADERS, [frow()]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 0)
        self.assert_no_code(rep.yellow, 'F-OVERDUE')

    def test_nested_fence_markers_do_not_activate_examples(self):
        self.write('ledger/foreshadowing-ledger.md', '````markdown\n```\n' +
                   table(F_HEADERS, [frow(plan='第3章')]) + '```\n````\n' + table(F_HEADERS, [frow()]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 0)
        self.assert_no_code(rep.yellow, 'F-OVERDUE')

    def test_row_without_outer_pipes_is_not_silently_dropped(self):
        content = table(F_HEADERS, [frow()]) + ' | '.join(frow('F-2', plan='第3章')) + '\n'
        self.write('ledger/foreshadowing-ledger.md', content)
        rep = self.run_check()
        self.assertTrue(any('F-2' in item for item in rep.yellow), rep.yellow)

    def test_bad_encoding_is_reported_without_crash(self):
        (self.root / 'ledger' / 'foreshadowing-ledger.md').write_bytes(b'\xff\xfeBAD')
        self.assertEqual(self.run_check().exit_code, 2)

    def test_fenced_none_declaration_is_an_example_not_a_fact(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, []) +
                   '```markdown\n<!-- ledger-check: foreshadowing=none; reason=示例而非实际项目声明 -->\n```\n')
        self.assertEqual(self.run_check().exit_code, 2)

    def test_none_declaration_requires_concrete_reason(self):
        for text in ['<!-- ledger-check: foreshadowing=none -->',
                     '<!-- ledger-check: foreshadowing=none; reason=具体原因 -->']:
            self.write('ledger/foreshadowing-ledger.md', text + '\n')
            self.assertEqual(self.run_check().exit_code, 2)

    def test_final_cannot_silently_skip_missing_ledger(self):
        (self.root / 'ledger' / 'foreshadowing-ledger.md').unlink()
        rep = self.run_check(final=True)
        self.assertEqual(rep.exit_code, 2)
        self.assert_no_code(rep.ok, 'X-FINAL')

    def test_final_unresolved_and_future_entries_are_red(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(plant='第40章', state='计划中')]))
        rep = self.run_check(final=True)
        self.assert_code(rep.red, 'X-DANGLE')

    def test_final_sequel_and_discard_require_specific_disposition(self):
        for state in ['留续作', '已废弃', '已取消']:
            self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(state=state)]))
            self.assert_code(self.run_check(final=True).red, 'X-DISPOSITION')
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(state='留续作：外传解答来历，本书开锁承诺已在第18章兑现')]))
        self.assertEqual(self.run_check(final=True).exit_code, 0)

    def test_placeholder_disposition_is_not_completion(self):
        for state in ['留续作：待处理', '已废弃（待填）', '已取消：以后再说']:
            self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(state=state)]))
            self.assert_code(self.run_check(final=True).red, 'X-DISPOSITION')

    def test_actual_blank_templates_do_not_pass_final(self):
        templates = SCRIPT.parents[1] / 'templates'
        for filename in ['foreshadowing-ledger.md', 'power-ledger.md', 'outline-changelog.md', 'chapter-progress.md']:
            shutil.copyfile(templates / filename, self.root / 'ledger' / filename)
        shutil.copyfile(templates / 'story-bible.md', self.root / 'story-bible.md')
        rep = self.run_check(cur_ch=1, cur_vol=1, final=True)
        self.assertEqual(rep.exit_code, 2, rep.ok)
        self.assert_no_code(rep.ok, 'X-FINAL')

    def test_final_actual_closed_row_and_explicit_none_pass(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(state='已回收：第18章打开柜门')]))
        self.assertEqual(self.run_check(final=True).exit_code, 0)
        self.write('ledger/foreshadowing-ledger.md', '<!-- ledger-check: foreshadowing=none; reason=本作品没有设置需后续兑现的伏笔 -->\n')
        self.assertEqual(self.run_check(final=True).exit_code, 0)

    def test_final_disposition_column_supported_without_changing_old_schema(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS + ['处置说明'], [frow(state='已废弃') + ['已删去第1章暗示并检查后文依赖']]))
        self.assertEqual(self.run_check(final=True).exit_code, 0)

    def test_final_pending_questions_and_unsupported_omission_fail(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(state='已回收')]))
        self.write('story-bible.md', table(['疑问', '抛出章', '状态'], [['Q', '第1章', '延迟']]))
        self.assert_code(self.run_check(final=True).red, 'X-QUESTION')
        self.write('story-bible.md', table(['疑问', '抛出章', '状态'], [['Q', '第1章', '永不答']]))
        self.assert_code(self.run_check(final=True).red, 'X-QDISPOSITION')

    def test_future_questions_excluded_but_delay_is_pending(self):
        rows = [[f'Q{i}', '第1章', '延迟'] for i in range(6)] + [['未来', '第50章', '计划中']]
        self.write('story-bible.md', table(['疑问', '抛出章', '状态'], rows))
        rep = self.run_check()
        self.assert_code(rep.red, 'Q-HARD')
        self.assertEqual(sum('[Q-PEND]' in item for item in rep.yellow), 6)

    def test_outline_uses_max_actual_chapter_not_row_order(self):
        self.write('ledger/outline-changelog.md', table(['当前章数', '调整方向'], [['第19章', '改A'], ['第1章', '改B']]))
        rep = self.run_check()
        self.assertTrue(any('第19章' in item for item in rep.ok), rep.ok)

    def test_future_outline_record_is_not_current_evidence(self):
        self.write('ledger/outline-changelog.md', table(['当前章数', '调整方向'], [['第99章', '计划调整']]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 2)
        self.assert_code(rep.warn, 'O-FUTURE')

    def test_original_chapter_template_headers_are_supported(self):
        headers = ['章', '日期', '字数', '本章事件', '章末钩子类型', '情绪强度 1–10', '伏笔动作', '台账更新 ✓', '备注']
        rows = [[ch, '某日', '1000', '事件', '抉择', score, '无', '✓', ''] for ch, score in zip(range(17, 21), [4, 6, 5, 7])]
        self.write('ledger/chapter-progress.md', table(headers, rows))
        self.assertEqual(self.run_check().exit_code, 0)

    def test_chapter_aliases_work_beside_other_chapter_fields(self):
        for name in ['章', '章号', '章节', '章节号', '章节编号']:
            with self.subTest(header=name):
                headers = ['首次章', '预计回收章', '实际回收章', name,
                           '本章事件', '章末钩子类型', '情绪强度 1–10']
                rows = [[1, 100, 15, ch, '找回钥匙', '阶段收束', score]
                        for ch, score in zip(range(17, 21), [4, 6, 5, 7])]
                self.write('ledger/chapter-progress.md', table(headers, rows))
                rep = self.run_check()
                self.assertEqual(rep.exit_code, 0, rep.warn + rep.red)
                self.assert_code(rep.ok, 'C-CURVE')
                parsed = ledger.parse_tables(table(headers, rows))[0]
                self.assertEqual(ledger.col_of(parsed, '章'), 3)
                self.assertEqual(ledger.col_of(parsed, '预计回收章节'), 1)
                self.assertEqual(ledger.col_of(parsed, '首次章'), 0)
                self.assertEqual(ledger.col_of(parsed, '实际回收章'), 2)

    def test_known_header_formatting_and_original_status_annotation(self):
        self.write('ledger/chapter-progress.md', table(
            ['**章号**', '情绪强度（1－10分）', '状态（已完成/待写）'],
            [[ch, score, '已完成'] for ch, score in zip(range(17, 21), [4, 6, 5, 7])]))
        self.write('story-bible.md', table(
            ['疑问', '抛出章节', '状态（已答/延迟/永不答）', '计划解答章'],
            [['钥匙为何失踪', 1, '已答', 10]]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 0, rep.warn + rep.red)

    def test_foreshadowing_header_aliases_keep_deadline_semantics(self):
        for plant, plan in [('埋设章', '预计回收章'), ('埋设章号', '预计回收章号'),
                            ('埋设章节号', '计划回收章节')]:
            with self.subTest(plant=plant, plan=plan):
                headers = [plant if h == '埋设章节' else plan if h == '预计回收章节'
                           else h for h in F_HEADERS]
                headers += ['实际回收章', '首次章']
                self.write('ledger/foreshadowing-ledger.md', table(
                    headers, [frow(plan='第10章') + [19, 1]]))
                rep = self.run_check()
                self.assertEqual(rep.exit_code, 1, rep.warn)
                self.assert_code(rep.yellow, 'F-OVERDUE')
                self.assertTrue(any('第10章' in item for item in rep.yellow), rep.yellow)

    def test_similar_chapter_headers_do_not_supply_missing_chapter(self):
        for name in ['首次章', '预计回收章', '实际回收章', '本章事件', '章末钩子类型',
                     '章节标题', '总章数', '章号/预计回收章', '章（预计回收章）']:
            with self.subTest(header=name):
                self.write('ledger/chapter-progress.md', table(
                    [name, '情绪强度'], [[ch, 5] for ch in range(17, 21)]))
                rep = self.run_check()
                self.assertEqual(rep.exit_code, 2, rep.ok)
                self.assert_no_code(rep.ok, 'C-CURVE')
                self.assertTrue(any("缺列=['章']" in item for item in rep.warn), rep.warn)

    def test_actual_recovery_header_cannot_supply_planned_deadline(self):
        headers = ['实际回收章' if h == '预计回收章节' else h for h in F_HEADERS]
        self.write('ledger/foreshadowing-ledger.md', table(headers, [frow()]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 2, rep.ok)
        self.assertTrue(any("缺列=['预计回收章节']" in item for item in rep.warn), rep.warn)
        self.assert_no_code(rep.ok, 'F-LEDGER')

    def test_alias_duplicates_are_rejected_even_with_canonical_header(self):
        for first, second in [('章', '章号'), ('章号', '章节号'), ('章', '**章**')]:
            with self.subTest(headers=[first, second]):
                self.write('ledger/chapter-progress.md', table(
                    [first, second, '情绪强度'], [[ch, ch + 1, 5] for ch in range(17, 21)]))
                rep = self.run_check()
                self.assertEqual(rep.exit_code, 2, rep.ok)
                self.assertTrue(any("重复列=['章']" in item for item in rep.warn), rep.warn)
                self.assert_no_code(rep.ok, 'C-CURVE')

    def test_optional_state_duplicates_cannot_hide_pending_rows(self):
        self.write('ledger/chapter-progress.md', table(
            ['章号', '情绪强度', '状态', '状态（已完成/待写）'],
            [[ch, 5, '已完成', '待写'] for ch in range(17, 21)]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 2, rep.ok)
        self.assertTrue(any("重复列=['状态']" in item for item in rep.warn), rep.warn)
        self.assert_no_code(rep.ok, 'C-CURVE')

    def test_equivalent_rating_headers_are_duplicate_but_wrong_scale_is_missing(self):
        self.write('ledger/chapter-progress.md', table(
            ['章号', '情绪强度', '情绪强度（1–10）'], [[ch, 5, 5] for ch in range(17, 21)]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 2, rep.ok)
        self.assertTrue(any("重复列=['情绪强度']" in item for item in rep.warn), rep.warn)
        for wrong in ['情绪强度（0–10）', '情绪强度 1–5', '情绪强度说明']:
            with self.subTest(header=wrong):
                self.write('ledger/chapter-progress.md', table(
                    ['章号', wrong], [[ch, 5] for ch in range(17, 21)]))
                rep = self.run_check()
                self.assertEqual(rep.exit_code, 2, rep.ok)
                self.assert_no_code(rep.ok, 'C-CURVE')

    def test_two_alias_tables_remain_ambiguous(self):
        self.write('ledger/chapter-progress.md', table(
            ['章', '情绪强度'], [[ch, 5] for ch in range(17, 21)]) + '\n' + table(
            ['章号', '情绪强度 1–10'], [[ch, 6] for ch in range(17, 21)]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 2, rep.ok)
        self.assertTrue(any('多张同类表' in item for item in rep.warn), rep.warn)

    def test_alias_data_cannot_hide_behind_none_declaration(self):
        self.write('ledger/outline-changelog.md',
                   '<!-- ledger-check: outline=none; reason=未改过批准大纲 -->\n' +
                   table(['当前章号', '调整方向'], [[19, '改动了章节顺序']]))
        rep = self.run_check()
        self.assertEqual(rep.exit_code, 2, rep.ok)
        self.assertTrue(any('声明无记录/不适用，但表中仍有数据' in item for item in rep.warn), rep.warn)

    def test_future_curve_rows_do_not_mask_current_window(self):
        self.progress([17, 18, 19, 20, 21], [9, 9, 9, 9, 3])
        self.assert_code(self.run_check().yellow, 'C-HIGH')

    def test_curve_unsorted_records_are_sorted_by_chapter(self):
        self.progress([20, 17, 19, 18], [9, 9, 9, 9])
        self.assert_code(self.run_check().yellow, 'C-HIGH')

    def test_curve_gaps_duplicate_out_of_range_and_missing_current_are_incomplete(self):
        for chapters, scores in [([16, 18, 19, 20], [9] * 4), ([17, 18, 19, 19], [9] * 4),
                                 ([17, 18, 19, 20], [9, 9, 9, 99]), ([16, 17, 18, 19], [9] * 4)]:
            self.progress(chapters, scores)
            rep = self.run_check()
            self.assertEqual(rep.exit_code, 2)
            self.assert_no_code(rep.ok, 'C-CURVE')

    def test_missing_context_and_invalid_thresholds_are_incomplete(self):
        self.assertEqual(self.run_check(cur_ch=None).exit_code, 2)
        self.assertEqual(self.run_check(cur_ch=0).exit_code, 2)
        for thresholds in [{'unknown': 1}, {'short_gap': 0}, {'overdue_ratio': 2}, {'curve_window': 1},
                           {'curve_low': 9, 'curve_high': 3}, {'short_gap': '15'}, {'curve_high': None}]:
            with self.subTest(thresholds=thresholds):
                self.assertEqual(self.run_check(thresholds=thresholds).exit_code, 2)

    def test_warning_exit_code_takes_precedence_over_red(self):
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(plan='第1章')]))
        (self.root / 'story-bible.md').unlink()
        rep = self.run_check()
        self.assertTrue(rep.red)
        self.assertFalse(rep.complete)
        self.assertEqual(rep.exit_code, 2)

    def test_chinese_numbers_and_nonchapter_numbers(self):
        for text, number in [('第二十一章', 21), ('第一百零五章', 105), ('第两百章', 200), ('10', 10)]:
            self.assertEqual(ledger.parse_chapter(text), number)
        for text in ['第X章', 'F-001', '2026-09-26', '0', '-2', '第10章、第20章']:
            self.assertIsNone(ledger.parse_chapter(text), text)

    def test_cli_exit_codes_and_override_flag(self):
        def cli(*args):
            return subprocess.run([sys.executable, '-B', str(SCRIPT), *map(str, args)],
                                  capture_output=True, encoding='utf-8', errors='replace')
        good = cli(self.root, '--current-chapter', 20)
        self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
        self.write('ledger/foreshadowing-ledger.md', table(F_HEADERS, [frow(plan='')]))
        red = cli(self.root, '--current-chapter', 20)
        self.assertEqual(red.returncode, 1, red.stdout + red.stderr)
        custom = cli(self.root, '--current-chapter', 20, '--short-gap', 30)
        self.assertEqual(custom.returncode, 0, custom.stdout + custom.stderr)
        bad = cli(self.root, '--current-chapter', 0)
        self.assertEqual(bad.returncode, 2)
        demo = cli('--demo')
        self.assertEqual(demo.returncode, 1, demo.stdout + demo.stderr)
        self.assertIn('DEMO PASS', demo.stdout)


if __name__ == '__main__':
    unittest.main()
