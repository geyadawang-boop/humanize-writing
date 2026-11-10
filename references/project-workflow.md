# 项目执行：立项、续写、修订与完结

用户要求完整写小说、剧本或持续多轮创作时使用本流程；只改一段文字不必建立整个项目。执行器管理计划、正文、版本和评阅，不按字数生成作品，也不把台账通过当作文学质量。

## 1. 定义作品与交付范围

先确定文体、受众、媒介、结构、实际交付物及终局契约。小说明确全书、某卷、短篇还是样章；剧本先读 [screenplay-workflow.md](screenplay-workflow.md)，区分电影、连续剧、单元剧、混合结构、舞台和广播。大纲、分集梗概、样稿、完整正文是不同交付物。

- 小说以 chapter 为单元，每章一个 UTF-8 Markdown/TXT 正文文件。
- 剧本可按 scene 或 episode 存稿；按集存稿必须另登记该集每一场的计划和场标。
- 目标单元数约束范围，不是文学质量分数，不要求机械凑字数或套固定节拍。
- 宏观结局与角色选择先有方向；细纲允许滚动推进，改变交付范围须留痕。
- 跨会话分批完成有边界的单元，并保存交接；本轮写完不等于整部写完。

## 2. 初始化空项目

从 skill 根目录运行；Python 3.10+，仅标准库，无需安装、CI 或 Git hooks：

~~~powershell
python -B scripts/writing_project.py init "D:/作品/新小说" --kind novel --format "长篇现实小说" --units 40 --title "作品名"
python -B scripts/writing_project.py init "D:/作品/新短片" --kind screenplay --format film --unit-type scene --units 12 --title "短片名"
python -B scripts/writing_project.py init "D:/作品/新剧集" --kind screenplay --format screen_series --unit-type episode --units 8 --title "剧集名"
~~~

目标目录须不存在或为空；工具拒绝覆盖既有项目。迁入旧稿时先初始化独立空目录，再复制对应正文、补计划和台账；旧稿不会自动获得已评阅状态。

project-state.json 是唯一机器状态入口，由脚本生成，无需手抄另一份易过期的 JSON 模板。

| 字段 | 用途 |
|---|---|
| project | 标题、kind、format、unit_type、初始及当前目标数、current_volume |
| units | 顺序、ID、正文路径、因果摘要、成稿状态、场次、显式依赖 |
| support_files | 设定、台账、终局、交接及追加关键资料 |
| stage / next_step | planning、drafting、revising、paused、complete 与下一步 |
| checkpoint | 当前正文、计划、台账、收尾及显式依赖的 SHA-256 快照 |
| reviews | 单元/最终评阅的具名人、来源、版本、结论及证据文件摘要 |
| scope_changes / retired_units | 扩缩范围的原因、退出计划但仍保留的正文记录 |
| completion | 当前版本、评阅来源和完成级别；修改内容即失效 |

小说默认复制圣经、全书/分卷大纲、人物、规则、伏笔、战力、改纲与进度台账。剧本复制专用圣经、场景表和分集表，不套小说战力台账。共同生成 ending.json、session-handoff.md、quality-review.md、manuscript/。初始空模板不算已完成。

## 3. 每轮写作的闭环

1. 先 status，重读交接单、当前圣经、前章/场结尾与相关未解承诺。实际稿件与旧记录冲突时先查证，不凭会话记忆编造事实。
2. 完善本单元计划：谁想要什么、遇到什么阻碍、作何选择、造成什么结果，怎样接续前文。
3. 写入实际正文文件，核对因果、人物知识边界、时间地点、声音、节奏和情感效果；剧本再核对可拍可演、动作与潜台词、场景转折和媒介格式。
4. 同步角色、时间、世界规则、伏笔、场景/分集表。修改前文必须识别受影响后文，不能只改台账使检查变绿。
5. 登记单元状态，写交接和下一步，保存 checkpoint。快照只记录当前版本，不表示质量通过。

~~~powershell
python -B scripts/writing_project.py set-unit "D:/作品/新小说" CH001 --summary "林岚隐瞒欠款接下夜班，导致弟弟独自追查失踪者" --status drafted
python -B scripts/writing_project.py checkpoint "D:/作品/新小说" --next "重读弟弟的信息边界，再写 CH002 的追查受阻"
python -B scripts/writing_project.py check "D:/作品/新小说"
~~~

