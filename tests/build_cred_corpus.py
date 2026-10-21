import csv
import hashlib
import re
import sys
import statistics
from pathlib import Path

csv.field_size_limit(10_000_000)

REPO = Path(r"C:\Users\shiniyaya\AppData\Local\Temp\C-ReD_repo")
SRC = REPO / "benchmark data"
OUT = Path(__file__).parent / "corpus_cred"

DOMAINS = {
    "composition": "fiction",
    "film review": "general",
    "paper": "academic",
}
GEN_SHORT = {
    "claude-3.5-haiku": "claude35haiku",
    "deepseek-r1": "deepseekr1",
    "deepseek-v3": "deepseekv3",
    "doubao-1.5-pro": "doubao15pro",
    "gemini-2.5-flash": "gemini25flash",
    "gpt-3.5-turbo": "gpt35turbo",
    "gpt-4o": "gpt4o",
    "qwen-2.5": "qwen25",
    "qwen-3": "qwen3",
}
HUMAN_TARGET = 30
AI_TARGET = 10
MIN_CJK = 100

URL_RE = re.compile(r"https?://|www\.")
PHONE_RE = re.compile(r"1[3-9]\d{9}|0\d{2,3}-?\d{7,8}")


def cjk_len(t: str) -> int:
    return sum(1 for c in t if "\u4e00" <= c <= "\u9fff")


def ok_text(t: str) -> bool:
    if not t or t.strip() != t:
        pass
    s = t.strip()
    if "\ufffd" in s:
        return False
    if URL_RE.search(s) or PHONE_RE.search(s):
        return False
    if cjk_len(s) < MIN_CJK:
        return False
    return True


def dedup_key(t: str) -> str:
    return re.sub(r"\s+", "", t)[:40]


def read_rows(path: Path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            yield row


def main():
    OUT.mkdir(exist_ok=True)
    manifest = []
    stats = {}

    for domain, gate in DOMAINS.items():
        dpath = SRC / domain
        fname = domain.replace(" ", "_")
        human_path = dpath / f"CReD_{fname}_human.csv"
        humans = []
        seen = set()
        for row in read_rows(human_path):
            t = (row.get("text") or "").strip()
            if not ok_text(t):
                continue
            k = dedup_key(t)
            if k in seen:
                continue
            seen.add(k)
            humans.append((int(row["id"]), t))
        lens = sorted(cjk_len(t) for _, t in humans)
        med = lens[len(lens) // 2] if lens else 0
        lo, hi = max(MIN_CJK, int(med * 0.5)), int(med * 1.5)
        picked_h = humans[:HUMAN_TARGET]
        for i, (src_id, t) in enumerate(picked_h, 1):
            name = f"human_cred{domain.split()[0]}_{i:02d}.md"
            write_sample(name, t)
            manifest.append((name, f"{human_path.name}#id={src_id}", "human", cjk_len(t)))
        stats[domain] = {"gate": gate, "human_source_pool_n": len(humans),
                         "human_source_pool_median": statistics.median(lens) if lens else None,
                         "human_window_reference_upper_median": med, "ai_length_window": [lo, hi],
                         "human_picked": len(picked_h),
                         "human_picked_median": statistics.median(cjk_len(t) for _, t in picked_h) if picked_h else None,
                         "ai": {}, "ai_picked_medians": {}}

        ai_seen = set()
        for gen, short in GEN_SHORT.items():
            apath = dpath / f"CReD_{fname}_{gen}.csv"
            picked = []
            for row in read_rows(apath):
                t = (row.get("text") or "").strip()
                if not ok_text(t):
                    continue
                if not (lo <= cjk_len(t) <= hi):
                    continue
                k = dedup_key(t)
                if k in ai_seen:
                    continue
                ai_seen.add(k)
                picked.append((int(row["id"]), t))
                if len(picked) >= AI_TARGET:
                    break
            for i, (src_id, t) in enumerate(picked, 1):
                name = f"ai_cred{domain.split()[0]}_{short}_{i:02d}.md"
                write_sample(name, t)
                manifest.append((name, f"{apath.name}#id={src_id}", gen, cjk_len(t)))
            stats[domain]["ai"][gen] = len(picked)
            stats[domain]["ai_picked_medians"][gen] = statistics.median(cjk_len(t) for _, t in picked) if picked else None

    lines = ["| 文件 | 源 | 来源标注 | 中文字数 | sha256 |", "|---|---|---|---|---|"]
    for name, src, gen, n in manifest:
        p = OUT / name
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"| {name} | {src} | {gen} | {n} | {h} |")
    (OUT / "MANIFEST.md").write_text(
        "# corpus_cred 抽样清单\n\n抽样脚本：tests/build_cred_corpus.py（确定性协议，见 SOURCES.md）\n\n"
        + "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("MEDIAN/BOUNDS/PICKED per domain:")
    for d, s in stats.items():
        print(f"  {d}: source_pool_n={s['human_source_pool_n']} source_pool_median={s['human_source_pool_median']}"
              f" window_reference_upper_median={s['human_window_reference_upper_median']}"
              f" ai_window={s['ai_length_window']} picked_human={s['human_picked']} picked_human_median={s['human_picked_median']}")
        for g, n in s["ai"].items():
            print(f"    {g}: n={n} picked_median={s['ai_picked_medians'][g]}")
    total = len(manifest)
    print(f"TOTAL FILES: {total}")


def write_sample(name: str, text: str):
    with open(OUT / name, "w", encoding="utf-8", newline="") as f:
        f.write(text.strip() + "\n")


if __name__ == "__main__":
    main()
