# -*- coding: utf-8 -*-
"""ai_smell_lint.py — AI 味静态检查器（humanize-writing skill）

用法:
    python ai_smell_lint.py 文章.md [更多文件...]
    python ai_smell_lint.py -                     # 从 stdin 读取
    python ai_smell_lint.py --json 文章.md        # 输出 JSON（便于集成）
    python ai_smell_lint.py --language en -       # 显式声明英文；auto不自动识别语言
    --language auto/zh/en/mixed：默认auto；不足100中文字的未声明ASCII文本仅有限扫描。
    python ai_smell_lint.py --genre law 文章.md   # 文体门控（general/tech/academic/official/law/email/speech/fiction）

静态写作线索分 0-100，越高表示本规则集的加权命中越多，不等于文本越差。
这是编辑启发式指标，不是AI生成概率，不鉴定作者或预测外部检测通过率:
    < 25  静态命中较少      25-40 静态命中适中      > 40  静态命中较多
    中文线索在有效量不足 300 单位时按 300 单位归一；单位为中文字 + ASCII 词。
    英文线索沿用英文分支权重，不按中文字数放大；混语分数不兼容旧版。
    v0.42：句长标准差也改为零权重观察；与v0.41的短句占比、重复“不是…而是…”均不计分。
    v0.43：段落长度与正则锚点密度也改为零权重观察，不为比例或密度添删信息。
    v0.51：[分行结构] 在长文本（[分行] 触发）同样输出了；句末标点只认句号/问号/
           叹号/省略号（分号、冒号不算），清单与表格不再被当成诗行。
    不能用跨版本降分证明改稿收益。
    文体门控按 GENRE_SKIPS 逐文体关闭检查项：tech/academic/official 关闭全部结构类
    检查（该类文体本就需要平行结构与统一句式）；law 关闭短句/顿号连排/冒号列表/
    段落开头/总结式结尾；fiction 只关段落开头；speech 只关路标词；email 同 general。
    豁免清单仅参考 tests/corpus/ 四篇历史设计样本，不构成各文体充分标定（出处见 corpus/SOURCES.md）。
    四字套话连缀/段首序数/展望式收尾（v0.20）/文艺比喻/抽象名词化/礼貌框架
    （v0.23）全文体生效，不进豁免清单；段内枚举（v0.23）进 tech/academic/
    official 豁免清单——"一是…二是…"式平行编号是技术规范与公文的常规结构
    （TECH_SPEC 即设计样本，见 tests/selftest.py ⑬）。
    四字套话按密度判（≥3 处且 ≥2 对/300 字）；法律等文体的术语性并列可能合理，
    命中后仍需按语境判断，不保证豁免。
退出码:
    0 未超静态阈值    1 超过静态阈值（需按文体核读）
    2 输入不足、语言未确认/范围不支持、读取失败或参数错误

指标依据见 references/detection-principles.md，规则编号见 references/quick-reference.md。
"""
import json
import re
import statistics
import sys

RULESET_VERSION = "0.43"

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

MIN_CHARS = 100
GOOD_LINE = 25
PASS_LINE = 40
SCORE_NORM_CHARS = 300
# 混合文本门槛：中英各自都没到自己的门槛、但合起来已够判时，不该判"无法判定"。
# 判据用「中文字数 + 英文词数」的总量（两者都是"信息单位"，量纲近似可比）。
MIXED_MIN_UNITS = 100
# 各文体关闭的检查项（v0.19，依据 tests/corpus/ 四篇真实人写语料在 general 模式下
# 的实测触发项标定，出处登记见 tests/corpus/SOURCES.md）：技术规范/学术论文/公文
# 本就需要平行结构与统一句式，硬套"反 AI 结构"规则只会误伤（见 quick-reference.md
# 「何时不要用这些规则」）。
#   law：判决书惯用顿号列举证据项、当事人名起段、"首先/其次"引出争点，短句占比/
#        顿号连排/段落开头为洪秀凤案实测误伤，"综上……判决如下"属文体法定收束；
#        当时句长 std 与路标词在该设计样本未达罚线，未加入豁免；v0.42 句长已仅作零权重观察。
#   fiction：有意复沓（"孔乙己"起段 ×3）是修辞不是模板，只关段落开头。
#   speech：口语路标（第一/其次/最后）是演讲的天然骨架，只关路标词。
#   email：《两地书》四信实测零触发，不豁免任何检查。
GENRE_SKIPS = {
    "general": (),
    "tech": ("句长", "短句", "路标词", "顿号连排", "冒号列表", "总结式结尾", "段落均匀", "段落开头", "段内枚举"),
    "academic": ("句长", "短句", "路标词", "顿号连排", "冒号列表", "总结式结尾", "段落均匀", "段落开头", "段内枚举"),
    "official": ("句长", "短句", "路标词", "顿号连排", "冒号列表", "总结式结尾", "段落均匀", "段落开头", "段内枚举"),
    "law": ("短句", "顿号连排", "冒号列表", "段落开头", "总结式结尾"),
    "email": (),
    "speech": ("路标词",),
    "fiction": ("段落开头",),
}
GENRES = tuple(GENRE_SKIPS)
LANGUAGES = ("auto", "zh", "en", "mixed")

