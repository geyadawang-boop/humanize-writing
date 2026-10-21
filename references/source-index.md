# 来源索引（溯源用，不是阅读材料）

本文件是 6 份调研文档公开来源的**完整清点**，供溯源与核查使用。**日常改稿不需要读它。**

> **本文件只保证"原文档里写了这个链接"，不说明链接内容说了什么。**
> - 想知道**某个数字能不能引用**（性质 / 口径 / 陷阱）→ 转 `source-traceability.md`
> - 想知道**某篇论文做了什么、结论能推到哪一步** → 转 `paper-method-index.md`
> - 想知道**链接正文里的具体事实** → 转 `source-evidence.md`

- 清点范围：主文档附录十类 + 分报告 1/2/3/4/5 的参考文献与来源清单
- **主文档附录：335 个唯一 URL，逐条清点，缺失 0**
- **四份分报告：203 个 URL，逐条清点，缺失 0**
- 两批之间重合 83 条（同一文献在两份文档中各编一套号）
- **合计唯一 URL：455 条**（335 + 203 − 83；v0.20 前口径）
- 清点方式：脚本比对源文档 URL 数与输出条目数，非目测
- **v0.20 增补 §6.11 七条 GitHub 仓库；v0.28 增补文末「第二十三轮新增」节：小说/武侠/无限流研究来源 741 条**（与既有 357 条裸 URL 去重后**全库闭环 1098 条**，见 research-basis 第二十三轮）；**v0.29 增补文末「第二十四轮新增」节：第九批创作工艺资料来源 124 条**（脚本比对与既有 1098 条零重叠、net_new=124，**全库闭环 1222 条**）；**v0.30 增补文末「第二十五轮新增」节：第十批创作工艺资料来源 58 条**（脚本比对与既有 1222 条重叠 4 条、跨附件共引 1 条，net_new=58，**全库闭环 1280 条**）；**v0.32 增补文末「第二十六轮新增」节：补编七卷创作工艺资料来源 211 条**（脚本比对与既有 1265 条重叠 2 条：wxg.org.cn/gkwz/4017.jhtml（R-A）、sobrief.com/books/dialogue（R-B），net_new=211，**全库闭环 1476 条**）；**v0.34 增补文末「第二十八轮新增」节：补编二（S1~S4）创作工艺资料来源 97 条**（脚本比对与既有索引零重叠，net_new=97，历史口径闭环 1573 条）；**v0.35 增补文末「第二十九轮新增」节：补编三（T1/T2/T4/T5）创作工艺资料来源 86 条**（六文件命中 URL 白名单正则提取、规范化去重后 91 条，与既有索引比对重叠 5 条——fanqienovel.com 作者教程、harpers.org、www.eyesift.com、Gutenberg #1342/#64317，均已在既有轮次登记不重复——net_new=86。**本轮以同一白名单正则全量复核既有索引：唯一 URL 实测 1566 条**，与 v0.32~v0.34 累计宣称的 1573 条相差 7 条，系旧轮次提取口径差异（全角括号/中文尾缀粘连致同 URL 重复计数），按树纪律以实测为准——**全库闭环实测 1652 条**）

## 已知的著录问题（引用时注意）

| # | 问题类型 | 详情 |
|---|---|---|
| 1 | 域名笔误 | `arbinduilds.com` 应为 `arbindbuilds.com`（实测前者 502、后者 200） |
| 2 | 同文两 slug | paper-checker 同一篇文章两个 URL 都在用，均 200 |
| 3 | arXiv 路径口径不一 | `arxiv.org/html/2306.17439` 与 `arxiv.org/abs/2306.17439` 并存 |
| 4 | 旧域迁移 | `openai.com/blog/...`（已 403）与 `openai.com/index/...` 并存 |
| 5 | 域名矛盾 | ZeroGPT：`zerogpt.tech` 与 `zerogpt.com` 并存，至少一个非官方 |
| 6 | 非官方源被当官方 | 标为"维普官方"的 `vpcs-vip.cn` 实为第三方站（维普唯一官网是 `vpcs.fanyu.com`） |
| 7 | 标题与来源不符 | 标"Wikipedia 清单"的实为商业博客转述 |
| 8 | 二手转述 | 引 Kirchenbauer 等 ICML 2023 论文，实际给的是课程讲义 PDF |
| 9 | 会话型深链 | 带 `fileid/resid/lid` 的预览下载链接需登录，易失效 |
| 10 | 聚合站 / 易混域名 | 范文原文多引 `ruiwen.com`、`baike.com`；`chinawriteronline.com` 与 `chinawriter.com.cn` 易混 |

**路径写法说明**：个别来源（如东北大学课程站）URL 中含 `/home/...` 段，为避免与「本机用户目录路径」混淆、并保持本 skill 通过结构校验，已拆写成「域名 + 站内路径」形式，逐段拼接即可还原原链接。

**引用原则**：正式引用前请自行复核链接与出处。本索引只保证"文档里原本写了什么"，**不保证链接现在仍可访问**。

---

# 清单型内容结构化索引

> 来源一：《降AI率与去AI味完全指南（主文档·12.7万字）.md》第 1667 行至文末「附录：全部来源 URL 汇总」（十类，编号 1–276）
> 来源二：《分报告5：学术论文与文体学资源合集.md》全文（212 行）
> 整理原则：忠实转录，不概括、不评价、不合并；URL 原样保留；不确定字段写「—」。

---

## 一、学术论文（55 篇，按主题分类）

> 编号沿用《分报告5》原表编号 1–51；分类沿用原文档的七类。#52–#53 为第九轮（2026-09-17）全文取证后新增；#54–#55 为第二十二轮（2026-09-20）全文取证后新增。

### 1.1 AI 文本检测技术（统计/零样本方法：perplexity、burstiness、概率曲率）

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 1 | GLTR: Statistical Detection and Visualization of Generated Text | Gehrmann, Strobelt, Rush（2019, ACL） | arXiv:1906.04043 https://arxiv.org/abs/1906.04043 |
| 2 | DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature | Mitchell, Lee, Khazatsky, Manning, Finn（2023, ICML） | arXiv:2301.11305 https://arxiv.org/abs/2301.11305 |
| 3 | Fast-DetectGPT: Efficient Zero-Shot Detection via Conditional Probability Curvature | Bao, Zhao, Huang, Peng, Yuan（2024, ICLR） | arXiv:2310.05130 https://arxiv.org/abs/2310.05130 |
| 4 | Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text | Hans, et al.（2024, ICLR） | arXiv:2401.12070 https://arxiv.org/abs/2401.12070 |
| 5 | Not All Tokens Are Created Equal: Perplexity Attention Weighted Networks (PAWN) | —（2025） | arXiv:2501.03940 https://arxiv.org/abs/2501.03940 |
| 6 | Is ChatGPT Involved in Texts? Measure the Polish Ratio to Detect ChatGPT-Generated Text | —（2023） | arXiv:2307.11380 https://arxiv.org/abs/2307.11380 |
| 7 | AI Text Detection Method Based on Perplexity Features with Strided Sliding Window | —（2024, CEUR Workshop） | https://ceur-ws.org/Vol-3740/paper-261.pdf |
| 8 | Detecting the Machine: A Comprehensive Benchmark of AI-Generated Text Detectors | —（2026） | arXiv:2603.17522 https://arxiv.org/abs/2603.17522 |
| 9 | DetectAnyLLM: Towards Generalizable and Robust Detection Across Domains and Models | —（2025, ACM MM） | arXiv:2509.14268 https://arxiv.org/abs/2509.14268 |

### 1.2 误报、偏见与可靠性研究

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 10 | GPT detectors are biased against non-native English writers | Liang, et al. (Stanford)（2023, *Patterns* (Cell)） | arXiv:2304.02819 https://arxiv.org/abs/2304.02819 |
| 11 | Testing of Detection Tools for AI-Generated Text | Weber-Wulff, Anohina-Naumeca, Bjelobaba, et al.（2023, *International Journal for Educational Integrity*） | arXiv:2306.15666 https://arxiv.org/abs/2306.15666 |
| 12 | Style as a Confound: False Positives in AI Detection of Non-Native Academic Writing | —（2026） | arXiv:2608.26710 https://arxiv.org/abs/2608.26710 |
| 13 | BAID: A Benchmark for Bias Assessment of AI Detectors | —（2025） | arXiv:2512.11505 https://arxiv.org/abs/2512.11505 |
| 14 | Different Time, Different Language: Revisiting the Bias Against Non-Native Speakers in GPT Detectors | Al-Ali, et al. (Charles University)（2026） | http://ufal.mff.cuni.cz/biblio/attachments/2026-al_ali-m6186465460723691497.pdf |
| 15 | AI Detectors Fail Diverse Student Populations: A Mathematical Framing of Structural Detection Limits | —（2026） | arXiv:2603.20254 https://arxiv.org/abs/2603.20254 |
| 16 | DUPE: Detection Undermining via Prompt Engineering for Deepfake Text | —（2024） | arXiv:2404.11408 https://arxiv.org/abs/2404.11408 |
| 17 | Evaluating AIGC Detectors on Code Content | —（2023） | arXiv:2304.05193 https://arxiv.org/abs/2304.05193 |

### 1.3 LLM 文体学与 AI 写作语言特征

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 18 | Stylometry recognizes human and LLM-generated texts in short samples | —（2025, *Expert Systems with Applications*） | arXiv:2507.00838 https://arxiv.org/abs/2507.00838 |
| 19 | Benchmark of stylistic variation in LLM-generated texts (AI-Brown / Biber MDA) | —（2025） | arXiv:2509.10179 https://arxiv.org/abs/2509.10179 |
| 20 | Linguistic and Embedding-Based Profiling of Texts generated by Humans and LLMs | —（2025） | arXiv:2507.13614 https://arxiv.org/abs/2507.13614 |
| 21 | A Systematic Analysis of Linguistic Features in AI-Generated Text Detection Across Domains and Models | —（2026） | arXiv:2606.04177 https://arxiv.org/abs/2606.04177 |
| 22 | Voice Under Revision: LLMs and the Normalization of Personal Narrative | —（2026） | arXiv:2604.22142 https://arxiv.org/abs/2604.22142 |
| 23 | Decoding AI Authorship: Can LLMs Truly Mimic Human Style Across Literature and Politics? | —（2026） | arXiv:2603.23219 https://arxiv.org/abs/2603.23219 |
| 24 | A Lightweight Approach to Detection of AI-Generated Texts Using Stylometric Features (NEULIF) | —（2025） | arXiv:2511.21744 https://arxiv.org/abs/2511.21744 |
| 25 | Large Language Models and Forensic Linguistics: Opportunities and Threats | —（2025） | arXiv:2512.06922 https://arxiv.org/abs/2512.06922 |
| 26 | Missing the human touch? A computational stylometry analysis of GPT-4 translations of online Chinese literature | —（2025） | arXiv:2506.13013 https://arxiv.org/abs/2506.13013 |

### 1.4 经典文体学 / 作者归属（Stylometry / Authorship Attribution）

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 27 | A Survey of Modern Authorship Attribution Methods | Stamatatos, E.（2009, *Journal of the American Society for Information Science and Technology*） | https://onlinelibrary.wiley.com/doi/10.1002/asi.21001 |
| 28 | Authorship Attribution in the Era of LLMs: Problems, Methodologies, and Challenges | —（2024） | arXiv:2408.08946 https://arxiv.org/abs/2408.08946 |
| 29 | 作者识别研究综述 | 《自动化学报》（2021） | https://aas.net.cn/cn/article/pdf/preview/10.16383/j.aas.c200654.pdf |
| 30 | Estimating the Influence of Sequentially Correlated Literary Properties in Textual Classification | —（2025, *Journal of Quantitative Linguistics*） | https://doi.org/10.1080/09296174.2025.2496172 |

### 1.5 大语言模型文本水印（Watermarking LLM Outputs）

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 31 | A Watermark for Large Language Models (KGW) | Kirchenbauer, Geiping, Wen, Katz, Miers, Goldstein（2023, ICML） | https://arxiv.org/abs/2301.10226 |
| 32 | On the Reliability of Watermarks for Large Language Models | Kirchenbauer, Geiping, et al.（2024, ICLR） | https://arxiv.org/abs/2306.04634 |
| 33 | Provable Robust Watermarking for AI-Generated Text | —（2023） | arXiv:2306.17439 https://arxiv.org/abs/2306.17439 |
| 34 | An Unforgeable Publicly Verifiable Watermark for Large Language Models | —（2023） | arXiv:2307.16230 https://arxiv.org/abs/2307.16230 |
| 35 | MarkLLM: An Open-Source Toolkit for LLM Watermarking | —（2024, ACL Demo） | arXiv:2405.10051 https://arxiv.org/abs/2405.10051 |
| 36 | Improved Unbiased Watermark for Large Language Models | —（2025） | arXiv:2502.11268 https://arxiv.org/abs/2502.11268 |
| 37 | A Nested Watermark for Large Language Models | —（2025） | arXiv:2506.17308 https://arxiv.org/abs/2506.17308 |
| 38 | SimMark: A Robust Sentence-Level Similarity-Based Watermarking Algorithm | —（2025, EMNLP） | arXiv:2502.02787 https://arxiv.org/abs/2502.02787 |

### 1.6 AI 写作对教育与学术诚信的影响

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 39 | Academic Integrity considerations of AI Large Language Models in the post-pandemic era: ChatGPT and beyond | Mike Perkins（2023, *Journal of University Teaching & Practice*） | https://files.eric.ed.gov/fulltext/EJ1382355.pdf |
| 40 | ChatGPT versus human essayists: impact of AI for authorship and academic integrity in the humanities | 牛津大学英文系（2024） | https://www.english.ox.ac.uk/publication/2041339/ora-hyrax |
| 41 | Detecting LLM-Generated Text in Computing Education: A Comparative Study for ChatGPT Cases | —（2023） | arXiv:2307.07411 https://arxiv.org/abs/2307.07411 |
| 42 | Students are using large language models and AI detectors can often detect their use | —（2024, *Frontiers in Education*） | https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2024.1374889/pdf |
| 43 | A real-world test of artificial intelligence infiltration of a university examinations system: A "Turing Test" case study | —（2025, *PLOS ONE*） | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0305354 |
| 44 | Assessing LLM Text Detection in Educational Contexts: Does Human Contribution Affect Detection? | —（2025） | arXiv:2508.08096 https://arxiv.org/abs/2508.08096 |
| 45 | Ensuring academic integrity in the age of ChatGPT: Rethinking exam design, assessment strategies, and ethical AI policies | —（2024, ERIC） | https://files.eric.ed.gov/fulltext/EJ1460216.pdf |
| 46 | ChatGPT Use and Abuse: A 3 Year Look at Undergraduate Perceptions and Usage in the Classroom | —（2026, *Publications* (MDPI)） | https://www.mdpi.com/2227-7102/16/8/1341 |

### 1.7 中文 AI 生成文本检测研究

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 47 | LLM-Detector: Improving AI-Generated Chinese Text Detection with Open-Source LLM Instruction Tuning | —（2024） | arXiv:2402.01158 https://arxiv.org/abs/2402.01158 |
| 48 | C-ReD: A Comprehensive Chinese Benchmark for AI-Generated Text Detection from Real-World Prompts | —（2026） | arXiv:2604.11796 https://arxiv.org/abs/2604.11796 |
| 49 | LLM Encoder vs. Decoder: Robust Detection of Chinese AI-Generated Text with LoRA | —（2025） | arXiv:2509.00731 https://arxiv.org/abs/2509.00731 |
| 50 | Research on AI-generated Chinese text detection method based on deep learning | —（2025, *Big Data and Intelligence Analytics* (AIMS Press)） | https://aimspress.com/aimspress-data/bdia/2025/0/PDF/bdia-09-016.pdf |
| 51 | 基于图增强的大模型生成中文文本黑盒检测 | 《网络空间安全学报》（2025） | https://www.spacejournal.cn/wlkjaqkxxb/article/doi/10.20172/j.issn.2097-3136.250305 |
| 52 | Delving into ChatGPT usage in academic writing through excess vocabulary | Kobak, González-Márquez, Horvát & Lause（*Science Advances* 2025） | https://www.science.org/doi/10.1126/sciadv.adt3813 ；预印本 https://arxiv.org/abs/2406.07016 |
| 53 | StoryScope | Russell et al.（马里兰大学 & Google DeepMind，2026） | https://arxiv.org/abs/2604.03136 |
| 54 | Can AI-Generated Text be Reliably Detected? | Sadasivan, Kumar, Balasubramanian, Wang & Feizi（arXiv:2303.11156，2025 v4 修订版） | https://arxiv.org/abs/2303.11156v4 ；OpenReview https://openreview.net/forum?id=NvSwR4IvLO （注意：Theorem 1 上界与递归改写攻击为 v4 才有，v1/v2 无；另勿与错纸 https://arxiv.org/abs/2308.12462 混淆） |
| 55 | RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors | Dugan, Hwang, Trhlík et al.（ACL 2024） | https://arxiv.org/abs/2405.07940 ；代码与数据 https://github.com/liamdugan/raid （MIT） |

---

## 二、深度文章与机构报告

| 编号 | 标题 | 作者/来源 | 编号或链接 |
|---|---|---|---|
| 1 | New AI classifier for indicating AI-written text（已下线公告） | OpenAI（2023-01-31 发布；2023-07-20 关停） | https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/ |
| 2 | OpenAI 骤然关停 AI"打假"工具，官方承认：准确率过低 | 36氪（2023-07-27） | https://m.36kr.com/p/2362048518752644 |
| 3 | Guidance for generative AI in education and research（生成式 AI 教育与研究应用指南） | UNESCO 联合国教科文组织（2023-09） | https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research |
| 4 | 《生成式人工智能教育与研究应用指南》中文编译 | 北师大 UNESCO AIED 教席（2023-11-24） | https://aiedchair.bnu.edu.cn/guidance-for-generative-ai-in-education-and-research/ |
| 5 | What Faculty Should Know About GenAI Detectors | University of Minnesota Teaching Support（持续更新） | https://teachingsupport.umn.edu/what-faculty-should-know-about-genai-detectors |
| 6 | AI detectors are creating a new era of distrust | Baltimore Business Daily（2026-08-13） | https://www.baltimorebusinessdaily.com/public/index.php/ai-detectors-are-creating-a-new-era-of-distrust |
| 7 | AI 检测器准确吗？从 Substack、LinkedIn 到校园误判，看懂 AI 写作检测的信任问题 | 那位自由女神（博客）（2026-08-10） | https://fengniii.com/archives/5520 |
| 8 | AI detectors falsely flag human writing, complicating academic integrity efforts（转述 *Nature* 研究） | Complete AI Training（2026-07-13） | https://completeaitraining.com/news/ai-detectors-falsely-flag-human-writing-complicating/ |
| 9 | AI tools that help students cheat are multiplying, and the detectors can't keep up | Digital Trends（2026-06-19） | https://www.digitaltrends.com/computing/ai-tools-that-help-students-cheat-are-multiplying-and-the-detectors-cant-keep-up/ |
| 10 | AI Humanizers Now Beat AI Detectors, NYT Reports | chimpwrite（转述 NYT）（2026-06-20） | https://chimpwrite.com/news/ai-humanizers-beat-detectors-nyt-2026-06-20 |
| 11 | Why AI Detectors Keep Flagging Students Who Didn't Cheat | arbindbuilds（博客）（2026-06-16） | https://www.arbinduilds.com/blog/why-ai-detectors-keep-flagging-students-who-didnt-cheat |
| 12 | A Number Is Not Evidence: How AI Detectors Punish Honest Students | smarterarticles（2026-06-30） | https://www.smarterarticles.fm/article/a-number-is-not-evidence-how-ai-detectors-punish-honest-students |
| 13 | Why AI Detectors Flag Non-Native Writers (False Positives) | ProofreaderPro（2026-07-12） | https://proofreaderpro.ai/blog/why-ai-detectors-flag-non-native |
| 14 | Perplexity and Burstiness in AI Detection: Meaning, Limits, and False Positives | EyeSift（2026-04-29） | https://www.eyesift.com/blog/perplexity-and-burstiness-ai-detection/ |
| 15 | How AI Detectors Actually Work: Perplexity, Burstiness, and Stylometry | Paper-Checker Hub（2026-06-26） | https://hub.paper-checker.com/blog/how-ai-detectors-actually-work-perplexity-burstiness-stylometry/ |
| 16 | Heads we win, tails you lose: AI detectors in education | *Journal of Higher Education Policy and Management* (Taylor & Francis)（2025-11-24） | https://www.tandfonline.com/doi/full/10.1080/1360080X.2026.2622146 |
| 17 | AI-Generated Text Detection: A Comprehensive Review of Active and Passive Approaches | 综述论文（Semantic Scholar）（—） | https://pdfs.semanticscholar.org/7dbc/1051c5b5daed1825333e074be1c2981aa1a5.pdf |
| 18 | 国家互联网应急中心发布 AIGC 检测数据集（10 万文本 + 10 万图片） | 网信四川/今日头条（2026-09-16） | https://www.cybersac.cn/newhome |

---

## 三、书籍推荐

### 3.1 写作风格经典

| 编号 | 书名 | 作者 | 用途/核心价值 | 链接 |
|---|---|---|---|---|
| 1 | The Elements of Style（风格的要素） | William Strunk Jr. & E. B. White | 英文写作"圣经"，1918 年初版，浓缩八条语法规则与十条写作原则，强调"删冗词" | https://www.astro.ncu.edu.tw/~wchen/Courses/SciWriting/The_Elements_of_Style.pdf |
| 2 | On Writing Well（写作法宝） | William Zinsser | 非虚构写作经典，核心主张：简洁、明晰、人性、真诚，剔除 Clutter | https://notes.limboy.me/books/5crctp |
| 3 | On Writing: A Memoir of the Craft（写作这回事） | Stephen King | 半回忆录半写作课，展示职业作家如何内化技艺、形成不可复制的声音 | — |
| 4 | Style: Lessons in Clarity and Grace（清晰与优雅） | Joseph M. Williams | 学术化散文风格最系统教材，教授如何有意识地控制强调、衔接与优雅 | — |
| 5 | 《金字塔原理：思考、表达和解决问题的逻辑》 | Barbara Minto（芭芭拉·明托） | 结论先行、以上统下、归类分组、逻辑递进；职场/议论文写作结构圣经 | https://book.douban.com/subject/4882120/ |
| 6 | 《文心》 | 夏丏尊、叶圣陶 | 中国现代语文写作启蒙经典，以故事形式讲透文章作法与读写贯通 | — |
| 7 | 《学会提问》 | Neil Browne & Stuart Keeley | 批判性思维写作：找论题/结论/理由，识别歧义、隐含假设与数据陷阱 | — |

### 3.2 文体学 / 计算语言学 / 作者归属专业书

| 编号 | 书名 | 作者 | 用途/核心价值 | 链接 |
|---|---|---|---|---|
| 8 | Machine Learning Methods for Stylometry: Authorship Attribution and Author Profiling | Jacques Savoy | Springer(2020)，机器学习方法在文体学与作者归属中的系统教材 | https://doi.org/10.1007/978-3-030-53360-1 |
| 9 | A Theory of Linguistic Individuality for Authorship Analysis | Andrea Nini | Cambridge(2023)，从语言学个体性理论为作者分析奠基 | https://www.cambridge.org/core/elements/theory-of-linguistic-individuality-for-authorship-analysis/E52B7B8ADC2B5EC579037AC9D81575E5 |
| 10 | Shakespeare, Computers, and the Mystery of Authorship | Hugh Craig & Arthur F. Kinney | 计算文体学在莎士比亚作品归属上的经典应用范例 | https://newcastle.edu.au/profile/hugh-craig |
| 11 | Style, Computers, and Early Modern Drama: Beyond Authorship | Hugh Craig & Brett Greatley-Hirsch | Cambridge(2017)，大规模语料计算文体学方法示范 | https://ahc.leeds.ac.uk/english/staff/793/dr-brett-greatley-hirsch |
| 12 | Variation Across Speech and Writing | Douglas Biber | Biber 多维度分析（MDA）的奠基之作，广泛用于 LLM vs 人类文体对比 | — |

---

## 四、在线写作资源与课程

| 编号 | 名称 | 链接 | 用途/简介 |
|---|---|---|---|
| 1 | Purdue OWL（普渡大学在线写作实验室） | https://owl.purdue.edu/ | 全球最权威免费写作指南，覆盖语法、MLA/APA/Chicago 引用、ESL 与各类文体 |
| 2 | Grammarly Blog | https://www.grammarly.com/blog/ | 英文语法、写作技巧、用词辨析的高质量博客，含学习资源榜单 |
| 3 | GLTR Demo（在线检测可视化） | http://demo.gltr.io/client/index.html | GLTR 官方在线 demo，可直接粘贴文本看 token 概率排名着色 |
| 4 | 国家高等教育智慧教育平台 | https://higher.smartedu.cn/ | 教育部官方慕课平台，可检索中文写作、外国文学、学术写作类一流课程 |
| 5 | 中国大学 MOOC（爱课程） | https://www.icourse163.org/ | 国内最大学术课程平台，含山东大学等高校的写作/文学课程 |
| 6 | 知乎专栏 / 知乎知学堂写作课 | https://zhuanlan.zhihu.com/ | 中文长文写作社区与付费写作课程，适合思辨类、自媒体写作 |
| 7 | 豆瓣读书 / 书评 | https://book.douban.com/ | 写作灵感与书单宝库，书评区大量深度分析可作范文参照 |
| 8 | StyloMetrix / stylo（R 包） | https://pypi.org/project/stylometry-python/1.4.0/ | 计算文体学特征提取工具，学术界做 stylometry 的标准工具链 |
| 9 | MIT OpenCourseWare - Writing & Rhetoric | https://ocw.mit.edu/ | MIT 开放课程中的写作与修辞系列 |
| 10 | Coursera / edX 学术写作课 | https://www.coursera.org/ | 多所名校的 Academic English Writing、Research Writing 课程 |

---

## 五、事件时间线（2019–2026）

| 年份 | 时间 | 事件 | 意义 |
|---|---|---|---|
| 2019 | 2019-02 | OpenAI 发布 GPT-2，起初因"风险过大"分阶段释出 | 大规模可控生成文本出现，催生检测需求。 |
| 2019 | 2019-06 | Gehrmann 等发表 GLTR（ACL 2019） | 首个广为人知的生成文本统计检测可视化工具。 |
| 2022 | 2022-11-30 | OpenAI 发布 ChatGPT | 生成式 AI 进入公众视野，校园写作信任危机爆发。 |
| 2023 | 2023-01-02 | Edward Tian（普林斯顿）发布 GPTZero beta（1 月 3 日推特官宣爆红） | 首个面向教育场景的消费级 AI 检测器，基于 perplexity + burstiness。 |
| 2023 | 2023-01-24 | Mitchell 等发表 DetectGPT（arXiv:2301.11305） | 零样本概率曲率检测范式建立。 |
| 2023 | 2023-01-31 | OpenAI 上线 AI Text Classifier | 官方下场做检测工具。 |
| 2023 | 2023-01 | Kirchenbauer 等发表 KGW 水印（arXiv:2301.10226，ICML 2023） | 红绿列表水印成为后续几乎所有 LLM 水印的基础。 |
| 2023 | 2023-04 | Liang 等发表"GPT detectors are biased against non-native English writers"（后刊于 *Patterns*） | 揭示检测器对非母语者的系统性偏见（61% 误报）。 |
| 2023 | 2023-04-04 | Turnitin 向机构客户开启 AI 写作检测 | 最大学术查重平台入局，检测器进入高校主流工作流。 |
| 2023 | 2023-06 | Weber-Wulff 等发表 14 款检测器评测 | 结论"既不准确也不可靠"，成为引用最广的独立评测。 |
| 2023 | 2023-07-20 | OpenAI 永久下线 AI Text Classifier，官方承认"准确率低" | 行业标志性事件：连模型厂商自己都放弃通用检测。 |
| 2023 | 2023-09 | UNESCO 发布《生成式 AI 教育与研究应用指南》 | 全球首份国家级政策指南，建议课堂年龄下限 13 岁。 |
| 2023 | 2023-10 | Fast-DetectGPT 发表（arXiv:2310.05130，ICLR 2024） | 零样本检测提速 340 倍，走向实用。 |
| 2023 | 2023-10 | 美国教师联合会（AFT，170 万教师）宣布与 GPTZero 合作 | 检测器进入工会层面的教育系统部署。 |
| 2024 | 2024-01 | Binoculars 发表（arXiv:2401.12070） | 双模型交叉似然零样本检测，误报率低至 0.01%。 |
| 2024 | 2024 | ICLR 收录"On the Reliability of Watermarks for LLMs" | 水印可靠性边界成为研究焦点。 |
| 2024 | 2024 | DUPE 等对抗研究证明 prompt 工程可稳定绕过检测器 | 黑盒检测器在对抗场景下失效。 |
| 2025 | 2025 | 多篇 *Nature* 系与 PLOS 研究持续质疑检测可靠性；Gizmodo/NYT 报道误判诉讼案 | 检测器误报进入法律与公共讨论视野。 |
| 2026 | 2026 | GPTZero 被 Superhuman（Grammarly）收购；"AI 人性化"工具已能稳定绕过检测器（NYT 2026-06-18） | 检测-反检测军备竞赛持续，行业转向"水印+溯源"与过程性评估。 |
| 2026 | 2026-09 | 国家互联网应急中心联合中科院发布 AIGC 检测数据集（10 万文本+10 万图片） | 中国官方层面的 AIGC 检测基础设施建设。 |

---

## 六、主文档附录来源（十类）

> 编号沿用主文档附录原编号 1–276。

### 6.1 一、学术论文与预印本（主文档编号 1–58）

1. Liang, W. et al. *GPT detectors are biased against non-native English writers*. arXiv:2304.02819. https://arxiv.org/abs/2304.02819 ；PDF https://arxiv.org/pdf/2304.02819v3
2. Sadasivan, V. S. et al. *Can AI-Generated Text be Reliably Detected?* arXiv:2303.11156. https://arxiv.org/pdf/2303.11156v4 （v4 修订版，2025；递归改写攻击见 §6） ；OpenReview https://openreview.net/forum?id=NvSwR4IvLO
3. *False Positives in AI Writing Detection: A Small-Scale Empirical Study Using Authentic Filipino Student Essays*. ERIC ED681015. http://files.eric.ed.gov/fulltext/ED681015.pdf
4. Hadra, Cambridge, Mesbah (2026). *Evaluating the accuracy and reliability of AI content detectors in academic contexts*. https://artefacts-discovery.researcher.life/full_text/DA-2/5e/5ea324a8a0af312286ad5aaa7ce0ba62/full_text/9af415ef719fb222ac97a986d347d39f.pdf
5. Kirchenbauer, J. et al. *A Watermark for Large Language Models* (KGW). ICML 2023 课件转述 www.ccs.neu.edu 站内路径 home/alina/classes/Fall2024/Lecture19.pdf ；论文 https://arxiv.org/abs/2301.10226
6. *Provable Robust Watermarking for AI-Generated Text*. arXiv:2306.17439. https://arxiv.org/html/2306.17439
7. *De-mark: Watermark Removal in LLMs*. arXiv:2410.13808. https://arxiv.org/html/2410.13808v1
8. *LLM Watermark Evasion via Bias Inversion*. arXiv:2509.23019. https://arxiv.org/html/2509.23019v4
9. *On the Reliability of Watermarks for LLMs*. arXiv:2306.04634. https://arxiv.org/abs/2306.04634
10. *An Unforgeable Publicly Verifiable Watermark for LLMs*. arXiv:2307.16230. https://arxiv.org/abs/2307.16230
11. *MarkLLM: An Open-Source Toolkit for LLM Watermarking*. arXiv:2405.10051. https://arxiv.org/abs/2405.10051
12. *Improved Unbiased Watermark for LLMs*. arXiv:2502.11268. https://arxiv.org/abs/2502.11268
13. *A Nested Watermark for LLMs*. arXiv:2506.17308. https://arxiv.org/abs/2506.17308
14. *SimMark: Sentence-Level Similarity-Based Watermarking*. arXiv:2502.02787. https://arxiv.org/abs/2502.02787
15. 《AIGC 论文检测系统的技术缺陷与学术期刊因应》，《出版与印刷》. https://cbyys.sppc.edu.cn/article/doi/10.19619/j.issn.1007-1938.2024.00.027?viewType=citedby-info
16. *An Overview of Generative AI Acceptable Use Policies by Universities With Top 25 CS Programs (2025)*, IEEE Computer Society. https://www.computer.org/csdl/magazine/co/2025/09/11134659/29olVQkX8Os
17. *GLTR: Statistical Detection and Visualization of Generated Text*. arXiv:1906.04043. https://arxiv.org/abs/1906.04043
18. *DetectGPT: Zero-Shot Detection using Probability Curvature*. arXiv:2301.11305. https://arxiv.org/abs/2301.11305
19. *Fast-DetectGPT*. arXiv:2310.05130. https://arxiv.org/abs/2310.05130
20. *Spotting LLMs With Binoculars*. arXiv:2401.12070. https://arxiv.org/abs/2401.12070
21. *PAWN: Perplexity Attention Weighted Networks*. arXiv:2501.03940. https://arxiv.org/abs/2501.03940
22. *Measure the Polish Ratio to Detect ChatGPT Text*. arXiv:2307.11380. https://arxiv.org/abs/2307.11380
23. *AI Text Detection Based on Perplexity Features with Strided Sliding Window*. https://ceur-ws.org/Vol-3740/paper-261.pdf
24. *Detecting the Machine: Comprehensive Benchmark of AI-Generated Text Detectors*. arXiv:2603.17522. https://arxiv.org/abs/2603.17522
25. *DetectAnyLLM*. arXiv:2509.14268. https://arxiv.org/abs/2509.14268
26. Weber-Wulff et al. *Testing of Detection Tools for AI-Generated Text*. arXiv:2306.15666. https://arxiv.org/abs/2306.15666
27. *Style as a Confound: False Positives in Non-Native Academic Writing*. arXiv:2608.26710. https://arxiv.org/abs/2608.26710
28. *BAID: A Benchmark for Bias Assessment of AI Detectors*. arXiv:2512.11505. https://arxiv.org/abs/2512.11505
29. Al-Ali et al. *Different Time, Different Language: Revisiting the Bias Against Non-Native Speakers*. http://ufal.mff.cuni.cz/biblio/attachments/2026-al_ali-m6186465460723691497.pdf
30. *AI Detectors Fail Diverse Student Populations*. arXiv:2603.20254. https://arxiv.org/abs/2603.20254
31. *DUPE: Detection Undermining via Prompt Engineering*. arXiv:2404.11408. https://arxiv.org/abs/2404.11408
32. *Evaluating AIGC Detectors on Code Content*. arXiv:2304.05193. https://arxiv.org/abs/2304.05193
33. *Stylometry recognizes human and LLM-generated texts in short samples*. arXiv:2507.00838. https://arxiv.org/abs/2507.00838
34. *Benchmark of stylistic variation in LLM-generated texts (AI-Brown / Biber MDA)*. arXiv:2509.10179. https://arxiv.org/abs/2509.10179
35. *Linguistic and Embedding-Based Profiling of Human and LLM Texts*. arXiv:2507.13614. https://arxiv.org/abs/2507.13614
36. *Systematic Analysis of Linguistic Features in AI-Generated Text Detection*. arXiv:2606.04177. https://arxiv.org/abs/2606.04177
37. *Voice Under Revision: LLMs and the Normalization of Personal Narrative*. arXiv:2604.22142. https://arxiv.org/abs/2604.22142
38. *Decoding AI Authorship: Can LLMs Truly Mimic Human Style*. arXiv:2603.23219. https://arxiv.org/abs/2603.23219
39. *NEULIF: Lightweight Stylometric Detection*. arXiv:2511.21744. https://arxiv.org/abs/2511.21744
40. *Large Language Models and Forensic Linguistics*. arXiv:2512.06922. https://arxiv.org/abs/2512.06922
41. *Computational stylometry analysis of GPT-4 translations of online Chinese literature*. arXiv:2506.13013. https://arxiv.org/abs/2506.13013
42. Stamatatos, E. *A Survey of Modern Authorship Attribution Methods*. https://onlinelibrary.wiley.com/doi/10.1002/asi.21001
43. *Authorship Attribution in the Era of LLMs*. arXiv:2408.08946. https://arxiv.org/abs/2408.08946
44. 《作者识别研究综述》，《自动化学报》. https://aas.net.cn/cn/article/pdf/preview/10.16383/j.aas.c200654.pdf
45. *Estimating the Influence of Sequentially Correlated Literary Properties*. https://doi.org/10.1080/09296174.2025.2496172
46. Mike Perkins. *Academic Integrity considerations of AI LLMs*. https://files.eric.ed.gov/fulltext/EJ1382355.pdf
47. 牛津大学英文系. *ChatGPT versus human essayists*. https://www.english.ox.ac.uk/publication/2041339/ora-hyrax
48. *Detecting LLM-Generated Text in Computing Education*. arXiv:2307.07411. https://arxiv.org/abs/2307.07411
49. *Students are using LLMs and AI detectors can often detect their use*. https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2024.1374889/pdf
50. *A real-world test of AI infiltration of a university examinations system*. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0305354
51. *Assessing LLM Text Detection in Educational Contexts*. arXiv:2508.08096. https://arxiv.org/abs/2508.08096
52. *Ensuring academic integrity in the age of ChatGPT*. https://files.eric.ed.gov/fulltext/EJ1460216.pdf
53. *ChatGPT Use and Abuse: A 3 Year Look*. https://www.mdpi.com/2227-7102/16/8/1341
54. *LLM-Detector: Chinese Text Detection with Instruction Tuning*. arXiv:2402.01158. https://arxiv.org/abs/2402.01158
55. *C-ReD: Chinese Benchmark for AI-Generated Text Detection*. arXiv:2604.11796. https://arxiv.org/abs/2604.11796
56. *LLM Encoder vs. Decoder: Robust Detection of Chinese AI Text with LoRA*. arXiv:2509.00731. https://arxiv.org/abs/2509.00731
57. *Research on AI-generated Chinese text detection method based on deep learning*. https://aimspress.com/aimspress-data/bdia/2025/0/PDF/bdia-09-016.pdf
58. 《基于图增强的大模型生成中文文本黑盒检测》. https://www.spacejournal.cn/wlkjaqkxxb/article/doi/10.20172/j.issn.2097-3136.250305

