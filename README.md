# humanize-writing

面向中文写作的 AI 技能包：让小说、网文、剧本、诗歌、散文、议论文、学术论文、研究生学位论文与演讲稿**写得完整、写得清楚、写出声音**。

| 项目 | 说明 |
|---|---|
| 当前版本 | v0.51（程序与 lint 规则集 0.43） |
| 文档语言 | 简体中文 |
| 运行依赖 | Python 3.8+，仅标准库，无需安装第三方包 |
| 许可证 | [Apache-2.0](LICENSE) |
| 变更记录 | [CHANGELOG.md](CHANGELOG.md) |

## 一、这是什么

`humanize-writing` 是一份可直接装入 AI 智能体（Claude Code、Trae 等支持 `SKILL.md` 的环境）的**写作技能包**。它不是一组提示词模板，而是一套可路由的知识体系加可执行的检查工具：

- **创作**：短篇、散文、诗歌、文章、长篇小说、网文、电影/剧集/短剧/话剧/广播剧，从立项到整部修订。
- **编辑**：改稿、去模板感、文风提升、只查不改的评阅、标题拟定。
- **管理**：长篇项目的状态、大纲、正文清单、连续性台账、跨会话交接与完结验收。
- **检查**：静态写作线索扫描、台账完整性与红线审计。

**它不做什么**：不承诺降低 AI 检测率，不鉴定作者身份，不把小伎俩当成"人味"。去模板感只是编辑需求中的一种；把所有作品改到低分不是本项目的目标。

## 二、核心原理

### 1. 先认任务，再读知识

每次任务先分清四个维度：**操作**（新写/续写/改稿/评阅/改编）→ **作品**（文体与媒介）→ **阶段**（立项/推进/修订/完结）→ **症状**（当前具体问题）。入口只有一条：[统一路由](references/routing.md)。旧 A–I 模式仅作兼容别名。

按需加载，单次优先解决一两个主要问题，不把 62 份 `references` 塞进一次创作。这是本技能与"大而全提示词"的根本区别：**知识量不等于上下文里的字数量**。

### 2. 知识、记录、程序三层分离

| 层 | 载体 | 负责 | 不负责 |
|---|---|---|---|
| 知识 | `references/` | 讲清"怎么判断、为什么这样判断" | 不知道你的项目实际写到哪 |
| 记录 | `templates/` + `project-state.json` | 保存已经发生的事实、计划与承诺 | 不会替你写正文 |
| 程序 | `scripts/` | 检查文件契约、记录自洽与静态线索 | 不判断文学质量，不后台自动运行 |

三者混用是最常见的误用：把 lint 分数当作品判决、把空模板当已完成、把计划当已写。

### 3. 技法不是配额

句长分布、三幕结构、黄金三章、章末钩子、每卷字数、Scene/Sequel 配比、Show/Tell 百分比，都只是**可选诊断工具**。按题材、节奏与用户契约调整，不为凑数破坏作品。文档中未附稿约的"必须/禁用/固定比例"一律按经验建议理解；而已核实且适用的法律、平台发布规则会单独标注适用范围，不降级为偏好。

### 4. 只有一条判断优先级链

**用户目标与事实/原作约束 → 交付格式 → 人物、因果与连续性 → 可读性与声音 → 静态指标。**

出现冲突时按这条链裁决，只在 [文体适配](references/genre-router.md) 与 [编辑流程](references/editing-workflow.md) 集中定义，不在各分册另设相反门槛。

### 5. 检查不等于质量保证

- `ai_smell_lint.py` 输出的是**静态命中强度**（0–100 的加权计数），JSON 中明确标记 `is_ai_probability=false`，25/40 只是提示阈值。
- `ledger_check.py` 只检查伏笔、战力、改纲、疑问、情绪窗口与完结处置的记录是否自洽；红灯黄灯都不等于"作品好/坏"。
- 缺失文件、错表头、空表、占位符会被记为"检查未完成"，**不允许假绿**。

### 6. 改稿以"声音契约"收口

改稿前先约定必须保留什么（事实、立场、语气、专业格式），改完对照**原稿 / 修订稿 / 保留项**三方判断收益。不承诺"AI 率必降或归零"，不为降分加错字、伪造经历、硬插口头语或改掉立场。

