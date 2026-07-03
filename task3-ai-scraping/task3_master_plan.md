# Task 3: AI Shopping Response Retrieval, Cowork Execution Runbook

**Candidate:** Benedict Daxell Santoso
**Role:** Junior Research Scientist, NYU Stern Marketing (Prof. Ursu and Prof. Liu)
**Environment:** Cowork (scheduled retrieval loop plus file management)
**Status:** v2 finalized. All open decisions from the v1 scaffold are now closed and marked RESOLVED.

> This is the internal execution document. The public-facing repo face is `README.md`. The graded source justification lives in `prompts/prompts.md`.

---

## 0. What the task actually tests

Three things, in order of grading weight:

1. **Can you source AI shopping behavior defensibly?** The task explicitly asks you to argue for the quality of the source used to identify the top prompts. The justification is graded, not just the list.
2. **Can you retrieve programmatically over time and manage the output?** 10 prompts times 10 occasions, cleanly named JSON, no manual copy paste.
3. **Can you turn raw responses into honest statistics?** File count, per file word count, per file brand count, per file feature count, with a counting method that is documented and reproducible.

Everything below is built to clear those three bars and add one research-grade layer on top: measuring how stable and concentrated an LLM's brand recommendations are when the same shopper asks the same question repeatedly. That layer is what makes this a portfolio piece rather than a homework submission, and it maps directly onto the lab's interests in consumer search and digital marketing.

---

## 1. Deliverable (exact)

- The JSON files retrieved (100 files: 10 prompts times 10 occasions).
- Simple statistics: number of files, number of words per file, number of brands mentioned per file, number of product features mentioned per file.
- Plus, as the value-add layer: brand recommendation concentration (HHI) and cross-occasion stability (Jaccard overlap) per prompt.

---

## 2. Design decisions (RESOLVED)

| Open decision (v1) | Resolution | Reasoning |
|--------------------|------------|-----------|
| Source for the top 10 prompts | Three-layer sourcing: WildChat (1M real ChatGPT conversations, openly downloadable) as the empirical base, filtered for shopping intent and ranked; validated against OpenAI's published Shopping Research query categories and example prompts; anchored in the NBER "How People Use ChatGPT" usage study for topic-share credibility. Full argument in `prompts/prompts.md`. | The task grades source quality on recency, sample size, and relevance. WildChat gives reproducibility (anyone can re-derive the list), OpenAI's product data gives external validity and provider-confirmed shopping categories, the NBER paper gives scale. Asserting 10 prompts from intuition fails the grading bar. |
| Which API | Claude API (Messages endpoint), single provider, used consistently for all 100 retrievals. | One controllable API isolates one system's behavior, which is the correct experimental design when the research question is response variation over time. It is also fully reproducible and in the candidate's existing stack. Multi-provider comparison is documented as an extension, not the core deliverable, because it triples file count and confounds provider differences with temporal drift. |
| Cadence | Hourly for 10 hours over a single day. | Removes 10 days of calendar-time risk from a five-task submission on a rolling deadline. With the pure-model retrieval design below (no live tools, temperature 1.0), the meaningful variation is stochastic sampling, which 10 hourly pulls capture as well as 10 daily pulls. Daily-for-10-days is noted as an optional add-on if calendar drift is also of interest. |
| Brand and feature counting method | Two-pass structured extraction. Primary: Claude API extraction into a fixed JSON schema `{brands: [...], features: [...]}` per response, deduplicated within file, counted distinct. Validation: rule-based baseline (spaCy `ORG`/`PRODUCT` entities plus a curated feature lexicon) on a 10-file sample, plus a manual spot check. Method and prompt are committed to the repo. | Named entity extraction with a reviewed schema is reproducible and defensible, and it is squarely in the candidate's demonstrated skill set. A bare keyword grep would not survive faculty scrutiny on what counts as a "brand" versus a "feature." |

### Execution environment correction (post-run)

