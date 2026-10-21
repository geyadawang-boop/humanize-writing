# AI 对照样本登记（tests/corpus_ai）

本目录 4 篇为 **LLM 生成的同文体开发对照样本**，与 `tests/corpus/` 的真人语料按文体配对。历史 t13 使用了“盲测”名称；这些样本后来参与selftest回归，而人类对照曾用于门控标定。因此当前重跑仅为历史冻结语料回归与探索性来源阈值统计，不是新的独立外部验证。脚本和样本旧路径保留。

## 配对关系

| AI 样本 | 真人配对语料 | 文体 | 门控 |
|---|---|---|---|
| ai_law_memo.md | law_gongbao_hongxiufeng.md | 法律文书（法律意见书） | law |
| ai_email_reply.md | email_liangdishu.md | 邮件（工作通知） | email |
| ai_speech_ceremony.md | speech_wen_yiduo_zuihou.md | 演讲稿（开学典礼） | speech |
| ai_fiction_excerpt.md | fiction_kong_yiji.md | 小说（都市情感片段） | fiction |

## 生成声明

- 生成方：TRAE 智能体（与本 skill 同一开发会话），生成日期 2026-09-18。
- 生成方式：按各文体的常见委托场景，以模型**默认风格**写作——未针对 lint 的检查项做规避，也未刻意堆砌 AI 特征，未做人工"降 AI"后处理。
- 文件保持纯正文（与 tests/corpus 同规则），不内嵌说明文字，保证 lint 计分对象干净。

## 同源局限（必读）

- 样本与被测 lint **同源**：由同一开发线的同一模型生成，且各文体仅 1 篇（n=4+4）。
- 因此盲测指标**只能作方向性参考**，不构成对检测器泛化性能的估计；README 中按此口径声明。
- 后续若引入第三方 AI 语料或多人多模型样本，凭新证据修订本表并记 changelog。