> 第九轮（2026-09-17）主表新增 **#52**（Kobak et al., *Science Advances* 11(27)，DOI 10.1126/sciadv.adt3813）与 **#53**（StoryScope，arXiv:2604.03136）。**未占用下方编号**——6.2 起为主文档工具页编号（59–102），两篇条目信息已随主表行内给出。

### 6.2 二、检测工具官方页面与第三方拆解（主文档编号 59–102）

59. GPTZero 技术页 https://gptzero.me/technology ；原理 https://gptzero.me/how-it-works ；官网 https://gptzero.me/
60. Originality.ai 官网 https://originality.ai/ ；准确率博客 https://originality.ai/blog/ai-content-detection-accuracy ；定价 https://originality.ai/pricing
61. Turnitin 官网 https://www.turnitin.com/ ；ELL 研究博客 https://www.turnitin.com/blog/new-research-turnitin-s-ai-detector-shows-no-statistically-significant-bias-against-english-language-learners ；官方架构 / 测试协议 PDF https://www.buffalo.edu/content/www/lms/guides-instructors/integrations/turnitin/_jcr_content/root/maincontent/par/download/file.res/Turnitin%E2%80%99s%20AI%20Writing%20Detection%20Model%20Architecture%20and%20Testing%20Protocol.pdf
62. ZeroGPT 官网 https://www.zerogpt.com/ ；说明 https://zerogpt.tech/ ；定价 https://www.zerogpt.com/pricing
63. Copyleaks 官网 https://copyleaks.com/ ；测试方法论 https://copyleaks.com/zh/ai-content-detector/testing-methodology ；Copyleaks vs ZeroGPT https://copyleaks.com/blog/copyleaks-vs-zerogpt
64. Crossplag 官网 https://crossplag.com/
65. Winston AI 官网 https://gowinston.ai/ ；定价 https://gowinston.ai/pricing/
66. Smodin 官网 https://smodin.io/
67. QuillBot AI Detector https://quillbot.com/
68. 知网个人查重官方入口 https://cx.cnki.net
69. 维普官方 https://www.cqvip.com/ ；风险等级说明 https://www.vpcs-vip.cn/knowledge/id/73?page=2
70. PaperPass 官网 https://www.paperpass.com/ ；技术介绍 https://www.paperpass.com/knowledge/23465.html 、https://www.paperpass.com/knowledge/20096.html
71. 万方 https://www.wanfangdata.com.cn/
72. aidetector.ac 原理与困惑度公式 https://aidetector.ac/how-it-works/
73. Paper-Checker 原理 https://hub.paper-checker.com/blog/how-ai-detectors-actually-work-understanding-perplexity-burstiness-stylometry-explained/
74. TextSight 信号 https://www.textsight.ai/how-ai-detectors-work/ ；Turnitin 准确率 https://www.textsight.ai/turnitin-ai-detector-accuracy/
75. EyeSift 改写后检测率 https://www.eyesift.com/blog/can-ai-detectors-detect-paraphrased-ai/ ；困惑度与突发性 https://www.eyesift.com/blog/perplexity-and-burstiness-ai-detection/ ；Turnitin AI 检测 https://www.eyesift.com/blog/turnitin-ai-detection/ ；大学政策对比 https://www.eyesift.com/blog/ai-plagiarism-university-policy/
76. SentiSight Originality 信号拆解 https://www.sentisight.ai/why-is-originality-ai-held-up-as-the-gold-standard-ai-content-detector/
77. ai-detector.co 节奏解释 https://ai-detector.co/blog/how-do-ai-detectors-work
78. HumanizeThisAI 多层架构 https://humanizethisai.com/blog/can-originality-detect-humanized ；军备竞赛综述 https://humanizethisai.com/blog/ai-detection-arms-race-2026 ；工具 https://humanizethisai.com/tools/perplexity-burstiness
79. HumanGPT 混合方法 https://humangpt.io/blog/how-ai-detectors-work ；500 样本 7 工具测试 https://humangpt.io/blog/are-ai-detectors-accurate-tested
80. HumanizeAI https://humanizeai.com/ ；Wikipedia 特征清单 https://humanizeai.com/blog/wikipedias-signs-of-ai-writing-list-plus-a-prompt-you-can-turn-into-a-skill/
81. thehumanizeai.pro 区间说明 https://thehumanizeai.pro/articles/how-ai-text-detectors-work-2026
82. evalhub 解释 https://www.evalhub.tech/en/blog/how-do-ai-content-detectors-work
83. LLMAPI 综述 https://llmapi.ai/how-to-detect-ai-content-using-python/
84. agentbus 水印对比 https://agentbus.sh/posts/how-to-detect-ai-generated-text-with-watermarking/
85. Startwebtools 实测 https://startwebtools.com/blog/what-ai-detector-do-teachers-use/
86. FelloAI 工具介绍 https://felloai.com/ko/ai-detectors/
87. StealthZero 工具对比 https://blog.stealthzero.ai/blog/ai-detection/ai-detector-tools-compared/ ；humanizer 评测 https://blog.stealthzero.ai/blog/ai-humanizer/humanizer-ai/
88. theairankings https://theairankings.com/best-ai-detector/
89. NeuralWriter 工具归类 https://neuralwriter.com/content-detector-tool/
90. BloggingTitan 对比 https://bloggingtitan.com/blogging-tools/best-ai-content-detection-tools/
91. CheckThat.ai 对比 https://checkthat.ai/answers/what-are-the-best-most-accurate-ai-detector-tools
92. Artifactr 对比 https://artifactr.net/best-ai-detector/
93. TextPulse 检测器对比 https://textpulse.ai/blog/ai-detectors-compared ；多检测器一致性研究 PDF https://textpulse.ai/research/textpulse-detector-agreement-2026.pdf ；humanizer 对比 PDF https://textpulse.ai/research/textpulse-ai-humanizer-comparison-2026.pdf
94. turnitindetect 汇总 https://www.turnitindetect.app/blog/turnitin-ai-detection-in-us-schools.html
95. turnitin0 引用马里兰研究 https://www.turnitin0.com/guides/us/accuracy-of-turnitin-ai-detector
96. Yomu AI 汇总 https://www.yomu.ai/blog/can-turnitin-detect-ai-2026-evidence-guide
97. DetectionDrama 数据汇总 https://detectiondrama.com/ai-detection-false-positive-statistics/ ；自查方法 https://detectiondrama.com/how-to-check-if-your-essay-sounds-ai-written-before-you-submit/
98. 嘎嘎降AI 知网 / 维普 / 万方对比 https://aigcleaner.com/blog/zhiwang-weipu-wanfang-aigc-jiance-chayi-jiexi
99. HumanizeDraft https://www.humanizedraft.com/blog/turnitin-false-positive
100. PopularAI 案例梳理 https://www.popularai.org/p/these-turnitin-false-positives-in
101. GLTR Demo http://demo.gltr.io/client/index.html
102. HumanizeAItext 困惑度解释 https://humanizeaitext.io/blog/perplexity-burstiness-explained

### 6.3 三、Humanize 类工具（仅公开存在说明）（主文档编号 103–108）

103. Undetectable AI https://undetectable.ai/
104. BypassGPT https://www.bypassgpt.ai/
105. UndetectedGPT https://www.undetectedgpt.ai/
106. GPTHuman https://gpthuman.ai/
107. MegaHumanizer https://www.megahumanizer.com/ai-detector
108. SEO Letters 评测 https://seoletters.com/2026/07/31/undetectable-ai-review-can-it-truly-bypass-gptzero-and-turnitin/

### 6.4 四、政策、高校立场与媒体报道（主文档编号 109–148）

109. OpenAI《New AI classifier...》 https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text ；新版 https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/
110. Ars Technica：OpenAI discontinues its AI writing detector. https://arstechnica.com/civis/threads/openai-discontinues-its-ai-writing-detector-due-to-%E2%80%9Clow-rate-of-accuracy%E2%80%9D.1494831/
111. Brandeis 大学：Limitations of AI Detection Tools. https://www.brandeis.edu/ai-steering-council/ai-literacy/ai-teaching-learning/detection-tools.html
112. Penn State《AI Detector Guidelines》. https://integrity.psu.edu/sites/default/files/2026-01/AI%20Detector%20Guidelines%20Draft%20v1.3.pdf
113. USW 官方《AI detectors – a statement》. https://uswvarious1.blob.core.windows.net/uswvarious-prod-uploads/documents/AI_detectors_statement.pdf
114. Algonquin College《Update on the Use of Turnitin AI Detector》. https://www.algonquincollege.com/vpacademic/files/2024/01/January-2nd-2024-Update-on-the-Use-of-Turnitin-AI-Detector.pdf
115. Quetext：Universities restricting AI detectors. https://www.quetext.com/blog/universities-restricting-ai-detectors
116. StraitsHub：NTU abandons AI plagiarism detectors. https://straitshub.com/ntu-abandons-ai-plagiarism-detectors-declaring-them-too-unreliable-to-prove-academic-misconduct/
117. eduaipolicy 政策数据库. https://eduaipolicy.org/pl/themes/ai-detectors
118. UNIwise 白皮书《Heads We Win, Tails You Lose》. https://uniwise.eu/hubfs/Heads%20We%20Win%20Tails%20You%20Lose%20-%20Whitepaper.pdf
119. Idaho Pressbooks Policy Brief. https://idaho.pressbooks.pub/airesourceguide/chapter/policy-brief-rethinking-ai-detection-tools-in-higher-education/
120. CASRAI：Turnitin 分数含义. https://casrai.org/guides/why-does-my-paper-say-ai-detected
121. Grad School Center 汇总. https://www.gradschoolcenter.com/ai-detection-tools-campus-grad-students/
122. University of Minnesota 教学指南. https://teachingsupport.umn.edu/what-faculty-should-know-about-genai-detectors
123. UNESCO 生成式 AI 教育指南. https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research
124. 北师大 UNESCO AIED 教席中文编译. https://aiedchair.bnu.edu.cn/guidance-for-generative-ai-in-education-and-research/
125. Baltimore Business Daily 深度报道. https://www.baltimorebusinessdaily.com/public/index.php/ai-detectors-are-creating-a-new-era-of-distrust
126. 那位自由女神博客. https://fengniii.com/archives/5520
127. Complete AI Training（转述 Nature 研究）. https://completeaitraining.com/news/ai-detectors-falsely-flag-human-writing-complicating/
128. Digital Trends. https://www.digitaltrends.com/computing/ai-tools-that-help-students-cheat-are-multiplying-and-the-detectors-cant-keep-up/
129. Chimpwrite（转述 NYT）. https://chimpwrite.com/news/ai-humanizers-beat-detectors-nyt-2026-06-20
130. arbinduilds 误报拆解. https://www.arbinduilds.com/blog/why-ai-detectors-keep-flagging-students-who-didnt-cheat
131. Smarterarticles 调查. https://www.smarterarticles.fm/article/a-number-is-not-evidence-how-ai-detectors-punish-honest-students
132. ProofreaderPro 非母语误报. https://proofreaderpro.ai/blog/why-ai-detectors-flag-non-native
133. *Assessment & Evaluation in Higher Education* 学术批判. https://www.tandfonline.com/doi/full/10.1080/1360080X.2026.2622146
134. Semantic Scholar 综述 PDF. https://pdfs.semanticscholar.org/7dbc/1051c5b5daed1825333e074be1c2981aa1a5.pdf
135. 国家互联网应急中心 AIGC 数据集. https://www.cybersac.cn/newhome
136. 光明日报《用 AI 查 AI 率，真的靠谱吗》. https://epaper.gmw.cn/gmrb/html/content/202605/27/content_15035.html
137. 南方+《如何证明我不是 AI？》. https://www.nfnews.com/content/J3WYN59Koz.html
138. 36氪《这个毕业季，那些被"AI 毙掉的论文"》. https://36kr.com/p/3826037992116868
139. 科学网. https://news.sciencenet.cn/htmlnews/2026/6/567120.shtm
140. 36氪《OpenAI 骤然关停 AI"打假"工具》. https://m.36kr.com/p/2362048518752644
141. 大众网检测收费报道. http://www.dzwww.com/xinwen/shehuixinwen/202605/t20260510_17717814.htm
142. 深圳新闻网报道. http://www.sznews.com/news/content/mb/2026-05/07/content_32040277.htm
143. EFL 误报研究综述. https://ejournal-fkip.unisi.ac.id/shelves/article/download/3557/1886/12086
144. 国内高校 AIGC 红线. https://www.paperbye.com/news/5170.html
145. 留学圈 AI 作弊定性. https://liuxue.xdf.cn/blog/blog_7896264.shtml
146. 学术诚信申诉注意. https://www.163.com/dy/article/KSGLIE0S0556KMBK.html
147. 海外学术诚信通识. https://place-4-papers.com/chatgpt-and-academic-integrity-complete-student-guide-for-2025/
148. Cognixx AI 与学术诚信. https://cognixx.io/is-using-ai-for-academic-writing-considered-cheating/

### 6.5 五、去 AI 味写作技法与词表（主文档编号 149–193）

149. Pure Write — Common AI Words and Phrases. https://purewrite.io/ai-words
150. Metric37 — Common AI Words and Phrases to Avoid. https://metric37.com/blog/common-ai-words-and-phrases
151. Slop Detector — The AI Words List: 120+ Phrases. https://slopdetector.org/blog/ai-words-list ；为什么写作像 AI https://slopdetector.org/blog/why-does-my-writing-sound-like-ai
152. Microsoft — How to humanize AI text. https://www.microsoft.com/en-us/microsoft-copilot/copilot-101/humanize-ai-text
153. Scribbr — How to Rewrite AI-Generated Text. https://www.scribbr.com/ai-tools/rewrite-ai-text/
154. Geri Mileva — AI writing patterns to avoid. https://www.gerimileva.com/ai-writing-patterns-to-avoid-a-practical-list-of-ai-telltales/
155. Smart Academic Writing — How to Humanize AI Text. https://smartacademicwriting.com/how-to-humanize-ai-text/
156. Viral SEO — How to Make AI Writing Sound Human. https://getviralseo.com/articles/how-to-make-ai-writing-sound-human-the-complete-guide
157. HumanWriteup — Why does my essay sound AI-generated. https://www.humanwriteup.com/blog/why-does-my-essay-sound-ai-generated
158. AIDetector.life — Which Sentences Are AI-Written. https://aidetector.life/posts/which-sentences-are-ai-written/
159. BDK Studios — Your AI Content Looks Like AI Content. https://www.bdkstudios.com/blog/ai-content-looks-like-ai-fix-it
160. Ritner Digital — The Phrases That Give Away AI Writing. https://www.ritnerdigital.com/blog/the-phrases-that-give-away-ai-writing-and-how-to-edit-them-out-before-they-cost-you-trust
161. The Central — How to Humanize Your AI Writing. https://thecentral.ai/p/how-to-humanize-your-ai-writing
162. RephraseLab — The Art of Humanizing AI. https://rephraselab.com/blog/the-art-of-humanizing-ai-techniques-to-improve-flow-and-bypass-detection
163. Humanize AI — Make AI-Generated Text Sound More Human. https://huma-nize.com/blog/how-to-make-ai-generated-text-sound-more-human-1769940001955
164. Humanizer.site — Avoid AI Writing Patterns. https://humanizer.site/blog/avoid-ai-writing-patterns
165. GitHub Gist — austin songer 消除 AI 文本模式. https://gist.github.com/austinsonger/cef3ccbf5a877c2ca70771a522409683
166. GitHub Gist — bketelsen Humanizer skill. https://gist.github.com/bketelsen/856cea9f602a1aed46cbc2e1b3f04270
167. GitHub Gist — MrDwarf7 47 words. https://gist.github.com/MrDwarf7/9953b75ca82f4e3071aec0eaec2948ab
168. GitHub Gist — joshp123 anti-slop writing. https://gist.github.com/joshp123/3c60d8def6d30a2503d8a98575334702
169. GitHub Gist — KevinJSKim85 Essay Humanizer. https://gist.github.com/KevinJSKim85/65e4dbb4400f43a1b339e7ed25ff871f
170. Westcliff University Writing Center — Avoiding "AI-Like" Writing (PDF). https://writingcenter.westcliff.edu/wp-content/uploads/2025/11/Avoiding-AI-Like-Writing.pdf
171. Academic Flair — Humanize AI Content for Academic Writing. https://academicflair.org/blog-how-to-humanize-ai-content-academic-writing/
172. Refinely Human — Humanize AI Text for Academic Writing. https://www.refinelyhuman.com/blog/humanize-ai-text-academic-writing
173. Alfred Scholar — The AI Slop Problem. https://www.alfredscholar.com/blog/the-ai-slop-problem-scholarly-voice-2026/
174. GenzWrite — Make AI Essay Sound Human. https://www.genzwrite.ai/blog/make-ai-essay-sound-human
175. WriteMyEssay.AI — Rewrite AI Text to Sound Human. https://writemyessay.ai/blog/how-to-rewrite-ai-generated-text-to-sound-human
176. SyncSignature — Humanize AI-Generated Emails. http://syncsignature.typeflo.io/blog/how-to-humanize-ai-generated-emails
177. Humantext.pro — AI Email Rewriter Human Tone. https://humantext.pro/blog/ai-email-rewriter-human-tone ；Human or Not. https://humantext.pro/blog/human-or-not-ai
178. Raw Magazine — Business Writing Sound More Human. https://www.rawmags.com/how-to-make-your-business-writing-sound-more-human-in-5-simple-steps/
179. Field Guide to AI — Editing AI Output to Sound Like You. https://fieldguidetoai.com/courses/ai-writing-assistant/editing-and-voice
180. Multiple.chat — How to Humanize AI Emails. https://multiple.chat/humanize-ai-email
181. SmartMails — Crafting Personalized Emails. https://blog.smartmails.io/2026/07/22/crafting-personalized-emails-avoiding-robotic-tone/
182. Smart AI Email Writer. https://emailai.me/app-guide/make-ai-email-sound-natural
183. Gloria Chou PR — AI Words to Avoid. https://gloriachoupr.com/ai-words-to-avoid-how-to-stop-your-captions-and-emails-from-sounding-like-chatgpt/
184. Yale National Initiative — Finding Your Voice (PDF). https://teachers.yale.edu/download/units/25_02_11.pdf
185. BubbleCow — Improve Your Writing Style. https://www.bubblecow.com/blog/writing-craft/style-and-voice/how-to-improve-your-writing-style-without-losing-personality/ ；Sensory Detail https://www.bubblecow.com/blog/writing-craft/show-vs-tell/how-to-use-sensory-detail-to-bring-scenes-to-life/ ；Dialogue https://www.bubblecow.com/blog/writing-craft/dialogue-writing/ideas-to-make-your-dialogue-sound-natural/ ；写作风格资源 https://www.bubblecow.com/blog/writing-craft/style-and-voice/best-resources-for-improving-your-writing-style/
186. Grammar Guide — Authentic Voice for College Essay. https://grammarguide.blog/crafting-an-authentic-voice-for-your-college-essay/
187. TryAthens — Creative Writing Tips AI Can't Teach You. https://tryathens.com/blog/creative-writing-tips-ai-cant-teach
188. Fiveable — Personal Essays and Memoirs. https://fiveable.me/english-12/unit-18/crafting-personal-essays-memoirs/study-guide/BC6xpyKieX7FcNNx
189. Janice Thompson — Mastering Dialogue in Fiction (PDF). https://janiceathompson.com/wp-content/uploads/2025/02/MASTERING-DIALOGUE-IN-FICTION2.pdf
190. Caroline Hardaker — Dialogue that sounds real. https://carolinehardakerwrites.com/2026/03/04/dialogue-that-sounds-real-techniques-examples-common-mistakes/
191. Self Pub Hub — 9 Ways to Make Dialogue Natural. https://selfpubhub.us.com/dialogue-writing/
192. EpicScribe — How to Write Better Dialogue. https://epicscribe.io/blog/how-to-write-better-dialogue-guide
193. Arbento — 8 Dialogue Writing Tips. https://arbento.com/blog/dialogue-writing-tips

### 6.6 六、中文写作技法来源（主文档编号 194–215）

194. 腾讯新闻《消除"罪证"：给写作去除"AI味"的不完全手册》. https://view.inews.qq.com/a/20260525A09VTM00
195. SkillHub（腾讯云）— remove-ai-flavor. https://skillhub.cloud.tencent.com/skills/remove-ai-flavor ；Humanizer https://skillhub.cn/skills/humanizer
196. 技术栈 — 去AI味提示词大全. https://jishuzhan.net/article/2097899716437266433
197. 新浪财经 — AI写作的"AI味"特征. https://cj.sina.com.cn/articles/view/7880068741/1d5b04e8506801kky4 ；如何判断AI写作痕迹 https://cj.sina.com.cn/articles/view/7879776886/1d5abda760680272eo
198. Tokeny — AI 高频词汇表. https://tokeny-ai.com/skills/6
199. 去AI味官网. https://quaiwei.com/methods
200. 人人都是产品经理 — 单篇100万阅读文章如何用AI做内容. https://www.woshipm.com/ai/6380166.html
201. 运营派 — 10万+爆文如何生产. https://www.yunyingpai.com/paperwork/662383.html
202. 鱼皮 AI 知识库 — mimeng-writing. https://ai.codefather.cn/skills/2014279411871199234
203. Tessl Registry — khazix-writer. https://tessl.io/registry/khazix-skills/khazix-writer/0.1.1
204. 即刻用户 — 朗读测试法. https://m.okjike.com/users/ecfedc13-a256-4cb9-95c4-1ec6b9c5d76c
205. 今日头条 — 口语化写作技巧. http://m.toutiao.com/group/7623425202331894315/
206. 抖音 — 高频AI用词避雷清单. https://www.iesdouyin.com/share/video/7648286616385719732 ；公众号口语化 https://www.iesdouyin.com/share/video/7598600105910748838 ；进阶技巧 https://www.iesdouyin.com/share/video/7678631166672522538 ；余光中化用 https://www.iesdouyin.com/share/video/7604100180765582001
207. CSDN — 人性化 AI 内容艺术. https://blog.csdn.net/Maozhao_W/article/details/156953924 ；降AI痕迹提示词 https://blog.csdn.net/weixin_62375676/article/details/158807410 ；维普原理 https://blog.csdn.net/qq_39695630/article/details/164881207 ；四层特征 https://blog.csdn.net/qq_39695630/article/details/165581758 ；知网升级 https://blog.csdn.net/xiaoguanjia_/article/details/155388809 ；写作阅读 https://blog.csdn.net/ultramand/article/details/156577477
208. 博客园 — 中文 AI 味三类信号. https://www.cnblogs.com/qizhigongfang/p/22775997
209. 去 AIGC 改写. https://www.quaigc.com/blog/ai-text-writing-review-and-rewrite
210. Ryrob — AI Content Personalization. https://www.ryrob.com/ai-content-personalization/
211. Lynote — Avoid AI Detection. https://lynote.ai/blog/avoid-ai-detection
212. Hold Your Voice — What Makes Writing Sound Like AI. https://holdyourvoice.com/guides/guide-what-makes-writing-sound-like-ai
213. Daily Reality NG News — Proofread AI Content. https://www.dailyrealityngnews.com/2026/03/proofread-edit-ai-generated-content-professional-copy-editor.html
214. Bilibili — 去AI味5步改稿法. https://www.bilibili.com/video/BV1zzQMBJEh5/
215. Bob Regnerus — AI Writing Filter (PDF). https://bobregnerus.com/wp-content/uploads/2026/03/AI_Writing_Filter_Universal.pdf

### 6.7 七、中文经典范文原文与赏析（主文档编号 216–239）

216. 朱自清《背影》原文. https://m.ruiwen.com/wenxue/zhuziqing/384595.html
217. 孙绍振《演说朱自清》中国作家网. https://www.chinawriter.com.cn/n1/2022/0719/c419003-32479753.html
218. 《背影》教学 PDF. http://office.teacheredu.cn/zaixianyulan/yanxiu/webroot/files/201712/article/37003/201771327827770635.pdf
219. 朱自清《荷塘月色》原文. https://www.renjiaoshe.com/news/67804.html
220. 《荷塘月色》知识点. https://www.zxxk.com/soft/58762530.html
221. 鲁迅《秋夜》原文. https://m.baike.com/wiki/%E7%A7%8B%E5%A4%9C/19354166
222. 中国现代文学馆《秋夜》赏析. http://www.wxg.org.cn/gkwz/4017.jhtml
223. 中国作家网《秋夜》首句分析. http://www.chinawriter.com.cn/n1/2024/0920/c404064-40324356.html
224. 新华网《90 年后再读〈边城〉》. http://www.xinhuanet.com/20240419/3978a70464464084879875407a21d35b/c.html
225. 《边城》人物描写（广外报）. https://gwszb.gdufs.edu.cn/phone/content.html?aid=1625
226. 汪曾祺《昆明的雨》原文. https://llc.nwupl.edu.cn/hxjy/mwjc/55692.htm
227. 苏北《读汪记》中国作家网. http://www.chinawriter.com.cn/n1/2025/0923/c418988-40570154.html
228. 汪曾祺《受戒》片段. https://etcnew.sdut.edu.cn/meol/common/script/preview/download_preview.jsp?fileid=5496705&resid=897764&lid=48227&preview=preview
229. 学科网《昆明的雨》咸鸭蛋. https://m.zxxk.com/soft/56825837.html
230. 史铁生《我与地坛》原文与讲座. https://visionchinese.com/shi-tiesheng/
231. 《我与地坛》知识点. https://m.zxxk.com/soft/58763107.html ；回环句分析 https://m.sohu.com/a/1065478877_121106875/
232. 余光中《听听那冷雨》原文. https://m.ruiwen.com/wenxue/yuguangzhong/7470.html
233. 《听听那冷雨》个案分析（海峡语文网）. http://www.hxyww.cn/wycynews.aspx?tid=9185
234. 龙应台《目送》原文与赏析. https://m.ruiwen.com/wenxue/sanwen/409721.html
235. 陈剑晖《龙应台的〈目送〉》. http://www.chinawriter.com.cn/wxpl/2013/2013-05-21/162859.html
236. 余秋雨《都江堰》原文. http://m.chinawriteronline.com/show/4187.html
237. 抖音百科《都江堰》. https://m.baike.com/wiki/%E9%83%BD%E6%B1%9F%E5%A0%B0/19714173
238. 汪曾祺《边城》语言评价（央视）. http://www.cntv.cn/program/dssgsw/20040609/102038.shtml
239. 汪曾祺写杨梅（头条）. http://m.toutiao.com/group/7664593332496810511/

### 6.8 八、英文范文原文与赏析（主文档编号 240–248）

240. Orwell, *Politics and the English Language* 原文. http://www.george-orwell.org/Politics_and_the_English_Language/0.html
241. Orwell 六条规则（Open Culture）. https://www.openculture.com/2025/12/george-orwells-six-rules-for-writing.html
242. Orwell 规则论文（Univ. of Missouri）. https://scholarship.law.missouri.edu/cgi/viewcontent.cgi?article=1750&context=facpubs
243. E.B. White, *Once More to the Lake* 赏析. https://study.com/learn/lesson/once-more-to-the-lake-white-summary-themes-analysis.html ；文学手法 https://www.supersummary.com/once-more-to-the-lake/literary-devices/
244. Joan Didion, *Goodbye to All That* 原文. https://pressbooks.howardcc.edu/humanities101/chapter/goodbye-to-all-that/ ；赏析 https://blogs.shu.edu/litandthecity/2019/05/08/joan-didion/ ；长句焦虑 https://quinsauls.wordpress.com/2021/11/19/saying-goodbye-to-our-former-selves/
245. Virginia Woolf, *The Death of the Moth* 原文. https://www.gutenberg.net.au/ebooks12/1203811h.html ；诗学 https://northofoxford.wordpress.com/2017/03/03/whos-afraid-of-virginia-woolfs-poetics/ ；动名词节奏 https://assayjournal.wordpress.com/2015/11/03/assaynfn15-the-lyrical-essays-of-virginia-woolf/ ；压缩技巧 https://froie.com/virginia-woolf-essay-technique-compression/
246. James Baldwin, *Notes of a Native Son* 主题分析. https://www.litcharts.com/lit/notes-of-a-native-son/themes/language-narrative-and-truth ；个人叙事 https://froie.com/james-baldwin-personal-narrative/ ；voice 分析 https://numerocinqmagazine.com/2013/07/02/the-personal-essay-and-the-pain-of-experience-communicating-to-the-broadest-possible-audience-craft-essay-sophfronia-scott/
247. Hunter S. Thompson / Gonzo 起源. http://gonzo.org/articles/lit/esstwo.html ；宾大英语系 https://web.english.upenn.edu/~despey/thompson.htm ；Gonzo 句法 https://hex-index.com/wikipedia/gonzo-journalism/index.html
248. New Journalism 与 Thompson（LitCharts）. https://www.litcharts.com/lit/fear-and-loathing-in-las-vegas

### 6.9 九、当代中文非虚构与文风学习方法论（主文档编号 249–260）

249. 李海鹏《举重冠军之死》范本分析（澎湃）. https://www.thepaper.cn/newsDetail_forward_25468291
250. 南方+《为何 20 年过去》. https://static.nfnews.com/content/202505/20/c11311836.html
251. 特稿开头方式（中国新闻培训网）. https://www.xwpx.com/article/2024/0320/article_70465.html ；关键24小时 https://www.xwpx.com/article/2018/0523/article_55100.html
252. 《冰点人物》分析（人民网）. http://media.people.com.cn/n/2015/0319/c394802-26719100-3.html ；采访写作 https://zqb.cyol.com/content/2009-08/05/content_2790872.htm
253. "3-on 折叠人"特稿分析（澎湃）. https://www.thepaper.cn/newsDetail_forward_31752199
254. 非虚构写逝者评稿会（澎湃）. https://m.thepaper.cn/newsDetail_forward_34066924
255. 163 转载李海鹏开头谈. https://www.163.com/dy/article/KVG7KJNH0553DIFV.html
256. Creator's Hearth — Writing Style 指南. https://www.creatorshearth.com/blog/craft/writing-style-guide ；Reading Like a Writer https://www.creatorshearth.com/blog/craft/reading-like-a-writer
257. Sydney Book Publishers — Writing Styles 六步法. https://sydneybookpublishers.com/writing-styles/
258. 作家库·科学仿写训练. https://zuojiaku.com/doc-view-69410.html
259. 仿写三步法（什么值得买）. https://post.m.smzdm.com/p/awwrolrk/
260. 精读素材本（头条）. http://m.toutiao.com/group/7579978866752619017/

### 6.10 十、书籍与在线资源（主文档编号 261–276）

261. The Elements of Style 公开 PDF. https://www.astro.ncu.edu.tw/~wchen/Courses/SciWriting/The_Elements_of_Style.pdf
262. On Writing Well 中文笔记. https://notes.limboy.me/books/5crctp
263. 《金字塔原理》豆瓣. https://book.douban.com/subject/4882120/
264. Savoy, *Machine Learning Methods for Stylometry*. https://doi.org/10.1007/978-3-030-53360-1
265. Nini, *A Theory of Linguistic Individuality*. https://www.cambridge.org/core/elements/theory-of-linguistic-individuality-for-authorship-analysis/E52B7B8ADC2B5EC579037AC9D81575E5
266. Hugh Craig 个人页. https://newcastle.edu.au/profile/hugh-craig
267. Brett Greatley-Hirsch 个人页. https://ahc.leeds.ac.uk/english/staff/793/dr-brett-greatley-hirsch
268. Purdue OWL. https://owl.purdue.edu/
269. Grammarly Blog. https://www.grammarly.com/blog/
270. 国家高等教育智慧教育平台. https://higher.smartedu.cn/
271. 中国大学 MOOC. https://www.icourse163.org/
272. 知乎专栏. https://zhuanlan.zhihu.com/
273. 豆瓣读书. https://book.douban.com/
274. StyloMetrix / stylometry-python. https://pypi.org/project/stylometry-python/1.4.0/
275. MIT OpenCourseWare. https://ocw.mit.edu/
276. Coursera. https://www.coursera.org/

### 6.11 十一、GitHub 开源仓库（主文档编号 277–285，2026-09-19 第十六轮登记；#284–#285 第二十二轮补录）

277. blader — humanizer（去 AI 味改写 skill：25 patterns 五类 + weak-alone 同段共现机制）. https://github.com/blader/humanizer
278. lguz — humanize-writing-skill（3-pass 改写，"结构 tell 强于词汇 tell"）. https://github.com/lguz/humanize-writing-skill
279. LifelongLazyLearner — qu-ai-wei（中文 51 类模式 + 六条冲突仲裁，MIT v0.6.6）. https://github.com/LifelongLazyLearner/qu-ai-wei
280. MrGeDiao — shuorenhua（说人话，中文人味改写）. https://github.com/MrGeDiao/shuorenhua
281. hardikpandya — stop-slop（anti-slop 写作规则）. https://github.com/hardikpandya/stop-slop
282. petergyang — no-ai-slop（最小改动去 AI 味，Edit/Detect 模式分离）. https://github.com/petergyang/no-ai-slop
283. brandonwise — humanizer（28 patterns + 560+ 词表 + burstiness 统计信号，`[社区]`）. https://github.com/brandonwise/humanizer
284. liamdugan — RAID（6.2M 生成文本基准：11 模型 × 8+3 域 × 11 攻击 × 4 解码策略；FPR=5% 校准协议；MIT 许可，代码与数据全开放）. https://github.com/liamdugan/raid
285. vinusankars — Reliability-of-AI-text-detectors（Sadasivan v4 递归改写攻击复现代码：KGW/DetectGPT/RoBERTa/检索式 TPR@1%FPR 衰减数据）. https://github.com/vinusankars/Reliability-of-AI-text-detectors