Retrieval and analysis both ran locally in Terminal on macOS, not in Cowork as originally planned. Cowork's sandbox network layer blocks any outbound request to `api.anthropic.com` that carries an `x-api-key` header, confirmed by Cowork's own diagnostic curl against the endpoint. This is a sandboxing control, not a bug, so Cowork remains correct for file assembly and repo structuring, but any task in this project requiring a live API key must run in a local terminal instead.

Also encountered: Claude Sonnet 5 deprecated the `temperature` parameter. The retrieval call (temperature 1.0) still works since Sonnet 5 accepts it there, but the extraction call in `analyze.py` originally set `temperature=0` and was rejected with a 400. Fixed by removing the parameter from the extraction call entirely, extraction is a well-specified schema task and does not need forced determinism to behave consistently.

### Retrieval parameters (locked)

- **Model:** current Claude Sonnet class model (cost and quality balance for 100 calls). Set the exact model string in `scripts/retrieve.py` and check `docs.claude.com` for the latest string at run time.
- **Temperature:** 1.0. This is deliberate. Temperature 0 would make all 10 occasions near-identical and the brand-variation statistics meaningless. Temperature 1.0 surfaces genuine model-intrinsic recommendation variability, which is the phenomenon under study.
- **Tools:** none in the primary run. A no-tools run isolates model-intrinsic variation and is fully reproducible and cheap. A web-search-enabled run (which adds live retrieval drift) is documented as an extension in the README, not run for the core 100 files, to keep the variation source clean.
- **Max tokens:** 1024. Enough for a realistic shopping recommendation, capped for cost control across 100 calls.
- **System prompt:** a single fixed line positioning the model as a shopping assistant, identical across all 100 calls so the only things varying are the sampling seed and the occasion.

---

## 3. Pipeline architecture

Three stages, each a committed script or document.

**Stage 1, prompt set.** `prompts/prompts.md` (human, graded justification) and `prompts/prompts.json` (machine, consumed by the scripts). Ten prompts, each carrying an `id`, the prompt text, a category label, and a query-archetype label.

**Stage 2, retrieval loop.** `scripts/retrieve.py` runs one occasion per invocation. Each invocation pulls all 10 prompts once and writes 10 JSON files into `output/occasion_{r}/`. A scheduler (cron, or the included driver) fires it 10 times, once per hour. One-occasion-per-invocation makes the run resumable: if hour 6 fails, you rerun only occasion 6.

**Stage 3, analysis.** `scripts/analyze.py` walks the output tree, computes the required per-file statistics and the value-add concentration and stability metrics, and writes `output/stats.csv` (one row per file) and `output/summary.json` (aggregates).

---

## 4. Repo and output structure

```
task3-ai-scraping/
  README.md                     <- public portfolio face
  task3_master_plan.md          <- this document (internal runbook)
  prompts/
    prompts.md                  <- 10 prompts + graded source justification
    prompts.json                <- machine-readable prompt set
  scripts/
    retrieve.py                 <- one occasion per invocation
    analyze.py                  <- required stats + concentration/stability
    requirements.txt
  output/
    occasion_0/  ... occasion_9/ <- 10 JSON files each (prompt_00..prompt_09)
    stats.csv                    <- per-file statistics
    summary.json                 <- aggregate statistics
```

Each response file is self-describing JSON:

```json
{
  "prompt_id": "prompt_00",
  "occasion": 0,
  "timestamp_utc": "2026-07-03T14:00:11Z",
  "model": "claude-sonnet-5",
  "temperature": 1.0,
  "category": "electronics",
  "archetype": "budget_constrained_recommendation",
  "prompt_text": "...",
  "response_text": "...",
  "usage": { "input_tokens": 0, "output_tokens": 0 }
}
```

---

## 5. Statistics methodology

**Required by the task:**

