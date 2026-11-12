# -*- coding: utf-8 -*-
"""corpus_build.py — 构建 corpora/ 冻结语料（humanize-writing skill v0.60）

用法：
    python -B scripts/corpus_build.py --hc3 /path/to/all.jsonl
    python -B scripts/corpus_build.py --hc3 /path/to/all.jsonl --full   # 含心理/医学域
    python -B scripts/corpus_build.py --download                        # 从 ModelScope 拉取

设计原则：
1. 只做“取样 + 清洗 + 切分”，不改写任何被抽文本的措辞（除剔除 URL/电话/邮箱等隐私串）。
2. 不保存上游 prompt（question）字段：配对关系由同一行记录保证，prompt 原文不随包分发。
3. 默认排除 psychology / medicine 两个含个人健康披露的域；--full 才纳入。
4. 按 pair id 哈希切分 train/cal/test，同一 pair 不会跨切分，避免同题泄漏。
5. 每个输出文件写 sha256 到 manifest.json，便于复现与校验。
"""

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "corpora")
PAIR_DIR = os.path.join(OUT_DIR, "pairs")

SOURCE_URL = "https://www.modelscope.cn/api/v1/datasets/simpleai/HC3-Chinese"
HF_URL = "https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese"
LICENSE = "CC BY-SA 4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
PAPER = "https://arxiv.org/abs/2301.07597"

# 上游 all.jsonl 的 sha256（2026-11-12 下载核对）
EXPECTED_SHA256 = "425e7071bbd5dd88efd85d51e28a5adec9c72e04d96c52d194bdfb95fef00b0d"
DOWNLOAD_CANDIDATES = [
    "https://www.modelscope.cn/api/v1/datasets/simpleai/HC3-Chinese/repo?Revision=master&FilePath=all.jsonl",
    "https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese/resolve/main/all.jsonl",
]

STATUS = {"train": 0.70, "cal": 0.15, "test": 0.15}

MIN_CJK = 80
MAX_CHARS = 1200

# 个人健康 / 高风险内容过滤（保守，命中任一词即跳过整对）
RISK_WORDS = (
    "自杀", "自残", "轻生", "遗书", "抑郁", "焦虑症", "精神分裂",
    "色情", "裸照", "性行为", "强奸", "猥亵", "约炮",
    "吸毒", "毒品", "赌博", "博彩", "杀人", "凶杀", "虐童",
)

URL_RE = re.compile(r"(?:https?://|www\.)\S+")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
PHONE_RE = re.compile(r"1[3-9]\d{9}|0\d{2,3}-?\d{7,8}")
SPACE_RE = re.compile(r"[ \t\u3000]+")
MULTI_NL_RE = re.compile(r"\n{3,}")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cjk_len(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text or ""))


def clean(text):
    """去掉隐私串与版式噪声，保留措辞与标点。"""
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    t = URL_RE.sub("", t)
    t = EMAIL_RE.sub("", t)
    t = PHONE_RE.sub("", t)
    t = t.replace("\ufffd", "")
    t = SPACE_RE.sub(" ", t)
    t = MULTI_NL_RE.sub("\n\n", t)
    lines = [ln.strip() for ln in t.split("\n")]
    t = "\n".join(lines).strip()
    return t


def truncate(text, limit=MAX_CHARS):
    """按句末标点截断，避免半句；找不到就硬截。"""
    if cjk_len(text) <= limit:
        return text
    marks = "。！？…"
    cut = 0
    count = 0
    for i, ch in enumerate(text):
        if re.match(r"[\u4e00-\u9fff]", ch):
            count += 1
        if count >= limit and ch in marks:
            cut = i + 1
            break
    return text[:cut] if cut else text[: limit + 40]


def has_risk(text):
    return any(w in text for w in RISK_WORDS)


def acceptable(text):
    if cjk_len(text) < MIN_CJK:
        return False
    if has_risk(text):
        return False
    if text.count("```") or "<html" in text.lower():
        return False
    return True


def read_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build(rows, full=False):
    pairs = []
    seen = set()
    skipped = {"short": 0, "risk": 0, "dup": 0, "domain": 0}
    allow = {"baike", "open_qa", "finance", "law", "nlpcc_dbqa"}
    if full:
        allow |= {"psychology", "medicine"}
    for idx, r in enumerate(rows):
        domain = (r.get("source") or "").strip()
        if domain not in allow:
            skipped["domain"] += 1
            continue
        humans = [clean(a) for a in (r.get("human_answers") or []) if a]
        ais = [clean(a) for a in (r.get("chatgpt_answers") or []) if a]
        humans = [a for a in humans if acceptable(a)]
        ais = [a for a in ais if acceptable(a)]
        if not humans or not ais:
            skipped["short"] += 1
            continue
        human = truncate(max(humans, key=cjk_len))
        ai = truncate(max(ais, key=cjk_len))
        if has_risk(human) or has_risk(ai):
            skipped["risk"] += 1
            continue
        key = sha256_text(human)[:16]
        if key in seen:
            skipped["dup"] += 1
            continue
        seen.add(key)
        pair_id = "hc3-" + sha256_text((r.get("question") or "") + domain)[:12]
        pairs.append({
            "id": pair_id,
            "domain": domain,
            "human": human,
            "ai": ai,
            "human_len": cjk_len(human),
            "ai_len": cjk_len(ai),
            "source": "HC3-Chinese",
            "license": LICENSE,
        })
    # 同一 id 去重（同题只留一条）
    by_id = {}
    for p in pairs:
        by_id.setdefault(p["id"], p)
    pairs = list(by_id.values())
    return pairs, skipped


