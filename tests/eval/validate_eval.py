# -*- coding: utf-8 -*-
"""校验 tests/eval 下的真实任务评测集，并可汇总一次路由预测。

这组用例评估的是模型的路由选择，不是 Markdown 链接是否存在：
文件可达只保证“能走到”，不证明“选得对”。真正跑语义路由需要另起模型会话，
按 README 的协议记录首读与最终加载文档，再用本脚本的 --routing-predictions 汇总。

运行:
    python -B tests/eval/validate_eval.py
    python -B tests/eval/validate_eval.py --routing-predictions tests/eval/predictions.example.json
"""
import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

EVAL = Path(__file__).resolve().parent
ROOT = EVAL.parents[1]
LINK = re.compile(r'\[[^\]\n]*\]\(([^)\n]+)\)')


def load_cases(name):
    data = json.loads((EVAL / name).read_text(encoding='utf-8'))
    return data['cases']


def link_depths(start):
    """从 start 出发，返回 {resolved_path: 最少链接跳数}。"""
    start = start.resolve()
    depth = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for raw in LINK.findall(current.read_text(encoding='utf-8')):
            target = raw.split(' "', 1)[0].strip('<> ').split('#')[0]
            if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            nxt = (current.parent / target).resolve()
            if nxt.suffix == '.md' and nxt.is_file() and nxt not in depth:
                depth[nxt] = depth[current] + 1
                queue.append(nxt)
    return depth


def linked_targets(path):
    """只返回 path 正文里直接链接到的 Markdown 文件。"""
    out = set()
    for raw in LINK.findall(path.read_text(encoding='utf-8')):
        target = raw.split(' "', 1)[0].strip('<> ').split('#')[0]
        if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        resolved = (path.parent / target).resolve()
        if resolved.suffix == '.md' and resolved.is_file():
            out.add(resolved)
    return out


def as_list(value):
    if isinstance(value, str):
        return [value]
    return list(value or [])


def validate_routing(cases):
    errors = []
    if not 20 <= len(cases) <= 30:
        errors.append(f'routing_cases.json 应有 20–30 条用例，当前 {len(cases)} 条')
    ids, tasks = set(), set()
    from_skill = link_depths(ROOT / 'SKILL.md')
    from_routing = link_depths(ROOT / 'references' / 'routing.md')
    entry_links = (linked_targets(ROOT / 'SKILL.md')
                   | linked_targets(ROOT / 'references' / 'routing.md'))
    families = set()
    for case in cases:
        cid = case.get('id', '<missing>')
        for field in ('id', 'family', 'task', 'expect_first', 'expect_final', 'why'):
            if not case.get(field):
                errors.append(f'{cid}: 缺字段 {field}')
        if cid in ids:
            errors.append(f'{cid}: id 重复')
        ids.add(cid)
        task = case.get('task', '')
        if task in tasks:
            errors.append(f'{cid}: 任务文本重复')
        tasks.add(task)
        families.add(case.get('family', ''))

        first = as_list(case.get('expect_first'))
        finals = as_list(case.get('expect_final'))
        accept = as_list(case.get('accept_first'))
        avoid = as_list(case.get('avoid'))
        if len(first) != 1:
            errors.append(f'{cid}: expect_first 必须是一篇文档')
        if not finals:
            errors.append(f'{cid}: expect_final 不能为空')
        if set(first) & set(avoid):
            errors.append(f'{cid}: expect_first 同时出现在 avoid 中')

        for rel in first + finals + accept + avoid:
            path = (ROOT / rel)
            if not rel.startswith('references/') or not path.is_file():
                errors.append(f'{cid}: 目标不存在 {rel}')
                continue
        for rel in first + finals + accept:
            resolved = (ROOT / rel).resolve()
            if resolved not in from_skill:
                errors.append(f'{cid}: 从 SKILL.md 走不到 {rel}')
            elif from_skill[resolved] > 3:
                errors.append(f'{cid}: {rel} 距 SKILL.md {from_skill[resolved]} 跳，超过 3 跳')
            if resolved not in from_routing:
                errors.append(f'{cid}: 从 routing.md 走不到 {rel}')
            elif from_routing[resolved] > 2:
                errors.append(f'{cid}: {rel} 距 routing.md {from_routing[resolved]} 跳，超过 2 跳')

        if first and (ROOT / first[0]).is_file():
            first_path = (ROOT / first[0]).resolve()
            first_links = linked_targets(first_path)
            for rel in finals:
                resolved = (ROOT / rel).resolve()
                if resolved == first_path:
                    continue
                if resolved not in first_links and resolved not in entry_links:
                    errors.append(
                        f'{cid}: 首读 {first[0]} 没有链接最终落点 {rel}，'
                        '入口/路由也没有直接给出该落点')

    if len(families) < 10:
        errors.append(f'任务族只有 {len(families)} 类，覆盖面不足')
    return errors


