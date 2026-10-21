# templates：长篇项目的规划、正文索引与连续性台账

> 本目录连接创作知识与实际项目。v0.37 在既有小说台账上补足项目闭环与检查语义；数值阈值是可配置的审计默认值，不能当成文学定律或作品质量证明。

新项目推荐先用 `scripts/writing_project.py init` 建立执行目录，按 [项目工作流](../references/project-workflow.md) 推进；剧本项目结合 [剧本全作品工作流](../references/screenplay-workflow.md)。完整参数先看相应脚本的 `--help`。旧手工小说项目仍可单独运行 `ledger_check.py` 或调用 `run_checks`，无需迁移才可审计。脚本只在被实际运行时检查，不表示已经安装自动钩子或 CI。

## 一、三层分工

- templates：实际项目可填写的正文辅助材料，不是完成的作品。
- project-state.json：项目工具生成的状态、文件与评阅索引；story-bible 是故事事实入口。
- 检查脚本：只在被运行时检查文件与记录；人工/模型文本评阅仍需回到实际正文。

## 二、初始化与已有项目

推荐使用 writing_project.py init 创建到空目录；小说默认结构如下：

~~~text
project-state.json
story-bible.md
volume-outline.md
ending.json
session-handoff.md
quality-review.md
manuscript/CH001.md ...
ledger/character-sheet.md
ledger/world-rules.md
ledger/foreshadowing-ledger.md
ledger/power-ledger.md
ledger/outline-changelog.md
ledger/chapter-progress.md
~~~

旧手工项目可继续将分卷大纲放 ledger/volume-outline.md；ledger_check 不依赖它的路径。接入项目工具时按项目工作流建立状态，不能覆盖旧稿。剧本用 screenplay-bible、scene-list、episode-outline 三份专用模板，见剧本工作流；无战力或无分集需求按事实说明不适用。

## 三、每章更新

1. 保存实际正文，再在章节进度中登记对应章号、事件、情绪判断和台账变化，不提前把规划登记成已写。
2. 新埋/唤醒/回收伏笔时更新相应行并保留正文位置；无变化不必造条目。
3. 已提出疑问保留历史与状态；延迟不等于已回答，未发生的设想不计读者当前负担。
4. 同步实际变化的人物知识、时间、空间、关系、物件和规则；没有变化时无需形式化改日期。
5. 检查章末功能是否有效，可为悬念、决定、余波或阶段解决，不强迫三章三种钩子。
6. 保存交接与checkpoint，再按项目需要运行check/ledger_check。调用台账检查时同时给当前章和当前卷，不能把缺上下文的检查算通过。
7. 卷末增加卷级核读；正文改动使相关旧评阅失效后需实际重读再登记。

## 四、每卷与整书核读

1. 对照分卷目标和实际正文，记录完成、转移或撤销的承诺及原因。
2. 有力量体系时核对规则、资源、代价与每名当前适用角色的状态；退场/未登场者如实标记，不靠批量更新卷号消警。
3. 检查人物、时间、空间、信息和规则一致性，同时核对伤势/物件/关系的因果后果。
4. 伏笔与疑问逐条决定后续处置。读者核心承诺不能统一转续作以逃避完结；已解决行保留历史。
5. 以实际阅读间隔、章节体量和伏笔重要性决定是否唤醒；阈值仅提醒，不按固定50章强行安排复述。
6. 核主角的行动、选择与代价；正弧、负弧、平弧都可成立，不硬要求每卷成长一格。
7. 有改纲就留下原因及受影响范围；没有改纲可明确声明，不要求为满足检查而制造改纲事件。
8. 运行完整性与台账检查并回读原文。整书完成另需全部约定正文、终局处置和当前版本的质量评阅证据。

## 五、ledger_check.py——六组可执行检查与人工边界

| 检查 | 红线（RED） | 黄线（YELLOW）/输入检查 | 依据与边界 |
|---|---|---|---|
| 伏笔兑现与唤醒 | 逾期 >5项或占已生效未处置行 >20% | 超计划章、无计划的临时窗口、独立唤醒断档 | 有明确回收计划优先；无计划短/中期默认埋后15/50章。中期唤醒默认100章仅为“两卷各50章”的可改占位估算；长期唤醒默认50章。回收与唤醒不能互相抵消 |
| 战力更新断档 | **该角色**落后当前卷 ≥2卷 | 该角色落后1卷；未来更新卷为输入问题 | 逐行判级，严重行不污染其他行。未登场/已退场等明确非当前适用行排除；无战力题材须声明不适用 |
| 大纲调整记录 | — | 距最近已发生调整 >30章提醒核对；未来记录不算已发生 | 不是要求每30章必须改纲；没有调整可以明确声明 |
| 已抛出疑问负担 | 未答 >5个 | 3–5个提醒；未来/未抛出项不计当前负担 | “延迟”仍是未答，不能靠改状态清掉读者负担 |
| 已完成章情绪窗口 | — | 最近4个**连续章号**均 ≥8或 ≤3 | 依章号排序，忽略未来行；缺当前章、错分数、重复或窗口缺章会报告不完整。样本不足不会宣布曲线健康 |
| 完结处置（`--final`） | 伏笔/疑问没有终态，或“留续作/已废弃/永不答/已取消”等缺具体处置说明 | 缺表/错行同样不能通过完结审计 | 计划回收不等于已回收；仅检查账面处置，实际正文兑现、铺垫公平、人物弧光与整体完成度仍需人工审查 |

