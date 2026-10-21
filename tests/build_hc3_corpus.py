# -*- coding: utf-8 -*-
"""从 HC3-Chinese 重建 tests/corpus_hc3/ 第三方语料（确定性、可复现）。

用法：
    python tests/build_hc3_corpus.py            # 下载（若缺）+ 重建样本
    python tests/build_hc3_corpus.py --raw DIR  # 指定源 jsonl 所在目录

来源与协议见 tests/corpus_hc3/SOURCES.md。
本脚本只做"取样本 + 清洗"，不改任何被抽文本的措辞（除剔除 URL/电话等隐私信息）。
"""
import argparse
import hashlib
import json
import pathlib
import re
import ssl
import tempfile
import urllib.parse
import urllib.request

BASE = "https://www.modelscope.cn/api/v1/datasets/simpleai/HC3-Chinese"
DEST = pathlib.Path(__file__).resolve().parent / "corpus_hc3"
UA = {"User-Agent": "Mozilla/5.0"}

SRC_SHA = {
    "law.jsonl": "03993cd7d9e1c1e277927f599760c85083d928f65cec7d9c99cc3641b557309c",
    "baike.jsonl": "04eb6995caef39b32afe05e369de49ae6ad1ddded973f31e3f91be938a0c9d5c",
}

# (输出前缀, 源文件, 字段, 区间下限, 区间上限, 篇数)
PLAN = [
    ("ai_hc3law_long_%02d.md", "law.jsonl", "chatgpt_answers", 200, 300, 12),
    ("ai_hc3law_m_%02d.md", "law.jsonl", "chatgpt_answers", 100, 199, 12),
    ("human_hc3law_%02d.md", "law.jsonl", "human_answers", 100, 199, 12),
    ("ai_hc3baike_%02d.md", "baike.jsonl", "chatgpt_answers", 200, 300, 12),
    ("human_hc3baike_%02d.md", "baike.jsonl", "human_answers", 200, 300, 12),
]


def cn_len(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s or ""))


def clean(s):
    """只做必要的清洗：隐私剔除 + 空白规整。不改写措辞。"""
    s = s.replace("\r\n", "\n").strip()
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"www\.\S+", "", s)
    s = re.sub(r"1[3-9]\d{9}", "", s)
    s = re.sub(r"0\d{2,3}-?\d{7,8}", "", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def fetch(name, raw_dir):
    p = raw_dir / name
    if p.exists():
        return p.read_bytes()
    url = BASE + "/repo?Revision=master&FilePath=" + urllib.parse.quote(name)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=180, context=ctx).read()
    p.write_bytes(data)
    return data


def verify_source(name, data):
    """Require the complete registered SHA-256 before using source bytes."""
    expected = SRC_SHA.get(name)
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("No valid registered SHA-256 for HC3 source %s" % name)
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise ValueError(
            "HC3 source SHA-256 mismatch for %s: expected %s; got %s. "
            "Corpus not written." % (name, expected, actual)
        )
    return actual


def pick(answers, lo, hi, n):
    seen, out = set(), []
    for a in answers:
        t = clean(a)
        if not (lo <= cn_len(t) <= hi):
            continue
        key = t[:40]
        if key in seen:
            continue
        seen.add(key)
        out.append(t)
        if len(out) >= n:
            break
    return out


def build(raw_dir, dest):
    """Validate every source before creating or writing the corpus directory."""
    cache = {}
    for fname in sorted({p[1] for p in PLAN}):
        data = fetch(fname, raw_dir)
        sha = verify_source(fname, data)
        # Parse the exact bytes whose digest passed, not a second file read.
        recs = [json.loads(l) for l in data.decode("utf-8").splitlines() if l.strip()]
        cache[fname] = recs
        print("%-14s %9d B  sha256=%s  rows=%d" % (fname, len(data), sha, len(recs)))

    dest.mkdir(parents=True, exist_ok=True)
    total = 0
    for pattern, fname, field, lo, hi, n in PLAN:
        answers = [a for r in cache[fname] for a in (r.get(field) or [])]
        got = pick(answers, lo, hi, n)
        for i, t in enumerate(got, 1):
            (dest / (pattern % i)).write_text(t + "\n", encoding="utf-8", newline="\n")
        total += len(got)
        print("%-26s %2d 篇（%d-%d 字）" % (pattern % 0, len(got), lo, hi))
    print("\n共写入 %d 篇到 %s" % (total, dest))
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--raw",
        default=str(pathlib.Path(tempfile.gettempdir()) / "hc3_raw"),
        help="源 jsonl 缓存目录（默认放系统临时目录，避免把数 MB 原始语料写进技能树）",
    )
    args = ap.parse_args()
    raw_dir = pathlib.Path(args.raw)
    raw_dir.mkdir(parents=True, exist_ok=True)
    try:
        build(raw_dir, DEST)
    except ValueError as exc:
        ap.error(str(exc))


if __name__ == "__main__":
    main()