def validate_revision(cases):
    errors = []
    if not 6 <= len(cases) <= 8:
        errors.append(f'revision_cases.json 应有 6–8 组，当前 {len(cases)} 组')
    ids, genres = set(), set()
    for case in cases:
        cid = case.get('id', '<missing>')
        for field in ('id', 'genre', 'target', 'source', 'preserve', 'traps'):
            if not case.get(field):
                errors.append(f'{cid}: 缺字段 {field}')
        if cid in ids:
            errors.append(f'{cid}: id 重复')
        ids.add(cid)
        genres.add(case.get('genre', ''))
        if len(case.get('source', '')) < 150:
            errors.append(f'{cid}: source 少于 150 字，改稿任务太短')
        if len(as_list(case.get('preserve'))) < 2:
            errors.append(f'{cid}: preserve 至少要有 2 条')
        if len(as_list(case.get('traps'))) < 2:
            errors.append(f'{cid}: traps 至少要有 2 条')
    if len(genres) != len(cases):
        errors.append('revision 用例的文体应互不重复')
    return errors


def validate_drift(cases):
    errors = []
    if len(cases) != 3:
        errors.append(f'drift_cases.json 应有 3 条，当前 {len(cases)} 条')
    ids = set()
    for case in cases:
        cid = case.get('id', '<missing>')
        for field in ('id', 'title', 'genre', 'premise', 'state', 'outline',
                      'excerpt', 'task', 'checkpoints', 'traps'):
            if not case.get(field):
                errors.append(f'{cid}: 缺字段 {field}')
        if cid in ids:
            errors.append(f'{cid}: id 重复')
        ids.add(cid)
        if len(as_list(case.get('state'))) < 5:
            errors.append(f'{cid}: state 至少要有 5 条')
        if len(as_list(case.get('outline'))) < 3:
            errors.append(f'{cid}: outline 至少要有 3 章')
        if len(case.get('excerpt', '')) < 200:
            errors.append(f'{cid}: excerpt 少于 200 字')
        if len(as_list(case.get('checkpoints'))) < 5:
            errors.append(f'{cid}: checkpoints 至少要有 5 条')
        if len(as_list(case.get('traps'))) < 3:
            errors.append(f'{cid}: traps 至少要有 3 条')
    return errors


def validate_all():
    return {
        'routing': validate_routing(load_cases('routing_cases.json')),
        'revision': validate_revision(load_cases('revision_cases.json')),
        'drift': validate_drift(load_cases('drift_cases.json')),
    }


def score_routing(cases, predictions_path):
    data = json.loads(Path(predictions_path).read_text(encoding='utf-8'))
    runs = data.get('runs', data) if isinstance(data, dict) else data
    by_id = {run.get('id'): run for run in runs}
    missing = [case['id'] for case in cases if case['id'] not in by_id]
    if missing:
        print('缺少预测：' + ', '.join(missing))
        return 1

    first_hits = final_hits = 0
    loaded_counts = []
    avoid_hits = []
    for case in cases:
        run = by_id[case['id']]
        acceptable_first = [case['expect_first']] + as_list(case.get('accept_first'))
        first_ok = run.get('first') in acceptable_first
        final_ok = bool(set(as_list(run.get('final'))) & set(as_list(case.get('expect_final'))))
        loaded = as_list(run.get('loaded')) or as_list(run.get('final')) or [run.get('first')]
        avoided = sorted(set(loaded) & set(as_list(case.get('avoid'))))
        first_hits += first_ok
        final_hits += final_ok
        loaded_counts.append(len(loaded))
        if avoided:
            avoid_hits.append(f"{case['id']}: {', '.join(avoided)}")
        flag = 'OK' if first_ok and final_ok and not avoided else 'CHECK'
        print(f"  {case['id']} {flag} first={run.get('first')} final={run.get('final')}")
    total = len(cases)
    print()
    print(f'首读命中：{first_hits}/{total} = {first_hits / total:.2f}')
    print(f'最终命中：{final_hits}/{total} = {final_hits / total:.2f}')
    print(f'平均加载：{sum(loaded_counts) / total:.1f} 篇')
    print('误加载：' + ('无' if not avoid_hits else '; '.join(avoid_hits)))
    return 0


def main():
    parser = argparse.ArgumentParser(description='校验 humanize-writing 的真实任务评测集')
    parser.add_argument('--routing-predictions', help='一次路由运行的预测 JSON')
    args = parser.parse_args()

    groups = validate_all()
    errors = []
    for name, group_errors in groups.items():
        status = 'OK' if not group_errors else f'{len(group_errors)} 个问题'
        print(f'{name}: {status}')
        for error in group_errors:
            print('  - ' + error)
        errors.extend(group_errors)
    if errors:
        return 1

    if args.routing_predictions:
        return score_routing(load_cases('routing_cases.json'), args.routing_predictions)
    return 0


if __name__ == '__main__':
    sys.exit(main())