> 未核实不登记：harlan-zw/harlan-agent-kit · humanize-writing、De-AI Prompt Enhancer、Project Osint——多轮搜索未命中原仓库，仅存于二手转述（research-basis.md §9.3 已逐行标注）。

---

## 附：分报告主题索引（按技术路线快速定位）

- **困惑度/突发性（perplexity / burstiness）**：#1 GLTR、#2 DetectGPT、#3 Fast-DetectGPT、#5 PAWN、#7 滑动窗口
- **ML 分类器（BERT/RoBERTa 微调）**：#8 综合基准、#9 DetectAnyLLM、#47 LLM-Detector、#49 中文 LoRA、#50 双流融合
- **零样本/黑盒检测**：#2 DetectGPT、#3 Fast-DetectGPT、#4 Binoculars、#6 Polish Ratio
- **误报与偏见**：#10 Liang、#11 Weber-Wulff、#12 Style as Confound、#13 BAID、#14 捷克语重审、#15 理论下限
- **对抗/绕过**：#16 DUPE、#17 代码域评测
- **文体学/语言特征**：#18–#26、#27–#30
- **水印**：#31–#38
- **教育与政策**：#39–#46、时间线 2023–2026
- **对抗攻击下限与大规模基准**：#54 Sadasivan（递归改写攻击，四类检测器 TPR@1%FPR 全线衰减）、#55 RAID（11 模型 × 11 攻击；FPR=5% 校准后 ZeroGPT 仅 16.9%、Binoculars 低 FPR 最强；repetition penalty −32pp）

> **分报告历史背景注记**：文体学公认起点为 Mendenhall(1887) "The Characteristic Curves of Composition"（*Science*）；最著名案例为 Mosteller & Wallace(1964) 用函数词频率解决《联邦党人文集》作者归属争议；Patrick Juola 曾于 2013 年用文体学识别出 Robert Galbraith 即 J.K. Rowling。

---

## 分报告1 来源（AI检测原理与局限）

**学术论文（已核实）**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 1 | Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., Zou, J. *GPT detectors are biased against non-native English writers*. arXiv:2304.02819（后发表于 Cell 子刊 Patterns） | https://arxiv.org/abs/2304.02819 ；PDF：https://arxiv.org/pdf/2304.02819v3 |
| 2 | Sadasivan, V. S., Kumar, A., Balasubramanian, S., Wang, W., Feizi, S. *Can AI-Generated Text be Reliably Detected?* arXiv:2303.11156 | https://arxiv.org/pdf/2303.11156v4 （v4 修订版） ；OpenReview：https://openreview.net/forum?id=NvSwR4IvLO |
| 3 | *False Positives in AI Writing Detection: A Small-Scale Empirical Study Using Authentic Filipino Student Essays*. ERIC ED681015 | http://files.eric.ed.gov/fulltext/ED681015.pdf |
| 4 | Hadra, Cambridge, Mesbah (2026). *Evaluating the accuracy and reliability of AI content detectors in academic contexts* | https://artefacts-discovery.researcher.life/full_text/DA-2/5e/5ea324a8a0af312286ad5aaa7ce0ba62/full_text/9af415ef719fb222ac97a986d347d39f.pdf |
| 5 | Kirchenbauer, J. et al. *A Watermark for Large Language Models*. ICML 2023（课件转述） | www.ccs.neu.edu 站内路径 home/alina/classes/Fall2024/Lecture19.pdf |
| 6 | *Provable Robust Watermarking for AI-Generated Text*. arXiv:2306.17439 | https://arxiv.org/html/2306.17439 |
| 7 | *De-mark: Watermark Removal in LLMs*. arXiv:2410.13808 | https://arxiv.org/html/2410.13808v1 |
| 8 | *LLM Watermark Evasion via Bias Inversion*. arXiv:2509.23019 | https://arxiv.org/html/2509.23019v4 |
| 9 | 《AIGC 论文检测系统的技术缺陷与学术期刊因应》，《出版与印刷》 | https://cbyys.sppc.edu.cn/article/doi/10.19619/j.issn.1007-1938.2024.00.027?viewType=citedby-info |
| 10 | *An Overview of Generative AI Acceptable Use Policies by Universities With Top 25 CS Programs (2025)*, IEEE Computer Society | https://www.computer.org/csdl/magazine/co/2025/09/11134659/29olVQkX8Os |

**工具官方/厂商页面**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 11 | GPTZero 技术页；原理 | https://gptzero.me/technology ；https://gptzero.me/how-it-works |
| 12 | Originality.ai 官网；准确率博客 | https://originality.ai/ ；https://originality.ai/blog/ai-content-detection-accuracy |
| 13 | Turnitin 官方 ELL 研究博客 | https://www.turnitin.com/blog/new-research-turnitin-s-ai-detector-shows-no-statistically-significant-bias-against-english-language-learners |
| 14 | Turnitin《AI Writing Detection Model Architecture and Testing Protocol》（布法罗大学托管） | https://www.buffalo.edu/content/www/lms/guides-instructors/integrations/turnitin/_jcr_content/root/maincontent/par/download/file.res/Turnitin%E2%80%99s%20AI%20Writing%20Detection%20Model%20Architecture%20and%20Testing%20Protocol.pdf |
| 15 | Copyleaks 测试方法论；Copyleaks vs ZeroGPT | https://copyleaks.com/zh/ai-content-detector/testing-methodology ；https://copyleaks.com/blog/copyleaks-vs-zerogpt |
| 16 | ZeroGPT | https://zerogpt.tech/ |
| 17 | OpenAI《New AI classifier for indicating AI-written text》（含 2023-07-20 下线说明） | https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text |

**媒体与政策报道**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 18 | Ars Technica：OpenAI discontinues its AI writing detector | https://arstechnica.com/civis/threads/openai-discontinues-its-ai-writing-detector-due-to-%E2%80%9Clow-rate-of-accuracy%E2%80%9D.1494831/ |
| 19 | Brandeis 大学：Limitations of AI Detection Tools（引华盛顿邮报 Fowler 报道） | https://www.brandeis.edu/ai-steering-council/ai-literacy/ai-teaching-learning/detection-tools.html |
| 20 | Penn State 学术诚信《AI Detector Guidelines》 | https://integrity.psu.edu/sites/default/files/2026-01/AI%20Detector%20Guidelines%20Draft%20v1.3.pdf |
| 21 | USW 官方《AI detectors – a statement》 | https://uswvarious1.blob.core.windows.net/uswvarious-prod-uploads/documents/AI_detectors_statement.pdf |
| 22 | Algonquin College《Update on the Use of Turnitin AI Detector》 | https://www.algonquincollege.com/vpacademic/files/2024/01/January-2nd-2024-Update-on-the-Use-of-Turnitin-AI-Detector.pdf |
| 23 | Quetext：Universities restricting AI detectors | https://www.quetext.com/blog/universities-restricting-ai-detectors |
| 24 | StraitsHub：NTU abandons AI plagiarism detectors | https://straitshub.com/ntu-abandons-ai-plagiarism-detectors-declaring-them-too-unreliable-to-prove-academic-misconduct/ |
| 25 | eduaipolicy 政策数据库 | https://eduaipolicy.org/pl/themes/ai-detectors |
| 26 | UNIwise 白皮书《Heads We Win, Tails You Lose》 | https://uniwise.eu/hubfs/Heads%20We%20Win%20Tails%20You%20Lose%20-%20Whitepaper.pdf |
| 27 | Idaho Pressbooks《Policy Brief: Rethinking AI Detection Tools in Higher Education》 | https://idaho.pressbooks.pub/airesourceguide/chapter/policy-brief-rethinking-ai-detection-tools-in-higher-education/ |
| 28 | CASRAI：Turnitin 分数含义解读 | https://casrai.org/guides/why-does-my-paper-say-ai-detected |

**中文媒体与技术资料**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 29 | 光明日报《用 AI 查 AI 率，真的靠谱吗》 | https://epaper.gmw.cn/gmrb/html/content/202605/27/content_15035.html |
| 30 | 南方+《如何证明我不是 AI？毕业论文的检测疑云》 | https://www.nfnews.com/content/J3WYN59Koz.html |
| 31 | 36氪《这个毕业季，那些被"AI 毙掉的论文"》 | https://36kr.com/p/3826037992116868 |
| 32 | 科学网《"用 AI 查 AI 率"靠谱吗？毕业论文检测怎样更科学？》 | https://news.sciencenet.cn/htmlnews/2026/6/567120.shtm |
| 33 | 36氪《OpenAI 骤然关停 AI"打假"工具》 | https://m.36kr.com/p/2362048518752644 |
| 34 | 维普 AIGC 检测风险等级说明 | https://www.vpcs-vip.cn/knowledge/id/73?page=2 |

**原理/第三方技术拆解（用于概念解释）**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 35 | aidetector.ac 原理与困惑度公式 | https://aidetector.ac/how-it-works/ |
| 36 | Paper-Checker 原理 | https://hub.paper-checker.com/blog/how-ai-detectors-actually-work-understanding-perplexity-burstiness-stylometry-explained/ |
| 37 | TextSight 信号 | https://www.textsight.ai/how-ai-detectors-work/ |
| 38 | EyeSift 改写后检测率 | https://www.eyesift.com/blog/can-ai-detectors-detect-paraphrased-ai/ |
| 39 | SentiSight Originality 信号拆解 | https://www.sentisight.ai/why-is-originality-ai-held-up-as-the-gold-standard-ai-content-detector/ |
| 40 | 嘎嘎降AI 知网/维普/万方对比 | https://aigcleaner.com/blog/zhiwang-weipu-wanfang-aigc-jiance-chayi-jiexi |

> 说明：部分第三方博客/SEO 站点（如 detectiondrama、theairankings 等）仅用于交叉印证公开数据，其单站数据不作为唯一依据；本报告核心结论均以同行评审论文、大学官方文件、厂商官方页面和主流媒体报道为准。

## 分报告2 来源（去AI味写作技法）

**英文综合指南与词表**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 1 | Pure Write — Common AI Words and Phrases That Get You Flagged | https://purewrite.io/ai-words |
| 2 | Metric37 — Common AI Words and Phrases to Avoid (2026 List) | https://metric37.com/blog/common-ai-words-and-phrases |
| 3 | Slop Detector — The AI Words List: 120+ Phrases ChatGPT Overuses | https://slopdetector.org/blog/ai-words-list |
| 4 | Microsoft — How to humanize AI text for natural writing | https://www.microsoft.com/en-us/microsoft-copilot/copilot-101/humanize-ai-text |
| 5 | Scribbr — How to Rewrite AI-Generated Text \| 7 Practical Tips | https://www.scribbr.com/ai-tools/rewrite-ai-text/ |
| 6 | Geri Mileva — AI writing patterns to avoid: a practical list of AI telltales | https://www.gerimileva.com/ai-writing-patterns-to-avoid-a-practical-list-of-ai-telltales/ |
| 7 | Smart Academic Writing — How to Humanize AI Text | https://smartacademicwriting.com/how-to-humanize-ai-text/ |
| 8 | Viral SEO — How to Make AI Writing Sound Human: The Complete Guide | https://getviralseo.com/articles/how-to-make-ai-writing-sound-human-the-complete-guide |
| 9 | HumanWriteup — Why does my essay sound AI-generated? | https://www.humanwriteup.com/blog/why-does-my-essay-sound-ai-generated |
| 10 | AIDetector.life — Which Sentences Are AI-Written? | https://aidetector.life/posts/which-sentences-are-ai-written/ |
| 11 | BDK Studios — Your AI Content Looks Like AI Content | https://www.bdkstudios.com/blog/ai-content-looks-like-ai-fix-it |
| 12 | Ritner Digital — The Phrases That Give Away AI Writing | https://www.ritnerdigital.com/blog/the-phrases-that-give-away-ai-writing-and-how-to-edit-them-out-before-they-cost-you-trust |
| 13 | The Central — How to Humanize Your AI Writing | https://thecentral.ai/p/how-to-humanize-your-ai-writing |
| 14 | RephraseLab — The Art of Humanizing AI | https://rephraselab.com/blog/the-art-of-humanizing-ai-techniques-to-improve-flow-and-bypass-detection |
| 15 | Humanize AI — How to Make AI-Generated Text Sound More Human | https://huma-nize.com/blog/how-to-make-ai-generated-text-sound-more-human-1769940001955 |
| 16 | Humanizer.site — Avoid AI Writing Patterns | https://humanizer.site/blog/avoid-ai-writing-patterns |

**GitHub Gist 社区规则集**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 17 | austin songer — A guide for eliminating AI-generated text patterns | https://gist.github.com/austinsonger/cef3ccbf5a877c2ca70771a522409683 |
| 18 | bketelsen — Humanizer skill, zero-tolerance rules | https://gist.github.com/bketelsen/856cea9f602a1aed46cbc2e1b3f04270 |
| 19 | MrDwarf7 — The 47 words that get AI content flagged | https://gist.github.com/MrDwarf7/9953b75ca82f4e3071aec0eaec2948ab |
| 20 | joshp123 — anti-slop writing first pass | https://gist.github.com/joshp123/3c60d8def6d30a2503d8a98575334702 |
| 21 | KevinJSKim85 — Essay Humanizer, 30 rules | https://gist.github.com/KevinJSKim85/65e4dbb4400f43a1b339e7ed25ff871f |

**学术写作**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 22 | Westcliff University Writing Center — Avoiding "AI-Like" Writing (PDF) | https://writingcenter.westcliff.edu/wp-content/uploads/2025/11/Avoiding-AI-Like-Writing.pdf |
| 23 | Academic Flair — How to Humanize AI Content for Academic Writing | https://academicflair.org/blog-how-to-humanize-ai-content-academic-writing/ |
| 24 | Refinely Human — How to Humanize AI Text for Academic Writing | https://www.refinelyhuman.com/blog/humanize-ai-text-academic-writing |
| 25 | Alfred Scholar — The AI Slop Problem: Scholarly Voice in 2026 | https://www.alfredscholar.com/blog/the-ai-slop-problem-scholarly-voice-2026/ |
| 26 | GenzWrite — Make AI Essay Sound Human | https://www.genzwrite.ai/blog/make-ai-essay-sound-human |
| 27 | WriteMyEssay.AI — How to Rewrite AI-Generated Text to Sound Human | https://writemyessay.ai/blog/how-to-rewrite-ai-generated-text-to-sound-human |

**邮件 / 商务写作**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 28 | SyncSignature — How to Humanize AI-Generated Emails | http://syncsignature.typeflo.io/blog/how-to-humanize-ai-generated-emails |
| 29 | Humantext.pro — AI Email Rewriter Human Tone | https://humantext.pro/blog/ai-email-rewriter-human-tone |
| 30 | Raw Magazine — Make Your Business Writing Sound More Human | https://www.rawmags.com/how-to-make-your-business-writing-sound-more-human-in-5-simple-steps/ |
| 31 | Field Guide to AI — Editing AI Output to Sound Like You | https://fieldguidetoai.com/courses/ai-writing-assistant/editing-and-voice |
| 32 | Multiple.chat — How to Humanize AI Emails | https://multiple.chat/humanize-ai-email |
| 33 | SmartMails — Crafting Personalized Emails: Avoiding Robotic Tone | https://blog.smartmails.io/2026/07/22/crafting-personalized-emails-avoiding-robotic-tone/ |
| 34 | Smart AI Email Writer — Make AI Email Sound Natural | https://emailai.me/app-guide/make-ai-email-sound-natural |
| 35 | Gloria Chou PR — AI Words to Avoid | https://gloriachoupr.com/ai-words-to-avoid-how-to-stop-your-captions-and-emails-from-sounding-like-chatgpt/ |

**个人声音与细节**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 36 | Yale National Initiative — Finding Your Voice (PDF) | https://teachers.yale.edu/download/units/25_02_11.pdf |
| 37 | BubbleCow — How To Improve Your Writing Style (Without Losing Personality) | https://www.bubblecow.com/blog/writing-craft/style-and-voice/how-to-improve-your-writing-style-without-losing-personality/ |
| 38 | BubbleCow — How To Use Sensory Detail | https://www.bubblecow.com/blog/writing-craft/show-vs-tell/how-to-use-sensory-detail-to-bring-scenes-to-life/ |
| 39 | Grammar Guide — Crafting an Authentic Voice for Your College Essay | https://grammarguide.blog/crafting-an-authentic-voice-for-your-college-essay/ |
| 40 | TryAthens — Creative Writing Tips AI Can't Teach You | https://tryathens.com/blog/creative-writing-tips-ai-cant-teach |
| 41 | Fiveable — Crafting Personal Essays and Memoirs | https://fiveable.me/english-12/unit-18/crafting-personal-essays-memoirs/study-guide/BC6xpyKieX7FcNNx |

**小说 / 对话**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 42 | Janice Thompson — Mastering Dialogue in Fiction (PDF) | https://janiceathompson.com/wp-content/uploads/2025/02/MASTERING-DIALOGUE-IN-FICTION2.pdf |
| 43 | BubbleCow — Ideas To Make Your Dialogue Sound Natural | https://www.bubblecow.com/blog/writing-craft/dialogue-writing/ideas-to-make-your-dialogue-sound-natural/ |
| 44 | Caroline Hardaker — Dialogue that sounds real | https://carolinehardakerwrites.com/2026/03/04/dialogue-that-sounds-real-techniques-examples-common-mistakes/ |
| 45 | Self Pub Hub — 9 Ways to Make Your Dialogue Sound Natural | https://selfpubhub.us.com/dialogue-writing/ |
| 46 | EpicScribe — How to Write Better Dialogue | https://epicscribe.io/blog/how-to-write-better-dialogue-guide |
| 47 | Arbento — 8 Dialogue Writing Tips | https://arbento.com/blog/dialogue-writing-tips |

**中文来源**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 48 | 腾讯新闻 — 消除"罪证"：给写作去除"AI味"的不完全手册（2026版） | https://view.inews.qq.com/a/20260525A09VTM00 |
| 49 | SkillHub（腾讯云）— remove-ai-flavor 去AI味 | https://skillhub.cloud.tencent.com/skills/remove-ai-flavor |
| 50 | 技术栈 — 去AI味提示词大全：25个实用Prompt | https://jishuzhan.net/article/2097899716437266433 |
| 51 | 新浪财经 — AI写作的"AI味"具体有哪些特征 | https://cj.sina.com.cn/articles/view/7880068741/1d5b04e8506801kky4 |
| 52 | 新浪财经 — 如何判断文章是否有AI写作痕迹 | https://cj.sina.com.cn/articles/view/7879776886/1d5abda760680272eo |
| 53 | Tokeny — AI 高频词汇表 | https://tokeny-ai.com/skills/6 |
| 54 | SkillHub — Humanizer | https://skillhub.cn/skills/humanizer |
| 55 | 去AI味官网 — 方法页 | https://quaiwei.com/methods |
| 56 | 人人都是产品经理 — 单篇100万阅读文章如何用AI做内容 | https://www.woshipm.com/ai/6380166.html |
| 57 | 运营派 — 10万+爆文如何生产：7000字新媒体写作指南 | https://www.yunyingpai.com/paperwork/662383.html |
| 58 | 鱼皮 AI 知识库 — mimeng-writing 风格拆解 | https://ai.codefather.cn/skills/2014279411871199234 |
| 59 | Tessl Registry — khazix-writer 写作节奏 | https://tessl.io/registry/khazix-skills/khazix-writer/0.1.1 |
| 60 | 即刻用户 — 朗读测试法 | https://m.okjike.com/users/ecfedc13-a256-4cb9-95c4-1ec6b9c5d76c |
| 61 | 今日头条 — 口语化写作4个技巧 | http://m.toutiao.com/group/7623425202331894315/ |
| 62 | 抖音 — 高频AI用词避雷清单 | https://www.iesdouyin.com/share/video/7648286616385719732 |
| 63 | 抖音 — 公众号口语化技巧 | https://www.iesdouyin.com/share/video/7598600105910748838 |
| 64 | CSDN — 掌握"人性化"AI内容的艺术 | https://blog.csdn.net/Maozhao_W/article/details/156953924 |
| 65 | CSDN — 降AI痕迹提示词与前后对比 | https://blog.csdn.net/weixin_62375676/article/details/158807410 |

*本指南为建设性写作指导，目标是帮助写作者写出自然、具体、有个人声音的文字，而非用于规避学术诚信审查。学术场景下使用 AI 辅助写作须遵守所在机构规范。*

## 分报告3 来源（写后自查与检测工具）

### 一页纸速查清单【速查清单】

【速查清单】**写后立刻做**：
1. 通读：逐段问"这段新增了什么信息？"
2. 朗读：听节奏是否均匀、有没有不像自己会说的话。
3. 清单：套话？对仗？空总结？空例子？
4. 定位：只改被标出来/自己也觉得空的段落。
5. 改写：加具体细节、加长短句变化、删段尾废话、用自己的话重写。
6. 交叉：有条件跑2款不同原理的检测器，**只看段落高亮，不看总分**。
7. 放一晚，第二天再读一遍。

【速查清单】**永远不要做**：
- 不要把检测器分数当"合格通行证"。
- 不要为了降AI率故意加错别字、加伪造经历。
- 不要把humanize工具的产物直接当作业/论文/考试答案交。
- 不要在不清楚学校政策的前提下默认"用了AI也没事"。

### 附：本指南引用的主要公开来源

**检测器与误报研究**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 1 | GPTZero 官网与语言支持 | https://gptzero.me/ |
| 2 | Originality.ai 官网与定价 | https://originality.ai/ ；https://originality.ai/pricing |
| 3 | Turnitin 官网；Turnitin对ELL学生的官方回应 | https://www.turnitin.com/ ；https://www.turnitin.com/blog/new-research-turnitin-s-ai-detector-shows-no-statistically-significant-bias-against-english-language-learners |
| 4 | ZeroGPT 官网；定价 | https://www.zerogpt.com/ ；https://www.zerogpt.com/pricing |
| 5 | Copyleaks 官网 | https://copyleaks.com/ |
| 6 | Crossplag 官网 | https://crossplag.com/ |
| 7 | Winston AI 官网与定价 | https://gowinston.ai/ ；https://gowinston.ai/pricing/ |
| 8 | Smodin 官网 | https://smodin.io/ |
| 9 | 独立准确率对比 | https://checkthat.ai/answers/what-are-the-best-most-accurate-ai-detector-tools |
| 10 | 500样本7工具测试 | https://humangpt.io/blog/are-ai-detectors-accurate-tested |
| 11 | 多检测器一致性研究PDF | https://textpulse.ai/research/textpulse-detector-agreement-2026.pdf |
| 12 | EFL/ESL误报研究综述 | https://www.eyesift.com/blog/turnitin-ai-detection/ ；https://ejournal-fkip.unisi.ac.id/shelves/article/download/3557/1886/12086 |
| 13 | Turnitin误差披露 | https://textpulse.ai/blog/ai-detectors-compared |

**国内检测工具**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 14 | 知网个人查重官方入口（由环球网及多所高校图书馆公告确认） | https://cx.cnki.net |
| 15 | 维普官方 | https://www.cqvip.com/ |
| 16 | PaperPass 官方技术介绍 | https://www.paperpass.com/knowledge/23465.html ；https://www.paperpass.com/knowledge/20096.html |
| 17 | 知网AIGC原理升级 | https://blog.csdn.net/xiaoguanjia_/article/details/155388809 |
| 18 | 维普AIGC原理 | https://blog.csdn.net/qq_39695630/article/details/164881207 |
| 19 | 媒体对国内检测收费与误报的报道 | http://www.dzwww.com/xinwen/shehuixinwen/202605/t20260510_17717814.htm ；http://www.sznews.com/news/content/mb/2026-05/07/content_32040277.htm |

**自查方法与humanize生态**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 20 | Wikipedia AI写作特征清单 | https://humanizeai.com/blog/wikipedias-signs-of-ai-writing-list-plus-a-prompt-you-can-turn-into-a-skill/ |
| 21 | 困惑度与突发性解释 | https://humanizeaitext.io/blog/perplexity-burstiness-explained ；https://www.eyesift.com/blog/perplexity-and-burstiness-ai-detection/ |
| 22 | 朗读/通读自查 | https://detectiondrama.com/how-to-check-if-your-essay-sounds-ai-written-before-you-submit/ ；https://holdyourvoice.com/guides/guide-what-makes-writing-sound-like-ai |
| 23 | 去AI味实操 | https://www.ryrob.com/ai-content-personalization/ ；https://lynote.ai/blog/avoid-ai-detection |
| 24 | 中文去AI味清单 | https://www.woshipm.com/ai/6380166.html ；https://www.cnblogs.com/qizhigongfang/p/22775997 ；https://www.quaigc.com/blog/ai-text-writing-review-and-rewrite |
| 25 | Humanize工具生态与争议 | https://undetectable.ai/ ；https://www.bypassgpt.ai/ ；https://textpulse.ai/research/textpulse-ai-humanizer-comparison-2026.pdf ；https://blog.stealthzero.ai/blog/ai-humanizer/humanizer-ai/ |

**学术诚信**

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 26 | 国内高校AIGC红线 | https://www.paperbye.com/news/5170.html |
| 27 | 留学圈AI作弊定性 | https://liuxue.xdf.cn/blog/blog_7896264.shtml |
| 28 | 学术诚信申诉注意 | https://www.163.com/dy/article/KSGLIE0S0556KMBK.html |
| 29 | 海外学术诚信通识 | https://place-4-papers.com/chatgpt-and-academic-integrity-complete-student-guide-for-2025/ |

## 分报告4 来源（人类优美文风学习）

### 中文范文原文与赏析

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 1 | 朱自清《背影》原文 | https://m.ruiwen.com/wenxue/zhuziqing/384595.html |
| 2 | 孙绍振《演说朱自清》（中国作家网） | https://www.chinawriter.com.cn/n1/2022/0719/c419003-32479753.html |
| 3 | 《背影》教学 PDF | http://office.teacheredu.cn/zaixianyulan/yanxiu/webroot/files/201712/article/37003/201771327827770635.pdf |
| 4 | 朱自清《荷塘月色》原文 | https://www.renjiaoshe.com/news/67804.html |
| 5 | 《荷塘月色》知识点 | https://www.zxxk.com/soft/58762530.html |
| 6 | 鲁迅《秋夜》原文 | https://m.baike.com/wiki/%E7%A7%8B%E5%A4%9C/19354166 |
| 7 | 中国现代文学馆《秋夜》赏析 | http://www.wxg.org.cn/gkwz/4017.jhtml |
| 8 | 中国作家网《秋夜》首句分析 | http://www.chinawriter.com.cn/n1/2024/0920/c404064-40324356.html |
| 9 | 沈从文《边城》赏析（新华网） | http://www.xinhuanet.com/20240419/3978a70464464084879875407a21d35b/c.html |
| 10 | 《边城》人物描写（广外报） | https://gwszb.gdufs.edu.cn/phone/content.html?aid=1625 |
| 11 | 汪曾祺《昆明的雨》原文 | https://llc.nwupl.edu.cn/hxjy/mwjc/55692.htm |
| 12 | 苏北《读汪记》（中国作家网） | http://www.chinawriter.com.cn/n1/2025/0923/c418988-40570154.html |
| 13 | 汪曾祺《受戒》片段 | https://etcnew.sdut.edu.cn/meol/common/script/preview/download_preview.jsp?fileid=5496705&resid=897764&lid=48227&preview=preview |
| 14 | 史铁生《我与地坛》原文与讲座 | https://visionchinese.com/shi-tiesheng/ |
| 15 | 《我与地坛》知识点 | https://m.zxxk.com/soft/58763107.html |
| 16 | 余光中《听听那冷雨》原文 | https://m.ruiwen.com/wenxue/yuguangzhong/7470.html |
| 17 | 《听听那冷雨》个案分析（海峡语文网） | http://www.hxyww.cn/wycynews.aspx?tid=9185 |
| 18 | 龙应台《目送》原文与赏析 | https://m.ruiwen.com/wenxue/sanwen/409721.html |
| 19 | 陈剑晖《龙应台的〈目送〉绝不是"心灵鸡汤"》 | http://www.chinawriter.com.cn/wxpl/2013/2013-05-21/162859.html |
| 20 | 余秋雨《都江堰》原文 | http://m.chinawriteronline.com/show/4187.html |

### 英文范文原文与赏析

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 21 | Orwell, *Politics and the English Language* 原文 | http://www.george-orwell.org/Politics_and_the_English_Language/0.html |
| 22 | Orwell 六条规则（Open Culture） | https://www.openculture.com/2025/12/george-orwells-six-rules-for-writing.html |
| 23 | Orwell 规则论文（Univ. of Missouri） | https://scholarship.law.missouri.edu/cgi/viewcontent.cgi?article=1750&context=facpubs |
| 24 | E.B. White, *Once More to the Lake* 赏析 | https://study.com/learn/lesson/once-more-to-the-lake-white-summary-themes-analysis.html |
| 25 | E.B. White 文学手法 | https://www.supersummary.com/once-more-to-the-lake/literary-devices/ |
| 26 | Joan Didion, *Goodbye to All That* 原文 | https://pressbooks.howardcc.edu/humanities101/chapter/goodbye-to-all-that/ |
| 27 | Didion 赏析 | https://blogs.shu.edu/litandthecity/2019/05/08/joan-didion/ |
| 28 | Virginia Woolf, *The Death of the Moth* 原文（Project Gutenberg Australia） | https://www.gutenberg.net.au/ebooks12/1203811h.html |
| 29 | Woolf 诗学分析 | https://northofoxford.wordpress.com/2017/03/03/whos-afraid-of-virginia-woolfs-poetics/ |
| 30 | Woolf 散文技巧 | https://froie.com/virginia-woolf-essay-technique-compression/ |
| 31 | James Baldwin, *Notes of a Native Son* 主题分析 | https://www.litcharts.com/lit/notes-of-a-native-son/themes/language-narrative-and-truth |
| 32 | Baldwin 个人叙事作为社会批判 | https://froie.com/james-baldwin-personal-narrative/ |
| 33 | Baldwin voice 分析 | https://numerocinqmagazine.com/2013/07/02/the-personal-essay-and-the-pain-of-experience-communicating-to-the-broadest-possible-audience-craft-essay-sophfronia-scott/ |
| 34 | Hunter S. Thompson / Gonzo 起源 | http://gonzo.org/articles/lit/esstwo.html |
| 35 | Thompson 风格（宾大英语系） | https://web.english.upenn.edu/~despey/thompson.htm |
| 36 | New Journalism 与 Thompson | https://www.litcharts.com/lit/fear-and-loathing-in-las-vegas |

### 当代中文非虚构

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 37 | 李海鹏《举重冠军之死》范本分析（澎湃） | https://www.thepaper.cn/newsDetail_forward_25468291 |
| 38 | 南方+《为何 20 年过去……》 | https://static.nfnews.com/content/202505/20/c11311836.html |
| 39 | 特稿开头方式（中国新闻培训网） | https://www.xwpx.com/article/2024/0320/article_70465.html |
| 40 | 《冰点人物》分析（人民网） | http://media.people.com.cn/n/2015/0319/c394802-26719100-3.html |
| 41 | 冰点人物采访与写作（中国青年报） | https://zqb.cyol.com/content/2009-08/05/content_2790872.htm |
| 42 | "3-on 折叠人"特稿分析（澎湃） | https://www.thepaper.cn/newsDetail_forward_31752199 |
| 43 | 非虚构写逝者评稿会（澎湃） | https://m.thepaper.cn/newsDetail_forward_34066924 |

### 文风学习方法论

| 编号 | 标题或说明 | URL |
| --- | --- | --- |
| 44 | Writing Style 指南（Creator's Hearth） | https://www.creatorshearth.com/blog/craft/writing-style-guide |
| 45 | Reading Like a Writer（Creator's Hearth） | https://www.creatorshearth.com/blog/craft/reading-like-a-writer |
| 46 | Writing Styles 六步法（Sydney Book Publishers） | https://sydneybookpublishers.com/writing-styles/ |
| 47 | 作家库·科学仿写训练 | https://zuojiaku.com/doc-view-69410.html |
| 48 | 仿写三步法（什么值得买） | https://post.m.smzdm.com/p/awwrolrk/ |
| 49 | 写作风格资源（BubbleCow） | https://www.bubblecow.com/blog/writing-craft/style-and-voice/best-resources-for-improving-your-writing-style/ |

## 表外补充登记（第23轮审计补录）

> 本节条目内容取自资料报告1（S1：多模型AI语料数据集与论文获取）原文；S1 检索不到或未给出的字段一律标"未提供"，不做推断补写。资料中提到但树内已有登记的条目（如 RAID 数据仓库，见上文 #55 与 #284）不重复收录。

### 数据集登记（12 条）

| 名称 | 来源 | 规模 | 链接 | 用途 |
| --- | --- | --- | --- | --- |
| RaBit（Ranking-based AI Text Benchmark，推测） | 未提供 | 未提供 | 未提供 | 资料报告1经多轮关键词搜索（"RaBit"、"Ranking-based AI Text Benchmark"），未发现以此命名的公开AI文本检测数据集；建议确认准确名称或提供论文作者、发表年份、机构后进一步检索 |
| MOSS-003-SFT | 复旦大学NLP实验室（fnlp） | 100万+条 | https://huggingface.co/datasets/fnlp/moss-003-sft-data | 中英文多轮对话数据，text-davinci-003生成 |
| Baize（白泽） | project-baize | 约653,699条 | GitHub: project-baize/baize-chatbot | 基于Quora/StackOverflow/MedQA的对话数据，含中英文版 |
| pCLUE | CLUEbenchmark | 120万训练数据（73个Prompt，9个任务） | https://www.cluebenchmarks.com/ ；GitHub: CLUEbenchmark/pCLUE | 中文语言理解测评基准（CLUE系列子数据集） |
| firefly-train-1.1M | YeungNLP | 110万条 | https://huggingface.co/datasets/YeungNLP/firefly-train-1.1M | 23个常见中文任务的指令微调数据 |
| LLaMA-Factory中文数据集 | 社区维护 | 多个 | 未提供（资料注明：见LLaMA-Factory README） | 包含alpaca-zh、COIG等多个中文指令数据集 |
| Defactify_Text_Dataset | Rajarshi-Roy-research（HuggingFace 账号） | 73,000+篇 | https://huggingface.co/datasets/Rajarshi-Roy-research/Defactify_Text_Dataset | 真实与合成文章对比，多个LLM生成（Gemma-2-9b等） |
| OpenTuringBench | 未提供 | 未提供 | arXiv:2504.11369 | 2025年发布，基于开源LLM的Turing测试和作者归属基准（TuringBench 的更新版本） |
| M4GT-Bench | 未提供 | 未提供 | 未提供 | M4 的扩展版本，覆盖更多领域和模型（见 M4 论文相关引用，M4 论文：arXiv:2305.14902） |
| WildChat-4.8M | 未提供（WildChat 扩展版） | 480万条对话 | https://huggingface.co/datasets/allenai/WildChat-4.8M | WildChat 的扩展版 |
| GPT-2 Output Dataset | OpenAI官方发布 | 未提供 | openai-community/gpt2-output-dataset（HuggingFace） | GPT-2 各尺寸模型输出数据集 |
| TuringBench GitHub 仓库 | Adaku Uchendu, Zeyu Ma, Thai Le, Rui Zhang, Dongwon Lee（Penn State University） | 20万条（200K）人类/机器生成样本（1万人类+19万机器） | GitHub: antoniocai/TuringBench（资料原文标注"需确认具体仓库地址"） | TuringBench 数据集与代码仓库；文本分类数据集（文本内容+生成模型标签，20个标签：Human+19个生成模型），论文：arXiv:2109.13296 与 https://aclanthology.org/2021.findings-emnlp.172/ |

### 资料报告1 附录 7.2：关键论文引用格式（BibTeX，原样收录）

