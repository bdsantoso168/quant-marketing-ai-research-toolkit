# Do AI Assistants Recommend the Same Products Twice?

**Measuring the stability and concentration of brand recommendations that large language models give to shoppers.**

When a shopper asks an AI assistant "what laptop should I buy under $1000," does the same question asked ten times return the same brands? Or does the model quietly reshuffle who it recommends on every ask? This project measures that. It retrieves an LLM's answers to ten realistic shopping questions, ten times each, and quantifies how much the recommended brands and product features move from one identical query to the next.

This matters because AI assistants are becoming a real product-discovery channel. ChatGPT's Shopping Research alone handles on the order of 50 million shopping queries per day, and AI-referred shoppers have shown higher conversion and order value than traditional search traffic. If those recommendations are volatile or heavily concentrated toward a handful of brands, that has direct consequences for consumer choice and for how brands compete for AI visibility.

---

## Research question

For a fixed model answering an identical shopping prompt repeatedly:

1. **Stability.** How consistent are the recommended brands across repeated asks?
2. **Concentration.** How concentrated are recommendations toward a few brands, measured with the Herfindahl-Hirschman Index?
3. **Content shape.** How much do response length, brand density, and feature density vary?

---

## Method

**Prompt set.** Ten shopping prompts spanning the five highest-volume AI shopping categories (electronics, beauty, home and garden, kitchen and appliances, sports and outdoor) crossed with the recurring query archetypes seen in real usage: constrained recommendation, head-to-head comparison, persona gift, deal seeking, and decisive best-pick. The prompts are grounded in three sources (WildChat's one million real conversations, OpenAI's published Shopping Research query data, and the NBER "How People Use ChatGPT" study) rather than invented. The full sourcing argument is in [`prompts/prompts.md`](prompts/prompts.md).

**Retrieval.** Each prompt is sent to the Claude API ten times, at temperature 1.0, with no tools, holding the system prompt and model fixed. Temperature 1.0 is deliberate: it surfaces the model's intrinsic recommendation variability, which is the phenomenon under study. Holding everything else fixed means the only thing changing between the ten pulls is the sampling seed. Result: 100 self-describing JSON files.

**Extraction and statistics.** A second structured pass extracts, from every response, the distinct brands and the distinct product features mentioned, into a fixed JSON schema. From those, the pipeline computes:

- per-file word count, brand count, and feature count (the base statistics);
- **brand recommendation HHI** per prompt, treating pooled brand mentions as a market;
- **cross-occasion stability** per prompt, as the mean pairwise Jaccard overlap of brand sets;
- the overall leaderboard of most-recommended brands.

The counting method is documented and re-runnable from the committed JSON, with a rule-based spaCy baseline available as a cross-check.

---

## Repository layout

```
prompts/
  prompts.md      the 10 prompts and the source justification
  prompts.json    machine-readable prompt set
scripts/
  retrieve.py     pulls one occasion of responses (resumable, backoff)
  analyze.py      base stats + HHI + stability, writes stats.csv and summary.json
  requirements.txt
output/
  occasion_0..9/  10 JSON responses each
  stats.csv       one row per file
  summary.json    aggregate statistics
```

---

## Reproduce it

```bash
pip install -r scripts/requirements.txt
export ANTHROPIC_API_KEY=sk-...

# retrieve all 10 occasions, one per hour
for i in $(seq 0 9); do
    python scripts/retrieve.py --occasion $i
    [ "$i" -lt 9 ] && sleep 3600
done

# compute statistics
python scripts/analyze.py
```

Every response file records its own model, temperature, timestamp, prompt, and token usage, so the run is auditable end to end.

---

## Results

100 responses retrieved (10 prompts times 10 occasions), no refusals, no off-topic responses. All files valid, all schema fields populated.

| Metric | Value |
|--------|-------|
| Response files | 100 |
| Mean words per response | 263.1 (range 114 to 386) |
| Mean distinct brands per response | 5.77 |
| Mean distinct features per response | 9.61 |

**Most brand-stable prompt:** prompt_07, beginner road bike, Jaccard 0.600. The model converges on the same three bikes (Giant Contend 3, Trek Domane AL 2, Specialized Allez) almost every time.

**Least brand-stable prompt:** prompt_03, fishing gift, Jaccard 0.079. Forty distinct brands surfaced across ten occasions for the same question, the model essentially never repeats itself here.

**Most concentrated prompt (highest HHI):** prompt_08, iPhone vs Galaxy flagship comparison, HHI 3043.5. Only 6 distinct brands pooled across all ten occasions, dominated by Samsung Galaxy S24 Ultra (10/10 occasions) and iPhone 16 Pro Max (7/10). A binary comparison prompt structurally forces concentration since the question names the category.

**Least concentrated prompt (lowest HHI):** prompt_04, sneaker deal seeking, HHI 301.9, with 59 distinct brands pooled. This is the direct counterpoint to prompt_08: an open-ended deal-seeking prompt with no named comparison anchor produces maximum brand spread.

**Most-recommended brands overall:** Amazon, Student Beans, and UNiDAYS each appeared in all 10 occasions of their respective prompts, alongside CeraVe and Vanicream (moisturizer, tied 10/10) and the Vitamix E310 (blender, 10/10). These are the brands the model treats as close to a fixed answer rather than a recommendation.

**The stability-concentration pattern is the core finding.** Prompts that name a closed category (bike models, blender models, phone flagships) produce both high concentration and high stability, the model has effectively memorized a canonical answer. Prompts that are open-ended within a broad category (fishing gifts, sneaker deals) produce both low concentration and low stability, the model generates fresh each time rather than recalling. This is visible directly by comparing prompt_08 (HHI 3043.5, Jaccard 0.597) against prompt_03 (HHI 382.1, Jaccard 0.079).

Full per-prompt breakdown, including all top-5 brand lists, is in `output/summary.json`. Per-file data is in `output/stats.csv`.

---

## Design notes

- **Single provider by design.** All retrieval runs through one API so that the variation measured is one system's behavior over repeated identical queries, not a confound between providers. A multi-provider comparison is a natural extension.
- **No live tools in the core run.** This isolates model-intrinsic variation and keeps the run cheap and fully reproducible. A web-search-enabled variant, which would additionally capture live retrieval drift, is a documented next step.

---

## Tech stack

Python, Anthropic Claude API, structured JSON extraction, pandas-free standard-library analysis, optional spaCy for the validation baseline.