### 输入不完整不能假绿

检查会识别缺失文件、缺列或重复列、歧义的同类多表、错位行、重复ID、占位章号、空表、未指定当前章/卷等问题。将这些记为 `WARN`，表示**本次检查未完成**；不会把解析失败或未提供的记录算成0条问题。各文件中的代码围栏示例不作为实际台账或免检声明。

确实无记录时，人工确认后可在相应文件独立写一行：

```markdown
<!-- ledger-check: foreshadowing=none; reason=本作品当前没有设置需后续兑现的伏笔 -->
<!-- ledger-check: questions=none; reason=当前正文没有悬而未答的问题 -->
<!-- ledger-check: outline=none; reason=截至当前章未偏离已确定大纲 -->
<!-- ledger-check: power=not-applicable; reason=本作没有分级战力体系 -->
```

四行分别放到伏笔表、story-bible、改纲表、战力表，按事实选用，不能整块复制。声明与实际记录或未清理占位行冲突会报输入问题；初始模板的空白不能自动转成“无”。章节进度不能用 none 豁免。

### 调用、可配置项与退出码

```text
python -B scripts/ledger_check.py 项目目录 --current-chapter 60 --current-volume 2
python -B scripts/ledger_check.py 项目目录 --current-chapter 60 --current-volume 2 --final
python -B scripts/ledger_check.py 项目目录 --current-chapter 60 --current-volume 2 --mid-gap 40 --mid-wake-gap 70
python -B scripts/ledger_check.py --demo
```

- `--help` 列出实际支持的阈值参数：`--short-gap`、`--mid-gap`、`--mid-wake-gap`、`--long-wake-gap`、`--overdue-hard`、`--overdue-ratio`、`--power-lag-red`、`--outline-gap`、`--questions-hard`、`--curve-window`、`--curve-high`、`--curve-low`。列名不支持任意命令行覆盖。项目应记录所采用的阈值，避免不同会话更换口径。
- **退出码0**：已完成适用检查且无红线，**仍可能有黄线**；不是“作品全绿”。**退出码1**：存在红线。**退出码2**：用法或输入不完整，优先于红线，不能据此宣布健康或完结。
- Python API 保持 `run_checks(root, cur_ch=None, cur_vol=None, final=False, thresholds=None)`，返回 `Report`；`red / yellow / ok / warn` 为字符串列表，`complete` 表示没有输入问题，`exit_code` 与命令行一致。可选 `thresholds` 的键为参数名的下划线写法。
- `--demo` 故意含红线：出现 `DEMO PASS` 且退出码1才是预期，不要把退出码1误认成演示脚本损坏。
- 回归测试：`python -B -m unittest discover -s tests -p test_ledger_check.py -v`。测试验证解析和检查语义，不替代作品审读，也不会替用户后台持续检查。

## 六、模板与知识来源

| 模板 | 主要来源或目的 |
|---|---|
| story-bible / character-sheet / world-rules | 故事事实、人物、关系与规则；适用字段按题材选用 |
| volume-outline / outline-changelog | 三层大纲、滚动计划与变更影响 |
| foreshadowing-ledger / power-ledger | 伏笔兑现、规则与代价的原有工艺，v0.37补审计语义 |
| chapter-progress | 实际章节覆盖、因果摘要与情绪窗口 |
| screenplay-bible / screenplay-scene-list / screenplay-episode-outline | 补编四的分集与格式资料，经适用范围与证据纠正后形成字段契约 |
| session-handoff / quality-review | 跨会话恢复与有正文定位的评阅证据 |

创作方法来自既有references及本次用户补编；机器字段、hash、退出码和默认阈值是执行层设计，不冒称全部逐字来自书籍。经验数值可按项目调整，修改须保留口径，不能为追求全绿无限放宽。知识讲怎样设计与判断，记录支持检索与恢复，程序检查记录；三者均不能替代整部正文及实际审读。
