# corpus_cred 来源登记（C-ReD 抽样语料）

## 用途声明

本目录语料**仅用于测量（r8 新测量），不用于调参或校准**。校准/盲测分离纪律沿用 `tests/corpus_ai_calib/CALIB.md`；引入第三方语料须同步修订 CALIB.md 的既定承诺（r9 执行）。

## 来源

- **数据集**：C-ReD（Chinese Real-vs-AI Detection benchmark），128,610 样本（human 12,997 / AI 115,613），5 域 × 9 生成器。
- **论文**：ACL 2026 Findings, pp. 42703–42733（arXiv 2604.11796）。
- **仓库**：`github.com/HeraldofLight/C-ReD`，HEAD commit `b90072cd218b6ebdbd1d1478ce6e439677f18192`（2026-07-06 "Update README.md"）。
- **取得方式**：`git clone --depth 1 https://github.com/HeraldofLight/C-ReD.git`（2026-09-20 克隆至本机临时目录；raw.githubusercontent.com 与 github.com 直连均可用，api.github.com 当时限流）。样本不随仓库分发；重建命令见文末。
- **许可**：**仓库未附 LICENSE 文件**（已核实 `/blob/main/LICENSE` 404）。引用以论文条目为准；语料仅作本地测量用途，不再分发。

## 抽样协议（确定性，可复现）

构建脚本：`tests/build_cred_corpus.py`；逐文件来源与哈希：`MANIFEST.md`。

1. **域选择**：仅取 3 域——composition / film review / paper。news 不取（无对应门控，新闻体裁的电头导语结构偏离本技能测量目标）；question answer 不取（与 corpus_hc3 百科问答同域，信号重复）。
2. **human 抽样**：按 CSV 原始 id 顺序遍历，剔除不合格样本（见下）后取前 30 条/域。
3. **AI 抽样**：9 生成器各取 10 条/域；仅取 CJK 字数落在该域全部合格 human 源池参考长度 ±50% 窗内的样本（原序取前）；跨生成器共享去重池。参考长度沿用历史构建器排序后的上中位数 `lens[len(lens)//2]`，不是实收前30篇的中位数。
4. **历史抽样窗**（全源池上中位数 → AI 窗）：composition 752 → [376, 1128]；film review 118 → [100, 177]；paper 298 → [149, 447]。保留此算法以可复现冻结样本；新报告同时区分全源池常规中位数、历史窗参考值、实收中位数。
5. **纯度过滤**：CJK 字数 < 100 剔除；含 URL / 中国大陆电话号码 / U+FFFD 替换符剔除。
6. **去重**：正文剥空白后前 40 字作键，human 域内去重、AI 跨生成器去重。
7. **写出**：纯正文 UTF-8 无 BOM，末尾恰一换行；文件名沿用 corpus_hc3 范式。

## 域 → 门控映射

| C-ReD 域 | 文件名 slug | 门控 | 实收 |
|---|---|---|---|
| composition | `credcomposition` | fiction | 30 human + 90 AI |
| film review | `credfilm`（取首词） | general | 30 human + 90 AI |
| paper | `credpaper` | academic | 30 human + 90 AI |

合计 360 文件（human 90 / AI 270），全部足额，无窗口内缺额。

## 实收统计

| 域 | 实收 human 中位 CJK | 实收 AI 中位 CJK | human 实收 | 每生成器实收 |
|---|---:|---:|---:|---|
| composition | 559.5 | 595.0 | 30 | 9 生成器 × 10 |
| film review | 100.5 | 133.5 | 30 | 9 生成器 × 10 |
| paper | 173.5 | 208.5 | 30 | 9 生成器 × 10 |

2026-09-26 校正：旧表的752/118/298实际是构建窗使用的全源池参考值，误标为实收中位数。本表按冻结文件重算标准中位数（偶数样本取中间两数平均）；360份文件与原MANIFEST哈希一致，未重建或改写任何样本。

全库长度分布（CJK 字数）：min 100 / 中位 201 / max 934。

**9 生成器**：claude-3.5-haiku、deepseek-r1、deepseek-v3、doubao-1.5-pro、gemini-2.5-flash、gpt-3.5-turbo、gpt-4o、qwen-2.5、qwen-3（短名依次 claude35haiku / deepseekr1 / deepseekv3 / doubao15pro / gemini25flash / gpt35turbo / gpt4o / qwen25 / qwen3）。

## 命名范式

- `human_cred<slug>_NN.md`（NN = 01–30）
- `ai_cred<slug>_<生成器短名>_NN.md`（NN = 01–10）

## 局限（如实声明）

1. **窗约束不等于实收长度分布匹配**：film review 实收 human 中位100.5字、范围100–112，AI中位133.5、范围100–177。短文归一仍受组间长度差异影响，不能将得分差异全部归因于来源。AI窗口也压缩了自由输出长度分布；composition、paper同样须连同实收两组长度解释。
2. **原序抽样非随机**：确定性优先于随机性（可复现、可审计），样本不代表数据集整体分布，仅代表"窗内靠前样本"。
3. **体裁不对称**：paper 域 human 样本为真实论文摘要/段落（含 `paper_title` 等元数据已剥离），AI 样本为模型生成的论文式文本，两者写作任务设定并非严格对齐。
4. **生成器版本时效**：AI 样本反映 2024–2026 年各模型输出风格，不代表其后版本的检测表现。
5. **无 LICENSE**：见"来源"节，仅本地测量使用；样本不进入 git 仓库与 npm 包。

## 重建

```bash
python -B tests/build_cred_corpus.py --repo /path/to/C-ReD
```

也可用环境变量 `CRED_REPO` 指定仓库根目录；脚本会寻找其中的 `benchmark data/`，按本文协议确定性写出 360 个样本，并重写 `MANIFEST.md`。
