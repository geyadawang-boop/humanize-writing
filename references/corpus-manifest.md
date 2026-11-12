# 语料清单与来源（v0.60）

本文件登记随包分发的语料、项目内冻结语料，以及**有但未随包分发**的公开数据集。每条都写明来源、许可、用途与核查状态；许可不明的一律标出，不当作可自由再分发。

核查日期：2026-11-12。许可证会变，再分发或商用前请按链接回到上游确认。

---

## 1. 随包分发的新语料（`corpora/pairs/`）

| 项 | 内容 |
|---|---|
| 名称 | HC3-Chinese 中文同题配对子集 |
| 上游 | https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese |
| 镜像 | https://www.modelscope.cn/datasets/simpleai/HC3-Chinese |
| 论文 | https://arxiv.org/abs/2301.07597 |
| 许可 | **CC BY-SA 4.0**（HuggingFace `cardData.license`，2026-11-12 核对） |
| 许可全文 | https://creativecommons.org/licenses/by-sa/4.0/ |
| 原始文件 | `all.jsonl`，21,726,779 字节 |
| sha256 | `425e7071bbd5dd88efd85d51e28a5adec9c72e04d96c52d194bdfb95fef00b0d` |
| 语言 | 简体中文（上游混有少量繁体/异体，未统一转换） |
| 体裁 | 网络问答、百科、金融、法律、NLPCC 问答 |
| 规模 | 5203 对（人写 + ChatGPT 回答） |
| 用途 | 训练/校准/测试 `scripts/ai_rate.py`；规则证据测量 |

切分与文件：

| 文件 | 配对数 | 字节 | sha256（前 12 位） |
|---|---|---|---|
| `hc3_train.jsonl` | 3667 | 4,815 KB | `83c9faaf8ed4` |
| `hc3_cal.jsonl` | 823 | 1,071 KB | `777fa9811b55` |
| `hc3_test.jsonl` | 713 | 944 KB | `da51b874e392` |

字段：`id / domain / human / ai / human_len / ai_len / source / license`。

处理规则（`scripts/corpus_build.py`）：

- 每侧至少 80 汉字，截断到 1200 汉字（按句末标点收口）；
- 剔除 URL、邮箱、电话；剔除含自伤、色情、暴力等高风险词的整对；
- 同一问题只留一条；`psychology`、`medicine` 默认排除（含个人健康披露）；
- 按 `sha256(id)` 取模切分，同一 pair 不跨训练/校准/测试；
- **不保存上游 prompt 原文**，只保留配对关系与主题域。

再分发注意：CC BY-SA 4.0 要求署名并以相同许可共享。若你把它并入自己的作品分发，需保留本表信息与许可链接；`NOTICE` 已登记。

---

## 2. 项目内既有冻结语料（`tests/`）

这些是仓库原有的回归/校准集，v0.60 未改动内容，仍由原有测试驱动。

| 目录 | 文件数 | 体量 | 内容 | 许可/来源 | 用途 |
|---|---|---|---|---|---|
| `tests/corpus/` | 5 | 60 KB | 鲁迅《孔乙己》、闻一多《最后一次的讲演》、梁启超家书、最高法公报裁判文书 | 公版作品 / 官方公开文书；逐篇 URL 见 `tests/corpus/SOURCES.md` | lint 设计样本 |
| `tests/corpus_hc3/` | 61 | 252 KB | HC3-Chinese 抽样（法律、百科等，人写 + ChatGPT） | CC BY-SA 4.0；`tests/corpus_hc3/SOURCES.md` 登记 sha256 | 跨来源回归与盲测 |
| `tests/corpus_cred/` | 360（本地生成） | 1.5 MB | C-ReD 抽样（作文、影评、论文；9 个模型 + 人写） | **上游未声明许可证**；样本不随仓库/包分发，见第 4 节 | 跨语料评估（本地研究用途） |
| `tests/corpus_classic/` | 12 | 72 KB | 鲁迅、朱自清等 11 篇公版散文/小说/演讲/诏书 | 公版；逐篇 URL 与繁简转换说明见 `SOURCES.md` | 人写误报测试 |
| `tests/corpus_ai_calib/` | 8 | 40 KB | 独立会话生成的 7 篇多文体 AI 样本 | 本项目生成；协议见 `CALIB.md` | 校准（允许调参） |
| `tests/samples/` | 5 | 36 KB | 合成正反例 | 本项目生成 | 单元测试 |