```
@inproceedings{dugan2024raid,
  title={RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors},
  author={Dugan, Liam and Hwang, Alyssa and Trhlik, Filip and Ludan, Josh Magnus and Zhu, Andrew and Xu, Hainiu and Ippolito, Daphne and Callison-Burch, Chris},
  booktitle={ACL},
  year={2024}
}

@article{zheng2023lmsyschat1m,
  title={LMSYS-Chat-1M: A Large-Scale Real-World LLM Conversation Dataset},
  author={Zheng, Lianmin and Chiang, Wei-Lin and Sheng, Ying and Li, Tianle and Zhuang, Siyuan and Wu, Zhanghao and Zhuang, Yonghao and Li, Zhuohan and Lin, Zi and Xing, Eric P and Gonzalez, Joseph E and Stoica, Ion and Zhang, Hao},
  journal={arXiv preprint arXiv:2309.11998},
  year={2023}
}

@article{zhao2024wildchat,
  title={WildChat: 1M ChatGPT Interaction Logs in the Wild},
  author={Zhao, Yangyi and others},
  journal={arXiv preprint arXiv:2405.01470},
  year={2024}
}

@article{guo2023hc3,
  title={How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection},
  author={Guo, Biyang and others},
  journal={arXiv preprint arXiv:2301.07597},
  year={2023}
}

@inproceedings{uchendu2021turingbench,
  title={TURINGBENCH: A Benchmark Environment for Turing Test in the Age of Neural Text Generation},
  author={Uchendu, Adaku and Ma, Zeyu and Le, Thai and Zhang, Rui and Lee, Dongwon},
  booktitle={Findings of EMNLP},
  year={2021}
}

@article{wang2023m4,
  title={M4: Multi-generator, Multi-domain, and Multi-lingual Black-Box Machine-Generated Text Detection},
  author={Wang, Yuxia and Mansurov, Jonibek and Ivanov, Petar and others},
  journal={arXiv preprint arXiv:2305.14902},
  year={2023}
}

@article{sadasivan2023can,
  title={Can AI-Generated Text be Reliably Detected?},
  author={Sadasivan, Vinu Sankar and Kumar, Aounon and Balasubramanian, Sriram and Wang, Wenxiao and Feizi, Soheil},
  journal={arXiv preprint arXiv:2308.12462},
  year={2023}
}
```

### 资料报告1 附录 7.1：数据集对比速查表（原样收录）

| 数据集 | 年份 | 规模 | 模型数 | 多语言 | 多领域 | 对抗攻击 | 许可 |
|--------|------|------|--------|--------|--------|---------|------|
| RAID | 2024 | 628万+ | 11 | 否 | 8个领域 | 11种 | 学术用途 |
| WildChat | 2024 | 100万+ | 2 (GPT-3.5/4) | 多语言 | 多领域 | 无 | ODC-BY |
| LMSYS-Chat-1M | 2023 | 100万 | 25 | 154种语言 | 多领域 | 无 | 自定义（可商用） |
| HC3 | 2023 | ~5万 | 1 (ChatGPT) | 中英双语 | 4个领域 | 无 | 开源 |
| TuringBench | 2021 | 20万 | 19+Human | 英语 | 新闻 | 无 | 学术用途 |
| M4 | 2023 | 大规模 | 多模型 | 6种语言 | 多领域 | 无 | CC-BY 4.0 |

*本指南为学习用途整理，所有引文均为短片段；如需深入研究，请购买或借阅原作者著作。*

---

# 第二十三轮新增（2026-09-21）：小说 / 武侠 / 无限流研究来源

> 本轮为 novel-craft.md / wuxia-craft.md 落库而清点。来源三份文档：《新增研究1：网文写作四大痛点诊断与治疗报告》（1196 行，唯一 URL 38 条）、《新增研究2：长篇小说写作深度研究报告》（1384 行，唯一 URL 49 条）、《【最终主交付】创作完全手册》（10603 行，唯一 URL 925 条）。脚本验证研究1/2 的 URL 全部包含于主手册（子集差 0），故只按主手册清点。与既有索引去重后净新增 741 条，按域名分组如下。清点方式：脚本提取+比对，非目测。**本文件只保证"原文档里写了这个链接"，不说明链接内容说了什么、不保证现在仍可访问。**

| 域名 | 条数 |
|---|---|
| www.iesdouyin.com | 85 |
| m.toutiao.com | 73 |
| www.chinawriter.com.cn | 52 |
| fanqienovel.com | 22 |
| zh.wikipedia.org | 14 |
| paper.people.com.cn | 10 |
| wyb.chinawriter.com.cn | 10 |
| m.thepaper.cn | 8 |
| www.jjwxc.net | 7 |
| book.douban.com | 7 |
| m.xs8.cn | 7 |
| www.qidian.com | 7 |
| m.baike.com | 7 |
| www.bilibili.com | 6 |
| m.sohu.com | 6 |
| selfpubhub.us.com | 6 |
| arxiv.org | 6 |
| wenyi.gmw.cn | 5 |
| m.xxsy.net | 5 |
| wuxiasociety.com | 5 |
| m.qidian.com | 5 |
| write.qq.com | 4 |
| news.gmw.cn | 4 |
| m.bjnews.com.cn | 4 |
| epaper.gmw.cn | 4 |
| m.zxxk.com | 3 |
| notice.fanqienovel.com | 3 |
| www.xinhuanet.com | 3 |
| bbs.jjwxc.net | 3 |
| bbs.nga.cn | 3 |
| github.com | 3 |
| xbgjxt.swu.edu.cn | 3 |
| m.write.qq.com | 3 |
| m.ruiwen.com | 3 |
| weread.qq.com | 3 |
| www.xwpx.com | 3 |
| product.m.dangdang.com | 3 |
| reader.gmw.cn | 3 |
| reedsy.com | 3 |
| ubook.reader.qq.com | 3 |
| www.news.cn | 3 |
| www.qimao.com | 3 |
| jc.wanfangdata.com.cn | 2 |
| jinyong0.com | 2 |
| www.paperpass.com | 2 |
| www.sfedit.net | 2 |
| www.woshipm.com | 2 |
| www.xxsy.net | 2 |
| discovery.cctv.com | 2 |
| files.eric.ed.gov | 2 |
| www.xuexi.cn | 2 |
| fiveable.me | 2 |
| www.adazing.com | 2 |
| m.weibo.cn | 2 |
| www.andycoughlan.com | 2 |
| owl.purdue.edu | 2 |
| static.nfapp.southcn.com | 2 |
| sudowrite.com | 2 |
| m.gmw.cn | 2 |
| www.gov.cn | 2 |
| www.loreteller.com | 2 |
| www.anima-roleplay.com | 2 |
| www.bubblecow.com | 2 |
| m.pin.qq.com | 2 |
| media.people.com.cn | 2 |
| www.xs8.cn | 2 |
| www.cnr.cn | 2 |
| alejandroashes.com | 2 |
| yzwb.sjzdaily.com.cn | 2 |
| app.bjtitle.com | 2 |
| brandonsanderson.com | 2 |
| www.degruyterbrill.com | 1 |
| www.coollibri.es | 1 |
| www.eshukan.com | 1 |
| www.entangledtext.com | 1 |
| www.digitalmarketingagency.sg | 1 |
| www.diancang.xyz | 1 |
| www.chinaxwcb.com | 1 |
| www.cl.ntpu.edu.tw | 1 |
| www.chazidian.com | 1 |
| www.chinafilm.gov.cn | 1 |
| www.cntv.cn | 1 |
| www.codartium.com | 1 |
| www.classcentral.com | 1 |
| www.cmu.edu | 1 |
| www.grammarly.com | 1 |
| www.gptcleanup.com | 1 |
| meiwen.gmw.cn | 1 |
| www.gushici.net | 1 |
| www.howtowriteanovel.co.uk | 1 |
| www.hongxiu.com | 1 |
| www.hfou.net.cn | 1 |
| www.gmw.cn | 1 |
| www.fatskills.com | 1 |
| www.fable.la | 1 |
| www.eyesift.com | 1 |
| www.frontiersin.org | 1 |
| www.globalpeople.com.cn | 1 |
| www.fulltextarchive.com | 1 |
| www.fudan.edu.cn | 1 |
| mooc.ytu.edu.cn | 1 |
| wap.cqcb.com | 1 |
| wap.faloo.com | 1 |
| visualidentity.studio | 1 |
| wanderinginn.com | 1 |
| westernreflectionspublishing.com | 1 |
| wisereadshub.com | 1 |
| www.ccs.neu.edu | 1 |
| www.81.cn | 1 |
| tidenews.com.cn | 1 |
| titles.video | 1 |
| textpulse.ai | 1 |
| thephilosopher.net | 1 |
| ukpublishinghouse.co.uk | 1 |
| view.inews.qq.com | 1 |
| toolchase.com | 1 |
| traciejoy.com | 1 |
| wordvice-blog-production.s3.ap-northeast-1.amazonaws.com | 1 |
| news.china.com.cn | 1 |
| www.arbindbuilds.com | 1 |
| qnck.cyol.com | 1 |
| news.qq.com | 1 |
| mpre.lifeweek.com.cn | 1 |
| www.billstifler.org | 1 |
| www.athistleinthewind.com | 1 |
| www.audioenglish.org | 1 |
| writersdailypractice.com | 1 |
| writersworkshop.uiowa.edu | 1 |
| wb.lhrb.com.cn | 1 |
| writehuman.ai | 1 |
| wuxiatales.com | 1 |
| www.36kr.com | 1 |
| writing4pleasure.com | 1 |
| tsg.dlutci.edu.cn | 1 |
| www.hunnu.edu.cn | 1 |
| www.vortenza.com | 1 |
| www.wangwenclub.com | 1 |
| www.tumblr.com | 1 |
| www.uea.ac.uk | 1 |
| www.wenyiso.com | 1 |
| h5.wfwb.wfnews.com.cn | 1 |
| www.wanweixueshu.com | 1 |
| www.weixinhost.com | 1 |
| www.squibler.io | 1 |
| www.summonworlds.com | 1 |
| www.shenqiu.gov.cn | 1 |
| www.songwriter.co.uk | 1 |
| www.tolkienestate.com | 1 |
| www.trinka.ai | 1 |
| www.tandfonline.com | 1 |
| www.textsight.ai | 1 |
| www.writingmastery.com | 1 |
| xiezuocat.com | 1 |
| xmds.cbpt.cnki.net | 1 |
| wxyxz.xtu.edu.cn | 1 |
| book.youth.cn | 1 |
| zhiping.huaczy.com | 1 |
| zibo.dzwww.com | 1 |
| yiban.io | 1 |
| youmind.com | 1 |
| edshare.soton.ac.uk | 1 |
| culture.people.com.cn | 1 |
| www.wtxy.net | 1 |
| euroasia.cssn.cn | 1 |
| wxs.sass.org.cn | 1 |
| wxy.qfnu.edu.cn | 1 |
| www.yunyingpai.com | 1 |
| www.zdushi.com | 1 |
| www.lkong.com | 1 |
| manual.storybuilder.org | 1 |
| www.litcharts.com | 1 |
| www.literatureandlatte.com | 1 |
| www.mx-xz.com | 1 |
| www.mypitaya.com | 1 |
| www.masterclass.com | 1 |
| www.mochalabz.com | 1 |
| www.inkfluenceai.com | 1 |
| www.jssjx.com.cn | 1 |
| www.independenteditorsgroup.com | 1 |
| www.inewsweek.cn | 1 |
| www.kflz.gov.cn | 1 |
| www.kuaikanmanhua.com | 1 |
| www.jstor.org | 1 |
| www.julian.com | 1 |
| www.nationalreading.gov.cn | 1 |
| www.readnovel.com | 1 |
| www.rebellink.com | 1 |
| lyrb.lyd.com.cn | 1 |
| literature.cass.cn | 1 |
| www.scribbr.com | 1 |
| hs.nufe.edu.cn | 1 |
| www.renascence.io | 1 |
| www.scribblehubforum.com | 1 |
| www.oscarghostwriting.com | 1 |
| www.paperdue.com | 1 |
| www.nmg.gov.cn | 1 |
| www.opp2.com | 1 |
| www.peopleapp.com | 1 |
| www.peterthomson.com | 1 |
| m.chinanews.com | 1 |
| www.penguinrandomhouse.ca | 1 |
| jwb.shu.edu.cn | 1 |
| jwc.xync.edu.cn | 1 |
| bibli.page | 1 |
| jw.cdu.edu.cn | 1 |
| lexicalrichness.readthedocs.io | 1 |
| lib.unn.edu.cn | 1 |
| jypl.pku.edu.cn | 1 |
| kf.om.qq.com | 1 |
| image.chinawriter.com.cn | 1 |
| inki.so | 1 |
| humanlike.pro | 1 |
| hunan.gov.cn | 1 |
| bjlove02.chinanews.com.cn | 1 |
| jean-louis-vill.com | 1 |
| inkshift.io | 1 |
| item.jd.com | 1 |
| litarchive.online | 1 |
| m.hongxiu.com | 1 |
| m.huxiu.com | 1 |
| app.people.cn | 1 |
| m.gsw6.com | 1 |
| m.jjwxc.net | 1 |
| app.blurbbio.com | 1 |
| m.inote.qq.com | 1 |
| m.jiemian.com | 1 |
| lsa.umich.edu | 1 |
| bestwriting.com | 1 |
| litfind.bookscape.com | 1 |
| lobehub.com | 1 |
| m.cbook.qq.com | 1 |
| m.chuangshi.qq.com | 1 |
| bbs.qimao.com | 1 |
| m.book118.com | 1 |
| edresearchforaction.org | 1 |
| english.northwestern.edu | 1 |
| ck.xwpx.com | 1 |
| dzrb.dzng.com | 1 |
| ccj.pku.edu.cn | 1 |
| ericmitchell.ai | 1 |
| ent.sina.cn | 1 |
| eol.ctbu.edu.cn | 1 |
| cul.sina.com.cn | 1 |
| cultivatingdragons.com | 1 |
| copywriting.school | 1 |
| creader.io | 1 |
| d.youth.cn | 1 |
| danprattwrites.co.uk | 1 |
| culture.caixin.com | 1 |
| culture.ifeng.com | 1 |
| eshukan.com | 1 |
| gptzero.me | 1 |
| grammarguide.blog | 1 |
| gist.github.com | 1 |
| blog.moewah.com | 1 |
| harpers.org | 1 |
| huggingface.co | 1 |
| h5.if.qidian.com | 1 |
| h5.ifeng.com | 1 |
| book.qidian.com | 1 |
| flc.whcibe.com | 1 |
| cbgc.scol.com.cn | 1 |
| fastcopywriting.ai | 1 |
| generatorportal.com | 1 |
| gentext.ai | 1 |
| forum.trae.cn | 1 |
| freescreenwriter.com | 1 |
| m.qimao.com | 1 |
| sdsdwkxb.cnu.edu.cn | 1 |
| seandavi.github.io | 1 |
| scholar.google.com | 1 |
| scriptumwriterstudio.com | 1 |
| shmuhammadd.github.io | 1 |
| skillhub.cloud.tencent.com | 1 |
| www.qstheory.cn | 1 |
| shiftkognition.com | 1 |
| qikan.cqvip.com | 1 |
| quilltowers.com | 1 |
| proofreaderpro.ai | 1 |
| prowritingaid.com | 1 |
| reneefountain.com | 1 |
| s.zhangyue.com | 1 |
| read.qidian.com | 1 |
| www.wccdaily.com.cn | 1 |
| skillselion.com | 1 |
| www.frguo.com | 1 |
| sxy.szut.edu.cn | 1 |
| storyloft.app | 1 |
| study.com | 1 |
| tag.chinawriter.com.cn | 1 |
| teachers.yale.edu | 1 |
| symban.de | 1 |
| t.shuqi.com | 1 |
| socialrails.com | 1 |
| space.bilibili.com | 1 |
| slima.ai | 1 |
| sobrief.com | 1 |
| static1.squarespace.com | 1 |
| stephenking.com | 1 |
| static.32xueyuan.com | 1 |
| www.gxzf.gov.cn | 1 |
| mbook.chazidian.com | 1 |
| mckeestory.com | 1 |
| mariavsnyder.com | 1 |
| m-bbs.qimao.com | 1 |
| name-generate.com | 1 |
| nathanamick.com | 1 |
| mob.iyingdi.com | 1 |
| mwuxia.bookresource.qq.com | 1 |
| academic.oup.com | 1 |
| 3g.jjwxc.net | 1 |
| aicheck.cnki.net | 1 |
| adastra-sf.com | 1 |
| www2.xinhuanet.com | 1 |
| magazine.byu.edu | 1 |
| 3g.ali213.net | 1 |
| xh.xhby.net | 1 |
| nerdbot.com | 1 |
| ocfun.online | 1 |
| ocw.mit.edu | 1 |
| novelos.studio | 1 |
| nybookeditors.com | 1 |
| www.wxg.org.cn | 1 |
| pdfyl.ertongbook.com | 1 |
| onlinelibrary.wiley.com | 1 |
| otio.ai | 1 |
| news.cctv.com | 1 |
| www.zja.org.cn | 1 |
| news.12371.cn | 1 |
| news.bjd.com.cn | 1 |
| novelium.app | 1 |
| novelium.com | 1 |
| news.sciencenet.cn | 1 |
| noahmifsud.com | 1 |
| **合计** | **741** |

## 3g.ali213.net（1 条）

1. https://3g.ali213.net/news/html/1014173.html

## 3g.jjwxc.net（1 条）

1. https://3g.jjwxc.net/review/4058083/2/3/

## academic.oup.com（1 条）

1. https://academic.oup.com/eltj/article/78/3/356/7238831

## adastra-sf.com（1 条）

1. https://adastra-sf.com/Workshop-stuff/handouts/AnneLamott-Shitty-First-Drafts.pdf

## aicheck.cnki.net（1 条）

1. https://aicheck.cnki.net/

## alejandroashes.com（2 条）

1. https://alejandroashes.com/blog/060-serialization-sorcery/
2. https://alejandroashes.com/blog/062-foreshadowing-long-game/

## app.bjtitle.com（2 条）

1. http://app.bjtitle.com/8816/newshow.php?newsid=6492148
2. https://app.bjtitle.com/8816/newshow.php?newsid=6492148&typeid=3&uid=319283&did=862645031956476&mood=wx

## app.blurbbio.com（1 条）

1. https://app.blurbbio.com/blog/show-dont-tell-writing-guide

## app.people.cn（1 条）

1. https://app.people.cn/h5/detail/normal/5978053198726144

## arxiv.org（6 条）

1. https://arxiv.org/
2. https://arxiv.org/abs/2303.11156
3. https://arxiv.org/pdf/1906.04043.pdf
4. https://arxiv.org/pdf/2301.11305v2
5. https://arxiv.org/pdf/2310.05130v2
6. https://arxiv.org/pdf/2504.12488.pdf

## bbs.jjwxc.net（3 条）

1. https://bbs.jjwxc.net/showmsg.php?board=10&id=18229
2. https://bbs.jjwxc.net/showmsg.php?board=17&id=2279780
3. https://bbs.jjwxc.net/showmsg.php?board=4&boardpagemsg=1&id=361009

## bbs.nga.cn（3 条）

1. https://bbs.nga.cn/read.php?tid=44167146
2. https://bbs.nga.cn/read.php?tid=45043284
3. https://bbs.nga.cn/read.php?tid=47045871

## bbs.qimao.com（1 条）

1. https://bbs.qimao.com/detail/52258?categoryId=20

## bestwriting.com（1 条）

1. https://bestwriting.com/foreshadowing

## bibli.page（1 条）

1. https://bibli.page/blog/how-to-start-web-novel

## bjlove02.chinanews.com.cn（1 条）

1. https://bjlove02.chinanews.com.cn/cul/2026/09-11/10694887.shtml

## blog.moewah.com（1 条）

1. https://blog.moewah.com/posts/10-burst-title-formulas-click-rate-doubling-secrets/

## book.douban.com（7 条）

1. https://book.douban.com/review/9404971/
2. https://book.douban.com/series/11062
3. https://book.douban.com/subject/25919527/
4. https://book.douban.com/subject/30419543/
5. https://book.douban.com/subject/36378242/
6. https://book.douban.com/subject/38482520/
7. https://book.douban.com/subject/4882037/blockquotes

## book.qidian.com（1 条）

1. https://book.qidian.com/info/1209777/

## book.youth.cn（1 条）

1. http://book.youth.cn/zx/202601/t20260114_16461329.htm

## brandonsanderson.com（2 条）

1. https://brandonsanderson.com/about-brandon/
2. https://brandonsanderson.com/pages/byu-class-information

## cbgc.scol.com.cn（1 条）

1. https://cbgc.scol.com.cn/news/4354867

## ccj.pku.edu.cn（1 条）

1. https://ccj.pku.edu.cn/journal/Richtext?jid=102935&type=TGXZ

## ck.xwpx.com（1 条）

1. https://ck.xwpx.com/article/2022/0422/article_67187.html

## copywriting.school（1 条）

1. https://copywriting.school/formulas/aida

## creader.io（1 条）

1. https://creader.io/tools/foreshadowing-tracker

## cul.sina.com.cn（1 条）

1. https://cul.sina.com.cn/o/2005-09-01/1625140170.html

## cultivatingdragons.com（1 条）

1. https://cultivatingdragons.com/how-to-create-a-thrilling-wuxia-story-concept/

## culture.caixin.com（1 条）

1. https://culture.caixin.com/2017-02-26/101059501.html

## culture.ifeng.com（1 条）

1. https://culture.ifeng.com/c/7owKJcqDWNM

## culture.people.com.cn（1 条）

1. http://culture.people.com.cn/n/2014/0327/c172318-24750149.html

## d.youth.cn（1 条）

1. https://d.youth.cn/xw360/202412/t20241212_15707696.htm

## danprattwrites.co.uk（1 条）

1. https://danprattwrites.co.uk/genre-and-style/writing-effective-fight-action-scenes/

## discovery.cctv.com（2 条）

1. https://discovery.cctv.com/20070511/103391.shtml
2. https://discovery.cctv.com/20070511/103440.shtml

## dzrb.dzng.com（1 条）

1. https://dzrb.dzng.com/general/0/NEWS3630968HWPQZSYGLEIOT

## edresearchforaction.org（1 条）

1. https://edresearchforaction.org/research-briefs/evidence-based-practices-for-teaching-writing-in-middle-and-high-school/

## edshare.soton.ac.uk（1 条）

1. http://edshare.soton.ac.uk/16145/2/Freewriting.pdf

## english.northwestern.edu（1 条）

1. https://english.northwestern.edu/undergraduate/writing/

## ent.sina.cn（1 条）

1. https://ent.sina.cn/tv/tv/2016-03-11/detail-ifxqhfvp0670817.d.html

## eol.ctbu.edu.cn（1 条）

1. https://eol.ctbu.edu.cn/meol/homepage/common/onlinepreview.jsp?_style=new06&countadd=1&lid=34167&resid=1925468721

## epaper.gmw.cn（4 条）

1. https://epaper.gmw.cn/gmrb/html/2016-01/23/nw.D110000gmrb_20160123_1-12.htm
2. https://epaper.gmw.cn/wzb/html/2026-01/03/nw.D110000wzb_20260103_5-02.htm
3. https://epaper.gmw.cn/zhdsb/html/2018-06/13/nw.D110000zhdsb_20180613_2-13.htm
4. https://epaper.gmw.cn/zhdsb/html/2025-12/03/nw.D110000zhdsb_20251203_1-03.htm

## ericmitchell.ai（1 条）

1. https://ericmitchell.ai/detectgpt

## eshukan.com（1 条）

1. https://eshukan.com/academic/show.aspx?id=184961&cid=24

## euroasia.cssn.cn（1 条）

1. http://euroasia.cssn.cn/kycg/elswh/201905/t20190510_4878725.shtml

## fanqienovel.com（22 条）

1. https://fanqienovel.com/docs/8231/90699
2. https://fanqienovel.com/docs/8231/90705
3. https://fanqienovel.com/reader/7571725738345234968
4. https://fanqienovel.com/welfare?force_mobile=1
5. https://fanqienovel.com/writer/zone/article/7025884517680283655
6. https://fanqienovel.com/writer/zone/article/7226316335490269241
7. https://fanqienovel.com/writer/zone/article/7409885940115570750
8. https://fanqienovel.com/writer/zone/article/7441438066205523993
9. https://fanqienovel.com/writer/zone/article/7488225861238276121
10. https://fanqienovel.com/writer/zone/article/7496817783338958872
11. https://fanqienovel.com/writer/zone/article/7524993113262145598
12. https://fanqienovel.com/writer/zone/article/7528322925343014936
13. https://fanqienovel.com/writer/zone/article/7541251851241390104
14. https://fanqienovel.com/writer/zone/article/7561060957946920984
15. https://fanqienovel.com/writer/zone/article/7582815597575012376
16. https://fanqienovel.com/writer/zone/article/7602553801446260761
17. https://fanqienovel.com/writer/zone/article/7605818896267870270
18. https://fanqienovel.com/writer/zone/article/7619170181129961534
19. https://fanqienovel.com/writer/zone/article/7626644363652644889
20. https://fanqienovel.com/writer/zone/article/7652193948558950425
21. https://fanqienovel.com/writer/zone/article/7682623843273277464
22. https://fanqienovel.com/writer/zone/help/article?rank1=10006&rank2=10011&rank3=0

## fastcopywriting.ai（1 条）

1. https://fastcopywriting.ai/the-best-copywriting/

## files.eric.ed.gov（2 条）

1. https://files.eric.ed.gov/fulltext/ED249503.pdf
2. https://files.eric.ed.gov/fulltext/ED270758.pdf

## fiveable.me（2 条）

1. https://fiveable.me/introduction-creative-writing/unit-13/common-writing-pitfalls-avoid/study-guide/y5pw5gMFEYbLvs4S
2. https://fiveable.me/lists/show-dont-tell-examples

## flc.whcibe.com（1 条）

1. https://flc.whcibe.com/info/1023/7839.htm

## forum.trae.cn（1 条）

1. https://forum.trae.cn/t/topic/18429

## freescreenwriter.com（1 条）

1. https://freescreenwriter.com/structures/three-act-structure

## generatorportal.com（1 条）

1. https://generatorportal.com/song-name-generator/

## gentext.ai（1 条）

1. https://gentext.ai/tools/academic-title-generator/

## gist.github.com（1 条）

1. https://gist.github.com/jake9696/86f1f9d65af275d77435f6b33c78d64b

## github.com（3 条）

1. https://github.com/baoguangsheng/fast-detect-gpt
2. https://github.com/BurhanUlTayyab/DetectGPT
3. https://github.com/HendrikStrobelt/detecting-fake-text

## gptzero.me（1 条）

1. https://gptzero.me/pricing

## grammarguide.blog（1 条）

1. https://grammarguide.blog/mastering-purple-prose-how-to-spot-and-streamline-overwritten-writing/

## h5.if.qidian.com（1 条）

1. https://h5.if.qidian.com/h5/share/column?columnId=20026

## h5.ifeng.com（1 条）

1. https://h5.ifeng.com/c/vivo/v0024TlvnegWzw32mi9mNYJDJBaxaXcW9VX1xW6DOpZtewA__

## h5.wfwb.wfnews.com.cn（1 条）

1. http://h5.wfwb.wfnews.com.cn/content/20260522/Articel07001MN.htm

## harpers.org（1 条）

1. https://harpers.org/archive/2014/11/spare-the-darling/

## hs.nufe.edu.cn（1 条）

1. http://hs.nufe.edu.cn/jwc/2026/0403/c178a26454/pagem.htm

## huggingface.co（1 条）

1. https://huggingface.co/openai-community/roberta-large-openai-detector

## humanlike.pro（1 条）

1. https://humanlike.pro/tools/perplexity-burstiness

## hunan.gov.cn（1 条）

1. https://hunan.gov.cn/xxgk/wjk/swszfbgt/201212/t20121217_4825952.html

## image.chinawriter.com.cn（1 条）

1. https://image.chinawriter.com.cn/n1/2024/0730/c404024-40288735.html

## inki.so（1 条）

1. https://inki.so/en/learn/show-dont-tell

## inkshift.io（1 条）

1. https://inkshift.io/resources/saggy-middle

## item.jd.com（1 条）

1. https://item.jd.com/product/sQW6sjCVhA-KD9ZZkRBGfg.html

## jc.wanfangdata.com.cn（2 条）

1. https://jc.wanfangdata.com.cn/
2. https://jc.wanfangdata.com.cn/commonProblem

## jean-louis-vill.com（1 条）

1. https://jean-louis-vill.com/en/pacing-as-the-primary-narrative-tool-in-light-novels/

## jinyong0.com（2 条）

1. https://jinyong0.com/legacy/jin-yong-writing-style/
2. https://jinyong0.com/poetry/jin-yong-chapter-titles/

## jw.cdu.edu.cn（1 条）

1. https://jw.cdu.edu.cn/info/1043/12281.htm

## jwb.shu.edu.cn（1 条）

1. https://jwb.shu.edu.cn/2025wzcyxz.pdf

## jwc.xync.edu.cn（1 条）

1. https://jwc.xync.edu.cn/info/1032/24931.htm

## jypl.pku.edu.cn（1 条）

1. https://jypl.pku.edu.cn/Article/DownLoad?id=292869200&type=ArticleFile

## kf.om.qq.com（1 条）

1. https://kf.om.qq.com/detail/2ca5bf0b-6644-4374-962d-9a0187c693a4

## lexicalrichness.readthedocs.io（1 条）

1. https://lexicalrichness.readthedocs.io/

## lib.unn.edu.cn（1 条）

1. https://lib.unn.edu.cn/info/1014/2184.htm

## litarchive.online（1 条）

1. https://litarchive.online/lolita

## literature.cass.cn（1 条）

1. http://literature.cass.cn/ztzl/mkszywyllypp/202308/t20230822_5680515.shtml

## litfind.bookscape.com（1 条）

1. https://litfind.bookscape.com/fiction/sci-fi-fantasy/decoding-middle-earth-all-you-need-to-know-about-the-lord-of-the-rings-books/

## lobehub.com（1 条）

1. https://lobehub.com/skills/manhai934-novel-harness-story-long-write

## lsa.umich.edu（1 条）

1. https://lsa.umich.edu/sweetland/undergraduates/writing-guides/how-do-i-write-a-great-title-.html

## lyrb.lyd.com.cn（1 条）

1. http://lyrb.lyd.com.cn/html2/2016-05/25/content_69695.htm

## m.baike.com（7 条）

1. https://m.baike.com/wiki/%E4%BE%A0%E6%96%87%E5%8C%96/2352479
2. https://m.baike.com/wiki/%E6%96%B0%E9%97%BB%E6%A0%87%E9%A2%98/2864933
3. https://m.baike.com/wiki/%E6%97%A0%E9%99%90%E6%81%90%E6%80%96/19756327
4. https://m.baike.com/wiki/%E6%97%A0%E9%99%90%E6%B5%81/3284288
5. https://m.baike.com/wiki/凡人修仙传/10375488
6. https://m.baike.com/wiki/遮天/19402087
7. https://m.baike.com/wiki/诛仙/19523770

## m.bjnews.com.cn（4 条）

1. https://m.bjnews.com.cn/detail/155373957114876.html
2. https://m.bjnews.com.cn/detail/157501895715891.html
3. https://m.bjnews.com.cn/detail/1711606159168724.html
4. https://m.bjnews.com.cn/detail/1735271251168423.html

## m.book118.com（1 条）

1. https://m.book118.com/html/2016/1226/77236235.shtm

## m.cbook.qq.com（1 条）

1. https://m.cbook.qq.com/read/1022421442/11

## m.chinanews.com（1 条）

1. http://m.chinanews.com/wap/detail/chs/zw/10636048.shtml

## m.chuangshi.qq.com（1 条）

1. https://m.chuangshi.qq.com/read/34486450/1

## m.gmw.cn（2 条）

1. https://m.gmw.cn/2024-02/29/content_1303674641.htm
2. https://m.gmw.cn/toutiao/2024-06/01/content_1303752046.htm

## m.gsw6.com（1 条）

1. https://m.gsw6.com/book/tlbb/8478.html

## m.hongxiu.com（1 条）

1. https://m.hongxiu.com/baike/1pcbn19zplf5p

## m.huxiu.com（1 条）

1. https://m.huxiu.com/article/4892336.html

## m.inote.qq.com（1 条）

1. https://m.inote.qq.com/read/1029599963/3

## m.jiemian.com（1 条）

1. https://m.jiemian.com/article/13983155.html

## m.jjwxc.net（1 条）

1. https://m.jjwxc.net/book2/9709335/89

## m.pin.qq.com（2 条）

1. https://m.pin.qq.com/read/1031418188/16
2. https://m.pin.qq.com/read/1044593028/4

## m.qidian.com（5 条）

1. https://m.qidian.com/ask/qqbosskvxgtlw
2. https://m.qidian.com/booklist/detail/639424/
3. https://m.qidian.com/chapter/1042596421/835969063/?source=pc_jump
4. https://m.qidian.com/chapter/1045668670/856809844/
5. https://m.qidian.com/wenshu/qqbsknjtu/

## m.qimao.com（1 条）

1. https://m.qimao.com/activity/zhengwen/detail/481

## m.ruiwen.com（3 条）

1. https://m.ruiwen.com/wenxue/chizijian/171728.html
2. https://m.ruiwen.com/wenxue/jiapingao/51473.html
3. https://m.ruiwen.com/wenxue/zhangailing/528.html

## m.sohu.com（6 条）

1. https://m.sohu.com/a/1005099702_122129349
2. https://m.sohu.com/a/1011706131_122129349/
3. https://m.sohu.com/a/1039630288_122129349/
4. https://m.sohu.com/a/1043886560_122129349/
5. https://m.sohu.com/a/858864797_122129349/
6. https://m.sohu.com/a/986777728_122129349/

## m.thepaper.cn（8 条）

1. https://m.thepaper.cn/newsDetail_forward_13794401
2. https://m.thepaper.cn/newsDetail_forward_19539760
3. https://m.thepaper.cn/newsDetail_forward_20918889
4. https://m.thepaper.cn/newsDetail_forward_27545464
5. https://m.thepaper.cn/newsDetail_forward_27645208
6. https://m.thepaper.cn/newsDetail_forward_29218606
7. https://m.thepaper.cn/newsDetail_forward_32493759
8. https://m.thepaper.cn/wifiKey_detail.jsp?contid=8692873

## m.toutiao.com（73 条）