check 检查全部当前计划，创作中的缺章、空模板会显示待完成，这是正常进度。status 只显示状态，其退出码 0 不代表作品完成。空正文、仅标题/注释/明显占位符、缺文件、planned 状态、未填 summary、未登记正文均不能通过完整性检查。工具不设最低字数，是否写够由交付契约和实际评阅决定。

小说章节进度必须覆盖每个实际已写且登记 drafted/revised 的单元，不能只保留最新一章；final 还必须覆盖全部计划章节。未来章或尚未实际写成的章不能冒充完成记录。章节计划放在大纲和 units，完成进度放在进度表，两者不能混写成假完成。

### 小说台账适用性

默认调用 ledger_check.run_checks()；红线或缺失/格式错误均不得完结。无分级战力体系时，可在相应台账写实际适用性声明：

~~~markdown
<!-- ledger-check: power=not-applicable; reason=本作品为写实亲情故事，没有分级战力体系 -->
~~~

真实没有伏笔、未解疑问、改纲事件时可分别声明 foreshadowing=none、questions=none、outline=none 并给具体原因，详见 [templates/README.md](../templates/README.md)。初始化不替作者作“没有”的事实声明。不得默认标所有疑问已答、所有伏笔废弃，或删除难处理条目来获得全绿。

审计窗口可在 project.ledger_thresholds 持久化，例如 {"short_gap": 20, "mid_gap": 45, "curve_window": 4}；字段和合法取值由 ledger_check 验证，未知/无效参数使检查不完整而非静默忽略。项目保存的是该作品采用的启发式参数，不是普适文学定律。修改阈值改变全项目版本，使最终评阅过期。

### 剧本逐场、逐集覆盖

按集存稿时，相应 units 条目需要 scenes，例如：

~~~json
"scenes": [
  {"id": "E01-S01", "summary": "接下夜班令林岚错过约定", "marker": "# E01-S01 内景 值班室 夜"},
  {"id": "E01-S02", "summary": "弟弟追查发现与姐姐有关的票据", "marker": "# E01-S02 外景 桥头 夜"}
]
~~~

每个 marker 在所属集正文独占一行且只出现一次，场标后必须有动作/对白。场景表和分集表保留模板英文字段名；检查实体数据行，不把说明里的示例 ID 算完成。场景表一行一场，draft_path 与正文计划一致；一集多场可共用该集正文文件。分集表 scene_ids 用逗号、顿号或空格分隔，并与场景计划一致。独立作品在分集文件写 N/A: standalone 和具体理由。

代码围栏和 HTML 注释里的示例表、假场标和文字均不计入正式记录/正文。标准 Markdown 可省略表格行的首尾管道符，解析仍检查这些行，不能借格式差异藏掉未写场景。场景正文按真实整行 marker 的位置分段，注释、引用或句中提及的场号不能替代场次边界。

## 4. 停写、恢复和改变范围

停写前在交接单记录实际完成位置、新增事实、未解承诺、质量问题、下一次第一步，再 checkpoint：

~~~powershell
python -B scripts/writing_project.py pause "D:/作品/新小说" --next "从 CH012 的时间线矛盾开始核对"
python -B scripts/writing_project.py resume "D:/作品/新小说" --next "重读交接和 CH011-012，再修订"
python -B scripts/writing_project.py resize "D:/作品/新小说" --units 38 --reason "合并重复调查线，需将原39-40章信息移入终章并重核伏笔"
python -B scripts/writing_project.py reopen "D:/作品/新小说" --next "修订终局选择及其前文铺垫"
~~~

暂停/恢复不删稿。快照过期时先比较实际文件与记录，确认改动再同步。缩短范围会记录原因、保留退出计划的正文；增加回原目标时可重新纳入旧单元。直接改 target_units 却没有变更链会被拒绝。

已登记完结的作品先 reopen。它撤销旧完结和最终评阅，保留未变单元的评阅记录；是否仍有效由各单元及依赖 hash 判定。未完结的项目不能用 reopen 改状态（暂停项目用 resume）；直接在编辑器改正文，也会使下次检查发现旧完结失效。

## 5. 评阅作用域：适合长篇的增量核读

**单元评阅**绑定该单元正文、计划字段、文体契约和显式 depends_on；写新章或更新进度/交接，不会让未改的前章评阅自动过期。可在某单元的 depends_on 中登记关键依赖，如 ["ledger/world-rules.md", "manuscript/CH003.md"]。依赖变化会令该单元评阅失效。默认空列表，作者应按实际关系补充。

**最终评阅**绑定全项目快照；任何正文、计划、关键台账、终局、交接或声明的依赖变化都使终审/完结失效。评阅证据文件变化也须重新登记。单元之间未登记的因果影响不会被机器推断：前文大改必须做影响清单，更新相关单元依赖并复核；最终全篇核读承接这个范围。