## 三、能做什么

| 场景 | 交付物 | 首读入口 |
|---|---|---|
| 改稿、去模板感、文风提升 | 修订稿 + 保留项说明 | [编辑流程](references/editing-workflow.md) |
| 只查不改、评阅已有稿 | 带位置、影响与优先级的评阅 | [编辑流程](references/editing-workflow.md) |
| 解释 AI 检测报告 / 核验评分变化 | 口径核查与证据边界说明 | [检测证据与资料要求](references/detection-principles.md) |
| 起标题、改标题 | 按数量要求给候选 | [标题工艺](references/title-craft.md) |
| 新写短篇、散文、诗歌、文章 | 正文成稿 | [统一路由](references/routing.md) |
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

## 四、目录结构

```text
humanize-writing/
├── SKILL.md                 # 智能体入口：任务识别、执行边界、交付纪律
├── README.md                # 本文件：定位、原理、功能与用法
├── CHANGELOG.md             # 版本变更记录
├── LICENSE                  # Apache-2.0
├── references/              # 62 份按需读取的工艺、流程与证据文档
│   ├── README.md            # 分类索引（建议从这里进入）
│   ├── routing.md           # 唯一任务分派入口
│   ├── editing-workflow.md  # 改稿 / 评阅 / 停止条件
│   ├── novel-workflow.md    # 小说与网文全程
│   ├── screenplay-workflow.md   # 剧本全程
│   ├── project-workflow.md  # 项目状态、工具与检查证据
│   └── ...
├── templates/               # 13 份项目模板（见 templates/README.md）
├── scripts/                 # 3 个仅用标准库的脚本
│   ├── writing_project.py   # 11 个子命令的项目记录器
│   ├── ledger_check.py      # 6 组台账检查
│   └── ai_smell_lint.py     # 静态写作线索扫描
└── tests/                   # 11 组单元测试 + selftest + 6 套冻结语料
```

## 五、安装与快速开始

**1. 放入技能目录**

把整个仓库目录复制到智能体的用户级 skills 目录，例如：

```text
Claude Code（Windows）: C:\Users\<用户名>\.claude\skills\humanize-writing
Claude Code（macOS/Linux）: ~/.claude/skills/humanize-writing
```

Trae 或其他支持 `SKILL.md` 的环境放入各自的 skills 目录即可。技能以自身根目录定位脚本，不依赖当前工作目录。

**2. 验证安装**

```text
python -B tests/selftest.py
python -B -m unittest discover -s tests -p "test_*.py"
```

**3. 直接对话触发**

- "把这篇三千字散文改掉模板感，保留我的观点和真实经历，告诉我改了哪里、为什么。"
- "新建一部 30 章的校园悬疑网文，先给故事 bible 和前 3 章大纲，不要一次写完。"
- "只看不改，评阅这三集竖屏短剧，按严重程度排序，标出具体位置。"
- "解释一下这份 AI 检测报告：我的分为什么变了，哪些结论能信？"

## 六、命令行工具

三个脚本都只用 Python 标准库，不要求安装 hook 或 CI，也不会在后台自动执行。

### 6.1 writing_project.py：项目记录器