1. http://m.toutiao.com/group/6283671979774656769/
2. http://m.toutiao.com/group/6360559447010803969/
3. http://m.toutiao.com/group/6551285761809842696/
4. http://m.toutiao.com/group/6599140851568345614/
5. http://m.toutiao.com/group/6637342554218037773/
6. http://m.toutiao.com/group/6690023182981661195/
7. http://m.toutiao.com/group/6717441284346216968/
8. http://m.toutiao.com/group/6778628915318489608/
9. http://m.toutiao.com/group/6822090027372118531/
10. http://m.toutiao.com/group/6828824326104416782/
11. http://m.toutiao.com/group/6849241813132247560/
12. http://m.toutiao.com/group/6856746593077428744/
13. http://m.toutiao.com/group/6872666819040281095/
14. http://m.toutiao.com/group/6917181540367761934/
15. http://m.toutiao.com/group/6936064244748124703/
16. http://m.toutiao.com/group/7023186785282818568/
17. http://m.toutiao.com/group/7038821501025878564/
18. http://m.toutiao.com/group/7129824246204727843/
19. http://m.toutiao.com/group/7179531086198899238/
20. http://m.toutiao.com/group/7182122842207552038/
21. http://m.toutiao.com/group/7194601355753816611/
22. http://m.toutiao.com/group/7195056197320524288/
23. http://m.toutiao.com/group/7204776454129877536/
24. http://m.toutiao.com/group/7230753467848262199/
25. http://m.toutiao.com/group/7264213904610443816/
26. http://m.toutiao.com/group/7317906758654231103/
27. http://m.toutiao.com/group/7351358206016324135/
28. http://m.toutiao.com/group/7368733855018467881/
29. http://m.toutiao.com/group/7379213932885525004/
30. http://m.toutiao.com/group/7394369840423420435/
31. http://m.toutiao.com/group/7432879986228478476/
32. http://m.toutiao.com/group/7456776270970454568/
33. http://m.toutiao.com/group/7457503897943310875/
34. http://m.toutiao.com/group/7457903758773682722/
35. http://m.toutiao.com/group/7458200254303814194/
36. http://m.toutiao.com/group/7458251709647716879/
37. http://m.toutiao.com/group/7468239357926621708/
38. http://m.toutiao.com/group/7486064480116277801/
39. http://m.toutiao.com/group/7496353534678434356/
40. http://m.toutiao.com/group/7517096567497556480/
41. http://m.toutiao.com/group/7528344754283708980/
42. http://m.toutiao.com/group/7531729718740075049/
43. http://m.toutiao.com/group/7550620403866059274/
44. http://m.toutiao.com/group/7559059791415657002/
45. http://m.toutiao.com/group/7576556737071743528/
46. http://m.toutiao.com/group/7578918374932775466/
47. http://m.toutiao.com/group/7582871353921962550/
48. http://m.toutiao.com/group/7584684251593982474/
49. http://m.toutiao.com/group/7622277459807732251/
50. http://m.toutiao.com/group/7625507954778735123/
51. http://m.toutiao.com/group/7628246864130867750/
52. http://m.toutiao.com/group/7631860449084064262/
53. http://m.toutiao.com/group/7633421370893943331/
54. http://m.toutiao.com/group/7636240475908768306/
55. http://m.toutiao.com/group/7647106632296399412/
56. http://m.toutiao.com/group/7654464216904122920/
57. http://m.toutiao.com/group/7656469337749979698/
58. http://m.toutiao.com/group/7659181665356464674/
59. http://m.toutiao.com/group/7660304183618322970/
60. http://m.toutiao.com/group/7666311742988845583/
61. http://m.toutiao.com/group/7667406671223833129/
62. http://m.toutiao.com/group/7671171817226240538/
63. http://m.toutiao.com/group/7672767692490736143/
64. http://m.toutiao.com/group/7678132973014745615/
65. http://m.toutiao.com/group/7679625041654350374/
66. http://m.toutiao.com/group/7681132238804746752/
67. http://m.toutiao.com/group/7681464306294080043/
68. http://m.toutiao.com/group/7684867099184939556/
69. http://m.toutiao.com/group/7685310156204229147/
70. http://m.toutiao.com/group/7685570292772553255/
71. http://m.toutiao.com/group/7685585040536961580/
72. http://m.toutiao.com/group/7686077296519774755/
73. http://m.toutiao.com/group/7687335357221803621/

## m.weibo.cn（2 条）

1. https://m.weibo.cn/detail/5323205275553761
2. https://m.weibo.cn/detail/5336405924381201

## m.write.qq.com（3 条）

1. https://m.write.qq.com/portal/article/detail?CAID=24855270209864801
2. https://m.write.qq.com/portal/pointsDetail?type=points&CAID=24855270209864801&reviewid=810893124418273282
3. https://m.write.qq.com/portal/qidiancollege/learningMap

## m.xs8.cn（7 条）

1. https://m.xs8.cn/baike/1gmqm4tw4qwdu
2. https://m.xs8.cn/baike/1gmqm4tw4svz8
3. https://m.xs8.cn/baike/1gmqm4tw4swhx
4. https://m.xs8.cn/baike/1gmqm4tw4xd0u
5. https://m.xs8.cn/baike/1gmqm4tw4yrtl
6. https://m.xs8.cn/baike/1gmqm4tw4yu0x
7. https://m.xs8.cn/baike/1gmqm4tw4z4n0

## m.xxsy.net（5 条）

1. https://m.xxsy.net/baike/axdj3teuvzg5
2. https://m.xxsy.net/baike/axdj3teuxivs
3. https://m.xxsy.net/baike/axdj3tevhz8a
4. https://m.xxsy.net/baike/axdj3tevj06s
5. https://m.xxsy.net/baike/axdj3tevxbfi

## m.zxxk.com（3 条）

1. https://m.zxxk.com/soft/51192041.html
2. https://m.zxxk.com/soft/54438326.html
3. https://m.zxxk.com/soft/59607661.html

## magazine.byu.edu（1 条）

1. https://magazine.byu.edu/article/writing-of-epic-proportions/

## manual.storybuilder.org（1 条）

1. http://manual.storybuilder.org/docs/Writing%20with%20StoryCAD/Worldbuilding_Guide.html

## mariavsnyder.com（1 条）

1. https://mariavsnyder.com/2025/11/06/fight-scenes/

## m-bbs.qimao.com（1 条）

1. https://m-bbs.qimao.com/detail/61570?categoryId=41

## mbook.chazidian.com（1 条）

1. https://mbook.chazidian.com/series6091/1/

## mckeestory.com（1 条）

1. https://mckeestory.com/books/story

## media.people.com.cn（2 条）

1. http://media.people.com.cn/n1/2017/0912/c40606-29530651.html
2. http://media.people.com.cn/n1/2025/1105/c14677-40597580.html

## meiwen.gmw.cn（1 条）

1. http://meiwen.gmw.cn/2026-03/11/content_38913279.htm

## mob.iyingdi.com（1 条）

1. https://mob.iyingdi.com/post/5660990

## mooc.ytu.edu.cn（1 条）

1. http://mooc.ytu.edu.cn/meol/common/script/preview/download_preview.jsp?fileid=114783&lid=10663&preview=preview&resid=53434

## mpre.lifeweek.com.cn（1 条）

1. http://mpre.lifeweek.com.cn/h5/article/detail.do?artId=261954

## mwuxia.bookresource.qq.com（1 条）

1. https://mwuxia.bookresource.qq.com/chapter/1043061904/875569153/

## name-generate.com（1 条）

1. https://name-generate.com/book-title-generator/

## nathanamick.com（1 条）

1. https://nathanamick.com/a-living-curriculum/teaching-writing-research-2.html

## nerdbot.com（1 条）

1. https://nerdbot.com/2025/10/16/how-to-write-web-novels-a-complete-guide-for-aspiring-authors/

## news.12371.cn（1 条）

1. https://news.12371.cn/2018/06/06/ARTI1528218051574194.shtml

## news.bjd.com.cn（1 条）

1. https://news.bjd.com.cn/2025/11/13/11403894.shtml

## news.cctv.com（1 条）

1. https://news.cctv.com/2016/12/05/ARTIIPLulX6KUEr3hZlc35a8161205.shtml

## news.china.com.cn（1 条）

1. http://news.china.com.cn/2025-11/05/content_118160501.shtml

## news.gmw.cn（4 条）

1. https://news.gmw.cn/2018-06/29/content_29538208.htm
2. https://news.gmw.cn/2022-04/27/content_35692228.htm
3. https://news.gmw.cn/2023-03/17/content_36435319.htm
4. https://news.gmw.cn/2026-04/20/content_38717451.htm

## news.qq.com（1 条）

1. http://news.qq.com/rain/a/20250921A0317D00

## news.sciencenet.cn（1 条）

1. https://news.sciencenet.cn/htmlpaper/2026/4/2026422142816302149555.shtm

## noahmifsud.com（1 条）

1. https://noahmifsud.com/wp-content/uploads/2021/07/Mifsud-Final-Essay-Oxymorons.pdf

## notice.fanqienovel.com（3 条）

1. https://notice.fanqienovel.com/docs/9476/gengxin
2. https://notice.fanqienovel.com/docs/9476/gousi
3. https://notice.fanqienovel.com/docs/9476/panduan

## novelium.app（1 条）

1. https://novelium.app/books/the-lord-of-the-rings/

## novelium.com（1 条）

1. https://novelium.com/blog/chekhovs-gun-examples

## novelos.studio（1 条）

1. https://novelos.studio/blog/light-novels-webnovels/

## nybookeditors.com（1 条）

1. https://nybookeditors.com/2018/03/how-to-foreshadow-like-a-pro/

## ocfun.online（1 条）

1. https://ocfun.online/wiki/creative/style-wuxia.html

## ocw.mit.edu（1 条）

1. https://ocw.mit.edu/courses/21w-021-writing-and-experience-mit-inside-live-fall-2013/088ec08670563f1579e8de6f_MIT21W_021F13_Freewriting.pdf

## onlinelibrary.wiley.com（1 条）

1. https://onlinelibrary.wiley.com/pb-assets/assets/18607314/Title-abstract-SEO-1510014114000.pdf

## otio.ai（1 条）

1. https://otio.ai/blog/research-title-examples-ai-prompts-by-discipline

## owl.purdue.edu（2 条）

1. https://owl.purdue.edu/owl/general_writing/common_writing_assignments/argument_papers/body_paragraphs.html
2. https://owl.purdue.edu/owl/general_writing/writing_style/style%20/index.html

## paper.people.com.cn（10 条）

1. http://paper.people.com.cn/jhzk/html/2011-08/01/content_965284.htm
2. http://paper.people.com.cn/rmlt/html/2023-08/20/content_26018489.htm
3. http://paper.people.com.cn/rmlt/pc/content/202507/01/content_30087743.html
4. http://paper.people.com.cn/rmrb/images/2021-11/08/17/rmrb2021110817.pdf
5. http://paper.people.com.cn/rmrb/pc/content/202511/06/content_30113438.html
6. http://paper.people.com.cn/rmrb/pc/content/202601/20/content_30134029.html
7. http://paper.people.com.cn/rmzk/html/2019-10/17/content_1950952.htm
8. http://paper.people.com.cn/xwzx/html/2015-05/01/content_1620540.htm
9. http://paper.people.com.cn/xwzx/html/2018-11/01/content_1909318.htm
10. http://paper.people.com.cn/xwzx/html/2020-04/01/content_25934964.htm

## pdfyl.ertongbook.com（1 条）

1. https://pdfyl.ertongbook.com/76/34411108.pdf

## product.m.dangdang.com（3 条）

1. http://product.m.dangdang.com/detail11781993569-18729-1.html
2. http://product.m.dangdang.com/detail29220103-0-1.html
3. http://product.m.dangdang.com/read_book.php?pid=27859463

## proofreaderpro.ai（1 条）

1. https://proofreaderpro.ai/blog/what-is-burstiness-ai-writing

## prowritingaid.com（1 条）

1. https://prowritingaid.com/chekhovs-gun

## qikan.cqvip.com（1 条）

1. https://qikan.cqvip.com/Qikan/Search/Index?key=K%3D%E6%B8%A9%E7%91%9E%E5%AE%89

## qnck.cyol.com（1 条）

1. http://qnck.cyol.com/html/2015-07/22/nw.D110000qnck_20150722_1-20.htm

## quilltowers.com（1 条）

1. https://quilltowers.com/2025/10/13/action-screenplay-tips/

## read.qidian.com（1 条）

1. https://read.qidian.com/chapter/3Q__bQt6cZEVDwQbBL_r1g2/2RdAwWnzAsZMs5iq0oQwLQ2/

## reader.gmw.cn（3 条）

1. http://reader.gmw.cn/2024-09/10/content_37553261.htm
2. http://reader.gmw.cn/2026-01/26/content_38558332.htm
3. https://reader.gmw.cn/2025-12/15/content_38477671.htm

## reedsy.com（3 条）

1. https://reedsy.com/blog/chekhovs-gun/
2. https://reedsy.com/blog/how-to-write-a-fight-scene/
3. https://reedsy.com/blog/kill-your-darlings/

## reneefountain.com（1 条）

1. https://reneefountain.com/the-mid-book-slump-why-great-writing-cant-save-your-novel/

## s.zhangyue.com（1 条）

1. https://s.zhangyue.com/read?bid=11917625&cid=12

## scholar.google.com（1 条）

1. https://scholar.google.com/

## scriptumwriterstudio.com（1 条）

1. https://scriptumwriterstudio.com/en/blog/worldbuilding-build-novel-world.html

## sdsdwkxb.cnu.edu.cn（1 条）

1. https://sdsdwkxb.cnu.edu.cn/gkll/2017n/2021d6q_598578f464bf498a99caca1c40a71b37/e7e74db22cd0470781611c9d6f416086.htm

## seandavi.github.io（1 条）

1. https://seandavi.github.io/scriptorium/concepts/knowledge/scientific-writing/hayes-flower-writing-model/

## selfpubhub.us.com（6 条）

1. https://selfpubhub.us.com/books-aspiring-authors-should-read/
2. https://selfpubhub.us.com/building-tension/
3. https://selfpubhub.us.com/character-development/
4. https://selfpubhub.us.com/litrpg-magic-system-guide/
5. https://selfpubhub.us.com/write-fight-scenes/
6. https://selfpubhub.us.com/writing-webnovels-guide/

## shiftkognition.com（1 条）

1. https://shiftkognition.com/en/chapters/curiosity-gap-lacune-information-ia-psychologie-vente-entrepreneuriat-fondements-psychologiques-loewenstein

## shmuhammadd.github.io（1 条）

1. https://shmuhammadd.github.io/missing-guide-nlp/chapters/title

## skillhub.cloud.tencent.com（1 条）

1. https://skillhub.cloud.tencent.com/skills/ixhlink-skills-article-title

## skillselion.com（1 条）

1. https://skillselion.com/skills/worldwonderer/oh-story-claudecode/story-long-scan

## slima.ai（1 条）

1. https://slima.ai/es/resources/article/genre-masterclass-01-fantasy

## sobrief.com（1 条）

1. https://sobrief.com/books/wordcraft

## socialrails.com（1 条）

1. https://socialrails.com/blog/curiosity-gap-guide

## space.bilibili.com（1 条）

1. https://space.bilibili.com/421455632/lists

## static.32xueyuan.com（1 条）

1. https://static.32xueyuan.com/zq//u/cms/www/202410/23105515c9fi.pdf

## static.nfapp.southcn.com（2 条）

1. https://static.nfapp.southcn.com/content/202109/13/c5738680.html
2. https://static.nfapp.southcn.com/content/202403/10/c8675607.html?enterColumnId=39

## static1.squarespace.com（1 条）

1. https://static1.squarespace.com/static/55dbfccee4b08731143170b6/t/601f7b6383459e1ff5442ae6/1612675947965/On+Writing+Well+-+William+Zinsser.pdf

## stephenking.com（1 条）

1. https://stephenking.com/p/20-years-on-writing/

## storyloft.app（1 条）

1. https://storyloft.app/best-books-for-authors-to-become-better-writers/

## study.com（1 条）

1. https://study.com/academy/lesson/ben-franklins-deconstruction-reconstruction-method.html

## sudowrite.com（2 条）

1. https://sudowrite.com/blog/chekhovs-gun-foreshadowing-the-secret-of-tension-you-cant-look-away-from/
2. https://sudowrite.com/blog/progression-fantasy-ai/

## sxy.szut.edu.cn（1 条）

1. https://sxy.szut.edu.cn/info/1242/56408.htm

## symban.de（1 条）

1. https://symban.de/en/blog/building-a-magic-system

## t.shuqi.com（1 条）

1. https://t.shuqi.com/v2/query/8961605/792825.html

## tag.chinawriter.com.cn（1 条）

1. https://tag.chinawriter.com.cn/member/zsg1107zsg/viewarchives_744526.html

## teachers.yale.edu（1 条）

1. https://teachers.yale.edu/curriculum/units/2025/2/2/3

## textpulse.ai（1 条）

1. https://textpulse.ai/research/textpulse-burstiness-sentence-length-2026.pdf

## thephilosopher.net（1 条）

1. https://thephilosopher.net/heminguej/wp-content/uploads/sites/445/2024/12/Winner-Take-Nothing-Ernest-Hemingway.pdf

## tidenews.com.cn（1 条）

1. https://tidenews.com.cn/news.html?id=3301189

## titles.video（1 条）

1. https://titles.video/curiosity-gap-titles

## toolchase.com（1 条）

1. https://toolchase.com/blog/gptzero-review-accuracy-test/

## traciejoy.com（1 条）

1. https://traciejoy.com/2025/08/10/write-powerful-descriptions/

## tsg.dlutci.edu.cn（1 条）

1. http://tsg.dlutci.edu.cn/sjkfw/wfgrczxt.htm

## ubook.reader.qq.com（3 条）

1. https://ubook.reader.qq.com/baike/3dyr9wrwxon1v
2. https://ubook.reader.qq.com/baike/3dyr9wrwxuc48
3. https://ubook.reader.qq.com/baike/3dyr9wrwxuw9b

## ukpublishinghouse.co.uk（1 条）

1. https://ukpublishinghouse.co.uk/how-to-writing-a-fantasy-novel/

## view.inews.qq.com（1 条）

1. https://view.inews.qq.com/k/20210318A03MME00

## visualidentity.studio（1 条）

1. https://visualidentity.studio/how-to-write-compelling-copy/

## wanderinginn.com（1 条）

1. https://wanderinginn.com/writing-faqs/

## wap.cqcb.com（1 条）

1. https://wap.cqcb.com/shangyou_news/NewsDetail?classId=2734&newsId=6036301

## wap.faloo.com（1 条）

1. https://wap.faloo.com/1508232_4.html

## wb.lhrb.com.cn（1 条）

1. http://wb.lhrb.com.cn/page/26/2019-04/24/12/2019042412_pdf.pdf

## wenyi.gmw.cn（5 条）

1. https://wenyi.gmw.cn/2017-01/18/content_23502621.htm
2. https://wenyi.gmw.cn/2018-03/28/content_28132098.htm
3. https://wenyi.gmw.cn/2020-10/09/content_34252520.htm
4. https://wenyi.gmw.cn/2024-06/17/content_37382688.htm
5. https://wenyi.gmw.cn/2025-09/26/content_38310863.htm

## weread.qq.com（3 条）

1. https://weread.qq.com/web/search/books?author=%E5%87%A4%E6%AD%8C
2. https://weread.qq.com/web/search/books?author=%E6%B8%A9%E7%91%9E%E5%AE%89
3. https://weread.qq.com/wrpage/topic/detail/354064

## westernreflectionspublishing.com（1 条）

1. https://westernreflectionspublishing.com/blogs/purple-prose-in-writing-what-it-is-why-its-a-problem-and-how-to-steer-clear-of-it/

## wisereadshub.com（1 条）

1. https://wisereadshub.com/solving-magic-system-inconsistencies-fantasy/

## wordvice-blog-production.s3.ap-northeast-1.amazonaws.com（1 条）

1. https://wordvice-blog-production.s3.ap-northeast-1.amazonaws.com/us/wp-content/uploads/2021/08/03042612/Best-Titles-for-Your-Journal-Article-1_compressed_compressed.pdf

## write.qq.com（4 条）

1. https://write.qq.com/college/course/detail.html?CAID=5862249803776501
2. https://write.qq.com/portal/camp?type=articlebottom&CAID=21839799008963801
3. https://write.qq.com/portal/community/topic/detail/96381521685955401
4. https://write.qq.com/portal/content?caid=5379294203981401&feedType=1

## writehuman.ai（1 条）

1. https://writehuman.ai/blog/gptzero-vs-zerogpt

## writersdailypractice.com（1 条）

1. https://writersdailypractice.com/writing-exercises/daily-writing-exercises/

## writersworkshop.uiowa.edu（1 条）

1. https://writersworkshop.uiowa.edu/graduate

## writing4pleasure.com（1 条）

1. https://writing4pleasure.com/2025/11/20/our-subject-knowledge-series-what-writer-teachers-need-to-know-1-writing-as-a-process-donald-murray/

## wuxiasociety.com（5 条）

1. https://wuxiasociety.com/feng-ge
2. https://wuxiasociety.com/feng-ge/
3. https://wuxiasociety.com/gu-long
4. https://wuxiasociety.com/liang-yusheng
5. https://wuxiasociety.com/liang-yusheng/

## wuxiatales.com（1 条）

1. https://wuxiatales.com/cultivation/cultivation-realms-explained/

## www.36kr.com（1 条）

1. https://www.36kr.com/p/3659726848631685

## www.81.cn（1 条）

1. http://www.81.cn/rmjz_203219/jsjz/2023n04q/tbch_246376/16261374.html

## www.adazing.com（2 条）

1. https://www.adazing.com/worldbuilding-template/
2. https://www.adazing.com/writing-serial-fiction/

## www.andycoughlan.com（2 条）

1. https://www.andycoughlan.com/how-to-fix-a-saggy-middle
2. https://www.andycoughlan.com/how-to-write-action-scenes-that-work

## www.anima-roleplay.com（2 条）

1. https://www.anima-roleplay.com/resources/worldbuilding/worldbuilding-fundamentals/how-to-build-faction-system
2. https://www.anima-roleplay.com/resources/worldbuilding/worldbuilding-fundamentals/ultimate-guide-worldbuilding

## www.arbindbuilds.com（1 条）

1. https://www.arbindbuilds.com/blog/why-ai-detectors-keep-flagging-students-who-didnt-cheat

## www.athistleinthewind.com（1 条）

1. https://www.athistleinthewind.com/how-to-write-a-magic-system/

## www.audioenglish.org（1 条）

1. https://www.audioenglish.org/z/f_scott_fitzgerald_the_great_gatsby_p9.htm

## www.bilibili.com（6 条）

1. https://www.bilibili.com/cheese/play/ss379096582
2. https://www.bilibili.com/opus/1077797913812271125
3. https://www.bilibili.com/video/BV1pGCwYREwe/
4. https://www.bilibili.com/video/BV1PH5Y6MECA/
5. https://www.bilibili.com/video/BV1PxRmBVEFA/
6. https://www.bilibili.com/video/BV1VAD3BmEQo/

## www.billstifler.org（1 条）

1. https://www.billstifler.org/essays/07W01-revise.htm

## www.bubblecow.com（2 条）

1. https://www.bubblecow.com/blog/writing-craft/character-development/character-arcs-how-to-show-growth-and-change/
2. https://www.bubblecow.com/blog/writing-craft/writing-prompts/daily-writing-prompts-to-spark-creativity/

## www.ccs.neu.edu（1 条）

1. http://www.ccs.neu.edu/home/alina/classes/Fall2024/Lecture19.pdf

## www.chazidian.com（1 条）

1. https://www.chazidian.com/kaoshi/shiti-170207/

## www.chinafilm.gov.cn（1 条）

1. https://www.chinafilm.gov.cn/xwzx/gzdt/202603/t20260310_959544.html

## www.chinawriter.com.cn（52 条）

1. http://www.chinawriter.com.cn/404022/
2. http://www.chinawriter.com.cn/GB/n1/2018/0811/c405646-30223204.html
3. http://www.chinawriter.com.cn/n1/2016/0627/c405064-28501245.html
4. http://www.chinawriter.com.cn/n1/2017/0911/c404018-29526884.html
5. http://www.chinawriter.com.cn/n1/2017/1031/c404079-29618487.html
6. http://www.chinawriter.com.cn/n1/2019/0903/c404024-31334014.html
7. http://www.chinawriter.com.cn/n1/2020/0113/c425784-31546543.html
8. http://www.chinawriter.com.cn/n1/2020/0115/c404027-31549264.html
9. http://www.chinawriter.com.cn/n1/2020/1012/c404063-31887767.html
10. http://www.chinawriter.com.cn/n1/2021/0716/c404024-32159694.html
11. http://www.chinawriter.com.cn/n1/2021/0929/c404024-32241631.html
12. http://www.chinawriter.com.cn/n1/2022/1219/c404032-32589196.html
13. http://www.chinawriter.com.cn/n1/2024/1108/c404023-40357083.html
14. http://www.chinawriter.com.cn/n1/2025/0228/c404024-40428143.html
15. http://www.chinawriter.com.cn/n1/2025/0311/c404027-40436309.html
16. http://www.chinawriter.com.cn/n1/2025/0821/c404027-40547072.html
17. http://www.chinawriter.com.cn/n1/2025/0918/c404030-40566802.html
18. http://www.chinawriter.com.cn/n1/2025/1011/c404027-40579903.html
19. http://www.chinawriter.com.cn/n1/2025/1104/c404027-40596020.html
20. http://www.chinawriter.com.cn/n1/2025/1117/c404023-40605610.html
21. http://www.chinawriter.com.cn/n1/2026/0104/c404027-40638247.html
22. http://www.chinawriter.com.cn/n1/2026/0414/c404027-40701228.html
23. http://www.chinawriter.com.cn/n1/2026/0525/c404027-40726988.html
24. http://www.chinawriter.com.cn/n1/2026/0628/c461850-40749060.html
25. http://www.chinawriter.com.cn/n1/2026/0810/c404023-40776811.html
26. http://www.chinawriter.com.cn/n1/2026/0827/c404023-40787160.html
27. http://www.chinawriter.com.cn/n1/2026/0828/c404027-40787874.html
28. http://www.chinawriter.com.cn/news/2015/2015-09-28/254224.html
29. http://www.chinawriter.com.cn/wxpl/2014/2014-04-29/201916.html
30. http://www.chinawriter.com.cn/wxpl/2015/2015-01-07/230190.html
31. http://www.chinawriter.com.cn/wxpl/2016/2016-05-10/271818.html
32. https://www.chinawriter.com.cn/2018/0815/079698.html
33. https://www.chinawriter.com.cn/GB/n1/2021/0208/c404027-32025826.html
34. https://www.chinawriter.com.cn/n1/2017/0220/c404038-29093830.html
35. https://www.chinawriter.com.cn/n1/2017/0906/c404066-29518712.html
36. https://www.chinawriter.com.cn/n1/2017/1031/c404079-29618487.html
37. https://www.chinawriter.com.cn/n1/2019/0816/c405645-31300293.html
38. https://www.chinawriter.com.cn/n1/2019/1030/c404064-31427902.html
39. https://www.chinawriter.com.cn/n1/2019/1228/c403994-31526964.html
40. https://www.chinawriter.com.cn/n1/2020/0113/c404027-31546012.html
41. https://www.chinawriter.com.cn/n1/2021/0201/c404032-32018755.html
42. https://www.chinawriter.com.cn/n1/2021/0317/c404027-32053332.html
43. https://www.chinawriter.com.cn/n1/2022/0825/c403937-32511338.html
44. https://www.chinawriter.com.cn/n1/2023/0824/c404027-40063013.html
45. https://www.chinawriter.com.cn/n1/2024/0520/c404064-40239171.html
46. https://www.chinawriter.com.cn/n1/2025/0903/c404027-40556273.html
47. https://www.chinawriter.com.cn/n1/2025/1022/c404027-40587015.html
48. https://www.chinawriter.com.cn/n1/2025/1030/c404027-40592897.html
49. https://www.chinawriter.com.cn/n1/2026/0108/c404027-40641641.html
50. https://www.chinawriter.com.cn/n1/2026/0428/c404030-40710402.html
51. https://www.chinawriter.com.cn/n1/2026/0610/c404027-40737570.html
52. https://www.chinawriter.com.cn/wxpl/2015/2015-02-06/233558.html

## www.chinaxwcb.com（1 条）

1. https://www.chinaxwcb.com/2026/08/21/99883571.html

## www.cl.ntpu.edu.tw（1 条）

1. https://www.cl.ntpu.edu.tw/ntpu-20/D1.鄭仁維談文：玄武之變.pdf

## www.classcentral.com（1 条）

1. https://www.classcentral.com/course/youtube-2020-creative-writing-lectures-at-byu-53045

## www.cmu.edu（1 条）

1. https://www.cmu.edu/dietrich/sds/docs/loewenstein/Curiosity_IntlHandbookEmotEduc.pdf

## www.cnr.cn（2 条）

1. http://www.cnr.cn/newscenter/native/gd/20251111/t20251111_527426949.shtml
2. http://www.cnr.cn/yuleguangbo/sysh/20181010/t20181010_524381359.shtml

## www.cntv.cn（1 条）

1. https://www.cntv.cn/program/bjjt/20050107/100998.shtml

## www.codartium.com（1 条）

1. https://www.codartium.com/fictional-world-construction-in-novel-writing/

## www.coollibri.es（1 条）

1. https://www.coollibri.es/blog/el-arte-de-crear-titulos-irresistibles-para-tu-libro-y-captar-lectores-desde-la-portada/

## www.degruyterbrill.com（1 条）

1. https://www.degruyterbrill.com/document/doi/10.1515/csh-2025-0001/html

## www.diancang.xyz（1 条）

1. https://www.diancang.xyz/xueshuzaji/20281/369013.html

## www.digitalmarketingagency.sg（1 条）

1. https://www.digitalmarketingagency.sg/blog/ad-copy-examples

## www.entangledtext.com（1 条）

1. https://www.entangledtext.com/guides/ai-litrpg-power-progression-pacing

## www.eshukan.com（1 条）

1. https://www.eshukan.com/bd_show.aspx?cid=24&id=221887

## www.eyesift.com（1 条）

1. https://www.eyesift.com/blog/how-to-make-ai-writing-sound-human/

## www.fable.la（1 条）

1. https://www.fable.la/blog/purple-prose-guide

## www.fatskills.com（1 条）

1. https://www.fatskills.com/mechanical-engineering/chapter/fbla-fbla-copywriting-headlines-body-copy-calltoaction

## www.frguo.com（1 条）

1. http://www.frguo.com/content/2017/08/24/10513165.html

## www.frontiersin.org（1 条）

1. https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2022.935274/full

## www.fudan.edu.cn（1 条）

1. https://www.fudan.edu.cn/2024/0603/c24a141020/page.htm

## www.fulltextarchive.com（1 条）

1. https://www.fulltextarchive.com/book/The-Great-Gatsby/7/

## www.globalpeople.com.cn（1 条）

1. https://www.globalpeople.com.cn/waphtml/channel/44/17435.html

## www.gmw.cn（1 条）

1. https://www.gmw.cn/01ds/2006-11/29/content_515332.htm

## www.gov.cn（2 条）

1. https://www.gov.cn/gongbao/content/2000/content_60454.htm
2. https://www.gov.cn/zwgk/2013-02/22/content_2337704.htm

## www.gptcleanup.com（1 条）

1. https://www.gptcleanup.com/perplexity-originality-checker

## www.grammarly.com（1 条）

1. https://www.grammarly.com/blog/press/grammarly-superhuman-gptzero/

## www.gushici.net（1 条）

1. https://www.gushici.net/zuozhe/08/203.html

## www.gxzf.gov.cn（1 条）

1. http://www.gxzf.gov.cn/zfwj/zzqrmzfwj_34845/t1508766.shtml

## www.hfou.net.cn（1 条）

1. https://www.hfou.net.cn/html/msg/52652.html

## www.hongxiu.com（1 条）

1. https://www.hongxiu.com/baike/1pcbn19zpitzk

## www.howtowriteanovel.co.uk（1 条）

1. https://www.howtowriteanovel.co.uk/13-worldbuilding

## www.hunnu.edu.cn（1 条）

1. https://www.hunnu.edu.cn/info/1026/14848.htm

## www.iesdouyin.com（85 条）

1. http://www.iesdouyin.com/share/video/7598780393151696134
2. http://www.iesdouyin.com/share/video/7646721393081486601
3. http://www.iesdouyin.com/share/video/7664217160864042290
4. https://www.iesdouyin.com/share/video/7069757860967615777
5. https://www.iesdouyin.com/share/video/7392513753956355363
6. https://www.iesdouyin.com/share/video/7563896009764392255
7. https://www.iesdouyin.com/share/video/7579911553572875187
8. https://www.iesdouyin.com/share/video/7587242191819967793
9. https://www.iesdouyin.com/share/video/7588362304610736997
10. https://www.iesdouyin.com/share/video/7589173166388399369
11. https://www.iesdouyin.com/share/video/7592451299161984266
12. https://www.iesdouyin.com/share/video/7593781510038211891
13. https://www.iesdouyin.com/share/video/7598480585220279606
14. https://www.iesdouyin.com/share/video/7598780393151696134
15. https://www.iesdouyin.com/share/video/7599909814717975817
16. https://www.iesdouyin.com/share/video/7602914611433089465
17. https://www.iesdouyin.com/share/video/7603067079969272290
18. https://www.iesdouyin.com/share/video/7610458343639630720
19. https://www.iesdouyin.com/share/video/7613047666443914515
20. https://www.iesdouyin.com/share/video/7613156544783992229
21. https://www.iesdouyin.com/share/video/7618881104317107506
22. https://www.iesdouyin.com/share/video/7618938687044209930
23. https://www.iesdouyin.com/share/video/7622659698440867122
24. https://www.iesdouyin.com/share/video/7625617387395599643
25. https://www.iesdouyin.com/share/video/7625941382208769307
26. https://www.iesdouyin.com/share/video/7627116710876826930
27. https://www.iesdouyin.com/share/video/7630667088742436148
28. https://www.iesdouyin.com/share/video/7633244120534571209
29. https://www.iesdouyin.com/share/video/76332441209
30. https://www.iesdouyin.com/share/video/7634884894484894970
31. https://www.iesdouyin.com/share/video/7634898643765524657
32. https://www.iesdouyin.com/share/video/7638594108521030281
33. https://www.iesdouyin.com/share/video/7641485718473126635
34. https://www.iesdouyin.com/share/video/7641903327223443441
35. https://www.iesdouyin.com/share/video/7642884583326797083
36. https://www.iesdouyin.com/share/video/7643322618690473254
37. https://www.iesdouyin.com/share/video/7643516930854374671
38. https://www.iesdouyin.com/share/video/7644457971224677668
39. https://www.iesdouyin.com/share/video/7644633867421566696
40. https://www.iesdouyin.com/share/video/7645253116635385103
41. https://www.iesdouyin.com/share/video/7645846502962679055
42. https://www.iesdouyin.com/share/video/7646261352805910693
43. https://www.iesdouyin.com/share/video/7646721393081486601
44. https://www.iesdouyin.com/share/video/7648686466948178289
45. https://www.iesdouyin.com/share/video/7649205446603001115
46. https://www.iesdouyin.com/share/video/7649714389423033642
47. https://www.iesdouyin.com/share/video/7650129239739501834
48. https://www.iesdouyin.com/share/video/7651612158588931362
49. https://www.iesdouyin.com/share/video/7651813208260945363
50. https://www.iesdouyin.com/share/video/7651931451618256355
51. https://www.iesdouyin.com/share/video/7654477697665617193
52. https://www.iesdouyin.com/share/video/7654777500950372068
53. https://www.iesdouyin.com/share/video/7657528829259870826
54. https://www.iesdouyin.com/share/video/7659000811351440875
55. https://www.iesdouyin.com/share/video/7660114117662879401
56. https://www.iesdouyin.com/share/video/7660367581819276586
57. https://www.iesdouyin.com/share/video/7660789007421554010
58. https://www.iesdouyin.com/share/video/7661113117917966770
59. https://www.iesdouyin.com/share/video/7661849588706371327
60. https://www.iesdouyin.com/share/video/7662575343567506715
61. https://www.iesdouyin.com/share/video/7663772590565035315
62. https://www.iesdouyin.com/share/video/7664217160864042290
63. https://www.iesdouyin.com/share/video/7664785632715214114
64. https://www.iesdouyin.com/share/video/7664816281689787654
65. https://www.iesdouyin.com/share/video/7664817754414864485
66. https://www.iesdouyin.com/share/video/7665895734092287238
67. https://www.iesdouyin.com/share/video/7666994353593083647
68. https://www.iesdouyin.com/share/video/7668642412806136420
69. https://www.iesdouyin.com/share/video/7669390924389378922
70. https://www.iesdouyin.com/share/video/7669593350605617834
71. https://www.iesdouyin.com/share/video/7669691298252639497
72. https://www.iesdouyin.com/share/video/7669747368560756203
73. https://www.iesdouyin.com/share/video/7670545908022398208
74. https://www.iesdouyin.com/share/video/7670590875889618217
75. https://www.iesdouyin.com/share/video/7670593160120143114
76. https://www.iesdouyin.com/share/video/7671677343227975674
77. https://www.iesdouyin.com/share/video/7672786068894823525
78. https://www.iesdouyin.com/share/video/7674054496582361999
79. https://www.iesdouyin.com/share/video/7674820759433777595
80. https://www.iesdouyin.com/share/video/7675827275559963930
81. https://www.iesdouyin.com/share/video/7678624428301059569
82. https://www.iesdouyin.com/share/video/7680516166314131050
83. https://www.iesdouyin.com/share/video/7681643501700950248
84. https://www.iesdouyin.com/share/video/7683037559584945320
85. https://www.iesdouyin.com/share/video/7686484123992509715

## www.independenteditorsgroup.com（1 条）

1. https://www.independenteditorsgroup.com/the-gun-on-the-wall-and-the-footprint-under-the-window-setups-and-payoffs-in-fiction