- **Number of files:** count of JSON files under `output/`. Target 100.
- **Words per file:** whitespace tokenization of `response_text`. Token count from the API `usage` field is recorded as a secondary measure.
- **Brands per file:** distinct brand or product names extracted by the structured pass, deduplicated case-insensitively within the file.
- **Features per file:** distinct product features or attributes (for example "battery life", "noise level", "screen size") extracted by the same pass, deduplicated within the file.

**Value-add layer (positions this as research, ties to the lab):**

- **Brand recommendation HHI, per prompt:** treat the pooled brand mentions across the 10 occasions of a single prompt as a market, compute the Herfindahl-Hirschman Index of mention share. High HHI means the model funnels shoppers toward a few brands; low HHI means it spreads recommendations. This is the same concentration lens that appears in Task 5.
- **Cross-occasion stability, per prompt:** mean pairwise Jaccard overlap of the brand sets across the 10 occasions. High overlap means the shopper gets the same brands every time; low overlap means recommendations are volatile.
- **Top brands by mention frequency:** the leaderboard of which brands the model surfaces most, aggregated across all prompts.

Every metric is defined in code, so the numbers are reproducible from the committed JSON files.

---

## 6. Cowork execution sequence

1. **Set up.** In Cowork, create the folder structure, drop in `prompts.json`, `retrieve.py`, `analyze.py`, `requirements.txt`. `pip install -r requirements.txt`. Set the Anthropic API key in the environment. Confirm the model string against `docs.claude.com`.
2. **Dry run.** Run `retrieve.py --occasion 0 --dry-run` to confirm the prompt set loads and one call round-trips. Inspect one output JSON for schema correctness.
3. **Kick off the loop.** Start the scheduler at the top of the hour. Either the included driver (`python scripts/retrieve.py --occasion $i` in a loop with a one-hour sleep) or a cron entry. Occasions 0 through 9, one per hour. Total wall-clock: about 10 hours.
4. **Monitor.** After each hour, confirm 10 new files landed in `output/occasion_{r}/`. If an hour errors, rerun only that occasion. The design is resumable by construction.
5. **Analyze.** After occasion 9 completes, run `python scripts/analyze.py`. Produces `stats.csv` and `summary.json`.
6. **Validate the counts.** Run the rule-based baseline on a 10-file sample and eyeball the brand and feature extractions. Note any systematic miss in the README.
7. **Write the README results section.** Fill the placeholders with the real numbers: file count, word-count distribution, brand and feature counts, HHI, and stability. Keep it honest, including any prompt where the model refused or returned an off-topic answer.
8. **Assemble.** The `output/` folder plus stats go into the compressed submission folder. The whole task folder becomes the GitHub showcase.

---

## 7. Acceptance criteria

- 100 JSON files, cleanly named, each self-describing and valid JSON.
- Source justification in `prompts.md` is written, specific, and defensible on recency, sample size, and relevance.
- `stats.csv` present with one row per file and the four required statistics populated.
- Brand and feature counting method is documented and re-runnable from the committed files.
- README states what was found, including HHI and stability, and flags any prompt that misbehaved rather than hiding it.
- Nothing fabricated. A refused or empty response is recorded as such, not backfilled.

---

## 8. Risk register

| Risk | Mitigation |
|------|------------|
| API rate limits or transient errors during a pull | One-occasion-per-invocation design makes any single hour independently re-runnable. Retry with backoff inside `retrieve.py`. |
| Temperature 0 by accident, killing variation | Temperature is set explicitly to 1.0 and written into every output file so it is auditable. |
| Extraction over- or under-counts brands or features | Rule-based baseline plus manual spot check on a sample, disagreement noted in the README. |
| Sample-task deadline shorter than expected | Hourly cadence completes the whole retrieval in one day. If even that is tight, occasions can be pulled back to back (documented as a design variant). |
| Model refuses a shopping prompt or returns off-topic text | Recorded honestly in the output and flagged in the README. Prompts are ordinary consumer shopping questions, so refusals are unlikely, but they are handled not hidden. |

---

*End of v2 finalized runbook.*
