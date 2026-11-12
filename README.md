# humanize-writing

面向中文写作的 AI 技能包：让小说、网文、剧本、诗歌、散文、议论文、学术论文、研究生学位论文与演讲稿**写得完整、写得清楚、写出声音**。

| 项目 | 说明 |
|---|---|
| 当前版本 | v0.59.1（程序与 lint 规则集 0.46） |
| 文档语言 | 简体中文 |
| 运行依赖 | Python 3.8+，仅标准库，无需安装第三方包 |
| 许可证 | [Apache-2.0](LICENSE) |
| 变更记录 | [CHANGELOG.md](CHANGELOG.md) |

**目录**

- [这是什么](#这是什么)
- [快速开始](#快速开始)
- [核心原理](#核心原理)
- [能做什么](#能做什么)
- [目录结构](#目录结构)
- [命令行工具](#命令行工具)
- [验证与边界](#验证与边界)
- [文档索引](#文档索引)
- [维护原则](#维护原则)
- [许可证](#许可证)

## 这是什么

`humanize-writing` 是一份可直接装入 AI 智能体（Claude Code、Trae 等支持 `SKILL.md` 的环境）的**写作技能包**。它不是一组提示词模板，而是一套可路由的知识体系加可执行的检查工具：

- **创作**：短篇、散文、诗歌、文章、长篇小说、网文、电影/剧集/短剧/话剧/广播剧，从立项到整部修订。
- **编辑**：改稿、去模板感、文风提升、只查不改的评阅、标题拟定。
- **管理**：长篇项目的状态、大纲、正文清单、连续性台账、跨会话交接与完结验收。
- **检查**：静态写作线索扫描、台账完整性与红线审计、改前改后对比报告。

**它不做什么**：不承诺降低 AI 检测率，不鉴定作者身份，不把小伎俩当成“人味”。去模板感只是编辑需求中的一种；把所有作品改到低分不是本项目的目标。

## 快速开始

**1. 放入技能目录**

把整个仓库目录复制到智能体的用户级 skills 目录，例如：

```text
Claude Code（Windows）: C:\Users\<用户名>\.claude\skills\humanize-writing
Claude Code（macOS/Linux）: ~/.claude/skills/humanize-writing
```

Trae 或其他支持 `SKILL.md` 的环境放入各自的 skills 目录即可。技能以自身根目录定位脚本，不依赖当前工作目录。

也可以用 npm 做内容分发（不提供 CLI）：`npm pack` 生成 `humanize-writing-0.59.1.tgz`，解包后把其中的 `humanize-writing/` 复制到上面的技能目录。

**2. 验证安装**

```bash
python -B tests/selftest.py
python -B -m unittest discover -s tests -p "test_*.py"
```

**3. 直接对话触发**

- “去 AI 味。”（把当前稿改到像人写的，保留事实与立场）
- “这段太 AI 了，说人话。”
- “把这篇三千字散文改掉模板感，保留我的观点和真实经历，告诉我改了哪里、为什么。”
- “新建一部 30 章的校园悬疑网文，先给故事 bible 和前 3 章大纲，不要一次写完。”
- “只看不改，评阅这三集竖屏短剧，按严重程度排序，标出具体位置。”
- “解释一下这份 AI 检测报告：我的分为什么变了，哪些结论能信？”

**4. 项目与检查**

```bash
# 立项：只创建待填写模板，不覆盖已有目录
python -B scripts/writing_project.py init ./我的小说 --kind novel --format web-novel --units 30 --title "作品名"
# 写完计划与第一章正文后
python -B scripts/ai_smell_lint.py --genre fiction ./我的小说/manuscript/CH001.md
python -B scripts/writing_project.py checkpoint ./我的小说 --next "核读第 1 章的对白与伏笔"
```

初始化只得到**待填写项目**：先写 bible、大纲与单元计划，再写正文并更新台账，`check` 才会逐步转为通过。

## 核心原理

### 1. 先认任务，再读知识

每次任务先分清四个维度：**操作**（新写/续写/改稿/评阅/改编）→ **作品**（文体与媒介）→ **阶段**（立项/推进/修订/完结）→ **症状**（当前具体问题）。入口只有一条：[统一路由](references/routing.md)。旧 A–I 模式仅作兼容别名。

按需加载，单次优先解决一两个主要问题，不把 64 份文档与规则台账塞进一次创作。这是本技能与“大而全提示词”的根本区别：**知识量不等于上下文里的字数量**。

### 2. 知识、记录、程序三层分离

| 层 | 载体 | 负责 | 不负责 |
|---|---|---|---|
| 知识 | `references/` | 讲清“怎么判断、为什么这样判断” | 不知道你的项目实际写到哪 |
| 记录 | `templates/` + `project-state.json` | 保存已经发生的事实、计划与承诺 | 不会替你写正文 |
| 程序 | `scripts/` | 检查文件契约、记录自洽与静态线索 | 不判断文学质量，不后台自动运行 |

三者混用是最常见的误用：把 lint 分数当作作品判决、把空模板当已完成、把计划当已写。

### 3. 技法不是配额

句长分布、三幕结构、黄金三章、章末钩子、每卷字数、Scene/Sequel 配比、Show/Tell 百分比，都只是**可选诊断工具**。按题材、节奏与用户契约调整，不为凑数破坏作品。文档中未附稿约的“必须/禁用/固定比例”一律按经验建议理解；而已核实且适用的法律、平台发布规则会单独标注适用范围，不降级为偏好。

### 4. 只有一条判断优先级链

**用户目标与事实/原作约束 → 交付格式 → 人物、因果与连续性 → 可读性与声音 → 静态指标。**

出现冲突时按这条链裁决，只在 [文体适配](references/genre-router.md) 与 [编辑流程](references/editing-workflow.md) 集中定义，不在各分册另设相反门槛。

### 5. 检查不等于质量保证

- `ai_smell_lint.py` 输出的是**静态命中强度**（0–100 的加权计数），JSON 中明确标记 `is_ai_probability=false`，25/40 只是提示阈值。
- `ledger_check.py` 只检查伏笔、战力、改纲、疑问、情绪窗口与完结处置的记录是否自洽；红灯黄灯都不等于“作品好/坏”。
- 缺失文件、错表头、空表、占位符会被记为“检查未完成”，**不允许假绿**。

### 6. 改稿以“声音契约”收口

改稿前先约定必须保留什么（事实、立场、语气、专业格式），改完对照**原稿 / 修订稿 / 保留项**三方判断收益。不承诺“AI 率必降或归零”，不为降分加错字、伪造经历、硬插口头语或改掉立场。

## 能做什么

| 场景 | 交付物 | 首读入口 |
|---|---|---|
| 改稿、去模板感、文风提升 | 修订稿 + 保留项说明 | [编辑流程](references/editing-workflow.md) |
| 只查不改、评阅已有稿 | 带位置、影响与优先级的评阅 | [编辑流程](references/editing-workflow.md) |
| 解释 AI 检测报告 / 核验评分变化 | 口径核查与证据边界说明 | [检测证据与资料要求](references/detection-principles.md) |
| 起标题、改标题 | 按数量要求给候选 | [标题工艺](references/title-craft.md) |
| 新写短篇、散文、诗歌、文章 | 正文成稿 | [统一路由](references/routing.md) |
| 句子别扭、重心不清、修饰语堆叠、收尾发虚 | 句层诊断与逐类修订 | [汉语行文决断](references/han-prose-grammar.md) |
| 写议论文 / 评论 / 驳论文 | 争点分层、材料与授权、让步—反驳 | [议论文工艺](references/argumentative-craft.md) |
| 期刊 / 会议论文 | 摘要双模型、强度与证据闭合、审稿回复信 | [学术工艺](references/academic-craft.md) |
| 研究生学位论文 / 开题 / 答辩 | 先取本校现行稿约、跨章一致、引用闭合与披露 | [学位论文工艺](references/thesis-craft.md) |
| 演讲稿 / 致辞 / 口播 | 场合语域、复沓各族、听读句法 | [演讲稿工艺](references/speech-craft.md) |
| 新建或续写小说 / 网文 | 大纲、分卷、章节正文、台账 | [小说全程](references/novel-workflow.md) + [项目执行](references/project-workflow.md) |
| 电影 / 剧集 / 短剧 / 话剧 / 广播剧 | 分集、分场到完整正文 | [剧本全程](references/screenplay-workflow.md) |
| 小说改剧本、剧本转小说、多交付物 | 分媒介验收的改编稿 | [统一路由](references/routing.md) 改编分支 |
| 校园青春题材 | 主流程 + 题材工艺 | [校园与青春](references/campus-youth-craft.md) |
| 中国影视制作与公开播出审校 | 条款适用范围核对 | [内容与未成年人边界](references/china-screen-content-boundaries.md) |
| 长篇中段塌陷、人物漂移、情节重复 | 实稿诊断 + 修改依赖 + 回读 | [长篇结构修订](references/longform-revision.md) |
| 查知识覆盖与能力短板 | 知识缺口 / 需求缺口 / 验证缺口 | [知识与能力地图](references/knowledge-map.md) |

## 目录结构

```text
humanize-writing/
├── SKILL.md                 # 智能体入口：任务识别、执行边界、交付纪律
├── README.md                # 本文件：定位、原理、功能与用法
├── CHANGELOG.md             # 版本变更记录
├── package.json             # npm 包元数据（内容分发，不暴露 CLI）
├── LICENSE                  # Apache-2.0
├── references/              # 64 份按需读取的工艺、流程与证据文档 + 规则台账
│   ├── README.md            # 分类索引（建议从这里进入）
│   ├── routing.md           # 唯一任务分派入口
│   ├── editing-workflow.md  # 改稿 / 评阅 / 停止条件
│   ├── novel-workflow.md    # 小说与网文全程
│   ├── screenplay-workflow.md   # 剧本全程
│   ├── project-workflow.md  # 项目状态、工具与检查证据
│   └── ...
├── templates/               # 13 份项目模板（见 templates/README.md）
├── scripts/                 # 4 个仅用标准库的脚本
│   ├── writing_project.py   # 11 个子命令的项目记录器
│   ├── ledger_check.py      # 6 组台账检查
│   ├── ai_smell_lint.py     # 静态写作线索扫描
│   └── compare_report.py    # 改前改后对比报告
└── tests/                   # 17 组、250 项单元测试 + selftest + 6 套冻结语料
```

## 命令行工具

四个脚本都只用 Python 标准库，不要求安装 hook 或 CI，也不会在后台自动执行。

### writing_project.py：项目记录器

```bash
python -B scripts/writing_project.py init <项目目录> --kind novel --format web-novel --units 30 --title "作品名"
python -B scripts/writing_project.py init <项目目录> --kind screenplay --format cn-tv --unit-type episode --units 12 --title "作品名"
python -B scripts/writing_project.py status <项目目录>
python -B scripts/writing_project.py checkpoint <项目目录> --next "接下来的具体工作"
python -B scripts/writing_project.py check <项目目录> [--final]
python -B scripts/writing_project.py complete <项目目录>
```

| 子命令 | 作用 |
|---|---|
| `init` | 仅在不存在或空目录初始化，拒绝覆盖旧稿 |
| `status` | 显示进度、待办与未决事项 |
| `check` | 检查正文覆盖、记录新鲜度与承诺处置 |
| `checkpoint` | 写入跨会话交接点 |
| `set-unit` | 登记单元状态与摘要 |
| `review` | 登记评阅来源与证据 |
| `resize` | 变更目标单元数（必须给原因） |
| `pause` / `resume` | 保存与恢复中断点 |
| `complete` / `reopen` | 完结与完结后重开修订（仅完结项目可重开） |

初始化后只是**待填写项目**，不是合格作品；须先写 bible、大纲与计划，再实际写正文并更新台账。完整字段与命令以 [项目执行](references/project-workflow.md) 及 `--help` 为准。

### ledger_check.py：台账审计

```bash
python -B scripts/ledger_check.py <项目目录> --current-chapter 12 --current-volume 1
python -B scripts/ledger_check.py <项目目录> --current-chapter 30 --current-volume 1 --final
python -B scripts/ledger_check.py --demo
```

六组检查：伏笔兑现与唤醒、战力更新断档、大纲调整记录、已抛出疑问负担、已完成章情绪窗口、完结处置（`--final`）。阈值可用 `--short-gap`、`--mid-gap`、`--questions-hard` 等参数调整，属项目审计策略而非文学定律，详见 [模板说明](templates/README.md)。

确实没有记录时，可在对应文件写明确声明（`foreshadowing=none` 等并附原因）；空模板不能自动当作“没有问题”。

### ai_smell_lint.py：静态写作线索

```bash
python -B scripts/ai_smell_lint.py --genre fiction --json <稿件.md>
python -B scripts/ai_smell_lint.py --language en <draft.md>
python -B scripts/ai_smell_lint.py <稿子目录>     # 递归 .md/.txt，逐文件报告 + 汇总
python -B scripts/ai_smell_lint.py -              # 从 stdin 读取
```

**分数怎么读**

| 区间 | 含义 |
|---|---|
| `<25` | 静态命中较少 |
| `25–40` | 适中，建议按文体核读 |
| `>40` | 命中较多，优先处理具体条目 |
| 无法判定 | 样本不足或语言未确认，不等于干净 |

分数只是加权计数，不是 AI 概率、作者身份或作品质量结论。

**门控与声明**

- 文体门控：`general / tech / academic / official / law / email / speech / fiction`，各文体豁免项不同。
- 语言声明：`auto / zh / en / mixed`。`auto` 不是语言识别器；中文不足 100 字时未声明文本只作有限扫描。
- 文件编码：UTF-8（含 BOM）、GBK、UTF-16/UTF-32（带 BOM）均可读取，单文件与目录批量一致。

**零权重观察（不计分，也不设配额）**

- v0.41–v0.43：句长标准差、短句占比、重复“不是……而是……”、段落长度、正则锚点密度退出计分。
- v0.44：`[路标词]` 与 `[段首序数]` 退出计分——`corpus_hc3`（12 对）与 `corpus_cred`（30 对）同题配对复测中，人类每千字 2.45 处、AI 0.06 处，罚次数与方向相反。`[AI 词]`（cred δ=-0.20）和`[段落开头]`（hc3 δ=-0.50）方向成立但样本小，保留原权重不加码。
- v0.52：默认输出 `[X 级]`——序数词小标题与“这意味着/这表明”式复述只计数、明确不改；同题配对中人类侧并不更少，列出是为了防止过度清理。
- v0.54：`[翻译腔]`（20 族词形 / 千汉字，两套配对语料方向相反）与 `[相邻同构]`（连续两/三句长度档与逗号数同款，分母是句数，比喻句不参与）。人类经典散文同样触发，标的是“整齐并列”而非来源。

**频率门与文体区分（v0.59，规则集 0.46）**

- 词表类信号（`[AI 词]`、`[英文 AI 词]`）单次命中只输出零权重定位行，不计分；同一词 ≥2 次才计分，或同一篇出现 ≥3 种不同套话且密度 ≥2 种/千字（英文为千词）时按「套话簇」计 `min(16, 4×种数)`。理由：自然写作里偶用一次“综上所述”“不是……而是”属于人的习惯，一刀切会逼出为降分而删词的改写。
- `[总结式结尾]`（全文 ≥2 处）、`[展望式收尾]`（末尾窗口 ≥2 处）、`[抽象名词化]`（≥2 处）、`[顿号连排]`（≥2 处）同样改为门槛制；单处仍会列出，只是 0 分。
- `[AI 句式]` 改按千字密度取阈：不仅…还 1.5 处/千字，随着…/在当今… 1.0 处/千字，下限 2 处；`[程度用语]` 改为同一词 ≥ max(3, 2 处/千字)。
- 文体豁免：`speech` 关闭顿号连排、总结式结尾、展望式收尾；`fiction` 关闭程度用语。词表侧按文体豁免常规用词（学术：众所周知/值得注意的是/不可或缺 等；公文：至关重要/全面提升/持续优化 等；演讲：未来可期/拭目以待；小说：恰似；英文 tech/academic/official：robust、crucial、leverage 等）。
- 标定变化：`corpus_cred` 30 对差值由 +1.00 回落到 -0.07（原先差距几乎全部来自单词单次命中），`corpus_hc3` 由 +1.58 升到 +2.83，合并后仍为正。跨版本分数不可直接比较。

**可选分析参数**

- `--fingerprint`：破折号、引号、分号、顿号、“的”的每千字密度与句长中位。这些量在不同模型上方向相反，**不能反推来源模型、不设目标值**，某项偏低不构成补写理由。
- `--candidates`：段间衔接接口、结论提示冒号、同义重命名、等长三连四类语义候选。只给位置与原文，须按判据逐条判读；候选本身不是问题，也不构成改写理由。
- `--all`：输出全部规则命中，含零权重观察项。

**规则台账**：[references/rule-ledger.json](references/rule-ledger.json) 登记全部 41 条规则的标签、类型、权重、证据与可触发探针；`tests/test_rule_ledger.py` 逐条驱动探针，保证新增规则必须登记、观察行永远零权重、文体门控确实生效。

### compare_report.py：改前改后对比

```bash
python -B scripts/compare_report.py 原稿.md 修订稿.md --format md
python -B scripts/compare_report.py 原稿.md 修订稿.md --format html --semantic 人工判读.json
```

同一规则集评改前改后两稿，输出指标对比表、分级命中清单（标注改后是否仍命中）、逐段标红对照，可合并人工判读 JSON。它展示“改了什么、哪些指标变了”，不证明改得更好。

### 退出码约定

| 工具 | 0 | 1 | 2 |
|---|---|---|---|
| `writing_project.py` | 操作成功 / 所查范围通过 | 未齐、过期或未通过 | 参数、路径或状态格式错误 |
| `ledger_check.py` | 检查完整且无红线（仍可能有黄线） | 存在红线 | 输入不完整或调用错误（优先于红线） |
| `ai_smell_lint.py` | 未超静态阈值 | 超过静态阈值，需按文体核读 | 输入不足、语言未确认或参数错误 |
| `compare_report.py` | 报告已生成 | — | 输入或判读 JSON 无法读取 |

退出码 0 只说明**该工具在该口径下通过了**，不构成作品质量结论。

## 验证与边界

**当前验证基线**

| 项目 | 现状 |
|---|---|
| 自动化测试 | 250 项 unittest 全部通过；`selftest.py` RC=0 |
| 结构审计 | 575 个文件全部 UTF-8 / LF；本地链接可达；64 篇 references 均有加载入口 |
| 规则台账 | 41 条（加权 16 / 观察 15 / 状态 10），探针逐条驱动 |
| 冻结语料 | 6 套（含 HC3 与 CReD 配对集），方向测试锁定权重 |
| 端到端 | `init` → 写章 → `lint` → 改写 → `compare_report` → `checkpoint` → `check` |
| 三副本 | Desktop / `.trae-cn` / `.claude` 逐文件 SHA256 一致 |

应同时看正例与反例：空模板拒绝、计划内伏笔不误报、战力逐行判级、正文或台账改动后评阅失效、小说与剧本的完整微型示例，以及真实请求的路由行为。

**历史记录**

- v0.38：81 项自动测试；完成 4015 汉字六章短篇网文（含文件交接续写）与 2252 汉字三集九场微型剧本，均为模型辅助评阅的完整草稿。
- v0.39–v0.40：追加文学选段实改、连载局部只读评阅与新写短请求试用，保留首轮缺陷与修正记录。
- v0.41–v0.58：主要调整文档、lint 计分口径与输入解码；规则集与分数未变，跨版本分数变化不能当作文风改善。
- v0.59：规则集 0.45 → 0.46。词表类信号改频率门、结尾类改门槛制、句式改千字密度，并按文体豁免常规用词；同一文本的分数会低于 0.45，两个版本不可直接比较。

各版本改动与验证证据见 [CHANGELOG.md](CHANGELOG.md)。

**当前不应宣称**

| 可以支持 | 不能宣称 |
|---|---|
| 按文体修订，诊断重复、空洞、视角与对白问题 | 低 lint 分证明好文笔或真人创作 |
| 全书 / 分卷 / 章场目标，人物、规则与伏笔台账 | 有大纲就等于写完整部 |
| 按媒介选格式，分集 / 分场到完整正文 | 文学剧本、拍摄稿、分镜是同一种交付 |
| 保存跨会话状态、最近正文、下一步与未决事项 | 模型凭记忆绝不丢线 |
| 检查正文覆盖、记录新鲜度、承诺处置与评阅证据 | 脚本能判断伏笔自然、战力合理或商业成功 |
| 回归测试、微型作品闭环、独立操作评阅 | 已完成几十万字真实长篇试验或外部检测验证 |

完整作品需要实际生成全部约定正文、逐章（集）修订与终局回读。工具登记的 assisted 评阅是模型辅助评阅，不能写成真实读者背书。

## 文档索引

- [references/README.md](references/README.md)：64 份文档与规则台账的分类索引（路由 / 流程 / 小说工艺 / 文体 / 边界与检测 / 研究档案）。
- [templates/README.md](templates/README.md)：模板分工、每章更新、整书核读与台账检查语义。
- [SKILL.md](SKILL.md)：智能体执行入口，含任务分派表与共同边界。

## 维护原则

1. **定向维护**：只改有明确问题的文档或程序，不做无证据的“全面升级”。
2. **文档与程序分开留证**：文档修改、试用记录、程序回归各自说明范围，互不冒认。
3. **不追分**：不为了压低分数调整阈值、不为了让检查变绿放宽口径。

变更详情见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

[Apache License 2.0](LICENSE)。