STRONG_WORDS = [
    "综上所述", "总而言之", "由此可见", "众所周知", "值得注意的是",
    "值得一提", "需要指出的是", "不容忽视", "不难发现", "概言之",
    "不可或缺", "蓬勃发展", "日新月异", "翻天覆地", "尤为重要",
    "赋能", "抓手", "闭环", "底层逻辑", "顶层设计", "深度剖析",
    "全方位", "系统性", "至关重要", "深耕", "多维", "欣欣向荣",
    "恰似", "极大地", "举足轻重", "深远影响", "奠定坚实基础",
    "彰显", "凸显", "诠释", "颗粒度", "拉通", "对齐", "复盘",
    "打法", "深度融合", "全面提升", "持续优化", "生态化", "矩阵式",
    "未来可期", "拭目以待", "机遇与挑战并存", "遇见更好的自己",
    "唯有如此",
]
ROAD_WORDS = ["首先", "其次", "再次", "最后", "与此同时", "一方面", "另一方面"]
ABSOLUTE_WORDS = ["全面", "彻底", "非常", "十分", "极其", "尤为"]
# Narrow quantity/time exclusions; this remains a lexical heuristic, not parsing.
DEGREE_SHIFEN = re.compile(r"十分(?!\s*(?:之|钟|鐘))")
TIME_BEFORE_SHIFEN = re.compile(r"(?<![第这這那每哪此零〇一二两兩三四五六七八九十百千万\d])[零〇一二两兩三四五六七八九十\d]+[点點时時]\s*[零〇一二两兩三四五六七八九\d]*$")
NOVEL_WORDS = [
    "眼底闪过一丝", "眸色沉沉", "眼神复杂", "面无表情", "唇角微微勾起",
    "莞尔一笑", "似笑非笑", "微微", "缓缓", "忽而", "骤然", "半晌",
    "良久", "不由得", "下意识", "不知为何", "心脏猛地一缩",
    "心跳漏了一拍", "五味杂陈", "骨节分明", "指尖泛白", "身子一僵",
    "呼吸一滞", "月色皎洁", "晚风习习", "灯火璀璨", "暮色沉沉", "岁月静好",
]
EN_PHRASES = [
    "delve", "tapestry", "leverage", "robust", "seamless", "foster",
    "pivotal", "crucial", "multifaceted", "intricate", "nuanced",
    "landscape", "testament", "beacon", "cornerstone", "embark",
    "elevate", "unlock", "streamline", "epitomize", "unravel",
    "supercharge", "spearhead", "catapult", "harness",
    "in conclusion", "it is important to note", "in today's fast-paced world",
    "moreover", "furthermore", "additionally", "subsequently",
    "consequently", "that being said", "last but not least",
    "when it comes to", "a wide range of", "in the realm of",
]
PATTERNS = {
    "不是…而是…": r"不是[^，。？！]{1,20}，?而是",
    "不仅…还/更…": r"不仅[^。？！]{1,30}(?:还|也|更|而且)",
    "一方面…另一方面": r"一方面[^。]{1,40}另一方面",
    "随着…的发展": r"随着[^，。]{1,20}的(?:发展|进步|推进|深入)",
    "在当今…时代": r"在(?:当今|当下|当前|这个)[^，。]{0,12}(?:社会|时代|背景下)",
}
SUMMARY_STARTS = ["综上所述", "综上", "总而言之", "总之", "由此可见", "可见"]
EN_MIN_WORDS = 100
EN_SUMMARY_STARTS = ["in conclusion", "in summary", "to sum up", "to conclude", "in short", "all in all"]
FOUR_CHAR_PAIR = re.compile(r"[\u4e00-\u9fff]{4}、[\u4e00-\u9fff]{4}(?![\u4e00-\u9fff、])")
# 密度门槛：四字并列要「个数 ≥3 且 ≥2 对/300 字」才算套话。法律文书等文体的
# 术语性并列（洪秀凤案「原始证据、直接证据」×4 对/约 4900 字 ≈ 0.2 对/300 字）
# 与演讲口号串（实测 3.6 对/300 字）在密度上相差一个量级，只看绝对个数会误伤；
# 标定与探针见 tests/selftest.py ⑮，依据登记见 tests/corpus/SOURCES.md。
FOUR_CHAR_MIN_COUNT = 3
FOUR_CHAR_MIN_DENSITY = 2.0
ORDINAL_START = re.compile(r"^(?:首先|其次|再次|最后|第[一二三四五六七八九十]+)[，,：:]")
OUTLOOK_PATTERNS = (
    re.compile(r"相信[^。]{0,30}一定能够"),
    re.compile(r"让我们以[^。]{0,40}携手并进"),
    # v0.23 以下为展望变体（speech_annual/email_invite 校准样本实测漏报）：
    re.compile(r"让我们把[^。]{0,24}(?:化作|变成)"),
    re.compile(r"共同举杯|为[^。！？]{0,10}喝彩"),
    re.compile(r"共同[^，。！？]{2,8}[、，]共同"),
    re.compile(r"期待[^。！？]{0,15}(?:相聚|重逢)"),
)
# v0.23 新增：模式层指纹。标定依据 tests/corpus_ai_calib/ 七篇独立会话样本
# （生成时不知 lint 词表，与 corpus_ai 同会话样本互为对照）；真人侧防误报闸 =
# tests/corpus/ 四篇真实人写语料（闻一多恰 1 处比喻 → count≥2 密度门挡住）。
SIMILE_RES = (
    re.compile(r"像是?[^，。！？；\n]{1,18}(?:似的|一样|一般)"),
    re.compile(r"(?:就像|好像|宛如|好似|仿佛像)[^，。！？；\n]{2,18}"),
    re.compile(r"像是[^，。！？；\n]{2,16}"),
    re.compile(r"像(?:一|某种|谁)[^，。！？；\n]{2,20}"),
)
SIMILE_MIN_COUNT = 2
SIMILE_MIN_DENSITY = 1.0
NOMINAL_RES = (
    re.compile(r"变成(?:了)?一种[^，。！？；]{2,12}"),
    re.compile(r"一种(?:难以言明|说不清道不明|说不清|莫名|钝钝|深深|淡淡|奇异|奇怪|微妙)[^，。！？；]{1,10}"),
)
ENUM_SEG = ("一是", "二是", "三是", "四是")
POLITE_A = re.compile(r"首先[^。！？]{0,15}感谢")
POLITE_B = re.compile(r"再次感谢")

