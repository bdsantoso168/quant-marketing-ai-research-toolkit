"""
retrieve.py
-----------
Pull AI shopping responses for one occasion.

Each invocation sends all 10 prompts once, at temperature 1.0, with no tools,
and writes one self-describing JSON file per prompt into output/occasion_{r}/.

Design choice: one occasion per invocation. This makes the 10-hour run
resumable. If hour 6 fails, rerun only occasion 6. A scheduler (cron or the
driver at the bottom of this file) fires this script 10 times, once per hour.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python retrieve.py --occasion 0
    python retrieve.py --occasion 0 --dry-run     # one call, no files written

Requires: anthropic  (see requirements.txt)
"""

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

from anthropic import Anthropic

# Set the current model string. Check docs.claude.com for the latest.
# Sonnet class is the cost/quality balance for 100 calls.
MODEL = "claude-sonnet-5"
TEMPERATURE = 1.0
MAX_TOKENS = 1024

# Fixed system line, identical across all 100 calls so the only things that
# vary are the sampling seed and the occasion.
SYSTEM_PROMPT = (
    "You are a helpful shopping assistant. Give a concrete product "
    "recommendation with specific brands and models where appropriate."
)

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_PATH = ROOT / "prompts" / "prompts.json"
OUTPUT_ROOT = ROOT / "output"


def load_prompts():
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def call_with_retry(client, prompt_text, max_attempts=4):
    """Single API call with exponential backoff on transient errors."""
    delay = 2.0
    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt_text}],
            )
            text = "".join(
                block.text for block in resp.content if block.type == "text"
            )
            usage = {
                "input_tokens": resp.usage.input_tokens,
                "output_tokens": resp.usage.output_tokens,
            }
            return text, usage
        except Exception as exc:  # broad on purpose for backoff
            if attempt == max_attempts:
                raise
            sys.stderr.write(
                f"  attempt {attempt} failed ({exc}); retrying in {delay:.0f}s\n"
            )
            time.sleep(delay)
            delay *= 2


def run_occasion(occasion, dry_run=False):
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    prompts = load_prompts()
    occasion_dir = OUTPUT_ROOT / f"occasion_{occasion}"
    if not dry_run:
        occasion_dir.mkdir(parents=True, exist_ok=True)

    for p in prompts:
        text, usage = call_with_retry(client, p["text"])
        record = {
            "prompt_id": p["id"],
            "occasion": occasion,
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "model": MODEL,
            "temperature": TEMPERATURE,
            "category": p["category"],
            "archetype": p["archetype"],
            "prompt_text": p["text"],
            "response_text": text,
            "usage": usage,
        }
        if dry_run:
            print(json.dumps(record, indent=2)[:800])
            print("... dry run, stopping after one prompt.")
            return
        out_path = occasion_dir / f"{p['id']}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        print(f"  wrote {out_path.relative_to(ROOT)}  ({usage['output_tokens']} out tokens)")


def main():
    ap = argparse.ArgumentParser(description="Retrieve one occasion of shopping responses.")
    ap.add_argument("--occasion", type=int, required=True, help="Occasion index 0..9")
    ap.add_argument("--dry-run", action="store_true", help="One call, print, write nothing")
    args = ap.parse_args()
    print(f"Occasion {args.occasion} starting at {dt.datetime.now().isoformat(timespec='seconds')}")
    run_occasion(args.occasion, dry_run=args.dry_run)
    print("Done.")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Scheduling the full 10-occasion run
#
# Option A, simple driver (run in the foreground, blocks for ~10 hours):
#
#   for i in $(seq 0 9); do
#       python retrieve.py --occasion $i
#       [ "$i" -lt 9 ] && sleep 3600
#   done
#
# Option B, cron (one occasion at the top of each hour). Track the occasion
# index in a small state file so each hourly fire advances it.
#
# Option A is recommended for a one-day run. Fewest moving parts, and fully
# resumable: if an occasion errors, rerun that single index.
# ---------------------------------------------------------------------------
