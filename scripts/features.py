# -*- coding: utf-8 -*-
"""features.py — 可解释写作特征层（humanize-writing skill v0.60）

只依赖 Python 标准库。每个特征都在 FEATURE_SPECS 中登记：
名称、中文标签、取值方式、先验方向、外部证据编号、本项目实测结果（由
scripts/evidence_measure.py 写入 references/feature-evidence.json）。

边界：
- 特征是"文本表面可测的量"，不是作者身份指纹，也不是某个厂商检测器的内部权重。
- 方向先验只表示"多数公开研究中的倾向"，单篇文本出现相反取值完全正常。
- 任何特征都不能单独用于判断作者；组合模型的结果见 scripts/ai_rate.py 的校准报告。
"""

import math
import re
import statistics
import unicodedata

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
SENT_SPLIT_RE = re.compile(r"[。！？!?；;…]+|\n{2,}")
PARA_SPLIT_RE = re.compile(r"\n\s*\n|\n")
LATIN_RE = re.compile(r"[A-Za-z]")
DIGIT_RE = re.compile(r"\d")
LIST_MARK_RE = re.compile(
    r"(?m)^\s*(?:\d+[.、]|[一二三四五六七八九十]+[、.]|[-*•·])\s*"
)

PUNCT_CHARS = "，。！？；：、（）《》〈〉「」『』—…·,.!?;:()<>-\"'"

# 连接词：只用于测量"显性衔接"，不代表用了就不好
CONNECTIVES = (
    "然而", "因此", "此外", "首先", "其次", "最后", "总之", "综上",
    "与此同时", "值得注意的是", "需要指出", "换句话说", "具体而言",
    "总体而言", "另一方面", "一方面", "由此可见",
)

# 套话/程式化短语：测量密度，不构成改写理由
STOCK_PHRASES = (
    "综上所述", "总而言之", "总的来说", "需要注意的是", "值得一提的是",
    "不可否认", "毋庸置疑", "在当今", "随着", "不仅", "而且", "更是",
    "赋能", "抓手", "闭环", "顶层设计", "深度融合", "持续优化",
    "全面提升", "至关重要", "不可或缺", "在一定程度上", "从某种意义上说",
    "这意味着", "这表明", "由此可见",
)

SUMMARY_MARKERS = ("综上", "总之", "总而言之", "由此可见", "总的来说")

FIRST_PERSON = ("我", "我们", "咱", "笔者")
SECOND_PERSON = ("你", "您", "你们")