def split(pairs):
    buckets = {k: [] for k in STATUS}
    limits = {"train": STATUS["train"], "cal": STATUS["train"] + STATUS["cal"]}
    for p in sorted(pairs, key=lambda x: x["id"]):
        h = int(hashlib.sha256(p["id"].encode()).hexdigest(), 16) % 1000 / 1000.0
        if h < limits["train"]:
            buckets["train"].append(p)
        elif h < limits["cal"]:
            buckets["cal"].append(p)
        else:
            buckets["test"].append(p)
    return buckets


def write_jsonl(path, items):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def download(dest):
    ctx = ssl.create_default_context()
    last = None
    for url in DOWNLOAD_CANDIDATES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120, context=ctx) as r, open(dest, "wb") as f:
                f.write(r.read())
            size = os.path.getsize(dest)
            if size > 1_000_000:
                return url, size
            last = "文件过小: %d 字节" % size
        except Exception as e:  # 网络失败时尝试下一个镜像
            last = "%s: %s" % (url, e)
    raise SystemExit("下载失败（%s）。请手动下载 all.jsonl 后用 --hc3 指定路径。" % last)


def main(argv=None):
    ap = argparse.ArgumentParser(description="构建 corpora/ 冻结语料")
    ap.add_argument("--hc3", help="HC3-Chinese all.jsonl 路径")
    ap.add_argument("--download", action="store_true", help="从 ModelScope/HuggingFace 拉取")
    ap.add_argument("--full", action="store_true", help="包含 psychology / medicine 域")
    ap.add_argument("--out", default=OUT_DIR, help="输出目录")
    args = ap.parse_args(argv)

    path = args.hc3
    if args.download and not path:
        # Windows 没有 /tmp；用系统临时目录，避免在盘根创建不可写路径
        path = os.path.join(tempfile.gettempdir(), "hc3_zh_all.jsonl")
        url, size = download(path)
        print("已下载 %s（%d 字节）" % (url, size))
    if not path or not os.path.isfile(path):
        raise SystemExit("缺少 HC3 源文件：用 --hc3 指定，或加 --download")

    src_sha = sha256_file(path)
    rows = read_rows(path)
    pairs, skipped = build(rows, full=args.full)
    if len(pairs) < 300:
        raise SystemExit("可用配对仅 %d 条，检查源文件或过滤条件" % len(pairs))

    buckets = split(pairs)
    os.makedirs(PAIR_DIR, exist_ok=True)
    files = {}
    for name, items in buckets.items():
        out = os.path.join(PAIR_DIR, "hc3_%s.jsonl" % name)
        write_jsonl(out, items)
        files[name] = {
            "path": os.path.relpath(out, ROOT).replace(os.sep, "/"),
            "pairs": len(items),
            "sha256": sha256_file(out),
        }

    domains = {}
    for name, items in buckets.items():
        for p in items:
            domains.setdefault(name, {}).setdefault(p["domain"], 0)
            domains[name][p["domain"]] += 1

    manifest = {
        "version": "0.60",
        "built": "2026-11-12",
        "source": {
            "name": "HC3-Chinese (Human ChatGPT Comparison Corpus, 中文版)",
            "url": HF_URL,
            "mirror": SOURCE_URL,
            "paper": PAPER,
            "license": LICENSE,
            "license_url": LICENSE_URL,
            "upstream_sha256": src_sha,
            "expected_sha256": EXPECTED_SHA256,
            "sha_matches_expected": src_sha == EXPECTED_SHA256,
        },
        "fields": ["id", "domain", "human", "ai", "human_len", "ai_len", "source", "license"],
        "note": "上游 prompt（question）未随包分发；同一 id 的人类/AI 回答来自同一 prompt。",
        "filters": {
            "min_cjk": MIN_CJK,
            "max_cjk": MAX_CHARS,
            "domains_included": sorted({p["domain"] for p in pairs}),
            "excluded_domains": [] if args.full else ["psychology", "medicine"],
            "risk_words": list(RISK_WORDS),
            "privacy_stripped": ["URL", "email", "phone"],
            "skipped": skipped,
        },
        "totals": {"pairs": len(pairs)},
        "splits": files,
        "split_rule": "sha256(id) 取模 1000 → 700/150/150，同 id 不跨切分",
        "domain_counts": domains,
    }
    with open(os.path.join(OUT_DIR, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("源文件 sha256: %s（与登记值一致: %s）" % (src_sha, manifest["source"]["sha_matches_expected"]))
    print("可用配对 %d；跳过 %s" % (len(pairs), skipped))
    for name in ("train", "cal", "test"):
        print("  %-5s %4d 对  %s" % (name, files[name]["pairs"], files[name]["sha256"][:12]))
    print("域分布: %s" % json.dumps(domains, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