SENT_SPLIT = re.compile(r"[。！？!?；;…]+")
DUNHAO_RUN = re.compile(r"(?:[^、，。？！\s]{1,10}、){3,}[^、，。？！\s]{1,10}")
COLON_LIST = re.compile(r"[：:][^。？！]{0,15}(?:一是|二是|①|（一）|其一)")
ANCHOR_RE = re.compile(
    r"\d+(?:\.\d+)?"
    r"|[一二三四五六七八九十两半零]{1,4}"
    r"(?:点半|块|毛|角|分|个|只|条|张|片|号|包|次|根|斤|里|米|寸|年|月|日|天|点|行|层|度|人|家|遍|圈|声|岁)"
    r"|[\u4e00-\u9fff]{2,4}(?:省|市|县|村|镇|路|街|巷|弄|大学|中学|公司|医院)"
)


def read_text(path):
    if path == "-":
        data = sys.stdin.buffer.read()
        for enc in ("utf-8", "utf-8-sig", "gbk"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                continue
        return data.decode("utf-8", errors="replace")
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def strip_markdown(t):
    t = re.sub(r"```[\s\S]*?```", " ", t)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.M)
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.M)
    t = re.sub(r"^>\s?", "", t, flags=re.M)
    t = re.sub(r"[*_~|>#]+", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    return t


def chinese_len(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def sentences(text):
    out = []
    for chunk in SENT_SPLIT.split(text):
        c = chunk.strip()
        if chinese_len(c) >= 2:
            out.append(c)
    return out


def raw_paragraphs(text):
    """空行优先分段；若只有单换行，则按单换行分段（Word 粘贴常见）。不过滤短段。"""
    raw = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(raw) < 2:
        raw = [p.strip() for p in text.split("\n") if p.strip()]
    return raw


def ending_paragraphs(text):
    """正文结尾保留短段；只排除明确礼仪行和日期，不猜测短句是否正文。"""
    out = []
    for p in raw_paragraphs(text):
        if re.fullmatch(r"(?:此致|敬礼|此致敬礼|敬上|Sincerely|Regards|Best regards)[，,。.!！]*", p, re.I):
            continue
        if re.fullmatch(r"(?:[0-9]{4}[-/年][0-9]{1,2}[-/月][0-9]{1,2}日?|(?:署名|作者|日期)\s*[:：].+)", p):
            continue
        out.append(p)
    return out


def paragraphs(text):
    """统计用分段：过滤 <20 字短段（礼仪行/短收尾句不参与句长与段落统计）。"""
    return [p for p in raw_paragraphs(text) if chinese_len(p) >= 20]


def count_degree_word(text, word):
    if word != "十分":
        return text.count(word)
    # Exclude numeric clocks, while keeping 当时十分担忧 and 第一/这一点十分重要.
    return sum(1 for match in DEGREE_SHIFEN.finditer(text)
               if not TIME_BEFORE_SHIFEN.search(text[max(0, match.start() - 32):match.start()]))


def ascii_word_len(body):
    """ASCII 词形的近似计数，不是语言识别。"""
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", body))


def chinese_word_issues(body):
    """同一中文词表在所有有效输入上使用同一权重。"""
    return [
        (min(12, 4 * body.count(w)),
         "[AI 词] '%s' × %d → 核对是否空泛或冗余；专业术语、引文、定义和必要重复保留，不为降分删除" % (w, body.count(w)))
        for w in STRONG_WORDS if w in body
    ]


ENGLISH_ISSUE_TAGS = ("[英文 AI 词]", "[英文总结式结尾]")


def english_issues(body, skips):
    """英文信号的唯一计分路径，避免中文达到门槛时重复定义权重。"""
    found = []
    for w in EN_PHRASES:
        n = len(re.findall(r"\b" + re.escape(w) + r"\b", body, flags=re.I))
        if n:
            found.append((min(10, 2 * n),
                          "[英文 AI 词] '%s' × %d → 核对语境与具体含义；术语、引文和必要重复保留" % (w, n)))
    if "总结式结尾" not in skips:
        tail_body = ending_paragraphs(body)
        tail_en = tail_body[-1][-220:].lower() if tail_body else ""
        hit = next((s for s in EN_SUMMARY_STARTS if s in tail_en), None)
        if hit:
            found.append((8, "[英文总结式结尾] 末段出现 '%s' → 核对是否重复；必要总结保留" % hit))
    return found


# 行末「句末标点」：句号/问号/叹号/省略号，允许其后紧跟收尾引号或括号。
# 分号与冒号是句内停顿，不算句末——否则「山一程；水一程；」这类分行会被误判为已闭合。
LINE_CLOSED = re.compile(r"[。！？…．?!]+[”\"'』」）)\]]*$")

# 列表/表格行首标记。清单、核对表与 Markdown 表格不是分行韵文，不能按诗行统计，
# 否则「检查版本号」这类条目会被报成韵脚候选（v0.51 实测的误报）。
LIST_MARK = re.compile(r"^\s*(?:[-*+•]\s+|\d{1,3}[.、)]\s*|\[[ xX]\]\s+|>\s?)")


def is_list_or_table(text):
    """行首标记占非空行过半时，把文本视为列表或表格，跳过诗行统计。"""
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if len(lines) < 4:
        return False
    marked = sum(1 for ln in lines if LIST_MARK.match(ln) or ln.count("|") >= 2)
    return marked * 2 >= len(lines)


def _line_label(nums, limit=8):
    """行号标签只展示前若干项，避免长诗把一行输出撑成整屏。"""
    shown = "、".join(map(str, nums[:limit]))
    if len(nums) > limit:
        return "第%s…行（共 %d 行）" % (shown, len(nums))
    return "第%s行" % shown


def line_structure_observations(body, raw=None):
    """Position statistics for line-broken text (poems, lyrics, scripts).

    Unlike the weighted density checks, these are counts and line numbers, so they stay
    meaningful for a four-line poem; they are emitted even on the "short"/"limited" paths where
    no score can be given, and on the scored path when the text is line-dominant. Zero weight,
    no judgment, no thresholds to hit.
    """
    if is_list_or_table(raw if raw is not None else body):
        return []
    lines = [ln.strip() for ln in body.split("\n") if chinese_len(ln.strip()) >= 2]
    if len(lines) < 4:
        return []
    open_ends = [i for i in range(len(lines) - 1) if not LINE_CLOSED.search(lines[i])]
    if len(open_ends) * 2 < len(lines) - 1:
        return []

    out = ["[分行结构] 有效行 %d 行，其中 %d 处行末没有句末标点（跨行候选）→ 只报位置；分行与跨行本身不产生诗意，也不因整齐或参差加减分"
           % (len(lines), len(open_ends))]
    lens = [chinese_len(x) for x in lines]
    shown_lens = "、".join(str(x) for x in lens[:24]) + ("…共 %d 行" % len(lens) if len(lens) > 24 else "")
    out.append("[分行结构] 行长 %d–%d 字（逐行 %s）→ 均匀与参差都可能有用，不设目标区间，不为参差改行"
               % (min(lens), max(lens), shown_lens))
    where = {}
    for i, x in enumerate(lines, 1):
        where.setdefault(x, []).append(i)
    repeated = [(k, v) for k, v in where.items() if len(v) > 1]
    if repeated:
        more = "（另有 %d 组未列出）" % (len(repeated) - 3) if len(repeated) > 3 else ""
        out.append("[分行结构] 整行原样复现：%s%s → 核对每次出现是否改变了语境；叠句不设次数上下限，无位移才算空转"
                   % ("；".join("「%s」%s" % (k, _line_label(v)) for k, v in repeated[:3]), more))
    tails = {}
    for i, x in enumerate(lines, 1):
        core = re.sub(r"[，、；：。！？…、“”\"'（）()\s]+$", "", x).strip()
        if core:
            tails.setdefault(core[-1], []).append(i)
    rhymes = sorted(((k, v) for k, v in tails.items() if len(v) >= 2), key=lambda kv: -len(kv[1]))
    if rhymes:
        more = "（另有 %d 组未列出）" % (len(rhymes) - 3) if len(rhymes) > 3 else ""
        out.append("[分行结构] 行末同字候选：%s%s → 仅作位置线索；是否合律要按用户指定的谱本与韵书逐字核验，这里不判合律也不判押韵好坏"
                   % ("；".join("「%s」%s" % (k, _line_label(v)) for k, v in rhymes[:3]), more))
    out.append("[分行结构] 以上是位置统计，不构成诗意或质量判断；密度类分数仍需有效中文 ≥%d，不足则记「无法判定」" % MIN_CHARS)
    return [(0, m) for m in out]


def check(text, genre="general", language="auto"):
    issues = []

    def add(w, msg):
        issues.append((w, msg))

    if language not in LANGUAGES:
        raise ValueError("未知 language: %s" % language)
    skips = GENRE_SKIPS.get(genre, ())

    body = strip_markdown(text)
    total = chinese_len(body)
    en_words = ascii_word_len(body)
    sents = sentences(body)
    paras = paragraphs(body)
    note = "有效中文 %d 字 · %d 句 · %d 段" % (total, len(sents), len(paras))

    if not total and not en_words and any(c.isalpha() for c in body):
        add(0, "[不支持的文字范围] 未取得中文字或ASCII词形；当前规则仅覆盖中文及调用者声明的英文/混语，不能把其他文字视为短文或零风险")
        return issues, "unsupported"
    if language == "zh" and total < MIN_CHARS:
        add(0, "[无法判定] 声明为中文，但有效中文 %d 字不足 %d；其他文字不代替中文统计样本" % (total, MIN_CHARS))
        issues.extend(line_structure_observations(body, text))
        return issues, "short"
    if language == "en" and en_words < EN_MIN_WORDS:
        add(0, "[无法判定] 声明为英文，但ASCII词形 %d 个不足 %d；计数并非语言识别" % (en_words, EN_MIN_WORDS))
        issues.extend(line_structure_observations(body, text))
        return issues, "short"
    if language == "mixed" and (not total or not en_words):
        add(0, "[语言声明不匹配] mixed 需要中文和ASCII词形均存在；请按实际输入声明语言")
        return issues, "unsupported"

    if total + en_words < MIXED_MIN_UNITS:
        add(0, "[无法判定] %s（ASCII 词形 %d 个，合计 %d）；样本量不足，统计特征不成立，勿据此判分"
               % (note, en_words, total + en_words))
        issues.extend(line_structure_observations(body, text))
        return issues, "short"

    if total < MIN_CHARS:
        limited = language == "auto"
        mode = "有限词表扫描：语言未确认" if limited else ("混合模式" if language == "mixed" else "英文词表模式（调用者声明）")
        add(0, "[%s] 中文 %d 字 + ASCII词形 %d 个；仅执行词表及适用的英文结尾检测。"
               "中文结构样本不足；ASCII词形不是英文语言识别，也没有跨语言校准。" % (mode, total, en_words))
        if limited:
            add(0, "[语言范围] auto 不识别实际语言；英文或中英混语请显式指定 --language en 或 --language mixed，声明不代表系统验证")
        issues.extend(chinese_word_issues(body))
        issues.extend(english_issues(body, skips))
        return issues, "limited" if limited else "ok"

    add(0, "[概览] " + note)

    # v0.49：分行文本的测量失效提示（零权重，不改变分数；实测 24 个有效行仅切出 1 句）
    # v0.51：同一条件（行多句少）下补出 [分行结构]——此前它只在短样本路径可达，
    #        超过 100 有效中文的长诗/歌词反而永远拿不到行级位置统计。
    lines = [ln for ln in body.split("\n") if chinese_len(ln.strip()) >= 2]
    if not is_list_or_table(text) and len(lines) >= 8 and len(sents) * 3 <= len(lines):
        add(0, "[分行] %d 行短行只切出 %d 句：行末没有句末标点时句子会跨行连读，"
               "句长、短句占比与段落类检查在这里几乎没有对象。此行为测量说明，不计分、"
               "不评价分行/跨行/节奏的好坏，也不因分行整齐或参差加减分" % (len(lines), len(sents)))
        issues.extend(line_structure_observations(body, text))

    if skips:
        add(0, "[genre] %s 文体：已关闭 %s（这些形式在该文体可有正常用途；历史设计样本见 tests/corpus/SOURCES.md，不代表充分标定），其余检查照常" % (genre, "、".join(skips)))
    lens = [chinese_len(s) for s in sents]
    if "句长" not in skips and len(lens) >= 4:
        std = statistics.pstdev(lens)
        add(0, "[句长] 标准差 %.1f（仅观察，不设目标区间）→ 核读动作、因果、指代与停顿；均匀或参差均可能有功能，不按比例插句、不为拉大差距改标点；长短句按内容与声音保留" % std)
    if "短句" not in skips and lens:
        short_ratio = sum(1 for L in lens if 3 <= L <= 8) / len(lens)
        add(0, "[短句] 3-8 字短句占比 %.0f%%（仅观察，不设合格比例）→ 核读动作、因果、指代是否被停顿切断；仅在影响阅读时合并或拆分，不为比例添情节；对白、诗歌、剧本拍点及有意简练按功能保留" % (short_ratio * 100))

    issues.extend(chinese_word_issues(body))
    if "路标词" not in skips:
        road = sum(body.count(w) for w in ROAD_WORDS)
        if road >= 3:
            add(min(9, 3 * (road - 2)), "[路标词] 首先/其次/最后… 共 %d 处（≥3）→ 核对是否冗余；必要流程顺序、论证导航和人物声口保留，不按比例删除" % road)
        elif road:
            add(0, "[路标词] 共 %d 处（尚可）" % road)
    novel_hits = [w for w in NOVEL_WORDS if w in body]
    if len(novel_hits) >= 3:
        add(5, "[常见小说表达] 命中 %d 种（%s…）→ 核对是否空泛、重复或不合人物声口；有叙事功能则保留，修订须保留动机与节奏" % (
            len(novel_hits), "、".join(novel_hits[:4])))
    elif len(novel_hits) == 2:
        add(3, "[常见小说表达] 命中 2 种（%s）→ 按视角与人物声口核读；确有空泛问题时再改，不统一替换为身体动作" % "、".join(novel_hits))
    for w in ABSOLUTE_WORDS:
        n = count_degree_word(body, w)
        if n >= 3:
            add(4, "[程度用语] '%s' × %d（≥3）→ 核对词义及证据是否支持；数量、术语和有依据的确定表述保留，不自动弱化" % (w, n))
    issues.extend(english_issues(body, skips))

    for name, pat in PATTERNS.items():
        n = len(re.findall(pat, body))
        limit = 1 if name == "不是…而是…" else 2
        if n > limit:
            if name == "不是…而是…":
                add(0, "[对照句式] '%s' × %d（仅定位复读）→ 核对否定项的依据及两项是否可并存；真实纠错、必要比较、引用和人物争执按功能保留，静态次数不能判断拉踩" % (name, n))
            else:
                add(5, "[AI 句式] '%s' × %d（>%d）→ 核对是否机械重复；有功能的强调、论证关系和人物声口保留，不因次数自动改写" % (name, n, limit))

    if "顿号连排" not in skips:
        runs = DUNHAO_RUN.findall(body)
        if runs:
            add(min(8, 4 * len(runs)), "[顿号连排] ≥4 项连排 × %d 处，例：'%s…' → 核对并列是否清楚；术语、完整列项和修辞节奏保留，仅在阅读受阻时调整" % (len(runs), runs[0][:24]))
    if "冒号列表" not in skips:
        colon_lists = COLON_LIST.findall(body)
        if len(colon_lists) >= 2:
            add(5, "[冒号列表] 冒号+编号解释 × %d → 核对信息层次；必要导航、步骤和编号引用保留，不统一改成叙述" % len(colon_lists))
    pairs = FOUR_CHAR_PAIR.findall(body)
    pair_density = len(pairs) / (total / SCORE_NORM_CHARS) if total else 0.0
    if len(pairs) >= FOUR_CHAR_MIN_COUNT and pair_density >= FOUR_CHAR_MIN_DENSITY:
        add(6, "[四字套话] 四字对仗连缀 × %d 处（%.1f 对/300 字 ≥2），例：'%s' → 核对具体含义；有功能的排比、术语和文体节奏保留，仅处理空泛或重复处" % (len(pairs), pair_density, pairs[0]))
    elif len(pairs) >= FOUR_CHAR_MIN_COUNT:
        add(0, "[四字套话] 四字并列 %d 处、密度 %.1f 对/300 字（<2）→ 术语性并列不计套话" % (len(pairs), pair_density))

    # v0.23 信号 A：文艺比喻密度（count + 密度双门，同四字套话构式；
    # 真人侧标定：闻一多恰 1 处 → count 门挡住，孔乙己 0 处）
    sim_spans = []
    for pat in SIMILE_RES:
        for m in pat.finditer(body):
            sim_spans.append((m.start(), m.end()))
    similes = []
    for s, e in sorted(sim_spans):
        if similes and s <= similes[-1][1]:
            if e > similes[-1][1]:
                similes[-1] = (similes[-1][0], e)
        else:
            similes.append((s, e))
    sim_density = len(similes) / (total / SCORE_NORM_CHARS) if total else 0.0
    if len(similes) >= SIMILE_MIN_COUNT and sim_density >= SIMILE_MIN_DENSITY:
        add(8, "[文艺比喻] '像…一样/仿佛/宛如'式明喻 × %d 处（%.1f/300 字 ≥1.0）→ 逐项核读准确性、信息增量和视角；有功能则保留，不设统一数量上限" % (len(similes), sim_density))
    elif len(similes) >= SIMILE_MIN_COUNT:
        add(0, "[文艺比喻] 明喻 %d 处、密度 %.1f/300 字（<1.0）→ 未超过本规则密度阈值，修辞质量仍需读稿" % (len(similes), sim_density))

    # v0.23 信号 B：抽象名词化（族内只报一次，不按处数加罚）
    nom_hit = next((m.group(0) for pat in NOMINAL_RES for m in [pat.search(body)] if m), None)
    if nom_hit:
        add(5, "[抽象名词化] '%s' → 核对是否空泛；准确概念、必要概述和内心叙述保留，不强制转成动作或补造感官细节" % nom_hit)

    if "总结式结尾" not in skips:
        tail_body = ending_paragraphs(body)
        last = tail_body[-1] if tail_body else ""
        head = last.lstrip("　 \t\r\n")[:8]
        hit = next((s for s in SUMMARY_STARTS if head.startswith(s)), None)
        if hit is None:
            hit = next((s for s in SUMMARY_STARTS if s in last[:40]), None)
        if hit:
            add(8, "[总结式结尾] 末段以 '%s' 起头或收束 → 核对是否重复或越过证据；必要总结、人物反思和收束功能保留，不强制换成场景或动作" % hit)
        else:
            add(0, "[结尾] 末段未出现总结路标 ✓")

    # v0.23：展望窗口用未过滤分段（raw_paragraphs）——paragraphs() 的 20 字门槛
    # 会把"期待周五与大家相聚，共同探讨、共同进步！"（17 字）整段滤掉，窗口再大
    # 也看不到（ai_email_invite 校准样本实测漏报的真因）；另跳过书信礼仪段
    # （此致/敬礼/署名/日期，≤6 字无标点）。
    tail_paras = [p for p in raw_paragraphs(body)
                  if not (chinese_len(p) <= 6 and not re.search(r"[。！？，,]", p))]
    outlook_hit = None
    for p in tail_paras[-3:]:
        for pat in OUTLOOK_PATTERNS:
            m = pat.search(p)
            if m:
                outlook_hit = m.group(0)
                break
        if outlook_hit:
            break
    if outlook_hit:
        add(8, "[展望式收尾] 末尾窗口出现 '%s' → 核对承诺依据与语气；真实计划、祝愿和邀请功能保留，不强制留白或补造事实" % outlook_hit)

    if "段落均匀" in skips and "段落开头" in skips:
        add(0, "[段落] %s 文体跳过段落层检测" % genre)
    elif len(paras) >= 3:
        if "段落均匀" not in skips:
            plens = [chinese_len(p) for p in paras]
            add(0, "[段落] 统计段落长度 %d~%d 字（仅观察，不设长短比）→ 按主题、场景、说话人和信息层次核读分段；等长或不等长均可有功能，不为比例重分段" % (min(plens), max(plens)))
        if "段落开头" not in skips:
            starts = [p[:3] for p in paras]
            for st in set(starts):
                if starts.count(st) >= 3:
                    add(5, "[段落开头] '%s…' 起头的段落 × %d → 核对重复作用；必要指称、排比和有意复沓保留，不为次数变换开头" % (st, starts.count(st)))
                    break
    else:
        add(0, "[段落] 段落数 <3，跳过段落层检测")

    ord_starts = [p for p in paras if ORDINAL_START.search(p)]
    if len(ord_starts) >= 3:
        add(6, "[段首序数] %d 段以 首先/其次/最后… 起头（≥3）→ 检查是否冗余；必要流程顺序与导航保留" % len(ord_starts))

    # v0.23 信号 C：段内枚举（段中无冒号的"一是…二是…"；要求前导标点，
    # 防"统一是/唯一是"误命中；真人公文的「一、」编号不受影响）。
    # tech/academic/official 豁免（GENRE_SKIPS）：平行编号是技术规范/公文的
    # 常规结构，TECH_SPEC 的"一是…二是…三是…"即 ⑬ 的设计样本。
    enum_pat = re.compile(r"(?:^|[。；，,：:（(、])(" + "|".join(ENUM_SEG) + r")")
    enum_n = len(enum_pat.findall(body))
    if "段内枚举" not in skips and enum_n >= 2:
        add(6, "[段内枚举] 一是/二是… 式段中编号 × %d → 核对层次与阅读负担；必要编号、流程顺序和引用关系保留，不统一拆段" % enum_n)

    # v0.23 信号 D：书信礼貌框架（成对才罚，单处不计）
    if POLITE_A.search(body) and POLITE_B.search(body):
        add(6, "[礼貌框架] '首先…感谢'与'再次感谢'成对出现 → 核对是否冗余；称谓、关系、正式程度及礼仪功能保留，不按比例删减或虚构具体事项")

    anchors = len(ANCHOR_RE.findall(body))
    density = anchors / (total / 300)
    add(0, "[锚点] 正则匹配 %d 处、密度 %.1f / 300 中文字（仅观察，不设密度目标）→ 匹配数不代表真实、具体或有叙事作用；按材料与文体核读必要细节，不为密度添加或删除数字、时间、地名；数值精度与不确定性须保留" % (anchors, density))

    return issues, "ok"


def evaluate(text, genre="general", language="auto"):
    issues, status = check(text, genre, language)
    # 英文信号保留其自身权重；不得因中文 99→100 字而被乘 3。
    english_score = sum(w for w, m in issues if m.startswith(ENGLISH_ISSUE_TAGS))
    chinese_score = sum(w for w, m in issues if not m.startswith(ENGLISH_ISSUE_TAGS))
    if status == "ok" and chinese_score > 0:
        body = strip_markdown(text)
        units = chinese_len(body) + ascii_word_len(body)
        if MIXED_MIN_UNITS <= units < SCORE_NORM_CHARS:
            chinese_score = round(chinese_score * SCORE_NORM_CHARS / units)
            issues.append((0, "[短文本] 有效量 %d 单位（中文字 + ASCII 词），中文线索按 %d 单位基准归一 ×%.2f；英文线索不放大" % (
                units, SCORE_NORM_CHARS, SCORE_NORM_CHARS / units)))
    score = min(100, english_score + chinese_score)
    return issues, status, score


def label_of(score, status):
    if status == "limited":
        return "语言未确认，仅有限词表线索"
    if status == "unsupported":
        return "文字范围不支持或语言声明不匹配"
    if status != "ok":
        return "无法判定"
    if score < GOOD_LINE:
        return "静态命中较少"
    if score <= PASS_LINE:
        return "静态命中适中"
    return "静态命中较多"


def main(argv):
    as_json = False
    genre = "general"
    language = "auto"
    paths = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--help", "-h"):
            print(__doc__)
            return 0
        elif a == "--json":
            as_json = True
        elif a == "--":
            paths.extend(argv[i + 1:])
            break
        elif a == "--language":
            i += 1
            if i >= len(argv):
                print("--language 需要一个值（可选: %s）" % "/".join(LANGUAGES), file=sys.stderr)
                return 2
            language = argv[i]
        elif a == "--genre":
            i += 1
            if i >= len(argv):
                print("--genre 需要一个值（可选: %s）" % "/".join(GENRES), file=sys.stderr)
                return 2
            genre = argv[i]
        elif a.startswith("-") and a != "-":
            print("未知参数: %s（使用 --help 查看用法）" % a, file=sys.stderr)
            return 2
        else:
            paths.append(a)
        i += 1
    paths = paths or ["-"]
    if genre not in GENRES:
        print("未知 --genre: %s（可选: %s）" % (genre, "/".join(GENRES)), file=sys.stderr)
        return 2
    if language not in LANGUAGES:
        print("未知 --language: %s（可选: %s）" % (language, "/".join(LANGUAGES)), file=sys.stderr)
        return 2
    results = []
    verdict = "pass"

    for p in paths:
        try:
            text = read_text(p)
        except (OSError, UnicodeError) as exc:
            print("无法读取输入 %s: %s" % (p, exc), file=sys.stderr)
            return 2
        issues, status, score = evaluate(text, genre, language)
        results.append({
            "path": p,
            "genre": genre,
            "language": language,
            "language_is_verified": False,
            "language_interpretation": "auto不是语言识别；zh/en/mixed为调用者声明，分数未经跨语言概率校准。",
            "score": score,
            "score_kind": "static_style_heuristic",
            "ruleset_version": RULESET_VERSION,
            "is_ai_probability": False,
            "interpretation": "仅表示本规则集的加权命中；不判作者身份、文学质量或外部检测结果。",
            "status": status,
            "label": label_of(score, status),
            "issues": [{"weight": w, "message": m} for w, m in issues],
        })
        if status == "ok" and score > PASS_LINE:
            verdict = "fail"
        elif status != "ok" and verdict != "fail":
            verdict = "short"

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if r["path"] != "-":
                print("\n=== %s ===" % r["path"])
            print("静态写作线索分: %d/100  →  %s" % (r["score"], r["label"]))
            print(r["interpretation"])
            for item in r["issues"]:
                w = item["weight"]
                m = item["message"]
                print("  %s%3s  %s" % ("-" if w else " ", w if w else "", m))

    return {"fail": 1, "short": 2}.get(verdict, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