# 每个特征：name -> 说明。direction 为 +1 表示公开研究中 AI 侧常更高，-1 表示常更低，
# 0 表示方向不稳或跨域相反。evidence 为 references/detection-evidence.md 中的来源编号。
FEATURE_SPECS = {
    "sent_len_mean": {
        "label": "平均句长（汉字/句）",
        "direction": 1,
        "evidence": ["2606.04177", "2507.00838"],
        "note": "跨域方向不稳；长句既可能来自 AI 的完整表述，也可能是人写的复杂句。",
    },
    "sent_len_sd": {
        "label": "句长标准差",
        "direction": 1,
        "evidence": ["2507.00838"],
        "note": "经典 burstiness 代理量，但只在一部分语料上成立。",
    },
    "sent_len_cv": {
        "label": "句长变异系数（SD/均值）",
        "direction": 1,
        "evidence": ["2507.00838"],
        "note": "去掉平均句长影响后的相对参差度。",
    },
    "sent_len_entropy": {
        "label": "句长分布熵（6 档）",
        "direction": 1,
        "evidence": ["2507.00838"],
        "note": "分布越均匀，熵越低；与本项目实测方向未必一致。",
    },
    "short_sent_ratio": {
        "label": "短句占比（<12 字）",
        "direction": 1,
        "evidence": ["2507.00838"],
        "note": "口语与叙事中短句天然多，不能当作人写标志。",
    },
    "long_sent_ratio": {
        "label": "长句占比（>45 字）",
        "direction": 1,
        "evidence": ["2606.04177"],
        "note": "长句常与信息密度、复句层次相关，需按文体核读。",
    },
    "comma_per_sent": {
        "label": "每句逗号数",
        "direction": 1,
        "evidence": ["2606.04177"],
        "note": "标点密度是排版习惯，受文体与平台影响很大。",
    },
    "enum_comma_per_1000": {
        "label": "顿号密度（每千汉字）",
        "direction": -1,
        "evidence": ["2606.04177"],
        "note": "并列名词清单的排版习惯；中文正式文本常用。",
    },
    "dash_per_1000": {
        "label": "破折号密度（每千汉字）",
        "direction": 0,
        "evidence": ["2601.07974"],
        "note": "不同模型方向相反，不设目标值。",
    },
    "quote_per_100": {
        "label": "引号密度（每百汉字）",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "对话、引文、强调都会改变该值，不能反推来源。",
    },
    "question_per_100": {
        "label": "问号密度（每百汉字）",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "设问是常见修辞，非来源标志。",
    },
    "exclaim_per_100": {
        "label": "感叹号密度（每百汉字）",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "与语气、平台规范相关。",
    },
    "colon_per_100": {
        "label": "冒号密度（每百汉字）",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "清单式表达常用，但正式文体同样高频。",
    },
    "punct_ratio": {
        "label": "标点占全部字符比例",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "受断句习惯与平台排版影响。",
    },
    "para_len_mean": {
        "label": "平均段长（汉字/段）",
        "direction": 0,
        "evidence": ["2601.07974"],
        "note": "本项目实测在部分领域方向相反，仅作诊断。",
    },
    "para_len_sd": {
        "label": "段长标准差",
        "direction": 0,
        "evidence": ["2601.07974"],
        "note": "同上。",
    },
    "connective_per_1000": {
        "label": "显性连接词密度（每千汉字）",
        "direction": -1,
        "evidence": ["2606.04177", "2602.15514"],
        "note": "学术写作的衔接需要；本项目在问答语料上方向与直觉相反。",
    },
    "stock_phrase_per_1000": {
        "label": "套话密度（每千汉字）",
        "direction": 1,
        "evidence": ["2406.07016"],
        "note": "超额词研究支持词表方向，但单词单次命中不足以判定。",
    },
    "de_per_1000": {
        "label": "「的」密度（每千汉字）",
        "direction": 0,
        "evidence": ["2506.13013"],
        "note": "功能词分布是文体学常用量，跨语料方向不稳。",
    },
    "particle_per_1000": {
        "label": "体貌助词密度（了/着/过/地/得，每千汉字）",
        "direction": 0,
        "evidence": ["2604.22142"],
        "note": "LLM 改写常减少口语助词，但正式文体本就少。",
    },
    "first_person_per_1000": {
        "label": "第一人称密度（每千汉字）",
        "direction": 0,
        "evidence": ["2604.22142"],
        "note": "第一人称减少是“声音被规范化”的已知迹象之一，但文体差异极大。",
    },
    "second_person_per_1000": {
        "label": "第二人称密度（每千汉字）",
        "direction": 0,
        "evidence": ["2604.22142"],
        "note": "同上。",
    },
    "number_per_1000": {
        "label": "阿拉伯数字密度（每千汉字）",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "数据型文本天然高；不能把数字多当作人写。",
    },
    "char_ttr": {
        "label": "汉字型例比（不同字/总字）",
        "direction": 1,
        "evidence": ["2606.04177", "2507.00838"],
        "note": "词汇丰富度是跨模型、跨领域较稳的信号之一。",
    },
    "bigram_ttr": {
        "label": "二元组型例比",
        "direction": 1,
        "evidence": ["2606.04177"],
        "note": "与重复度互补，短文本波动大。",
    },
    "hapax_ratio": {
        "label": "仅出现一次的汉字占比",
        "direction": 1,
        "evidence": ["2606.04177"],
        "note": "词汇丰富度的另一种量法。",
    },
    "repeat_bigram_ratio": {
        "label": "重复二元组占比",
        "direction": -1,
        "evidence": ["2606.04177"],
        "note": "越高表示局部重复越多；模板化文本常偏高。",
    },
    "latin_ratio": {
        "label": "拉丁字母占比",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "技术文本天然高；不代表来源。",
    },
    "list_marker_per_1000": {
        "label": "行首编号/项目符号密度（每千汉字）",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "清单化是体裁特征，本项目实测与 AI 侧无稳定关系。",
    },
    "summary_marker_per_1000": {
        "label": "总结路标密度（每千汉字）",
        "direction": 0,
        "evidence": ["2606.04177"],
        "note": "一次收束是正常功能；重复总结才值得核读。",
    },
    "para_start_repeat": {
        "label": "段首重复率（最高频两字开头占比）",
        "direction": 0,
        "evidence": ["2601.07974"],
        "note": "排比、指称、章节体都可能导致高重复。",
    },
}

FEATURE_NAMES = list(FEATURE_SPECS.keys())


def cjk_count(text):
    """统计汉字个数（不含标点、字母、数字）。"""
    return len(CJK_RE.findall(text or ""))


def text_units(text):
    """有效计量单位：汉字 + ASCII 词形。与 lint 的口径保持一致。"""
    body = text or ""
    words = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", body))
    return cjk_count(body), words


def sentences(text):
    parts = [p.strip() for p in SENT_SPLIT_RE.split(text or "") if p.strip()]
    return parts or ([text.strip()] if text and text.strip() else [])


def paragraphs(text):
    return [p.strip() for p in PARA_SPLIT_RE.split(text or "") if p.strip()]


def _per_1000(n, chars):
    return round(n * 1000.0 / max(chars, 1), 3)


def _per_100(n, chars):
    return round(n * 100.0 / max(chars, 1), 3)


def _entropy(counts):
    total = sum(counts)
    if not total:
        return 0.0
    p = [c / total for c in counts if c]
    return round(-sum(x * math.log2(x) for x in p), 3)