```text
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
| `complete` / `reopen` | 完结与完结后重开修订 |

初始化后只是**待填写项目**，不是合格作品；须先写 bible、大纲与计划，再实际写正文并更新台账。完整字段与命令以 [项目执行](references/project-workflow.md) 及 `--help` 为准。

### 6.2 ledger_check.py：台账审计

```text
python -B scripts/ledger_check.py <项目目录> --current-chapter 12 --current-volume 1
python -B scripts/ledger_check.py <项目目录> --current-chapter 30 --current-volume 1 --final
python -B scripts/ledger_check.py --demo
```

六组检查：伏笔兑现与唤醒、战力更新断档、大纲调整记录、已抛出疑问负担、已完成章情绪窗口、完结处置（`--final`）。阈值可用 `--short-gap`、`--mid-gap`、`--questions-hard` 等参数调整，属项目审计策略而非文学定律，详见 [模板说明](templates/README.md)。

确实没有记录时，可在对应文件写明确声明（`foreshadowing=none` 等并附原因）；空模板不能自动当作"没有问题"。

### 6.3 ai_smell_lint.py：静态写作线索

```text
python -B scripts/ai_smell_lint.py --genre fiction --json <稿件.md>
python -B scripts/ai_smell_lint.py --language en <draft.md>
python -B scripts/ai_smell_lint.py -            # 从 stdin 读取
```

- 分数区间只作编辑提示：`<25` 静态命中较少，`25–40` 适中，`>40` 较多；不等于文本质量。
- 文体门控：`general / tech / academic / official / law / email / speech / fiction`，各文体豁免项不同。
- 语言声明：`auto / zh / en / mixed`。`auto` 不是语言识别器；中文不足 100 字时未声明文本只作有限扫描。
- v0.41–v0.43 起，句长标准差、短句占比、重复"不是……而是……"、段落长度、正则锚点密度均为**零权重观察**，不再计分，也不设配额。

### 6.4 退出码约定

| 工具 | 0 | 1 | 2 |
|---|---|---|---|
| `writing_project.py` | 操作成功 / 所查范围通过 | 未齐、过期或未通过 | 参数、路径或状态格式错误 |
| `ledger_check.py` | 检查完整且无红线（仍可能有黄线） | 存在红线 | 输入不完整或调用错误（优先于红线） |
| `ai_smell_lint.py` | 未超静态阈值 | 超过静态阈值，需按文体核读 | 输入不足、语言未确认或参数错误 |

退出码 0 只说明**该工具在该口径下通过了**，不构成作品质量结论。

## 七、验证现状与能力边界

**回归方式**

```text
python -B tests/selftest.py
python -B -m unittest discover -s tests -p "test_*.py" -v
```

应同时看正例与反例：空模板拒绝、计划内伏笔不误报、战力逐行判级、正文或台账改动后评阅失效、小说与剧本的完整微型示例，以及真实请求的路由行为。

**已记录范围**

- 历史记录（v0.38）：81 项自动测试、lint 自测与技能格式校验通过；完成 4015 汉字六章短篇网文（含文件交接续写）与 2252 汉字三集九场微型剧本，均为模型辅助评阅的完整草稿。
- v0.39–v0.40：追加文学选段实改、连载局部只读评阅与新写短请求试用，保留首轮缺陷与修正记录；446 份冻结语料正文未改。
- v0.41–v0.48：只调整文档与 lint 计分口径，程序主体保持不变；跨版本分数变化不能当作文风改善。
- v0.49（2026-10-23）：补齐议论文、学术论文、研究生学位论文、演讲稿四个非虚构文体专章，新增零权重 `[分行]` 测量提示；六类文体来源各 ≥100 条。
- v0.50–v0.51（2026-10-24）：短诗也能拿到 `[分行结构]` 行级位置统计；v0.51 修正长文本不可达、清单/表格误报与句末标点判据，并加版本一致性守卫。
- 本次整理（2026-10-21）：`selftest.py` 通过，155 项 unittest 全部通过；结构测试同时校验本地链接、UTF-8 与 LF 行尾。
- 本次维护（2026-10-24）：`selftest.py` RC=0，**175 项 unittest 全部通过**；链接可达性、版本一致性、无 CRLF 与冻结分数逐项复核。

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

## 八、文档索引

- [references/README.md](references/README.md)：62 份文档的分类索引（路由 / 流程 / 小说工艺 / 文体 / 边界与检测 / 研究档案）。
- [templates/README.md](templates/README.md)：模板分工、每章更新、整书核读与台账检查语义。
- [SKILL.md](SKILL.md)：智能体执行入口，含任务分派表与共同边界。

## 九、维护原则

1. **定向维护**：只改有明确问题的文档或程序，不做无证据的"全面升级"。
2. **文档与程序分开留证**：文档修改、试用记录、程序回归各自说明范围，互不冒认。
3. **不追分**：不为了压低分数调整阈值、不为了让检查变绿放宽口径。

变更详情见 [CHANGELOG.md](CHANGELOG.md)。

## 十、许可证

[Apache License 2.0](LICENSE)。