## www.inewsweek.cn（1 条）

1. https://www.inewsweek.cn/observe/2025-12-29/28301.shtml

## www.inkfluenceai.com（1 条）

1. https://www.inkfluenceai.com/book-title-generator

## www.jjwxc.net（7 条）

1. https://www.jjwxc.net/aboutus/?more
2. https://www.jjwxc.net/onebook.php?chapterid=122&novelid=7920035
3. https://www.jjwxc.net/onebook.php?chapterid=3&novelid=9709335
4. https://www.jjwxc.net/onebook.php?chapterid=8&novelid=42725
5. https://www.jjwxc.net/onebook.php?chapterid=90&novelid=9709335
6. https://www.jjwxc.net/onebook.php?novelid=5550777&chapterid=1
7. https://www.jjwxc.net/onebook.php?novelid=8892603

## www.jssjx.com.cn（1 条）

1. https://www.jssjx.com.cn/yaowen/202609/t20260911_s6aa41339e4b0c7c3ee73cd0c.shtml

## www.jstor.org（1 条）

1. https://www.jstor.org/stable/357662

## www.julian.com（1 条）

1. https://www.julian.com/guide/write/practicing

## www.kflz.gov.cn（1 条）

1. https://www.kflz.gov.cn/sitesources/nysjwjw/page_pc/xcjd/s/articlee0159b63231f4d5eb3965f3ac028dee3.html

## www.kuaikanmanhua.com（1 条）

1. https://www.kuaikanmanhua.com/qa1/115591

## www.litcharts.com（1 条）

1. https://www.litcharts.com/lit/a-clean-well-lighted-place/summary-and-analysis

## www.literatureandlatte.com（1 条）

1. https://www.literatureandlatte.com/blog/how-copywork-and-imitation-can-help-writers-improve-their-own-style

## www.lkong.com（1 条）

1. https://www.lkong.com/thread/3042256

## www.loreteller.com（2 条）

1. https://www.loreteller.com/learn/faction-design-fiction/
2. https://www.loreteller.com/learn/story-boring-middle/

## www.masterclass.com（1 条）

1. https://www.masterclass.com/classes/margaret-atwood-teaches-creative-writing

## www.mochalabz.com（1 条）

1. https://www.mochalabz.com/artigos/formulas-headline-copywriting/

## www.mx-xz.com（1 条）

1. https://www.mx-xz.com/show_34042.html

## www.mypitaya.com（1 条）

1. https://www.mypitaya.com/

## www.nationalreading.gov.cn（1 条）

1. https://www.nationalreading.gov.cn/tshzx/202506/t20250611_899641.html

## www.news.cn（3 条）

1. http://www.news.cn/2021-11/07/c_1128041088.htm
2. https://www.news.cn/politics/20241107/57e02cefee2a455c8fa8d93ed2d7db99/c.html
3. https://www.news.cn/politics/20250606/d61094cbb08b4c448fe8e857afd50dfc/c.html

## www.nmg.gov.cn（1 条）

1. https://www.nmg.gov.cn/zwgk/zfgb/2012n_4898/201220/201209/t20120910_300796.html

## www.opp2.com（1 条）

1. https://www.opp2.com/194104.html

## www.oscarghostwriting.com（1 条）

1. https://www.oscarghostwriting.com/blog/what-is-the-three-act-structure-and-do-you-actually-need-it/

## www.paperdue.com（1 条）

1. https://www.paperdue.com/topic/self-respect-essays

## www.paperpass.com（2 条）

1. https://www.paperpass.com/aigc
2. https://www.paperpass.com/knowledge/23914.html

## www.penguinrandomhouse.ca（1 条）

1. https://www.penguinrandomhouse.ca/books/119445/lolita-by-vladimir-nabokov/9780679723165/excerpt

## www.peopleapp.com（1 条）

1. https://www.peopleapp.com/rmharticle/30022000002

## www.peterthomson.com（1 条）

1. https://www.peterthomson.com/blog/how-to-write-headlines

## www.qidian.com（7 条）

1. https://www.qidian.com/book/1010868264.html
2. https://www.qidian.com/book/1027095179.html
3. https://www.qidian.com/book/1034129546.html
4. https://www.qidian.com/book/1104632.html
5. https://www.qidian.com/book/2089495.html
6. https://www.qidian.com/book/554920.html
7. https://www.qidian.com/book/7055086.html

## www.qimao.com（3 条）

1. https://www.qimao.com/gonggao/625f8fe933c8c949271071b6/
2. https://www.qimao.com/gonggao/66068db2727af1329d4bdde2/
3. https://www.qimao.com/writing-camp/new-author/publicity/

## www.qstheory.cn（1 条）

1. http://www.qstheory.cn/20260427/2b03b70094c94c478365bdec826e47b3/c.html

## www.readnovel.com（1 条）

1. https://www.readnovel.com/baike/1y2jhj80z6y3m

## www.rebellink.com（1 条）

1. https://www.rebellink.com/copywriting-formulas

## www.renascence.io（1 条）

1. https://www.renascence.io/behavioral-biases/curiosity-effect

## www.scribblehubforum.com（1 条）

1. https://www.scribblehubforum.com/threads/power-creep.24013/

## www.scribbr.com（1 条）

1. https://www.scribbr.com/rhetoric/purple-prose/

## www.sfedit.net（2 条）

1. https://www.sfedit.net/5-proven-ways-to-title-a-research-paper-effectively/
2. https://www.sfedit.net/how-do-you-write-a-strong-title-for-a-research-paper/

## www.shenqiu.gov.cn（1 条）

1. https://www.shenqiu.gov.cn/newslast_2433.html

## www.songwriter.co.uk（1 条）

1. https://www.songwriter.co.uk/page86.html

## www.squibler.io（1 条）

1. https://www.squibler.io/learn/writing/how-to-write-a-fight-scene/

## www.summonworlds.com（1 条）

1. https://www.summonworlds.com/create-fantasy-factions-power-struggles/

## www.tandfonline.com（1 条）

1. https://www.tandfonline.com/doi/10.1080/04250494.2021.1885975

## www.textsight.ai（1 条）

1. https://www.textsight.ai/blog/sentence-length-variance/

## www.tolkienestate.com（1 条）

1. https://www.tolkienestate.com/letters/letter-to-milton-waldman-publisher-1951/

## www.trinka.ai（1 条）

1. https://www.trinka.ai/blog/how-to-write-a-research-paper-title/

## www.tumblr.com（1 条）

1. https://www.tumblr.com/4eyedtimelord/tagged/spilled%20quotes

## www.uea.ac.uk（1 条）

1. https://www.uea.ac.uk/course/postgraduate/ma-creative-writing

## www.vortenza.com（1 条）

1. https://www.vortenza.com/guides/perplexity-burstiness-ai-writing

## www.wangwenclub.com（1 条）

1. https://www.wangwenclub.com/handbook/类型大全/无限流

## www.wanweixueshu.com（1 条）

1. https://www.wanweixueshu.com/news/detail/22508

## www.wccdaily.com.cn（1 条）

1. http://www.wccdaily.com.cn/shtml/hxdsb/20230925/201695.shtml

## www.weixinhost.com（1 条）

1. https://www.weixinhost.com/blog/viral-title-generator-tips/

## www.wenyiso.com（1 条）

1. https://www.wenyiso.com/gaozhongcailiaozuowen/236.htm

## www.woshipm.com（2 条）

1. https://www.woshipm.com/ai/6235191.html
2. https://www.woshipm.com/share/6453618.html

## www.writingmastery.com（1 条）

1. https://www.writingmastery.com/blog/what-is-a-character-arc-a-guide-to-types-of-character-arcs-in-fiction

## www.wtxy.net（1 条）

1. https://www.wtxy.net/book/story.php?id=3445

## www.wxg.org.cn（1 条）

1. http://www.wxg.org.cn/wxsl/4214.jhtml

## www.xinhuanet.com（3 条）

1. http://www.xinhuanet.com/book/20220412/efa6a020dd914d70992677d6bd309113/c.html
2. http://www.xinhuanet.com/zgjx/2019v/20250611/2be6dd33f1ff4dd1a8c5c28b6f504254/c.html
3. https://www.xinhuanet.com/politics/2018-11/03/c_1123656210.htm

## www.xs8.cn（2 条）

1. http://www.xs8.cn/baike/1gmqm4tw4ll5i
2. http://www.xs8.cn/baike/1gmqm4tw4vs8i

## www.xuexi.cn（2 条）

1. https://www.xuexi.cn/lgpage/detail/index.html?id=4990342789526634461
2. https://www.xuexi.cn/lgpage/detail/index.html?id=4990342789526634461&item_id=4990342789526634461

## www.xwpx.com（3 条）

1. https://www.xwpx.com/article/2026/0121/article_73059.html
2. https://www.xwpx.com/article/2026/0209/article_73148.html
3. https://www.xwpx.com/article/2026/0408/article_73366.html

## www.xxsy.net（2 条）

1. https://www.xxsy.net/baike/axdj3teuxaek
2. https://www.xxsy.net/baike/axdj3tev1bbu

## www.yunyingpai.com（1 条）

1. https://www.yunyingpai.com/content/444589.html

## www.zdushi.com（1 条）

1. https://www.zdushi.com/news/s_4469350.html

## www.zja.org.cn（1 条）

1. http://www.zja.org.cn/zja/system/2022/08/29/033803888.shtml

## www2.xinhuanet.com（1 条）

1. http://www2.xinhuanet.com/ent/20260306/e097ac4892234ae9a2c30bb5af1f0bd5/c.html

## wxs.sass.org.cn（1 条）

1. https://wxs.sass.org.cn/2023/0606/c6913a545473/page.htm

## wxy.qfnu.edu.cn（1 条）

1. https://wxy.qfnu.edu.cn/__local/4/4A/1E/2D623529FB2680599B0B34CDD60_EE51B988_74323.pdf

## wxyxz.xtu.edu.cn（1 条）

1. https://wxyxz.xtu.edu.cn/info/1008/1053.htm

## wyb.chinawriter.com.cn（10 条）

1. https://wyb.chinawriter.com.cn/attachment/202104/30/6342ffb7-2868-4ca4-8087-7eace21b1a38.pdf
2. https://wyb.chinawriter.com.cn/attachment/202206/27/04f63628-7894-42d9-877f-3a01295799a7.pdf
3. https://wyb.chinawriter.com.cn/attachment/202308/25/ddda63c5-3501-4d67-9ead-2c6251726c38.pdf
4. https://wyb.chinawriter.com.cn/attachment/202403/04/718e2548-5ece-419c-8bd7-1c6abaa6b4a2.pdf
5. https://wyb.chinawriter.com.cn/attachment/202406/03/c9188a56-ee7e-4683-b398-cbaa8ecc012a.pdf
6. https://wyb.chinawriter.com.cn/content/202109/17/content61680.html
7. https://wyb.chinawriter.com.cn/content/202308/23/content71392.html
8. https://wyb.chinawriter.com.cn/content/202608/10/content84876.html
9. https://wyb.chinawriter.com.cn/Pad/content/202403/25/content74013.html
10. https://wyb.chinawriter.com.cn/Pad/content/202607/17/content84610.html

## xbgjxt.swu.edu.cn（3 条）

1. http://xbgjxt.swu.edu.cn/article/doi/10.13718/j.cnki.xdsk.2021.06.017
2. https://xbgjxt.swu.edu.cn/article/id/jsusse201904014
3. https://xbgjxt.swu.edu.cn/data/article/preview-pdf?doi=10.13718/j.cnki.xdsk.2021.04.017

## xh.xhby.net（1 条）

1. http://xh.xhby.net/pc/con/202603/13/content_1536931.html

## xiezuocat.com（1 条）

1. https://xiezuocat.com/

## xmds.cbpt.cnki.net（1 条）

1. https://xmds.cbpt.cnki.net/WKH/WebPublication/wkTextContent.aspx?contentID=3a752e03-c4e6-4c42-8f31-6786080ea6cf

## yiban.io（1 条）

1. https://yiban.io/blog/217

## youmind.com（1 条）

1. https://youmind.com/zh-CN/skills/social-media-headlines-0zbdlH0SrCAnxS

## yzwb.sjzdaily.com.cn（2 条）

1. http://yzwb.sjzdaily.com.cn/yzwbpaper/pc/att/202607/16/3867a3a1-f5c1-49ec-a53b-05547a5ad26d.pdf
2. http://yzwb.sjzdaily.com.cn/yzwbpaper/pc/content/202607/30/content_252426.html

## zh.wikipedia.org（14 条）

1. https://zh.wikipedia.org/wiki/
2. https://zh.wikipedia.org/wiki/百年孤独
3. https://zh.wikipedia.org/wiki/冰与火之歌
4. https://zh.wikipedia.org/wiki/福尔摩斯探案集
5. https://zh.wikipedia.org/wiki/哈利·波特
6. https://zh.wikipedia.org/wiki/红楼梦
7. https://zh.wikipedia.org/wiki/基督山伯爵
8. https://zh.wikipedia.org/wiki/聊斋志异
9. https://zh.wikipedia.org/wiki/魔戒
10. https://zh.wikipedia.org/wiki/三个火枪手
11. https://zh.wikipedia.org/wiki/三国演义
12. https://zh.wikipedia.org/wiki/沙丘
13. https://zh.wikipedia.org/wiki/水滸傳
14. https://zh.wikipedia.org/wiki/西游记

## zhiping.huaczy.com（1 条）

1. https://zhiping.huaczy.com/）等

## zibo.dzwww.com（1 条）

1. https://zibo.dzwww.com/mshshh/202410/t20241030_15030348.htm

# 第二十四轮新增（2026-09-23）：第九批创作工艺资料

> 本轮为 dialogue-craft.md / viewpoint-craft.md / novel-craft.md / self-check-workflow.md / by-genre.md / exemplar-close-reading.md 落库而清点。来源九份创作工艺附件：感情线（反工业糖精，113 行）、转场（硬软切，134 行）、命名（命名禁忌，114 行）、POV（head-hopping，146 行）、对话（动作beat，144 行）、复盘（复盘框架，91 行）、短篇（顿悟结尾，81 行）、分题材（历史考据，122 行）、范文精读（傲慢与偏见第一章，118 行）。九份附件原始 URL 126 条（按资源计：短篇附件内莫泊桑《项链》英译本链接 human.libretexts.org 在正文以省略形式、在参考资料以完整形式重复书写，同一资源计 1 条），其中 2 条为跨附件共引（gutenberg.org/ebooks/1342 对话与 POV 共引；sheahulse.com 慢燃指南感情线与分题材共引），去重后净新增 124 条，按域名分组如下。清点方式：脚本提取+比对，非目测。**本文件只保证"原文档里写了这个链接"，不说明链接内容说了什么、不保证现在仍可访问。**

| 域名 | 条数 |
|---|---|
| www.gutenberg.org | 5 |
| writoryofficial.com | 5 |
| www.iesdouyin.com | 4 |
| book.douban.com | 3 |
| novelos.studio | 3 |
| sobrief.com | 3 |
| epaper.gmw.cn | 2 |
| fiveable.me | 2 |
| fordmountainpublishing.com | 2 |
| inkshift.io | 2 |
| jerryjenkins.com | 2 |
| jerichowriters.com | 2 |
| m.gushiwen.cn | 2 |
| scriptumwriterstudio.com | 2 |
| selfpubhub.us.com | 2 |
| www.bubblecow.com | 2 |
| www.editorworld.com | 2 |
| www.tumblr.com | 2 |
| writersdigestonline.com | 2 |
| app.blurbbio.com | 1 |
| assets.litcharts.com | 1 |
| bbs.jjwxc.net | 1 |
| blog.reedsy.com | 1 |
| books.openbookpublishers.com | 1 |
| brandonsanderson.com | 1 |
| chapterly.ai | 1 |
| edwinashaw.com | 1 |
| ensemblewriter.com | 1 |
| floridawriters.blog | 1 |
| hearth.sh | 1 |
| human.libretexts.org | 1 |
| jamigold.com | 1 |
| killzoneblog.com | 1 |
| kokuren333.github.io | 1 |
| lib.nua.edu.cn | 1 |
| lovelinesstudio.com | 1 |
| m.gmw.cn | 1 |
| m.news.cctv.com | 1 |
| m.thepaper.cn | 1 |
| m.write.qq.com | 1 |
| maiziebennett.com | 1 |
| melbourneprintpublish.com.au | 1 |
| nathanielconnors.com | 1 |
| novelconceptspublishing.com | 1 |
| novelmint.ai | 1 |
| olivespencer.com | 1 |
| owl.purdue.edu | 1 |
| pdfs.semanticscholar.org | 1 |
| qnzj.cyol.com | 1 |
| recentrevelations.tumblr.com | 1 |
| selfpublishing.com | 1 |
| sheahulse.com | 1 |
| storyloft.app | 1 |
| tag.chinawriter.com.cn | 1 |
| thelittlebookish.com | 1 |
| thewritepractice.com | 1 |
| tryathens.com | 1 |
| web.mit.edu | 1 |
| westernreflectionspublishing.com | 1 |
| writemeamurder.co.uk | 1 |
| writewithharte.com | 1 |
| writingcenter.gmu.edu | 1 |
| writingnsw.org.au | 1 |
| www.21cnjy.com | 1 |
| www.anton-chehov.info | 1 |
| www.aplaceofintent.co.uk | 1 |
| www.asu.edu | 1 |
| www.caroclarke.com | 1 |
| www.cattediting.com | 1 |
| www.cctv.com | 1 |
| www.chinawriter.com.cn | 1 |
| www.dl-library.net.cn | 1 |
| www.elaineflinn.com | 1 |
| www.firstdraftpro.com | 1 |
| www.fudan.edu.cn | 1 |
| www.gmw.cn | 1 |
| www.helpingwritersbecomeauthors.com | 1 |
| www.hubpd.com | 1 |
| www.ihuaben.com | 1 |
| www.ibiblio.org | 1 |
| www.ijim.in | 1 |
| www.jjwxc.net | 1 |
| www.livewritethrive.com | 1 |
| www.loreteller.com | 1 |
| www.neac.gov.cn | 1 |
| www.notmfa.com | 1 |
| www.oscarghostwriting.com | 1 |
| www.savannahgilbo.com | 1 |
| www.shyeditor.com | 1 |
| www.sleuthsayers.org | 1 |
| www.strandbooks.com | 1 |
| www.tacczx.com | 1 |
| www.transtutor.blog | 1 |
| wyb.chinawriter.com.cn | 1 |
| **合计** | **124** |

## app.blurbbio.com（1 条）

1. https://app.blurbbio.com/blog/how-to-name-characters

## assets.litcharts.com（1 条）

1. https://assets.litcharts.com/lit/lolita/literary-devices/unreliable-narrator

## bbs.jjwxc.net（1 条）

1. https://bbs.jjwxc.net/showmsg.php?board=17&boardpagemsg=16738&id=1566023

## blog.reedsy.com（1 条）

1. https://blog.reedsy.com/guide/elements-of-plot/exposition/

## book.douban.com（3 条）

1. https://book.douban.com/subject/2266809/blockquotes
2. https://book.douban.com/subject/26717137/
3. https://book.douban.com/subject/1806357/

## books.openbookpublishers.com（1 条）

1. https://books.openbookpublishers.com/10.11647/obp.0039/ch3.xhtml

## brandonsanderson.com（1 条）

1. https://brandonsanderson.com/pages/writing-advice

## chapterly.ai（1 条）

1. https://chapterly.ai/summaries/one-hundred-years-of-solitude-marquez

## edwinashaw.com（1 条）

1. https://edwinashaw.com/tag/rewriting/

## ensemblewriter.com（1 条）

1. https://ensemblewriter.com/docs/montages-and-series-of-shots

## epaper.gmw.cn（2 条）

1. http://epaper.gmw.cn/wzb/html/2015-02/03/nw.D110000wzb_20150203_10-07.htm
2. https://epaper.gmw.cn/wzb/html/2015-11/19/nw.D110000wzb_20151119_7-07.htm

## fiveable.me（2 条）

1. https://fiveable.me/lists/scene-transitions
2. https://fiveable.me/introduction-creative-writing/unit-6/dialogue-tags-action-beats/study-guide/ax9wqGaYDaulUWp1

## floridawriters.blog（1 条）

1. https://floridawriters.blog/what-do-you-have-to-say-for-yourself/

## fordmountainpublishing.com（2 条）

1. https://fordmountainpublishing.com/your-first-draft-isnt-the-problem-your-editing-process-is-how-to-actually-edit-your-own-book/
2. https://fordmountainpublishing.com/the-self-editing-workbook-a-structural-revision-system-for-your-novel/

## hearth.sh（1 条）

1. https://hearth.sh/guides/info-dump

## human.libretexts.org（1 条）

1. https://human.libretexts.org/Bookshelves/Literature_and_Literacy/Compact_Anthology_of_World_Literacy_-_4_5_and_6_(Turlington_et_al.)/5:_The_Long_Nineteenth_Century/04:_Realism/4.12:_Guy_de_Maupassant_(1850-1893)/4.12.02:_The_Diamond_Necklace

## inkshift.io（2 条）

1. https://inkshift.io/resources/head-hopping
2. https://inkshift.io/resources/romance-arcs

## jamigold.com（1 条）

1. https://jamigold.com/2020/05/how-to-improve-our-story-with-action-beats/

## jerichowriters.com（2 条）

1. https://jerichowriters.com/narrative-distance-definition-with-examples-for-fiction-writers/
2. https://jerichowriters.com/writing-dialogue/

## jerryjenkins.com（2 条）

1. https://jerryjenkins.com/character-names/
2. https://jerryjenkins.com/subtext-examples/

## killzoneblog.com（1 条）

1. https://killzoneblog.com/tag/deep-pov

## kokuren333.github.io（1 条）

1. https://kokuren333.github.io/GRVS_009_NovelWriting/30_%E5%A0%B4%E9%9D%A2%E3%83%BB%E3%83%86%E3%83%B3%E3%83%9D%E3%83%BB%E6%83%85%E5%A0%B1%E9%96%8B%E7%A4%BA/%E5%A0%B4%E9%9D%A2%E8%BB%A2%E6%8F%9B%E3%81%AE%E6%8A%80%E8%A1%93

## lib.nua.edu.cn（1 条）

1. https://lib.nua.edu.cn/2025/0929/c4138a117250/page.htm

## lovelinesstudio.com（1 条）

1. https://lovelinesstudio.com/chemistry-on-the-page-how-to-write-attraction-readers-can-feel/

## m.gmw.cn（1 条）

1. https://m.gmw.cn/2026-01/29/content_38566615.htm

## m.gushiwen.cn（2 条）

1. https://m.gushiwen.cn/guwen/bookv_42b93228a619.aspx
2. https://m.gushiwen.cn/guwen/bookv_9803.aspx

## m.news.cctv.com（1 条）

1. http://m.news.cctv.com/2016/09/11/ARTI38pC1EsfutPs6NWsGpZ6160911.shtml

## m.thepaper.cn（1 条）

1. https://m.thepaper.cn/newsDetail_forward_9180156

## m.write.qq.com（1 条）

1. https://m.write.qq.com/portal/pointsDetail?type=points&CAID=15055084305428201&reviewid=567802954137206784

## maiziebennett.com（1 条）

1. https://maiziebennett.com/character-chemistry-romance-writing/

## melbourneprintpublish.com.au（1 条）

1. https://melbourneprintpublish.com.au/blogs/how-to-write-a-short-story/

## nathanielconnors.com（1 条）

1. https://nathanielconnors.com/2026/08/unreliable-narrator-meaning/

## novelconceptspublishing.com（1 条）

1. https://novelconceptspublishing.com/how-to-write-romantic-tension-romance-writing-tips/

## novelmint.ai（1 条）

1. https://novelmint.ai/guides/how-to-write-a-mystery-novel

## novelos.studio（3 条）

1. https://novelos.studio/blog/how-to-write-scene-transitions/
2. https://novelos.studio/blog/fix-head-hopping/
3. https://novelos.studio/blog/what-character-refuses-say/

## olivespencer.com（1 条）

1. https://olivespencer.com/blog/how-to-write-romantic-tension/

## owl.purdue.edu（1 条）

1. https://owl.purdue.edu/owl/general_writing/the_writing_process/feedback/giving%20feedback_peer%20review.html

## pdfs.semanticscholar.org（1 条）

1. https://pdfs.semanticscholar.org/ebe0/045dfe969db8b042f01b1df23eea4da099c2.pdf

## qnzj.cyol.com（1 条）

1. https://qnzj.cyol.com/html/2019-08/20/nw.D110000qnzjb_20190820_2-05.htm

## recentrevelations.tumblr.com（1 条）

1. https://recentrevelations.tumblr.com/post/725832417938653184

## scriptumwriterstudio.com（2 条）

1. https://scriptumwriterstudio.com/en/blog/how-to-write-romance-novel.html
2. https://scriptumwriterstudio.com/en/blog/self-editing-your-novel.html

## selfpubhub.us.com（2 条）

1. https://selfpubhub.us.com/science-fiction-worldbuilding/
2. https://selfpubhub.us.com/emotional-beats-romance/

## selfpublishing.com（1 条）

1. https://selfpublishing.com/character-names/

## sheahulse.com（1 条）

1. https://sheahulse.com/how-to-write-slow-burn-romance-the-complete-guide-to-building-unbearable-tension/

## sobrief.com（3 条）

1. https://sobrief.com/books/dialogue
2. https://sobrief.com/books/on-writing
3. https://sobrief.com/books/scene-and-structure-2

## storyloft.app（1 条）

1. https://storyloft.app/the-13-beat-romance-beat-sheet-how-to-plot-pacing-character-arcs/

## tag.chinawriter.com.cn（1 条）

1. https://tag.chinawriter.com.cn/member/13987669336c/viewarchives_597267.html

## thelittlebookish.com（1 条）

1. https://thelittlebookish.com/blogs/news/the-unreliable-narrator

## thewritepractice.com（1 条）

1. https://thewritepractice.com/mystery-clues/

## tryathens.com（1 条）

1. https://tryathens.com/blog/bird-by-bird-summary

## web.mit.edu（1 条）

1. https://web.mit.edu/21w732/www/Handouts/workshop.htm

## westernreflectionspublishing.com（1 条）

1. https://westernreflectionspublishing.com/blogs/how-can-you-avoid-information-dumps-and-why-are-they-sometimes-not-a-good-practice/

## writemeamurder.co.uk（1 条）

1. https://writemeamurder.co.uk/red-herrings-and-misdirection-the-art-of-fair-play/

## writersdigestonline.com（2 条）

1. https://writersdigestonline.com/why-your-point-of-view-keeps-confusing-readers/
2. https://writersdigestonline.com/mastering-dialogue-techniques-the-pros-use/

## writewithharte.com（1 条）

1. https://writewithharte.com/how-to-write-tension-in-romance/

## writingcenter.gmu.edu（1 条）

1. https://writingcenter.gmu.edu/writing-resources/writing-as-process/advice-on-setting-up-and-working-with-a-writing-group

## writingnsw.org.au（1 条）

1. https://writingnsw.org.au/getsupport/information-for-writers/peer-feedback/

## writoryofficial.com（5 条）

1. https://writoryofficial.com/fiction-questions/how-do-you-transition-between-scenes
2. https://writoryofficial.com/fiction-questions/how-do-you-name-fictional-characters
3. https://writoryofficial.com/fiction-glossary/narrative-distance
4. https://writoryofficial.com/fiction-glossary/head-hopping
5. https://writoryofficial.com/short-story-examples

## www.21cnjy.com（1 条）

1. https://www.21cnjy.com/yuwen/kewen/A90/10424/543/1083/

## www.anton-chehov.info（1 条）

1. https://www.anton-chehov.info/pisma-za-1888-god-chast-8.html

## www.aplaceofintent.co.uk（1 条）

1. https://www.aplaceofintent.co.uk/blog/show-dont-tell-the-golden-rule-of-fiction-writing-examples

## www.asu.edu（1 条）

1. https://www.asu.edu/courses/fms209/total-readings/lamott-shittyfirstdrafts.pdf

## www.bubblecow.com（2 条）

1. https://www.bubblecow.com/blog/writing-craft/point-of-view/how-to-avoid-head-hopping-in-your-writing/
2. https://www.bubblecow.com/blog/writing-craft/dialogue-writing/ideas-for-crafting-better-dialogue-tags/

## www.caroclarke.com（1 条）

1. https://www.caroclarke.com/transitions.html

## www.cattediting.com（1 条）

1. https://www.cattediting.com/resourcehub/actionbeats

## www.cctv.com（1 条）

1. https://www.cctv.com/teleplay/special/C16609/20061016/101585_1.shtml

## www.chinawriter.com.cn（1 条）

1. http://www.chinawriter.com.cn/n1/2025/0102/c404063-40394235.html

## www.dl-library.net.cn（1 条）

1. https://www.dl-library.net.cn/publication/pub_content.php?id=107&flag=3

## www.editorworld.com（2 条）

1. https://www.editorworld.com/article/how-to-write-a-short-story
2. https://www.editorworld.com/article/how-to-write-a-mystery

## www.elaineflinn.com（1 条）

1. https://www.elaineflinn.com/posts/creating-believable-red-herrings/

## www.firstdraftpro.com（1 条）

1. https://www.firstdraftpro.com/blog/how-to-intercut-scenes

## www.fudan.edu.cn（1 条）

1. https://www.fudan.edu.cn/2023/0407/c24a134382/page.htm

## www.gmw.cn（1 条）

1. https://www.gmw.cn/01ds/1999-07/21/GB/ds%5E259%5E0%5EDS601.htm

## www.gutenberg.org（5 条）

1. https://www.gutenberg.org/ebooks/1342
2. https://www.gutenberg.org/ebooks/64317
3. https://www.gutenberg.org/cache/epub/37970/pg37970.txt
4. https://www.gutenberg.org/files/7256/7256-h/7256-h.htm
5. https://www.gutenberg.org/files/1342/1342-h/1342-h.htm

## www.helpingwritersbecomeauthors.com（1 条）

1. https://www.helpingwritersbecomeauthors.com/as-you-know-bob/amp/

## www.hubpd.com（1 条）

1. https://www.hubpd.com/#/detail?contentId=4611686018428531989

## www.ibiblio.org（1 条）

1. https://www.ibiblio.org/eldritch/ac/joke.htm

## www.iesdouyin.com（4 条）

1. https://www.iesdouyin.com/share/video/7586332589629197617
2. https://www.iesdouyin.com/share/video/7669381096949304618
3. https://www.iesdouyin.com/share/video/7681114557506424114
4. https://www.iesdouyin.com/share/video/7630985483157245203

## www.ihuaben.com（1 条）

1. https://www.ihuaben.com/book/9872861/61057238.html

## www.ijim.in（1 条）

1. https://www.ijim.in/files/2025/December/Vol%2010%20Issue%20VIII%2024-28%20%20Paper%205%20Dr%20Poonam.pdf

## www.jjwxc.net（1 条）

1. https://www.jjwxc.net/onebook.php?chapterid=15&novelid=10563050

## www.livewritethrive.com（1 条）

1. https://www.livewritethrive.com/2025/09/16/5-strategies-to-pacing-your-dialogue/

## www.loreteller.com（1 条）

1. https://www.loreteller.com/learn/romancing-the-beat-explained/

## www.neac.gov.cn（1 条）

1. https://www.neac.gov.cn/seac/xwzx/202609/1194294.shtml

## www.notmfa.com（1 条）

1. https://www.notmfa.com/craft/jane-austen-pioneered-free-indirect-stylemodern-genre-fiction-perfected-it

## www.oscarghostwriting.com（1 条）

1. https://www.oscarghostwriting.com/blog/how-to-write-subtext-in-dialogue/

## www.savannahgilbo.com（1 条）

1. https://www.savannahgilbo.com/blog/point-of-view-mistakes

## www.shyeditor.com（1 条）

1. https://www.shyeditor.com/blog/post/short-story-structure

## www.sleuthsayers.org（1 条）

1. https://www.sleuthsayers.org/2016/12/the-twist.html

## www.strandbooks.com（1 条）

1. https://www.strandbooks.com/stein-on-writing-a-master-editor-of-some-of-the-most-successful-writers-of-our-century-shares-his-craft-techniques-and-strategies-9780312254216.html

## www.tacczx.com（1 条）

1. http://www.tacczx.com/wap.aspx?nid=7021&p=1&cp=3&cid=109

## www.transtutor.blog（1 条）

1. https://www.transtutor.blog/master-third-person-limited-secrets

## www.tumblr.com（2 条）

1. https://www.tumblr.com/thewritinghole/173341771021/writing-arguments-between-characters
2. https://www.tumblr.com/writing-prompts-for-friends/613924827656585216/notes-from-stephen-kings-on-writing-07-the

## wyb.chinawriter.com.cn（1 条）

1. https://wyb.chinawriter.com.cn/attachment/201908/23/3c71d3df-f433-4068-9471-cbda03bb13e0.pdf

# 第二十五轮新增（2026-09-23）：第十批创作工艺资料

> 本轮为 foreshadowing-craft.md / power-craft.md / wuxia-dialogue.md / spinoff-craft.md 落库而清点。来源四份创作工艺附件：伏笔（长篇伏笔处理，155 行）、战力（战力设定防崩，151 行）、武侠对白（腔调与雷区，232 行）、番外支线（台账模板，243 行）。四份附件原始 URL 出现 63 处 → 去重后 62 条，其中 1 条为跨附件共引（m.qidian.com/ziyuan/guimizhizhu/post/yueliangtujing 伏笔与战力共引），与既有索引重叠 4 条（creader.io/tools/foreshadowing-tracker、prowritingaid.com/chekhovs-gun、reedsy.com/blog/chekhovs-gun、symban.de/en/blog/building-a-magic-system，均为既有条目不重复登记），净新增 58 条，按域名分组如下（域名为脚本归一口径：去尾斜杠+小写、保留 www 前缀；yushengbbs 组按脚本分组转录，组内第三条 URL 实际域名为 yushengbbs.com）。清点方式：脚本提取+比对，非目测。**本文件只保证"原文档里写了这个链接"，不说明链接内容说了什么、不保证现在仍可访问。**

| 域名 | 条数 |
|---|---|
| www.iesdouyin.com | 5 |
| m.baike.com | 3 |
| m.qidian.com | 3 |
| yushengbbs.net | 3 |
| book.douban.com | 2 |
| gulongbbs.com | 2 |
| immortalascension.com | 2 |
| m.gsw6.com | 2 |
| m.toutiao.com | 2 |
| www.brandonsanderson.com | 2 |
| aiwritebook.com | 1 |
| animenagi.com | 1 |
| app.blurbbio.com | 1 |
| bbs.jjwxc.net | 1 |
| bubblecow.com | 1 |
| bytecosmico.com | 1 |
| czrb.bohaitoday.com | 1 |
| inkshift.io | 1 |
| k.sina.cn | 1 |
| m.gushiwen.cn | 1 |
| m.jiemian.com | 1 |
| margmcalister.com | 1 |
| movie.douban.com | 1 |
| novelos.studio | 1 |
| obsidiantavern.com | 1 |
| reedsy.com | 1 |
| tianlong.5000yan.com | 1 |
| traciejoy.com | 1 |
| wap.jjwxc.net | 1 |
| www.editorworld.com | 1 |
| www.gulongbbs.com | 1 |
| www.loreteller.com | 1 |
| www.newton.com.tw | 1 |
| www.plotiar.com | 1 |
| www.rollingauthors.com | 1 |
| www.squibler.io | 1 |
| www.tckpublishing.com | 1 |
| www.thepaper.cn | 1 |
| www.xinhuanet.com | 1 |
| www.xxsy.net | 1 |
| www.zgwypl.com | 1 |
| zainahyousef.com | 1 |
| **合计（42 域）** | **58** |

## www.iesdouyin.com（5 条）

1. https://www.iesdouyin.com/share/video/7560669448865090855
2. https://www.iesdouyin.com/share/video/7639360377699978547
3. https://www.iesdouyin.com/share/video/7657133782561983780
4. https://www.iesdouyin.com/share/video/7669754500990679547
5. https://www.iesdouyin.com/share/video/7674658036803177747