可边写边记录单元评阅，收尾时集中核对全篇。不要为了更新一章无差别重审前几百章，也不要把单元 hash 未变误解为所有后文因果都已验证。

## 6. 收尾、具名评阅和完结

先填 ending.json：主承诺、角色弧光、关系、伏笔、代价、读者/观众问题逐项核对。默认 main-conflict、protagonist-arc、aftermath 不可删，可追加其他承诺。每项写 promise、disposition、对应正文单元 units、处置 reason，另填 ending_note。

- resolved：在正文有落点；失败结局、负弧光或平弧光也可成立，不要求主人公成功或变好。
- intentional-open：次级开放项，说明艺术功能及本篇为何自足。
- removed：修订撤除的次级承诺，说明如何同步处理铺垫和后文。

主冲突、人物的选择/状态、后果与余韵须有本篇落点。开放结局不必回答全部事实，但不能借“留续作”逃避主要戏剧任务。机器只能检查处置记录和正文链接，不能证明承诺真正兑现。

将质量评阅模板写成 reviews/本轮评阅.md，记录实际核读范围、具体正文位置、判断、反例、修订与复核。增量创作优先每单元一份证据文件，以免追加新评阅改变旧证据的 hash。一份综合证据也可包含多个单元，但须实际核读并分别说明；后续编辑该文件会使引用它的记录需重新登记。

~~~powershell
python -B scripts/writing_project.py checkpoint "D:/作品/新小说" --next "核读全篇及终局处置"
python -B scripts/writing_project.py review "D:/作品/新小说" --scope CH001 --reviewer "实际评阅者" --source assisted --evidence "reviews/单元评阅.md" --verdict pass
# 其他单元实际核读后分别登记；不可自动把未读单元批量标 pass。
python -B scripts/writing_project.py review "D:/作品/新小说" --scope final --reviewer "实际辅助评阅者或模型标识" --source assisted --evidence "reviews/全篇评阅.md" --verdict pass
python -B scripts/writing_project.py check "D:/作品/新小说" --final
python -B scripts/writing_project.py complete "D:/作品/新小说"
~~~

assisted 表示辅助评阅，可在其他条件全部通过后完成“完整草稿/辅助终审完成”，不额外等待用户没有要求的人工审批。工具会明确标示“未经过独立人工评阅”，completion_level 为 assisted_draft_complete，并保留 review_source=assisted。

human 只在真实人工核读已发生时登记；其完成级别为 human_review_recorded，表示存在具名记录，不表示工具认证了评阅人或质量。不得冒充人类读者或制造人工通过。用户明确要求独立人工终审时，按该交付契约执行：可先完成全稿和辅助自审，另标“用户要求的人工终审未完成”，不能以 assisted 冒充该项达成。任何来源发现必改问题都须登记 revise。

complete 要求：全范围实稿与计划一致、小说台账或剧本场/集映射可检查、终局处置齐全、checkpoint 当前、各单元与最终具名评阅当前且通过。辅助来源不会降低这些检查，也不能被显示为人工来源。缺失、空白、未评阅、过期或结构错误均不可假完结。

## 7. 退出码、边界与验证

| 退出码 | 含义 |
|---|---|
| 0 | 此操作成功；check/complete 表示指定检查通过，init/checkpoint/status 不表示作品完成 |
| 1 | 内容未齐、红线、评阅未通过/过期、终局未处置 |
| 2 | 用法、路径、状态 JSON、台账/剧本清单缺失或格式错误；检查未完整 |

所有路径限定项目内，拒绝绝对路径、..、Windows 盘符/数据流与越界链接。正文支持 UTF-8 .md/.txt，导出 DOCX/PDF 是后续交付阶段。同一项目一次运行一个写状态命令；本工具不解决多人同时写入冲突，也不是防篡改签名系统。它不能自动保证文笔、戏剧效果、事实、法律合规或商业可卖。

~~~powershell
python -B -m unittest discover -s tests -p test_writing_project.py -v
~~~

测试覆盖完整微型小说与短片、空项目/缺稿/未评阅拒绝、增量写作评阅作用域、正文和台账修改后失效、分集漏场、停写恢复、改纲留痕、路径约束。夹具默认辅助评阅，不虚构真实人工核读。微型样例验证操作闭环，不能替代十万字长篇的逐单元创作、周期复核与全篇核读，也不能证明达到出版品质。