def extract(text):
    """返回 FEATURE_NAMES 顺序的字典。空文本返回全 0（调用方应先判长度）。"""
    text = unicodedata.normalize("NFC", text or "")
    chars = cjk_count(text)
    sents = sentences(text)
    paras = paragraphs(text)
    sl = [cjk_count(s) for s in sents] or [0]
    pl = [cjk_count(p) for p in paras] or [0]

    mean = statistics.mean(sl)
    sd = statistics.pstdev(sl) if len(sl) > 1 else 0.0
    denom = max(chars, 1)

    bg = [
        text[i:i + 2]
        for i in range(len(text) - 1)
        if CJK_RE.match(text[i]) and CJK_RE.match(text[i + 1])
    ]

    buckets = [0] * 6
    for x in sl:
        if x < 10:
            buckets[0] += 1
        elif x < 20:
            buckets[1] += 1
        elif x < 30:
            buckets[2] += 1
        elif x < 45:
            buckets[3] += 1
        elif x < 70:
            buckets[4] += 1
        else:
            buckets[5] += 1

    starts = [p[:2] for p in paras if len(p) >= 2]
    start_repeat = 0.0
    if starts:
        start_repeat = max(starts.count(s) for s in set(starts)) / float(len(starts))

    return {
        "sent_len_mean": round(mean, 2),
        "sent_len_sd": round(sd, 2),
        "sent_len_cv": round(sd / mean, 3) if mean else 0.0,
        "sent_len_entropy": _entropy(buckets),
        "short_sent_ratio": round(sum(1 for x in sl if x < 12) / len(sl), 3),
        "long_sent_ratio": round(sum(1 for x in sl if x > 45) / len(sl), 3),
        "comma_per_sent": round(text.count("，") / len(sl), 2),
        "enum_comma_per_1000": _per_1000(text.count("、"), chars),
        "dash_per_1000": _per_1000(text.count("——"), chars),
        "quote_per_100": _per_100(
            text.count("“") + text.count("”") + text.count("「") + text.count("」"), chars
        ),
        "question_per_100": _per_100(text.count("？"), chars),
        "exclaim_per_100": _per_100(text.count("！"), chars),
        "colon_per_100": _per_100(text.count("："), chars),
        "punct_ratio": round(sum(text.count(c) for c in PUNCT_CHARS) / max(len(text), 1), 3),
        "para_len_mean": round(statistics.mean(pl), 1),
        "para_len_sd": round(statistics.pstdev(pl) if len(pl) > 1 else 0.0, 1),
        "connective_per_1000": _per_1000(sum(text.count(w) for w in CONNECTIVES), chars),
        "stock_phrase_per_1000": _per_1000(sum(text.count(w) for w in STOCK_PHRASES), chars),
        "de_per_1000": _per_1000(text.count("的"), chars),
        "particle_per_1000": _per_1000(sum(text.count(w) for w in "了着过地得"), chars),
        "first_person_per_1000": _per_1000(sum(text.count(w) for w in FIRST_PERSON), chars),
        "second_person_per_1000": _per_1000(sum(text.count(w) for w in SECOND_PERSON), chars),
        "number_per_1000": _per_1000(len(DIGIT_RE.findall(text)), chars),
        "char_ttr": round(len(set(CJK_RE.findall(text))) / denom, 3),
        "bigram_ttr": round(len(set(bg)) / max(len(bg), 1), 3),
        "hapax_ratio": round(
            sum(1 for c in set(CJK_RE.findall(text)) if text.count(c) == 1) / denom, 3
        ),
        "repeat_bigram_ratio": round((len(bg) - len(set(bg))) / max(len(bg), 1), 3),
        "latin_ratio": round(len(LATIN_RE.findall(text)) / max(len(text), 1), 3),
        "list_marker_per_1000": _per_1000(len(LIST_MARK_RE.findall(text)), chars),
        "summary_marker_per_1000": _per_1000(sum(text.count(w) for w in SUMMARY_MARKERS), chars),
        "para_start_repeat": round(start_repeat, 3),
    }


def vector(text):
    """按 FEATURE_NAMES 顺序返回数值列表。"""
    f = extract(text)
    return [float(f[k]) for k in FEATURE_NAMES]


def windows(text, size=320, min_size=120, max_windows=8):
    """把长文本切成约 size 汉字的窗口，按句末标点收口。

    返回 [(起始汉字偏移, 文本)]。少于 min_size 汉字的尾窗并入前一窗。
    这是测量口径，不是文本质量判断：长文只有一个整体分时无法反映段落差异。
    """
    sents = sentences(text)
    if not sents:
        return []
    out = []
    buf = ""
    buf_len = 0
    offset = 0
    for s in sents:
        n = cjk_count(s)
        if buf_len and buf_len + n > size:
            out.append((offset, buf.strip()))
            offset += buf_len
            buf = ""
            buf_len = 0
        buf += s + "。"
        buf_len += n
    if buf.strip():
        if buf_len < min_size and out:
            out[-1] = (out[-1][0], out[-1][1] + buf.strip())
        else:
            out.append((offset, buf.strip()))
    if len(out) > max_windows:
        # 等距取样，保证首尾都在
        step = (len(out) - 1) / float(max_windows - 1)
        out = [out[int(round(i * step))] for i in range(max_windows)]
    return out