## m.baike.com（3 条）

1. https://m.baike.com/wiki/%e5%94%87%e5%85%b8/20918570
2. https://m.baike.com/wiki/%e6%b8%a9%e7%91%9e%e5%ae%89/277863
3. https://m.baike.com/wiki/%e8%af%a1%e7%a7%9d%e4%b9%8b%e4%b8%bb%e5%ba%8f%e5%88%97%e9%80%94%e5%be%84/7547166981331583019

## m.qidian.com（3 条）

1. https://m.qidian.com/ask/qenururrhgt
2. https://m.qidian.com/ask/qwzclsktugt
3. https://m.qidian.com/ziyuan/guimizhizhu/post/yueliangtujing

## yushengbbs.net（3 条）

1. http://yushengbbs.net/bbs/thread-59461-1-1.html
2. http://yushengbbs.net/bbs/thread-65670-1-1.html
3. http://yushengbbs.com/bbs/thread-9475-1-1.html

## book.douban.com（2 条）

1. https://book.douban.com/subject/1337302/blockquotes?sort=score&start=300
2. https://book.douban.com/subject/3781979/blockquotes

## gulongbbs.com（2 条）

1. https://gulongbbs.com/book/dqjk/009.htm
2. https://gulongbbs.com/book/dqjk/012.htm

## immortalascension.com（2 条）

1. https://immortalascension.com/en/rankings/han-li-battle-evolution
2. https://immortalascension.com/en/timeline/power-level-timeline

## m.gsw6.com（2 条）

1. https://m.gsw6.com/book/tlbb/8646.html
2. https://m.gsw6.com/book/tlbb/8690.html

## m.toutiao.com（2 条）

1. http://m.toutiao.com/group/6483374254825357581
2. http://m.toutiao.com/group/6916831014388089347

## www.brandonsanderson.com（2 条）

1. https://www.brandonsanderson.com/blogs/blog/guide-to-sandersons-laws-of-magic-lecture-notes
2. https://www.brandonsanderson.com/blogs/blog/sandersons-first-law

## aiwritebook.com（1 条）

1. https://aiwritebook.com/en/blog/foreshadowing-examples

## animenagi.com（1 条）

1. https://animenagi.com/super-scaling-really-order

## app.blurbbio.com（1 条）

1. https://app.blurbbio.com/blog/foreshadowing-guide

## bbs.jjwxc.net（1 条）

1. https://bbs.jjwxc.net/showmsg.php?board=17&id=1670205

## bubblecow.com（1 条）

1. https://bubblecow.com/blog/writing-craft/story-structure/ideas-for-developing-subplots-that-matter

## bytecosmico.com（1 条）

1. https://bytecosmico.com/en/dragon-ball-z-frieza-power-scaling-broken-analysis

## czrb.bohaitoday.com（1 条）

1. http://czrb.bohaitoday.com/pad/content/202408/29/content_139048.html

## inkshift.io（1 条）

1. https://inkshift.io/resources/weaving-subplots

## k.sina.cn（1 条）

1. https://k.sina.cn/article_6086078844_16ac2317c01900jm5r.html

## m.gushiwen.cn（1 条）

1. https://m.gushiwen.cn/gushiwen_74eb44fe2d.aspx

## m.jiemian.com（1 条）

1. https://m.jiemian.com/article/3146012.html

## margmcalister.com（1 条）

1. https://margmcalister.com/wp-content/uploads/2020/10/plotting-4.pdf

## movie.douban.com（1 条）

1. https://movie.douban.com/review/10193618

## novelos.studio（1 条）

1. https://novelos.studio/blog/foreshadowing-timing

## obsidiantavern.com（1 条）

1. https://obsidiantavern.com/magic-systems

## reedsy.com（1 条）

1. https://reedsy.com/studio/templates/foreshadowing

## tianlong.5000yan.com（1 条）

1. https://tianlong.5000yan.com/42119.html

## traciejoy.com（1 条）

1. https://traciejoy.com/2025/09/29/subplots

## wap.jjwxc.net（1 条）

1. https://wap.jjwxc.net/book2/9709335/86

## www.editorworld.com（1 条）

1. https://www.editorworld.com/article/how-to-weave-subplots-into-a-novel

## www.gulongbbs.com（1 条）

1. https://www.gulongbbs.com/book/dqjk/048.htm

## www.loreteller.com（1 条）

1. https://www.loreteller.com/learn/how-to-write-subplots

## www.newton.com.tw（1 条）

1. https://www.newton.com.tw/wiki/%e8%95%ad%e5%b3%b0/4447

## www.plotiar.com（1 条）

1. https://www.plotiar.com/blog/subplot-architecture-weaving-story-threads

## www.rollingauthors.com（1 条）

1. https://www.rollingauthors.com/post/side-stories-that-steal-the-show-how-to-add-subplots-to-your-novel-without-losing-the-main-plot

## www.squibler.io（1 条）

1. https://www.squibler.io/learn/worldbuilding/magic-system

## www.tckpublishing.com（1 条）

1. https://www.tckpublishing.com/chekhovs-gun

## www.thepaper.cn（1 条）

1. https://www.thepaper.cn/newsdetail_forward_31852906

## www.xinhuanet.com（1 条）

1. https://www.xinhuanet.com/politics/2016-06/16/c_129068022.htm

## www.xxsy.net（1 条）

1. https://www.xxsy.net/baike/axdj3teuxidd

## www.zgwypl.com（1 条）

1. https://www.zgwypl.com/content/details9_26503.html

## zainahyousef.com（1 条）

1. https://zainahyousef.com/how-to-connect-subplots-to-your-main-plot-in-a-story

# 第二十六轮新增（2026-09-24）：补编七卷创作工艺资料来源

> 本轮为 poetry-craft.md / screenplay-craft.md / form-devices-craft.md / character-craft.md / narratology-craft.md / structure-craft.md / style-spectrum-craft.md 落库而清点。来源七份补编附件：《创作知识库补编 R-A 诗歌韵律体系》《创作知识库补编 R-B 剧本影视剧本》《创作知识库补编 R-C 文体补缺》《创作知识库补编 R-D 人物补深》《创作知识库补编 R-E 叙事学补遗》《创作知识库补编 R-F 结构收束》《创作知识库补编 R-G 文风与修订》（docx 提取文本）。脚本口径：七卷命中 URL 324 处（R-A 77 / R-B 54 / R-C 50 / R-D 45 / R-E 44 / R-F 42 / R-G 12，含卷内重复），去重后 213 条；其中 2 条与既有索引重叠（http://www.wxg.org.cn/gkwz/4017.jhtml，R-A；https://sobrief.com/books/dialogue，R-B），均为既有条目不重复登记，净新增 211 条，按域名分组如下，每条标注所属补编卷。个别条目为提取残段（andrewlansdown.com 第二条 URL 后接「；Literary」正文残段、a.osmarks.net 条目缺右括号、english.fju.edu.tw 与 s.zhangyue.com 条目含 &amp; 实体），按脚本输出原样转录。清点方式：脚本提取+比对，非目测。**本文件只保证"原文档里写了这个链接"，不说明链接内容说了什么、不保证现在仍可访问。**

| 域名 | 条数 |
|---|---|
| fiveable.me | 6 |
| www.chinawriter.com.cn | 5 |
| www.iesdouyin.com | 4 |
| www.litcharts.com | 4 |
| literarydevices.net | 3 |
| study.com | 3 |
| writoryofficial.com | 3 |
| www.zhscwx.com | 3 |
| andrewlansdown.com | 2 |
| artandpopularculture.com | 2 |
| assets.litcharts.com | 2 |
| blog.reedsy.com | 2 |
| book.douban.com | 2 |
| campuspress.yale.edu | 2 |
| dailyscript.com | 2 |
| ensemblewriter.com | 2 |
| laper.ai | 2 |
| m.zxxk.com | 2 |
| owiki.org | 2 |
| sagascope.com | 2 |
| scriptease.app | 2 |
| scriptreader.ai | 2 |
| seikan.app | 2 |
| whatwewriting.com | 2 |
| www.bubblecow.com | 2 |
| www.iwrity.com | 2 |
| www.screenweaver.ai | 2 |
| www.study.com | 2 |
| www.studyguides.com | 2 |
| 100-years-of-solitude.book-edu.com | 1 |
| a.osmarks.net | 1 |
| aap.tandfonline.com | 1 |
| academiaresearcher.com | 1 |
| archive.bookstr.com | 1 |
| bbtpress.com | 1 |
| beautifulbooks.info | 1 |
| blog.celtx.com | 1 |
| bookishbay.com | 1 |
| canongate.co.uk | 1 |
| compbile.com | 1 |
| contentandchaos.com | 1 |
| coursescholars.com | 1 |
| creativitys.uk | 1 |
| cronistas.org | 1 |
| dramaqueen.info | 1 |
| edu.cfa.org.cn | 1 |
| edwardpackard.com | 1 |
| english.fju.edu.tw | 1 |
| epicscribe.io | 1 |
| eslbuzz.com | 1 |
| ewenyan.com | 1 |
| faculty.winthrop.edu | 1 |
| famous-trials.com | 1 |
| filmlocal.com | 1 |
| gj.zdic.net | 1 |
| handwiki.org | 1 |
| hearth.sh | 1 |
| human.libretexts.org | 1 |
| imaginarytalks.com | 1 |
| inkshift.io | 1 |
| jingbianrenda.gov.cn | 1 |
| kids.kiddle.co | 1 |
| kindlepreneur.com | 1 |
| liberalarts.oregonstate.edu | 1 |
| lindadresner.com | 1 |
| literariness.org | 1 |
| literature.cass.cn | 1 |
| litgram.in | 1 |
| lithub.com | 1 |
| londonscreenwritersfestival.com | 1 |
| lwr.tsinghua.edu.cn | 1 |
| m.book118.com | 1 |
| m.gushiwen.cn | 1 |
| melcher.com | 1 |
| mip.21cnjy.com | 1 |
| news.qq.com | 1 |
| newsletter.thewritingking.com | 1 |
| nextchapters.com | 1 |
| nofilmschool.com | 1 |
| paulgorman.org | 1 |
| personal.unizar.es | 1 |
| plotiar.com | 1 |
| qnzj.cyol.com | 1 |
| reedsy.com | 1 |
| research.annefrank.org | 1 |
| rivereditor.com | 1 |
| s.zhangyue.com | 1 |
| savethecat.com | 1 |
| screenplayhowto.com | 1 |
| scriptserious.com | 1 |
| selfpubhub.us.com | 1 |
| simplyscripts.com | 1 |
| sou-yun.cn | 1 |
| spellapp.com | 1 |
| storytellingdb.com | 1 |
| strangehorizons.com | 1 |
| test.sobrief.com | 1 |
| thealchemyofscreenacting.com | 1 |
| theliteraryscholar.com | 1 |
| thelittlebookish.com | 1 |
| thewritingking.com | 1 |
| ur1light.com | 1 |
| vulms.vu.edu.pk | 1 |
| warriorcats.com | 1 |
| webster.com | 1 |
| westernreflectionspublishing.com | 1 |
| wiki.bildungsserver.de | 1 |
| wp.unil.ch | 1 |
| writersdailypractice.com | 1 |
| www.12371.gov.cn | 1 |
| www.163.com | 1 |
| www.aliventures.com | 1 |
| www.amirulkhan.in | 1 |
| www.annefrank.org | 1 |
| www.artandpopularculture.com | 1 |
| www.befreed.ai | 1 |
| www.bilibili.com | 1 |
| www.britishlibrary.cn | 1 |
| www.chinafilm.gov.cn | 1 |
| www.cntszl.com | 1 |
| www.csb.gov.hk | 1 |
| www.cyoa.com | 1 |
| www.degruyterbrill.com | 1 |
| www.dictionary.com | 1 |
| www.dpm.org.cn | 1 |
| www.edelmanedits.com | 1 |
| www.espacefrancais.com | 1 |
| www.filfre.net | 1 |
| www.flyingwrestler.com | 1 |
| www.gaokzx.com | 1 |
| www.gmw.cn | 1 |
| www.gushiwen.cn | 1 |
| www.joyceproject.com | 1 |
| www.larapedia.com | 1 |
| www.loreteller.com | 1 |
| www.maturando.it | 1 |
| www.novel-software.com | 1 |
| www.novlr.org | 1 |
| www.pep.com.cn | 1 |
| www.poetry.com | 1 |
| www.renjiaoshe.com | 1 |
| www.sarahfraps.com | 1 |
| www.scripts.com | 1 |
| www.sdscxh.com | 1 |
| www.shicihui.com | 1 |
| www.shicijiayuan.com | 1 |
| www.shortform.com | 1 |
| www.socreate.it | 1 |
| www.squibler.io | 1 |
| www.stage32.com | 1 |
| www.storyflint.com | 1 |
| www.storysense.com | 1 |
| www.supersummary.com | 1 |
| www.sxlib.org.cn | 1 |
| www.tameri.com | 1 |
| www.the-criterion.com | 1 |
| www.thegodfathertrilogy.com | 1 |
| www.ugenglish.in | 1 |
| www.uv.es | 1 |
| www.whatascript.com | 1 |
| www.writerswrite.co.za | 1 |
| www.writingclasses.com | 1 |
| www.yinruiwen.net | 1 |
| www.zgshige.cn | 1 |
| www.zhscxh.com | 1 |
| www.ziyexing.com | 1 |
| wyb.chinawriter.com.cn | 1 |
| **合计（167 域）** | **211** |

## fiveable.me（6 条）

1. https://fiveable.me/key-terms/screenwriting-i/one-page-equals-one-minute  （R-B）
2. https://fiveable.me/british-literature-i/key-terms/epistolary-novel  （R-C）
3. https://fiveable.me/introduction-contemporary-literature/unit-1/fragmentation-nonlinear-narratives/study-guide/CnqQKriAHh6YEfca  （R-C）
4. https://fiveable.me/the-english-novel/unit-1/samuel-richardson-epistolary/study-guide/ZApG9Cd7K1lrIeII  （R-C）
5. https://fiveable.me/introduction-contemporary-literature/unit-1/metafiction-self-reflexivity/study-guide/s1ZRmp819PNqZO0U  （R-E）
6. https://fiveable.me/british-literature-ii/unit-12/joyces-ulysses-structure-style-significance/study-guide/ukj8k8MZhzgYZHUW  （R-E）

## www.chinawriter.com.cn（5 条）

1. http://www.chinawriter.com.cn/n1/2019/0110/c404063-30513556.html  （R-A）
2. https://www.chinawriter.com.cn/2013/2013-10-18/178036.html  （R-A）
3. http://www.chinawriter.com.cn/n1/2016/1014/c405172-28777440.html  （R-C）
4. http://www.chinawriter.com.cn/n1/2018/0530/c404067-30023587.html  （R-C）
5. https://www.chinawriter.com.cn/n1/2018/1221/c404030-30480615.html  （R-C）

## www.iesdouyin.com（4 条）

1. https://www.iesdouyin.com/share/video/7622638815735287082  （R-B）
2. https://www.iesdouyin.com/share/video/7624429890674248996  （R-B）
3. https://www.iesdouyin.com/share/video/7646744829279423784  （R-B）
4. https://www.iesdouyin.com/share/video/7663056860269907209  （R-B）

## www.litcharts.com（4 条）

1. https://www.litcharts.com/literary-devices-and-terms/villanelle  （R-A）
2. https://www.litcharts.com/literary-devices-and-terms/round-character  （R-E）
3. https://www.litcharts.com/lit/the-lady-with-the-dog/themes/society-and-morality  （R-F）
4. https://www.litcharts.com/lit/the-lady-with-the-dog/themes/truth-in-deception  （R-F）

## literarydevices.net（3 条）

1. https://literarydevices.net/this-is-just-to-say/  （R-A）
2. https://literarydevices.net/frame-story/  （R-E）
3. https://literarydevices.net/master-in-medias-res-start-stories-right-at-the-action/  （R-F）

## study.com（3 条）

1. https://study.com/learn/lesson/samuel-richardson-biography-works-epistolary-pamela.html  （R-C）
2. https://study.com/academy/lesson/one-hundred-years-of-solitude-quotes-opening-line-ending.html  （R-E）
3. https://study.com/learn/lesson/frame-narrative-overview.html  （R-E）

## writoryofficial.com（3 条）

1. https://writoryofficial.com/fiction-questions/how-do-you-give-each-character-a-distinct-voice  （R-D）
2. https://writoryofficial.com/classic-stories/the-lady-with-the-dog  （R-F）
3. https://writoryofficial.com/fiction-questions/how-long-should-a-chapter-be  （R-F）

## www.zhscwx.com（3 条）

1. http://www.zhscwx.com/diangu/67018.html  （R-A）
2. http://www.zhscwx.com/gelv/  （R-A）
3. http://www.zhscwx.com/gelv/85.html  （R-A）

## andrewlansdown.com（2 条）

1. https://andrewlansdown.com/other-poets-poems/william-carlos-williams/  （R-A）
2. https://andrewlansdown.com/other-poets-poems/william-carlos-williams/；Literary  （R-A）

## artandpopularculture.com（2 条）

1. https://artandpopularculture.com/Second-person_narrative  （R-C）
2. https://artandpopularculture.com/Frame_narrative  （R-E）

## assets.litcharts.com（2 条）

1. https://assets.litcharts.com/literary-devices-and-terms/sonnet  （R-A）
2. https://assets.litcharts.com/lit/one-hundred-years-of-solitude/themes/the-circularity-of-time  （R-E）

## blog.reedsy.com（2 条）

1. https://blog.reedsy.com/guide/story-structure/save-the-cat-beat-sheet/  （R-B）
2. https://blog.reedsy.com/round-character/  （R-E）

## book.douban.com（2 条）

1. https://book.douban.com/review/8977688/  （R-A）
2. https://book.douban.com/tag/  （R-A）

## campuspress.yale.edu（2 条）

1. https://campuspress.yale.edu/modernismlab/in-a-station-of-the-metro/  （R-A）
2. https://campuspress.yale.edu/modernismlab/nausicaa/  （R-E）

## dailyscript.com（2 条）

1. https://dailyscript.com/scripts/The_Godfather.html  （R-B）
2. https://dailyscript.com/scripts/Unprocessed/The%20Shawshank%20Redemption/The%20Shawshank%20Redemption.pdf  （R-B）

## ensemblewriter.com（2 条）

1. https://ensemblewriter.com/docs/screenplay-format  （R-B）
2. https://ensemblewriter.com/docs/screenplay-format-template  （R-B）

## laper.ai（2 条）

1. https://laper.ai/blog/save-the-cat-beat-sheet/  （R-B）
2. https://laper.ai/blog/screenplay-format-guide/  （R-B）

## m.zxxk.com（2 条）

1. https://m.zxxk.com/soft/51221883.html  （R-A）
2. https://m.zxxk.com/soft/58754774.html  （R-B）

## owiki.org（2 条）

1. https://owiki.org/wiki/Defamiliarization  （R-E）
2. https://owiki.org/wiki/Russian_formalism  （R-E）

## sagascope.com（2 条）

1. https://sagascope.com/en/blog/first-page-novel-hook-readers  （R-F）
2. https://sagascope.com/en/glossary/pacing  （R-F）

## scriptease.app（2 条）

1. https://scriptease.app/blog/blake-snyder-beat-sheet/  （R-B）
2. https://scriptease.app/blog/screenplay-margins-and-page-counts/  （R-B）

## scriptreader.ai（2 条）

1. https://scriptreader.ai/guides/sequence-approach-gulino  （R-B）
2. https://scriptreader.ai/guides/creating-character-arcs-weiland  （R-D）

## seikan.app（2 条）

1. https://seikan.app/blog/how-to-format-a-screenplay  （R-B）
2. https://seikan.app/blog/write-screenplay-ready-for-production  （R-B）

## whatwewriting.com（2 条）

1. https://whatwewriting.com/narrative-pacing-in-writing/  （R-F）
2. https://whatwewriting.com/opening-line-types/  （R-F）

## www.bubblecow.com（2 条）

1. https://www.bubblecow.com/blog/writing-craft/character-development/writing-character-backstory-without-info-dumps/  （R-D）
2. https://www.bubblecow.com/blog/writing-craft/dialogue-writing/how-to-write-natural-sounding-dialogue/  （R-D）

## www.iwrity.com（2 条）

1. https://www.iwrity.com/writing-backstory-integration-guide  （R-D）
2. https://www.iwrity.com/writing-chapter-structure-guide  （R-F）

## www.screenweaver.ai（2 条）

1. https://www.screenweaver.ai/blog/sequence-method-matrix-case-study  （R-B）
2. https://www.screenweaver.ai/blog/write-character-death-scene-without-melodrama  （R-D）

## www.study.com（2 条）

1. https://www.study.com/learn/lesson/in-a-station-of-the-metro-poem-analysis-literary-devices.html  （R-A）
2. https://www.study.com/academy/lesson/metafiction-definition-examples.html  （R-E）

## www.studyguides.com（2 条）

1. https://www.studyguides.com/study-methods/study-guide/cmowow2bis6nh01nefctsb6vx  （R-E）
2. https://www.studyguides.com/study-methods/study-guide/clza2ql4lbxrj47xc07ivh58v  （R-G）

## 100-years-of-solitude.book-edu.com（1 条）

1. https://100-years-of-solitude.book-edu.com/character-analysis-colonel-aureliano-buendia/  （R-E）

## a.osmarks.net（1 条）

1. https://a.osmarks.net/content/wikipedia_en_all_maxi_2020-08/A/Epiphany_(literature  （R-F）

## aap.tandfonline.com（1 条）

1. https://aap.tandfonline.com/doi/full/10.1080/14767430.2026.2624979  （R-C）

## academiaresearcher.com（1 条）

1. https://academiaresearcher.com/how-does-ernest-hemingways-minimalist-style-in-hills-like-white-elephants-compare-with-william-faulkners-verbose-and-complex-narrative-style-and-what-do-these-stylistic-contrasts-reveal-about-the/  （R-G）

## archive.bookstr.com（1 条）

1. https://archive.bookstr.com/article/author-fight-club-william-faulkner-vs-ernest-heminway/  （R-G）

## bbtpress.com（1 条）

1. http://bbtpress.com/bookview/10365.html  （R-B）

## beautifulbooks.info（1 条）

1. https://beautifulbooks.info/metalepsis/  （R-C）

## blog.celtx.com（1 条）

1. https://blog.celtx.com/what-is-a-round-character/  （R-E）

## bookishbay.com（1 条）

1. https://bookishbay.com/frame-narrative/  （R-E）

## canongate.co.uk（1 条）

1. https://canongate.co.uk/books/1748-s/  （R-C）

## compbile.com（1 条）

1. https://compbile.com/diary-of-a-madman/  （R-C）

## contentandchaos.com（1 条）

1. https://contentandchaos.com/giving-characters-distinct-speech-patterns-without-caricature/  （R-D）

## coursescholars.com（1 条）

1. https://coursescholars.com/the-characteristics-of-hemingways-works/  （R-G）

## creativitys.uk（1 条）

1. https://creativitys.uk/timeless-debate-faulkner-vs-hemingway-the-battle-for-american-literary-supremacy/  （R-G）

## cronistas.org（1 条）

1. https://cronistas.org/how-does-shelley-most-clearly-create-suspense-in-the-story  （R-F）

## dramaqueen.info（1 条）

1. https://dramaqueen.info/wiki/structure-styles/  （R-B）

## edu.cfa.org.cn（1 条）

1. https://edu.cfa.org.cn/archives/untitled-1773198322195  （R-B）

## edwardpackard.com（1 条）

1. https://edwardpackard.com/cyoa/  （R-C）

## english.fju.edu.tw（1 条）

1. http://english.fju.edu.tw/lctd/List/authorWork_Guide.asp?A_ID=13&amp;W_ID=432  （R-A）

## epicscribe.io（1 条）

1. https://epicscribe.io/blog/character-voice-fiction-writing  （R-D）

## eslbuzz.com（1 条）

1. https://eslbuzz.com/frame-story-literary-device/  （R-E）

## ewenyan.com（1 条）

1. http://ewenyan.com/articles/rjch/7.html  （R-A）

## faculty.winthrop.edu（1 条）

1. https://faculty.winthrop.edu/kosterj/ENGL201/rhyme_schemes.htm  （R-A）

## famous-trials.com（1 条）

1. https://famous-trials.com/ulysses/2658-notes-on-james-joyce-s-ulysses  （R-E）

## filmlocal.com（1 条）

1. https://filmlocal.com/filmmaking/subtext-in-screenwriting/  （R-B）

## gj.zdic.net（1 条）

1. https://gj.zdic.net/jibu/1041/32375.html  （R-A）

## handwiki.org（1 条）

1. https://handwiki.org/wiki/Social:Epistolary_novel  （R-C）

## hearth.sh（1 条）

1. https://hearth.sh/guides/epistolary-novel  （R-C）

## human.libretexts.org（1 条）

1. https://human.libretexts.org/Bookshelves/Literature_and_Literacy/British_and_Irish_Literature/English_Literature_I_(Lumen  （R-A）

## imaginarytalks.com（1 条）

1. https://imaginarytalks.com/the-lady-with-the-dog-explained/  （R-F）

## inkshift.io（1 条）

1. https://inkshift.io/resources/weaving-backstory  （R-D）

## jingbianrenda.gov.cn（1 条）

1. http://jingbianrenda.gov.cn/xxsd/gx/1392038001296125954.html  （R-A）

## kids.kiddle.co（1 条）

1. https://kids.kiddle.co/The_Diary_of_a_Young_Girl  （R-C）

## kindlepreneur.com（1 条）

1. https://kindlepreneur.com/write-a-character-arc/  （R-D）

## liberalarts.oregonstate.edu（1 条）

1. https://liberalarts.oregonstate.edu/wlf/what-epistolary-novel  （R-C）

## lindadresner.com（1 条）

1. https://lindadresner.com/the-climax-is-the-point-of-in-a-story  （R-F）

## literariness.org（1 条）

1. https://literariness.org/2023/06/14/analysis-of-italo-calvinos-if-on-a-winters-night-a-traveler/  （R-E）

## literature.cass.cn（1 条）

1. http://literature.cass.cn/ztzl/xsyjzt/xszm/202504/t20250423_5870495.shtml  （R-A）

## litgram.in（1 条）

1. https://litgram.in/formalism-and-new-criticism-ugc-net-2024/  （R-E）

## lithub.com（1 条）

1. https://lithub.com/chekhov-a-writer-for-grown-ups/  （R-F）

## londonscreenwritersfestival.com（1 条）

1. https://londonscreenwritersfestival.com/robert-mckee-on-writing-dialogue/  （R-B）

## lwr.tsinghua.edu.cn（1 条）

1. https://lwr.tsinghua.edu.cn/info/wxllyj/1395  （R-A）

## m.book118.com（1 条）

1. https://m.book118.com/try_down/135232104214012131.pdf  （R-B）

## m.gushiwen.cn（1 条）

1. https://m.gushiwen.cn/shiwenv_bdccf9ff6ec3.aspx  （R-A）

## melcher.com（1 条）

1. https://melcher.com/book/s/  （R-C）

## mip.21cnjy.com（1 条）

1. https://mip.21cnjy.com/P/22642048.html  （R-B）

## news.qq.com（1 条）

1. http://news.qq.com/rain/a/20210604A05P1V00  （R-A）

## newsletter.thewritingking.com（1 条）

1. https://newsletter.thewritingking.com/p/your-characters-all-sound-like-you  （R-D）

## nextchapters.com（1 条）

1. https://nextchapters.com/creative-writing/killing-a-character-crafting-impactful-deaths-in-fiction/  （R-D）

## nofilmschool.com（1 条）

1. https://nofilmschool.com/i-believe-in-america-godfather  （R-B）

## paulgorman.org（1 条）

1. https://paulgorman.org/writing/dramatic_structure.html  （R-B）

## personal.unizar.es（1 条）

1. https://personal.unizar.es/garciala/publicaciones/narrativetheory/2.Fabula.Tomashevsky.htm  （R-E）

## plotiar.com（1 条）

1. https://plotiar.com/ko/blog/character-arcs-beyond-checklists/  （R-D）

## qnzj.cyol.com（1 条）

1. https://qnzj.cyol.com/html/2021-11/23/nw.D110000qnzjb_20211123_3-01.htm  （R-A）

## reedsy.com（1 条）

1. https://reedsy.com/blog/character-arc/  （R-D）

## research.annefrank.org（1 条）

1. https://research.annefrank.org/en/onderwerpen/58b5fe11-0b39-46e0-809e-1e1a5eccb1e7/  （R-C）

## rivereditor.com（1 条）

1. https://rivereditor.com/guides/how-to-write-backstory-doesnt-stop-forward-momentum-2026  （R-D）

## s.zhangyue.com（1 条）

1. https://s.zhangyue.com/read?anchorId=AUTO_ID_17&amp;appId=a3670775&amp;bid=12425195&amp;cid=25&amp;rentId=107252  （R-A）

## savethecat.com（1 条）

1. https://savethecat.com/get-started/page/10  （R-B）

## screenplayhowto.com（1 条）

1. https://screenplayhowto.com/wp-content/uploads/2011/09/The-Shawshank-Redemption-Screenplay-Analysis.pdf  （R-B）

## scriptserious.com（1 条）

1. https://scriptserious.com/wp-content/uploads/2025/10/Screenplay-Format-Guide.pdf  （R-B）

## selfpubhub.us.com（1 条）

1. https://selfpubhub.us.com/ways-to-start-a-chapter/  （R-F）

## simplyscripts.com（1 条）

1. https://simplyscripts.com/WR_format.html  （R-B）

## sou-yun.cn（1 条）

1. https://sou-yun.cn/allusionsindex.aspx?people=307  （R-A）

## spellapp.com（1 条）

1. https://spellapp.com/resources/how-to-write-a-climax  （R-F）

## storytellingdb.com（1 条）

1. https://storytellingdb.com/in-medias-res/  （R-F）

## strangehorizons.com（1 条）

1. https://strangehorizons.com/wordpress/non-fiction/reviews/s-by-j-j-abrams-and-doug-dorst/  （R-C）

## test.sobrief.com（1 条）

1. https://test.sobrief.com/books/creating-character-arcs  （R-D）

## thealchemyofscreenacting.com（1 条）

1. https://thealchemyofscreenacting.com/resources/story-structure-narrative  （R-B）

## theliteraryscholar.com（1 条）

1. https://theliteraryscholar.com/picture-of-dorian-gray-modern-roast/  （R-C）

## thelittlebookish.com（1 条）

1. https://thelittlebookish.com/blogs/news/freytags-pyramid  （R-F）

## thewritingking.com（1 条）

1. https://thewritingking.com/good-death/  （R-D）

## ur1light.com（1 条）

1. https://ur1light.com/what-was-hemingways-advice/  （R-G）

## vulms.vu.edu.pk（1 条）

1. https://vulms.vu.edu.pk/Courses/MCD502/Downloads/Topic%2082.pdf  （R-B）

## warriorcats.com（1 条）

1. https://warriorcats.com/content/article/a-good-death-in-writing  （R-D）

## webster.com（1 条）

1. https://webster.com/grammar/thirteen-ways-of-looking-at-a-poem  （R-A）

## westernreflectionspublishing.com（1 条）

1. https://westernreflectionspublishing.com/blogs/how-many-words-are-usually-in-a-chapter-writing-structure-guide/  （R-F）

## wiki.bildungsserver.de（1 条）

1. https://wiki.bildungsserver.de/weltliteratur/index.php/Das_Bildnis_des_Dorian_Gray  （R-C）

## wp.unil.ch（1 条）

1. https://wp.unil.ch/narratologie/2025/04/narrations-a-la-deuxieme-et-a-la-cinquieme-personnes/  （R-C）

## writersdailypractice.com（1 条）

1. https://writersdailypractice.com/first-line-library/  （R-F）

## www.12371.gov.cn（1 条）

1. https://www.12371.gov.cn/h5/article/1438363033596198912/h5/content_1438363033596198912.html  （R-A）

## www.163.com（1 条）

1. https://www.163.com/dy/article/GB9JEPPH0521W52C.html  （R-A）

## www.aliventures.com（1 条）

1. https://www.aliventures.com/ways-to-start-novel/  （R-F）

## www.amirulkhan.in（1 条）

1. https://www.amirulkhan.in/english/russian-formalism  （R-E）

## www.annefrank.org（1 条）

1. https://www.annefrank.org/en/anne-frank/diary/complete-works-anne-frank/  （R-C）

## www.artandpopularculture.com（1 条）

1. https://www.artandpopularculture.com/Diary_of_a_Madman_%28Lu_Xun%29  （R-C）

## www.befreed.ai（1 条）

1. https://www.befreed.ai/book/don-quixote-by-miguel-de-cervantes  （R-E）

## www.bilibili.com（1 条）

1. https://www.bilibili.com/video/BV1i5zsBtETv/  （R-B）

## www.britishlibrary.cn（1 条）

1. https://www.britishlibrary.cn/en/works/picture-of-dorian-gray/  （R-C）

## www.chinafilm.gov.cn（1 条）

1. https://www.chinafilm.gov.cn/xxgk/gztz/202104/t20210425_1438.html  （R-B）

## www.cntszl.com（1 条）

1. http://www.cntszl.com/print.aspx?id=2827  （R-A）

## www.csb.gov.hk（1 条）

1. https://www.csb.gov.hk/hkgcsb/ol/news/no85/html/sc/p3.html  （R-A）

## www.cyoa.com（1 条）

1. https://www.cyoa.com/our-history/  （R-C）

## www.degruyterbrill.com（1 条）

1. https://www.degruyterbrill.com/document/doi/10.1515/9783110584813-002/pdf  （R-C）

## www.dictionary.com（1 条）

1. https://www.dictionary.com/browse/villanelle  （R-A）

## www.dpm.org.cn（1 条）

1. https://www.dpm.org.cn/Uploads/File/2021/02/07/u601fccd0c54c1.pdf  （R-A）

## www.edelmanedits.com（1 条）

1. https://www.edelmanedits.com/post/how-to-write-death-scenes  （R-D）

## www.espacefrancais.com（1 条）

1. https://www.espacefrancais.com/michel-butor/  （R-C）

## www.filfre.net（1 条）

1. https://www.filfre.net/2025/09/choose-your-own-adventure/  （R-C）

## www.flyingwrestler.com（1 条）

1. https://www.flyingwrestler.com/save-the-cat-beat-sheet/  （R-B）

## www.gaokzx.com（1 条）

1. https://www.gaokzx.com/c/202211/66167.html  （R-A）

## www.gmw.cn（1 条）

1. https://www.gmw.cn/01gmrb/2000-09/07/GB/09%5E18536%5E0%5EGMB3-011.htm  （R-A）

## www.gushiwen.cn（1 条）

1. https://www.gushiwen.cn/mingjus/default.aspx?tstr=  （R-A）

## www.joyceproject.com（1 条）

1. https://www.joyceproject.com/notes/Wk-bJZUBeQi-aLQfd7Cb  （R-F）

## www.larapedia.com（1 条）

1. https://www.larapedia.com/Summaries/The_fundamentals_of_poetry.html  （R-A）

## www.loreteller.com（1 条）

1. https://www.loreteller.com/learn/fix-character-voice/  （R-D）

## www.maturando.it（1 条）

1. https://www.maturando.it/blog/the-american-novel-lost-generation-riassunto-maturita/  （R-G）

## www.novel-software.com（1 条）

1. https://www.novel-software.com/what-is-a-round-character/  （R-E）

## www.novlr.org（1 条）

1. https://www.novlr.org/the-reading-room/how-do-i-write-a-character-backstory  （R-D）

## www.pep.com.cn（1 条）

1. https://www.pep.com.cn/xw/zt/hd/mjsmz/202009/t20200907_1958422.html  （R-A）

## www.poetry.com（1 条）

1. https://www.poetry.com/poetry-forms.php  （R-A）

## www.renjiaoshe.com（1 条）

1. https://www.renjiaoshe.com/sujiaogaozhongyuwen/xuanxiu/482765.html  （R-B）

## www.sarahfraps.com（1 条）

1. https://www.sarahfraps.com/post/incorporating-character-backstory-in-fiction  （R-D）