`tests/corpus_classic` 的取得方式需要说明：正文经一份用户提供的资料报告转引 `zh.wikisource.org`，再由 OpenCC（opencc-python-reimplemented 0.1.7，t2s）统一转为简体；除繁转简外未改写正文。该目录的 11 篇中有 6 篇为节选（报告自带“篇幅限制省略”标注），逐篇边界见其 `SOURCES.md`。

---

## 3. 未随包分发的公开数据集（可按脚本/链接自行获取）

| 数据集 | 语言/规模 | 许可核查 | 未随包分发的原因 |
|---|---|---|---|
| **C-ReD** https://github.com/HeraldofLight/C-ReD | 中文，128,610 条（12,997 人写 / 115,613 AI），5 域，9 模型 | **未声明**：仓库根目录无 LICENSE 文件（`/LICENSE` 返回 404，2026-11-12 核）；论文为 ACL 2026 Findings | 许可不明，不能随包再分发；`tests/corpus_cred` 是本项目早期抽样，仅作本地研究对照 |
| **M4 / M4GT-Bench** https://github.com/mbzuai-nlp/M4GT-Bench | 多语言、多生成器、多领域；数据在 Google Drive | 仓库根目录无 LICENSE（404）；论文 ACL 2024 | 无法通过脚本稳定拉取；许可未声明 |
| **RAID** https://huggingface.co/datasets/liamdugan/raid | 英文，600 万+ 生成样本，11 模型 / 8 域 / 11 攻击 | **MIT**（HF `cardData.license`）；`train.csv` 约 11.7 GB | 体量过大；英文为主，与本技能中文场景不符 |
| **HC3 全量（英文）** https://huggingface.co/datasets/Hello-SimpleAI/HC3 | 英/中，10K–100K | CC BY-SA 4.0 | 已用中文子集；英文全量对中文校准无直接增益 |
| **webnovel-chinese** https://huggingface.co/datasets/wdndev/webnovel-chinese | 中文网文，约 9000 本、约 9B tokens | 卡片声明 Apache-2.0，但正文为网络小说原文，**权利链不清** | 不能据此再分发；如自用需自行评估版权 |
| **Zhihu-KOL** | 中文知乎问答 | 访问返回 401，未取得 | 不可得 |

---

## 4. 已知问题（必须一起读）

1. **C-ReD 的许可缺口（已处置）。** `tests/corpus_cred/` 来自 C-ReD；上游仓库没有 LICENSE。现在只保留 `SOURCES.md`、`MANIFEST.md` 作为来源登记，360 个样本（`human_*.md` / `ai_*.md`）已从 git 与 npm 包移除；需要时用 `tests/build_cred_corpus.py --repo <目录>` 在本机重建，依赖该语料的方向测试会自动 skip。
2. **HC3 的模型单一。** 随包语料的 AI 侧全部是 ChatGPT（2022 年），不覆盖 Qwen、DeepSeek、GLM 等中文模型；跨模型泛化**未验证**，校准报告已如实标注。
3. **问答体偏差。** 语料是人类网络回答与 ChatGPT 回答，长度中位数约 170–184 字。小说、公文、学术、诗歌不在分布内。
4. **公版文本的版本问题。** `tests/corpus_classic` 经二手报告转引并繁转简，可能与权威版本有异文；用于统计可以，用于引文校对不行。
5. **不能把“随包语料”当 benchmark。** 它经过筛选、截断与去重，规模也小于上游全量；指标只对本包成立。

---

## 5. 重建与校验

```bash
# 重建新语料（需 HC3-Chinese all.jsonl）
python -B scripts/corpus_build.py --hc3 /path/to/all.jsonl

# 校验文件完整性
python -B - <<'PY'
import hashlib, json
m = json.load(open('corpora/manifest.json', encoding='utf-8'))
for name, info in m['splits'].items():
    h = hashlib.sha256(open(info['path'], 'rb').read()).hexdigest()
    print(name, h == info['sha256'])
PY

# 重建 C-ReD 抽样（需自行取得上游数据，注意许可）
python -B tests/build_cred_corpus.py --repo /path/to/C-ReD
```

`corpora/manifest.json` 记录了上游 sha256、过滤器、域分布、切分规则与每个输出文件的校验和；`tests/test_corpus_manifest.py` 会在测试中校验这些值。
