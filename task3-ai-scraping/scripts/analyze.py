"""
analyze.py
----------
Turn the 100 retrieved JSON files into statistics.

Required by the task:
    - number of files
    - words per file
    - brands mentioned per file
    - product features mentioned per file

Value-add layer (the research contribution):
    - brand recommendation HHI per prompt (concentration of what the model pushes)
    - cross-occasion stability per prompt (mean pairwise Jaccard of brand sets)
    - top brands by mention frequency across all prompts

Brand/feature counting method:
    Primary  = structured extraction via the Claude API into a fixed schema
               {"brands": [...], "features": [...]}, deduplicated within file.
    Baseline = a rule-based check (spaCy ORG/PRODUCT entities plus a feature
               lexicon) intended for a 10-file validation sample. Enable with
               --baseline. Kept separate so the primary numbers stay clean.

Outputs:
    output/stats.csv      one row per file
    output/summary.json   aggregates

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python analyze.py
    python analyze.py --baseline    # also run the rule-based sample check
"""

import argparse
import csv
import itertools
import json
from collections import Counter
from pathlib import Path

from anthropic import Anthropic

MODEL = "claude-sonnet-5"        # any current model; extraction is easy
EXTRACT_MAX_TOKENS = 600

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "output"

EXTRACT_SYSTEM = (
    "You extract structured data from a shopping assistant's reply. "
    "Return ONLY minified JSON, no prose, no code fences, in the exact shape "
    '{"brands": [], "features": []}. '
    '"brands" is the list of distinct brand or product names named in the reply '
    '(for example "Dyson V15", "Ninja", "iPhone 16 Pro"). '
    '"features" is the list of distinct product features or attributes discussed '
    '(for example "battery life", "noise level", "screen size", "price"). '
    "Deduplicate. If none, return empty lists."
)


def load_records():
    """Load every response JSON under output/occasion_*/ ."""
    records = []
    for occ_dir in sorted(OUTPUT_ROOT.glob("occasion_*")):
        for path in sorted(occ_dir.glob("prompt_*.json")):
            with open(path, "r", encoding="utf-8") as f:
                rec = json.load(f)
                rec["_path"] = str(path.relative_to(ROOT))
                records.append(rec)
    return records


def word_count(text):
    return len(text.split())


def extract_brands_features(client, response_text):
    """Structured extraction pass. Returns (brands, features) as deduped lists."""
    resp = client.messages.create(
    model=MODEL,
    max_tokens=EXTRACT_MAX_TOKENS,
    system=EXTRACT_SYSTEM,
    messages=[{"role": "user", "content": response_text}],
)
    raw = "".join(b.text for b in resp.content if b.type == "text").strip()
    # strip stray fences if the model adds them
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[raw.find("{"):]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return [], []
    dedup = lambda xs: sorted({x.strip().lower() for x in xs if x and x.strip()})
    return dedup(data.get("brands", [])), dedup(data.get("features", []))


def hhi(counter):
    """Herfindahl-Hirschman Index of a Counter of mention shares, 0..10000."""
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return round(sum((c / total * 100) ** 2 for c in counter.values()), 1)


def mean_pairwise_jaccard(sets):
    """Mean Jaccard overlap across all pairs of brand sets (stability)."""
    pairs = list(itertools.combinations(sets, 2))
    if not pairs:
        return None
    vals = []
    for a, b in pairs:
        union = a | b
        vals.append(len(a & b) / len(union) if union else 1.0)
    return round(sum(vals) / len(vals), 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", action="store_true", help="Run rule-based sample check")
    args = ap.parse_args()

    client = Anthropic()
    records = load_records()
    print(f"Loaded {len(records)} response files.")

    rows = []
    brand_sets_by_prompt = {}   # prompt_id -> list of brand sets (one per occasion)
    brand_counts_by_prompt = {} # prompt_id -> Counter of brand mentions
    all_brand_counts = Counter()

    for rec in records:
        brands, features = extract_brands_features(client, rec["response_text"])
        rows.append({
            "path": rec["_path"],
            "prompt_id": rec["prompt_id"],
            "occasion": rec["occasion"],
            "category": rec["category"],
            "archetype": rec["archetype"],
            "timestamp_utc": rec["timestamp_utc"],
            "word_count": word_count(rec["response_text"]),
            "brand_count": len(brands),
            "feature_count": len(features),
            "brands": "; ".join(brands),
            "features": "; ".join(features),
        })
        pid = rec["prompt_id"]
        brand_sets_by_prompt.setdefault(pid, []).append(set(brands))
        c = brand_counts_by_prompt.setdefault(pid, Counter())
        c.update(brands)
        all_brand_counts.update(brands)
        print(f"  {rec['_path']}: {len(brands)} brands, {len(features)} features")

    # per-file stats
    stats_path = OUTPUT_ROOT / "stats.csv"
    with open(stats_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {stats_path.relative_to(ROOT)}")

    # aggregates
    per_prompt = {}
    for pid, counter in brand_counts_by_prompt.items():
        per_prompt[pid] = {
            "brand_hhi": hhi(counter),
            "brand_stability_jaccard": mean_pairwise_jaccard(brand_sets_by_prompt[pid]),
            "distinct_brands_pooled": len(counter),
            "top_brands": counter.most_common(5),
        }

    word_counts = [r["word_count"] for r in rows]
    summary = {
        "file_count": len(rows),
        "word_count_mean": round(sum(word_counts) / len(word_counts), 1),
        "word_count_min": min(word_counts),
        "word_count_max": max(word_counts),
        "brand_count_mean": round(sum(r["brand_count"] for r in rows) / len(rows), 2),
        "feature_count_mean": round(sum(r["feature_count"] for r in rows) / len(rows), 2),
        "top_brands_overall": all_brand_counts.most_common(15),
        "per_prompt": per_prompt,
    }
    summary_path = OUTPUT_ROOT / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Wrote {summary_path.relative_to(ROOT)}")

    if args.baseline:
        run_baseline_sample(records[:10])


def run_baseline_sample(sample):
    """
    Rule-based validation on a small sample, for the README's method note.
    Uses spaCy ORG/PRODUCT entities as a brand proxy and a small feature
    lexicon. This is a cross-check on the primary extraction, not the
    reported numbers. Requires: pip install spacy && python -m spacy download en_core_web_sm
    """
    try:
        import spacy
    except ImportError:
        print("Baseline skipped: spaCy not installed.")
        return
    nlp = spacy.load("en_core_web_sm")
    feature_lexicon = {
        "battery", "battery life", "screen", "screen size", "camera", "price",
        "weight", "noise", "storage", "warranty", "durability", "comfort",
    }
    print("\nRule-based baseline on a 10-file sample:")
    for rec in sample:
        doc = nlp(rec["response_text"])
        brands = {e.text.lower() for e in doc.ents if e.label_ in ("ORG", "PRODUCT")}
        feats = {t for t in feature_lexicon if t in rec["response_text"].lower()}
        print(f"  {rec['prompt_id']} occ {rec['occasion']}: "
              f"{len(brands)} brand-proxy, {len(feats)} feature-proxy")


if __name__ == "__main__":
    main()