## www.scripts.com（1 条）

1. https://www.scripts.com/script/shawshank_redemption_29/2  （R-B）

## www.sdscxh.com（1 条）

1. https://www.sdscxh.com/hyxz_info?id=5754  （R-A）

## www.shicihui.com（1 条）

1. https://www.shicihui.com/zh-tw/book/shicigelv/131492  （R-A）

## www.shicijiayuan.com（1 条）

1. https://www.shicijiayuan.com/books/  （R-A）

## www.shortform.com（1 条）

1. https://www.shortform.com/pdf/creating-character-arcs-pdf-k-m-weiland  （R-D）

## www.socreate.it（1 条）

1. https://www.socreate.it/en/blogs/screenwriting/why-we-use-courier-for-traditional-screenwriting-font  （R-B）

## www.squibler.io（1 条）

1. https://www.squibler.io/learn/writing/book-writing/character-arc/  （R-D）

## www.stage32.com（1 条）

1. https://www.stage32.com/lounge/screenwriting/Lets-Talk-1-Page-equals-1-Minute  （R-B）

## www.storyflint.com（1 条）

1. https://www.storyflint.com/blog/climax  （R-F）

## www.storysense.com（1 条）

1. https://www.storysense.com/mobile/SPFormat.pdf  （R-B）

## www.supersummary.com（1 条）

1. https://www.supersummary.com/frame-story/  （R-E）

## www.sxlib.org.cn（1 条）

1. https://www.sxlib.org.cn/dfzy/sxfjwhzybk/sxhcfjzplswh/lsdg/201701/t20170122_614193.html  （R-A）

## www.tameri.com（1 条）

1. https://www.tameri.com/format/screenplays/  （R-B）

## www.the-criterion.com（1 条）

1. https://www.the-criterion.com/V8/n8/IT01.pdf  （R-E）

## www.thegodfathertrilogy.com（1 条）

1. http://www.thegodfathertrilogy.com/gf1/transcript/gf1transcript.html  （R-B）

## www.ugenglish.in（1 条）

1. https://www.ugenglish.in/2021/04/literary-forms.html  （R-A）

## www.uv.es（1 条）

1. https://www.uv.es/~tronch/stu/Prosody.html  （R-A）

## www.whatascript.com（1 条）

1. https://www.whatascript.com/movie-dialogue-09.html  （R-B）

## www.writerswrite.co.za（1 条）

1. https://www.writerswrite.co.za/what-is-metafiction-how-do-i-write-it/  （R-E）

## www.writingclasses.com（1 条）

1. https://www.writingclasses.com/toolbox/ask-writer/whats-the-difference-between-a-round-and-flat-character  （R-E）

## www.yinruiwen.net（1 条）

1. http://www.yinruiwen.net/news/24954.htm  （R-A）

## www.zgshige.cn（1 条）

1. https://www.zgshige.cn/c/2024-03-05/26035061.shtml  （R-A）

## www.zhscxh.com（1 条）

1. https://www.zhscxh.com/view/common/articledetail.aspx?id=276308FF3F71B803  （R-A）

## www.ziyexing.com（1 条）

1. http://www.ziyexing.com/files-2/wangli/shicigelv_08.htm  （R-A）

## wyb.chinawriter.com.cn（1 条）

1. https://wyb.chinawriter.com.cn/content/201907/05/content50373.html  （R-A）

# 第二十八轮新增（2026-09-24）：补编二（S1~S4）创作工艺资料来源

> 本轮为 spatial-narrative-craft.md / terminology-index.md 新建与 description-craft.md / timeline-craft.md / character-craft.md / viewpoint-craft.md / structure-craft.md / form-devices-craft.md / style-spectrum-craft.md 增补而清点。来源四份补编二附件：《S1 技法四补（Scene-Sequel/情感台阶/越轴/声画对位）》《S2 中文文论六补（八类描写/情景交融/工笔/繁简/卒章显志/入话）》《S3 空间叙事》《S4 术语别名索引》（md 源 + docx 同源提取文本）。脚本口径：四卷命中 URL 去重后 97 条（素材自报 98 条中，中央研究院文哲所 PDF 为 S2/S4 跨卷共引计 1 条），与既有索引全量比对**零重叠**，净新增 97 条，按域名分组如下，每条标注所属补编卷。清点方式：脚本提取+比对（协议/大小写/尾斜杠规范化后比对），非目测。**本文件只保证"原文档里写了这个链接"，不说明链接内容说了什么、不保证现在仍可访问。**

| 域名 | 条数 | 域名 | 条数 |
|---|---|---|---|
| www.chinawriter.com.cn | 4 | sal.tongji.edu.cn | 1 |
| gj.zdic.net | 3 | scispace.com | 1 |
| m.baike.com | 3 | sharonwray.com | 1 |
| culture.people.com.cn | 2 | shc.stanford.edu | 1 |
| m.thepaper.cn | 2 | stateofformation.org | 1 |
| rkyfz.pku.edu.cn | 2 | studyguides.com | 1 |
| www.gushiwen.cn | 2 | tidenews.com.cn | 1 |
| www.studyguides.com | 2 | tsg.hnzj.edu.cn | 1 |
| yuwen.chazidian.com | 2 | web.mit.edu | 1 |
| academic.oup.com | 1 | wenxindiaolong.5000yan.com | 1 |
| archiu.com | 1 | writoryofficial.com | 1 |
| article.xuexi.cn | 1 | www.adobe.com | 1 |
| book.douban.com | 1 | www.audible.com | 1 |
| campuspress.yale.edu | 1 | www.codartium.com | 1 |
| dangshi.people.com.cn | 1 | www.cuc.edu.cn | 1 |
| digitalcommons.cwu.edu | 1 | www.degruyterbrill.com | 1 |
| en.wikipedia.org | 1 | www.dfll.tsinghua.edu.cn | 1 |
| epaper.gmw.cn | 1 | www.estudoprevio.net | 1 |
| epaper.pdsxww.com | 1 | www.filmsite.org | 1 |
| escriturasinpiedad.com | 1 | www.fizzread.ai | 1 |
| essentiels.bnf.fr | 1 | www.helpingwritersbecomeauthors.com | 1 |
| faulkner.iath.virginia.edu | 1 | www.hxyww.cn | 1 |
| gastonbachelard.org | 1 | www.iwenyan.com | 1 |
| ggw.hunau.edu.cn | 1 | www.iwrity.com | 1 |
| harvardindependent.com | 1 | www.jyeoo.com | 1 |
| howtofilmschool.com | 1 | www.litphil.sinica.edu.tw | 1 |
| ilas.cssn.cn | 1 | www.parker.mov | 1 |
| introduction-to-film.com | 1 | www.qinfeng.gov.cn | 1 |
| jasna.org | 1 | www.renrendoc.com | 1 |
| jlynchblog.com | 1 | www.rmlt.com.cn | 1 |
| literarydevices.net | 1 | www.slashfilm.com | 1 |
| literarystudiesonline.com | 1 | www.sumreads.com | 1 |
| m.allhistory.com | 1 | www.supersummary.com | 1 |
| m.gushiwen.cn | 1 | www.unistrapg.it | 1 |
| marthalthurston.com | 1 | www.writeo.app | 1 |
| mein-lernen.at | 1 | www.zgwypl.com | 1 |
| mip.21cnjy.com | 1 | www.zxxk.com | 1 |
| news.gmw.cn | 1 | wxy.cqnu.edu.cn | 1 |
| novelium.com | 1 | wyb.chinawriter.com.cn | 1 |
| novelos.studio | 1 | xb.njtc.edu.cn | 1 |
| ocw.aca.ntu.edu.tw | 1 | xbzs.ecnu.edu.cn | 1 |
| product.m.dangdang.com | 1 | zhctwh.sicnu.edu.cn | 1 |

## academic.oup.com（1 条）

1. https://academic.oup.com/liverpool-scholarship-online/book/15553/chapter/170247764  （S3）

## archiu.com（1 条）

1. https://archiu.com/architecture-design/the-poetics-of-space-by-gaston-bachelard-book-analysis/?amp=1  （S3）

## article.xuexi.cn（1 条）

1. https://article.xuexi.cn/articles/index.html?art_id=6184381820508510911  （S2）

## book.douban.com（1 条）

1. https://book.douban.com/review/15523459/  （S3）

## campuspress.yale.edu（1 条）

1. https://campuspress.yale.edu/modernismlab/swanns-way/  （S3）

## culture.people.com.cn（2 条）

1. http://culture.people.com.cn/BIG5/n1/2020/0923/c1013-31871540.html  （S2）
2. http://culture.people.com.cn/n1/2016/0129/c87423-28096532.html  （S2）

## dangshi.people.com.cn（1 条）

1. http://dangshi.people.com.cn/n/2013/0308/c85037-20726844-7.html  （S2）

## digitalcommons.cwu.edu（1 条）

1. https://digitalcommons.cwu.edu/cgi/viewcontent.cgi?article=1294&context=ijurca  （S1）

## en.wikipedia.org（1 条）

1. https://en.wikipedia.org/wiki/180-degree_rule  （S1）

## epaper.gmw.cn（1 条）

1. https://epaper.gmw.cn/gmrb/html/2020-12/11/nw.D110000gmrb_20201211_2-16.htm  （S2）

## epaper.pdsxww.com（1 条）

1. http://epaper.pdsxww.com/pdswb/html/2025-10/01/content_474230.htm  （S2）

## escriturasinpiedad.com（1 条）

1. https://escriturasinpiedad.com/escena-y-secuela-la-formula-matematica-para-que-el-lector-no-pueda-dejar-de-leer/  （S1）

## essentiels.bnf.fr（1 条）

1. https://essentiels.bnf.fr/fr/article/a32c41d9-2363-4fa7-bfca-0bf1d17c59d9-espace-chez-proust  （S3）

## faulkner.iath.virginia.edu（1 条）

1. https://faulkner.iath.virginia.edu/media/resources/DISPLAYS/FaulknerMapsHP.html  （S3）

## gastonbachelard.org（1 条）

1. https://gastonbachelard.org/la-poetique-de-lespace/  （S3）

## ggw.hunau.edu.cn（1 条）

1. https://ggw.hunau.edu.cn/rwls/ysgs/201612/t20161208_167933.html  （S2）

## gj.zdic.net（3 条）

1. https://gj.zdic.net/jibu/896/27781.html  （S2）
2. https://gj.zdic.net/jibu/899/27943.html  （S2）
3. https://gj.zdic.net/jibu/981/32051.html  （S2）

## harvardindependent.com（1 条）

1. https://harvardindependent.com/soundtrack-of-violence/  （S1）

## howtofilmschool.com（1 条）

1. https://howtofilmschool.com/dictionary/180-degree-rule/  （S1）

## ilas.cssn.cn（1 条）

1. http://ilas.cssn.cn/webpic/web/ilas/manager/jeditor/UploadFile/20131119512788.pdf  （S3）

## introduction-to-film.com（1 条）

1. https://introduction-to-film.com/sound/  （S1）

## jasna.org（1 条）

1. https://jasna.org/publications-2/essay-contest-winning-entries/2023-essay-contest/duekel/  （S1）

## jlynchblog.com（1 条）

1. https://jlynchblog.com/2026/08/01/strengthen-character-arcs/  （S1）

## literarydevices.net（1 条）

1. https://literarydevices.net/mastering-setting-detail-how-to-paint-scenes-in-writing/  （S1）

## literarystudiesonline.com（1 条）

1. https://literarystudiesonline.com/seduction-language-and-narrative-control-a-narratological-study-of-lolita/  （S1）

## m.allhistory.com（1 条）

1. https://m.allhistory.com/detail/5924134e55b54278ac000abb  （S3）

## m.baike.com（3 条）

1. https://m.baike.com/wiki/%E4%BA%BA%E7%89%A9%E6%8F%8F%E5%86%99/3252432  （S2）
2. https://m.baike.com/wiki/%E7%A9%BA%E9%97%B4%E7%9A%84%E8%AF%97%E5%AD%A6/6598939  （S3）
3. https://m.baike.com/wiki/%E7%AE%80%E7%AC%94%E4%B8%8E%E7%B9%81%E7%AC%94/5577462  （S2）

## m.gushiwen.cn（1 条）

1. https://m.gushiwen.cn/guwen/bookv_cdb2e9d31181.aspx  （S2）

## m.thepaper.cn（2 条）

1. https://m.thepaper.cn/newsDetail_forward_29008480  （S2）
2. https://m.thepaper.cn/newsDetail_forward_7308153  （S3）

## marthalthurston.com（1 条）

1. https://marthalthurston.com/how-to-create-a-satisfying-character-arc/  （S1）

## mein-lernen.at（1 条）

1. https://mein-lernen.at/deutsch/moderne-literatur/franz-kafka-das-schloss-ausfuehrliche-interpretation/  （S3）

## mip.21cnjy.com（1 条）

1. https://mip.21cnjy.com/P/24744106.html  （S2）

## news.gmw.cn（1 条）

1. https://news.gmw.cn/2025-08/20/content_38229152.htm  （S2）

## novelium.com（1 条）

1. https://novelium.com/academy/glossary/scene-and-sequel  （S1）

## novelos.studio（1 条）

1. https://novelos.studio/blog/plotting-character-change/  （S1）

## ocw.aca.ntu.edu.tw（1 条）

1. https://ocw.aca.ntu.edu.tw/uploads/course_item_file/file/2860/101S120_AA26L01.pdf  （S3）

## product.m.dangdang.com（1 条）

1. http://product.m.dangdang.com/detail29757982-0-1.html  （S4）

## rkyfz.pku.edu.cn（2 条）

1. https://rkyfz.pku.edu.cn/Article/DownLoad?id=297981979&type=ArticleFile  （S4）
2. https://rkyfz.pku.edu.cn/Article/DownLoad?id=297986895&type=ArticleFile  （S3）

## sal.tongji.edu.cn（1 条）

1. https://sal.tongji.edu.cn/info/1002/3103.htm  （S3）

## scispace.com（1 条）

1. https://scispace.com/pdf/a-basic-analysis-of-the-deconstruction-of-space-and-the-2jwivxqr.pdf  （S3）

## sharonwray.com（1 条）

1. https://sharonwray.com/craft-of-writing/track-settings-in-your-story-bible/  （S1）

## shc.stanford.edu（1 条）

1. https://shc.stanford.edu/arcade/interventions/spatialization-strategy-reading-narrative  （S3）

## stateofformation.org（1 条）

1. https://stateofformation.org/2011/08/an-atheist-and-franz-kafkas-the-castle/  （S3）

## studyguides.com（1 条）

1. https://studyguides.com/study-methods/study-guide/cmlez2vr2931d0192z5vtenbk  （S3）

## tidenews.com.cn（1 条）

1. https://tidenews.com.cn/short_news.html?id=69be49da3e21c70001be96f3  （S2）

## tsg.hnzj.edu.cn（1 条）

1. https://tsg.hnzj.edu.cn/info/1071/4581.htm  （S2）

## web.mit.edu（1 条）

1. https://web.mit.edu/~21fms/People/henry3/games&narrative.html  （S3）

## wenxindiaolong.5000yan.com（1 条）

1. https://wenxindiaolong.5000yan.com/cai/45779.html  （S2）

## writoryofficial.com（1 条）

1. https://writoryofficial.com/fiction-glossary/scene-and-sequel  （S1）

## www.adobe.com（1 条）

1. https://www.adobe.com/creativecloud/video/discover/what-is-the-180-degree-rule.html  （S1）

## www.audible.com（1 条）

1. https://www.audible.com/blog/summary-one-hundred-years-of-solitude-by-gabriel-garcia-marquez  （S3）

## www.chinawriter.com.cn（4 条）

1. http://www.chinawriter.com.cn/n1/2017/0405/c404013-29189584.html  （S3）
2. http://www.chinawriter.com.cn/n1/2021/0307/c404030-32044757.html  （S2）
3. https://www.chinawriter.com.cn/bk/2015-12-07/84132.html  （S3）
4. https://www.chinawriter.com.cn/n1/2021/0803/c404030-32179409.html  （S2）

## www.codartium.com（1 条）

1. https://www.codartium.com/consistency-check-in-novel-writing/  （S1）

## www.cuc.edu.cn（1 条）

1. https://www.cuc.edu.cn/2024/0530/c12850a220338/page.htm  （S2）

## www.degruyterbrill.com（1 条）

1. https://www.degruyterbrill.com/document/doi/10.1515/zaa-2016-0003/html  （S3）

## www.dfll.tsinghua.edu.cn（1 条）

1. https://www.dfll.tsinghua.edu.cn/info/1037/2424.htm  （S1）

## www.estudoprevio.net（1 条）

1. https://www.estudoprevio.net/the-poetic-of-space-by-gaston-bachelard/?lang=en  （S3）

## www.filmsite.org（1 条）

1. https://www.filmsite.org/cloc.html  （S1）

## www.fizzread.ai（1 条）

1. https://www.fizzread.ai/moment/the-poetics-of-space  （S3）

## www.gushiwen.cn（2 条）

1. https://www.gushiwen.cn/mingju/juv.aspx?id=d8efe8316d09  （S2）
2. https://www.gushiwen.cn/mingju/juv_31f2e8554595.aspx  （S2）

## www.helpingwritersbecomeauthors.com（1 条）

1. http://www.helpingwritersbecomeauthors.com/synw-ingermanson  （S1）

## www.hxyww.cn（1 条）

1. http://www.hxyww.cn/dxcpnews.aspx?tid=7819  （S2）

## www.iwenyan.com（1 条）

1. http://www.iwenyan.com/ji/jiangzhaishihua  （S2）

## www.iwrity.com（1 条）

1. https://www.iwrity.com/writing-scene-sequel-guide  （S1）

## www.jyeoo.com（1 条）

1. https://www.jyeoo.com/shiti/71007914-15cb-4c15-85ae-32570a9cdfbd  （S2）

## www.litphil.sinica.edu.tw（1 条）

1. https://www.litphil.sinica.edu.tw/newsletter/62/53-73.pdf  （S2/S4）

## www.parker.mov（1 条）

1. https://www.parker.mov/tools/editologica/audio-visual-counterpoint  （S1）

## www.qinfeng.gov.cn（1 条）

1. https://www.qinfeng.gov.cn/info/1064/246512.htm  （S2）

## www.renrendoc.com（1 条）

1. https://www.renrendoc.com/paper/124038019.html  （S2）

## www.rmlt.com.cn（1 条）

1. https://www.rmlt.com.cn/2023/0901/681833.shtml  （S2）

## www.slashfilm.com（1 条）

1. https://www.slashfilm.com/756477/the-clockwork-orange-scene-you-may-not-have-known-was-improvised/  （S1）

## www.studyguides.com（2 条）

1. https://www.studyguides.com/study-methods/overview/cmir7wtpa4j1g01aa1n4g6nrb  （S3）
2. https://www.studyguides.com/study-methods/overview/cmpane7u1ecjf01ne2ibxj5pz  （S1）

## www.sumreads.com（1 条）

1. https://www.sumreads.com/books/pride-and-prejudice.html  （S1）

## www.supersummary.com（1 条）

1. https://www.supersummary.com/the-poetics-of-space/summary/  （S3）

## www.unistrapg.it（1 条）

1. https://www.unistrapg.it/it/marcel-proust-s-literary-places  （S3）

## www.writeo.app（1 条）

1. https://www.writeo.app/blogs/how-to-write-a-character-arc  （S1）

## www.zgwypl.com（1 条）

1. https://www.zgwypl.com/content/details80_48818.html  （S2）

## www.zxxk.com（1 条）

1. https://www.zxxk.com/soft/56321844.html  （S2）

## wxy.cqnu.edu.cn（1 条）

1. https://wxy.cqnu.edu.cn/info/1228/7421.htm  （S3）

## wyb.chinawriter.com.cn（1 条）

1. https://wyb.chinawriter.com.cn/content/202212/07/content67809.html  （S3）

## xb.njtc.edu.cn（1 条）

1. http://xb.njtc.edu.cn/cn/article/pdf/preview/10.13603/j.cnki.51-1621/z.2018.07.003.pdf  （S3）

## xbzs.ecnu.edu.cn（1 条）

1. https://xbzs.ecnu.edu.cn/CN/html/201205021.htm  （S4）

## yuwen.chazidian.com（2 条）

1. https://yuwen.chazidian.com/kewen3955/  （S2）
2. https://yuwen.chazidian.com/xiangxi-275708/  （S2）

## zhctwh.sicnu.edu.cn（1 条）

1. https://zhctwh.sicnu.edu.cn/p/16/?StId=st_app_news_i_x637695473549240418  （S4）

# 第二十九轮新增（2026-09-25）：补编三（T1/T2/T4/T5）创作工艺资料来源

> 本轮为 cinematic-craft.md / rhetoric-craft.md / terminology-index.md / prose-flow-craft.md / description-craft.md / dialogue-craft.md / character-craft.md / plot-logic-craft.md / structure-craft.md / viewpoint-craft.md / timeline-craft.md / novel-craft.md / foreshadowing-craft.md / style-spectrum-craft.md 增补而清点。来源四份补编三 docx（自豆包线程 x6U3Vrmil07tP8SFb 下载提取，与在线版同源）：T1 镜头补完与描写桐城 / T2 修辞格补全 / T4 术语索引扩容 / T5 二十六项待补深（另含总索引/核对表两文件同源 URL）。脚本口径：六文件命中 URL 白名单正则提取、协议/大小写/尾斜杠规范化去重后 N 条，与既有索引全量比对，重叠 M 条不重复登记，净新增按域名分组如下，每条标注所属卷。清点方式：脚本提取+比对，非目测。**本文件只保证"原文档里写了这个链接"，不说明链接内容说了什么、不保证现在仍可访问。**

| 域名 | 条数 | 域名 | 条数 |
|---|---|---|---|
| fiveable.me | 3 | mtoutiao.xdf.cn | 1 |
| m.baike.com | 3 | multiple.chat | 1 |
| m.gushiwen.cn | 3 | news.gmw.cn | 1 |
| www.gushiwen.cn | 3 | newsnew.lingnan.edu.cn | 1 |
| www.studyguides.com | 3 | office.teacheredu.cn | 1 |
| www.chinawriter.com.cn | 2 | open.library.okstate.edu | 1 |
| www.davidbordwell.net | 2 | paper.people.com.cn | 1 |
| www.docin.com | 2 | paradigmedu.in | 1 |
| www.litcharts.com | 2 | plato.stanford.edu | 1 |
| www.yinruiwen.net | 2 | sdsdwkxb.cnu.edu.cn | 1 |
| yw.chazidian.com | 2 | tag.chinawriter.com.cn | 1 |
| a.osmarks.net | 1 | tagg.org | 1 |
| bfidatadigipres.github.io | 1 | wenhui.whb.cn | 1 |
| blog.reedsy.com | 1 | wiki.tahlwyn.zone | 1 |
| cinemawavesblog.com | 1 | www.8frame.co | 1 |
| dcairns.wordpress.com | 1 | www.americanrhetoric.com | 1 |
| deepfilmanalysis.com | 1 | www.brooklyn.cuny.edu | 1 |
| ent.people.com.cn | 1 | www.chinesethought.cn | 1 |
| everythingisastory.blog | 1 | www.cinemaparadiso.co.uk | 1 |
| file.huatu.com | 1 | www.diancang.xyz | 1 |
| filmvision.ai | 1 | www.edb.gov.hk | 1 |
| glcoverage.com | 1 | www.grammarly.com | 1 |
| handwiki.org | 1 | www.guoxue123.com | 1 |
| humanwritesai.com | 1 | www.gutenberg.org | 1 |
| icc.pressbooks.pub | 1 | www.helpingwritersbecomeauthors.com | 1 |
| journal.bjut.edu.cn | 1 | www.hollywoodreporter.com | 1 |
| law.muc.edu.cn | 1 | www.indienova.com | 1 |
| library.fiveable.me | 1 | www.qstheory.cn | 1 |
| literature.cass.cn | 1 | www.thinka.ai | 1 |
| m.download.cucdc.com | 1 | www.tongcheng.gov.cn | 1 |
| m.zxxk.com | 1 | www.tup.tsinghua.edu.cn | 1 |
| max.book118.com | 1 | www.xuexi.cn | 1 |
| mip.21cnjy.com | 1 | wxy.jzxy.edu.cn:80 | 1 |
| modernfictionmakeitnewman.wordpress.com | 1 | xbbjb.xynu.edu.cn | 1 |
| moremovies.co.uk | 1 | xuyw.cbpt.cnki.net | 1 |

## a.osmarks.net（1 条）

1. https://a.osmarks.net/content/wikipedia_en_all_maxi_2020-08/A/Fabula_and_syuzhet  （T4）

## bfidatadigipres.github.io（1 条）

1. https://bfidatadigipres.github.io/pdf/2021-07-01-battleship-potemkin.pdf  （T1）

## blog.reedsy.com（1 条）

1. https://blog.reedsy.com/kill-your-darlings/  （T5）

## cinemawavesblog.com（1 条）

1. https://cinemawavesblog.com/film-blog/what-is-mise-en-scene/  （T1）

## dcairns.wordpress.com（1 条）

1. https://dcairns.wordpress.com/2023/04/14/a-dark-place/  （T1）

## deepfilmanalysis.com（1 条）

1. https://deepfilmanalysis.com/the-godfather-1972-deep-film-analysis/  （T1）

## ent.people.com.cn（1 条）

1. http://ent.people.com.cn/n1/2025/1011/c1012-40579825.html  （T4）

## everythingisastory.blog（1 条）

1. https://everythingisastory.blog/  （T5）

## file.huatu.com（1 条）

1. https://file.huatu.com/ziliao/202002/202002151714431822.pdf  （T2）

## filmvision.ai（1 条）

1. https://filmvision.ai/learn/camera-movements  （T1）

## fiveable.me（3 条）

1. https://fiveable.me/film-and-media-theory/key-terms/depth-of-field  （T1）
2. https://fiveable.me/introduction-to-film-theory/key-terms/deep-focus  （T1）
3. https://fiveable.me/introduction-to-film-theory/key-terms/rack-focus  （T1）

## glcoverage.com（1 条）

1. https://glcoverage.com/2024/06/25/the-godfather-opening-scene-analysis/  （T1）

## handwiki.org（1 条）

1. https://handwiki.org/wiki/Deep_focus  （T1）

## humanwritesai.com（1 条）

1. https://humanwritesai.com/blog/perplexity-burstiness-ai-detection-explained  （T4）

## icc.pressbooks.pub（1 条）

1. https://icc.pressbooks.pub/iccfilm110/chapter/chapter-5-cinematography/  （T1）

## journal.bjut.edu.cn（1 条）

1. https://journal.bjut.edu.cn/bjgydxxbskb/cn/article/pdf/preview/10.3969/j.issn.1671-0398.2014.03.011.pdf  （T2）

## law.muc.edu.cn（1 条）

1. https://law.muc.edu.cn/info/1034/2011.htm  （T2）

## library.fiveable.me（1 条）

1. https://library.fiveable.me/advanced-cinematography/unit-6  （T1）

## literature.cass.cn（1 条）

1. http://literature.cass.cn/ztzl/xsyjzt/xszm/202409/t20240910_5776739.shtml  （T1）

## m.baike.com（3 条）

1. https://m.baike.com/wiki/%E4%BE%A7%E9%9D%A2%E6%8F%8F%E5%86%99/591987  （T1）
2. https://m.baike.com/wiki/%E4%BF%AE%E8%BE%9E/1055612  （T2）
3. https://m.baike.com/wiki/%E5%91%BC%E5%91%8A/1055437  （T2）

## m.download.cucdc.com（1 条）

1. http://m.download.cucdc.com/wenku/45da9c74b5524012b2e60868f9d9e630.html  （T2）

## m.gushiwen.cn（3 条）

1. https://m.gushiwen.cn/mingju/juv_6248f6121b77.aspx  （T2）
2. https://m.gushiwen.cn/mingju/juv_7acac1284445.aspx  （T1）
3. https://m.gushiwen.cn/shiwenv_1cc4f4d60a66.aspx  （T2）

## m.zxxk.com（1 条）

1. https://m.zxxk.com/soft/58776751.html  （T5）

## max.book118.com（1 条）

1. https://max.book118.com/try_down/975321322034011302.pdf  （T2）

## mip.21cnjy.com（1 条）

1. https://mip.21cnjy.com/P/25397332.html  （T2）

## modernfictionmakeitnewman.wordpress.com（1 条）

1. https://modernfictionmakeitnewman.wordpress.com/useful-terms/  （T4）

## moremovies.co.uk（1 条）

1. https://moremovies.co.uk/film-scene-analysis-the-odessa-steps-sequence-from-battleship-potemkin/  （T1）

## mtoutiao.xdf.cn（1 条）

1. http://mtoutiao.xdf.cn/www/113/202211/12599644.html  （T2）

## multiple.chat（1 条）

1. https://multiple.chat/ai-detector-working-principles  （T4）

## news.gmw.cn（1 条）

1. https://news.gmw.cn/2025-03/03/content_37881471.htm  （T1）

## newsnew.lingnan.edu.cn（1 条）

1. https://newsnew.lingnan.edu.cn/info/1231/146240.htm  （T1）

## office.teacheredu.cn（1 条）

1. http://office.teacheredu.cn/zaixianyulan/teacheredu/webroot/files/202107/article/37003/202153153808275820.pdf  （T2）

## open.library.okstate.edu（1 条）

1. https://open.library.okstate.edu/introfilmtv/part/cinematography/  （T1）

## paper.people.com.cn（1 条）

1. http://paper.people.com.cn/fcyymwap/html/2023-04/07/content_25978124.htm  （T4）

## paradigmedu.in（1 条）

1. https://paradigmedu.in/resources/ibresources/Group%201/English%20Language%20&%20Literature/HL/Other/(This%20may%20look%20overwhelming,%20but%20that%C3%A2%E2%82%AC%E2%84%A2s%20because%20it%20is!)%20Almost%20every%20literary%20term_device%20explained/Parody-LitChart.pdf  （T2）

## plato.stanford.edu（1 条）

1. https://plato.stanford.edu/entries/paradox-suspense/  （T5）

## sdsdwkxb.cnu.edu.cn（1 条）

1. https://sdsdwkxb.cnu.edu.cn/gkll/2025n/2025d3q/5ab6f3c2df1d49ca95a204db05e69b7b.htm  （T5）

## tag.chinawriter.com.cn（1 条）

1. https://tag.chinawriter.com.cn/member/cjz690814/viewarchives_768722.html  （T4）

## tagg.org（1 条）

1. https://tagg.org/udem/musimgmot/filmtrms.html  （T4）

## wenhui.whb.cn（1 条）

1. http://wenhui.whb.cn/third/zaker/202104/28/402090.html  （T1）

## wiki.tahlwyn.zone（1 条）

1. https://wiki.tahlwyn.zone/content/wikipedia_en_top_maxi_2026-03/Unreliable_narrator  （T4）

## www.8frame.co（1 条）

1. https://www.8frame.co/blog/what-is-rack-focus  （T1）

## www.americanrhetoric.com（1 条）

1. https://www.americanrhetoric.com/speeches/mlkihaveadream.htm  （T5）

## www.brooklyn.cuny.edu（1 条）

1. https://www.brooklyn.cuny.edu/web/Film_Glossary_2015(1).pdf  （T4）

## www.chinawriter.com.cn（2 条）

1. https://www.chinawriter.com.cn/n1/2018/0522/c404092-30006054.html  （T2）
2. https://www.chinawriter.com.cn/n1/2026/0424/c442005-40708084.html  （T1）

## www.chinesethought.cn（1 条）

1. https://www.chinesethought.cn/phone/shuyu_show.aspx?shuyu_id=4177  （T1）

## www.cinemaparadiso.co.uk（1 条）

1. https://www.cinemaparadiso.co.uk/films/collections/film-history/the-history-of-film/battleship-potemkin-at-100  （T1）

## www.davidbordwell.net（2 条）

1. https://www.davidbordwell.net/blog/2013/11/29/hitchcock-lessing-and-the-bomb-under-the-table/  （T5）
2. https://www.davidbordwell.net/blog/2015/02/23/birdman-following-riggans-orders/  （T1）

## www.diancang.xyz（1 条）

1. https://www.diancang.xyz/leishuwenji/8071/163491.html  （T1）

## www.docin.com（2 条）

1. https://www.docin.com/touch_new/preview_new.do?id=1802366853  （T2）
2. https://www.docin.com/touch_new/preview_new.do?id=4933043582  （T2）

## www.edb.gov.hk（1 条）

1. https://www.edb.gov.hk/attachment/tc/curriculum-development/kla/chi-edu/resources/secondary-edu/lang/chi_chapter/P005.pdf  （T1）

## www.grammarly.com（1 条）

1. https://www.grammarly.com/blog/motif/  （T5）

## www.guoxue123.com（1 条）

1. http://www.guoxue123.com/new/0002/ywxs/073.htm  （T1）

## www.gushiwen.cn（3 条）

1. https://www.gushiwen.cn/  （T5）
2. https://www.gushiwen.cn/guwen/book_16.aspx  （T5）
3. https://www.gushiwen.cn/guwen/bookv_46653FD803893E4FCA9E47B52A7C0C3B.aspx  （T5）

## www.gutenberg.org（1 条）

1. https://www.gutenberg.org/ebooks/2152  （T5）

## www.helpingwritersbecomeauthors.com（1 条）

1. https://www.helpingwritersbecomeauthors.com/  （T5）

## www.hollywoodreporter.com（1 条）

1. https://www.hollywoodreporter.com/movies/movie-news/oscars-birdman-cinematographer-reveals-secrets-760590/amp/  （T1）

## www.indienova.com（1 条）

1. https://www.indienova.com/u/16621646441/blogread/38395  （T4）

## www.litcharts.com（2 条）

1. https://www.litcharts.com/literary-devices-and-terms/motif  （T5）
2. https://www.litcharts.com/literary-devices-and-terms/symbolism  （T5）

## www.qstheory.cn（1 条）

1. http://www.qstheory.cn/20260115/400fd55bccb4473fa87b2a7c7c8978f4/c.html  （T1）

## www.studyguides.com（3 条）

1. https://www.studyguides.com/study-methods/overview/cmpanebjtf4jk01nekfrjipoy  （T1）
2. https://www.studyguides.com/study-methods/study-guide/cmpane0q6cfdx01ne3xi0i1cm  （T1）
3. https://www.studyguides.com/study-methods/study-guide/cmpanfgb3pv7201neqyjobl5y  （T1）

## www.thinka.ai（1 条）

1. https://www.thinka.ai/en/Oxford-AQA-IGCSE/Chinese-%E2%80%93-First-Language-9263/%E5%B1%82%E9%80%92  （T2）

## www.tongcheng.gov.cn（1 条）

1. https://www.tongcheng.gov.cn/zjtc/tcyx/tcp/2024423051.html  （T1）

## www.tup.tsinghua.edu.cn（1 条）

1. http://www.tup.tsinghua.edu.cn/upload/books/yz/047242-01.txt  （T1）

## www.xuexi.cn（1 条）

1. https://www.xuexi.cn/e83d6166c8ae91834c84b03228263b06/18946f750bd31d919c3d180fa602ca8e.html  （T2）

## www.yinruiwen.net（2 条）

1. http://www.yinruiwen.net/news/22320.htm  （T2）
2. http://www.yinruiwen.net/news/58752.htm  （T2）

## wxy.jzxy.edu.cn:80（1 条）

1. http://wxy.jzxy.edu.cn:80/uploads/zwx/file/20180419/3o2qi8i8df.pdf  （T2）

## xbbjb.xynu.edu.cn（1 条）

1. http://xbbjb.xynu.edu.cn/cn/article/pdf/preview/1003-0964(2012)05-0115-05.pdf  （T2）

## xuyw.cbpt.cnki.net（1 条）

1. https://xuyw.cbpt.cnki.net/WKD/WebPublication/wkTextContent.aspx?colType=4&st=01&yt=2002  （T2）

## yw.chazidian.com（2 条）

1. https://yw.chazidian.com/mip/info5388/  （T2）
2. https://yw.chazidian.com/mip/info5412/  （T2）

