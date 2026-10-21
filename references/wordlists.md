# 常见模板表达与检查词表（中英文）

> **使用原则**：这些表达不是错误或作者身份的证据。密集或重复出现时，可检查其是否空泛、累赘或与语体不合；承担术语、衔接、声音或有意重复功能时保留。
> 自查方式：搜索只帮助定位，不设“出现几次就处理”的阈值；逐处说明问题后再决定保留、压缩或改写。
> 脚本 `ai_smell_lint.py` 可提示候选位置；计数不证明作者身份，也不能替代上下文判断。

## 中文

### 1. 过渡与衔接类（检查是否承担实际逻辑关系）
值得注意的是 / 值得一提的是 / 不容忽视的是 / 综上所述 / 总而言之 / 总的来说 / 由此可见 / 概言之 / 首先 / 其次 / 再次 / 最后 / 一方面……另一方面 / 此外 / 与此同时 / 然而 / 尽管如此 / 在此基础上 / 从某种意义上说 / 从某种角度来说 / 不难发现

### 2. 开头模板类
在当今社会 / 随着……的发展 / 近年来，随着…… / 在这个快节奏的时代 / 众所周知 / 毋庸置疑 / 自古以来 / 当今时代，科技日新月异

### 3. 强调与拔高类
至关重要 / 不可或缺 / 举足轻重 / 深远影响 / 奠定坚实基础 / 具有重要意义 / 彰显 / 凸显 / 见证 / 诠释 / 不仅……更是…… / 这不仅仅是……，更是……

### 4. 职场与互联网术语（依据读者知识解释，保留必要专业含义）
赋能 / 抓手 / 闭环 / 底层逻辑 / 颗粒度 / 拉通 / 对齐 / 复盘 / 打法 / 深度融合 / 全面提升 / 持续优化 / 生态化 / 矩阵式

### 5. 结尾升华类
未来可期 / 让我们拭目以待 / 机遇与挑战并存 / 愿你我都能…… / 遇见更好的自己 / 唯有如此，方能…… / 总而言之，让我们一起……

### 6. 网文 / 小说中可检查是否重复或失准的表达
- **神态**：眼底闪过一丝X / 眸色沉沉 / 眼神复杂 / 面无表情
- **笑容**：唇角微微勾起 / 莞尔一笑 / 似笑非笑
- **副词虚词**：微微 / 缓缓 / 忽而 / 骤然 / 淡淡 / 半晌 / 良久 / 不由得 / 下意识 / 不知为何
- **情绪**：心脏猛地一缩 / 心跳漏了一拍 / 五味杂陈
- **动作**：骨节分明的手 / 指尖泛白 / 身子一僵 / 呼吸一滞
- **写景**：月色皎洁 / 晚风习习 / 灯火璀璨 / 暮色沉沉 / 岁月静好

## 英文

### 1. 可检查是否空泛或与语境不合的动词 / 名词
delve, leverage, foster, underscore, tapestry, realm, navigate (the complexities of), harness, pivotal, robust, intricate, nuanced, multifaceted, landscape, testament, beacon, cornerstone, embark, elevate, unlock, streamline, epitomize, unravel, supercharge, spearhead, catapult, boast

### 2. hedging 与填充
It is important to note (that) / It is worth noting / It should be mentioned / In today's fast-paced world / In an ever-evolving landscape / When it comes to / plays a crucial role in / a wide range of / navigating the complexities of / in the realm of / one cannot overstate

### 3. 过渡与连接
Furthermore / Moreover / Additionally / Subsequently / Consequently / In conclusion / Ultimately / To sum up / The key takeaway is / That being said / Last but not least

### 4. 结尾乐观套话
The future looks bright / Exciting times lie ahead / Watch this space / Poised for growth / Take your X to the next level / The possibilities are endless / Step in the right direction / Don't get left behind

## 特别说明：破折号（em dash）

破折号被网友戏称为 "ChatGPT hyphen"，很多读者一看到满篇破折号就本能怀疑 AI。

但**研究层面它不是可靠判定证据**——很多优秀的人类写作者本来就爱用破折号。

处理原则：**如果你的读者群对它敏感，就控制密度；不要把它妖魔化**，更不要为了"去 AI 味"把正常的破折号全改成逗号（那会毁掉节奏）。

## 替换方向（保住事实、语义和语体）

### 按实际问题选择改法
1. **补证据**：抽象评价需要依据时，只补原稿已有或核验过的具体事实；没有材料就标待补，不新增经历、数值或来源。
2. **解释所指**：读者不熟悉术语时用易懂表达；专业概念、限定条件和正式语气需要时保留。
3. **调整措辞**：同义替换可以解决局部歧义或重复，但必须保持原意；不能保证改变检测结果，也不必为检测而改。

| 待检查的表述 | 可能仍未解决问题的换词 | 有证据时的具体化方向 |
|---|---|---|
| 取得了显著的成效 | 获得了突出的成果 | `[待补：真实结果与比较口径]`；证据不足时不增强“显著”判断 |
| 存在诸多问题 | 面临不少挑战 | 列出材料中确有的问题；不创造窗口数、队伍长度等场景 |
| 进行了深入的分析 | 开展了透彻的剖析 | 说明已记录的分析对象、方法和发现；不编造反复查看次数 |
| 极大提升了用户体验 | 大幅优化了用户感受 | `[待补：真实体验指标、变化幅度、样本与来源]`；没有数值时不补数值 |

### 中文黑话 → 人话（逐词对照）
| 黑话 | 改成 |
|---|---|
| 赋能 | 帮 / 让 / 支持 |
| 抓手 | 方法 / 切入点 |
| 闭环 | 做完整 / 跑通流程 |
| 底层逻辑 | 根本原因 / 到底怎么回事 |
| 对齐 | 商量一致 / 对一下 |
| 拉通 | 一起走通 / 打通 |
| 颗粒度 | 细到什么程度 |
| 复盘 | 事后回顾 / 总结一下 |
| 打法 | 做法 |
| 深刻影响 | 影响了……（只说明材料已有的影响，不增强因果确定性） |
| 进行了调研 | 开展了调研（只补原资料已有的对象、范围和时长） |
| 持续优化 | 一直在改 |
| 生态化 / 矩阵式 | 说清具体所指，否则删 |

### 英文表达的简化候选（核对语义和语域后使用）
| 原表达 | 可考虑的表达 |
|---|---|
| utilize | use |
| leverage | use / draw on |
| delve into | look at |
| navigate the complexities of | deal with the hard parts |
| a wide range of | 直接列出具体几项 |
| furthermore / moreover | also / and |
| in order to | to |
| it is important to note that | （删掉，直接说事） |
| due to the fact that | because |
