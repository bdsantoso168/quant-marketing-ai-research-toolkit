# Quant Marketing AI Research Toolkit

Applied research portfolio spanning LLM-driven data pipelines, quantitative marketing analysis, and automation systems for consumer and product intelligence.

**Philosophy:** LLMs are not impressive by default. They are impressive when they solve a real problem. Every module here produces a real, verifiable output — not a demo — with the method, judgment calls, and limitations documented alongside the result, not glossed over.

Built by **Benedict Daxell Santoso** — AI implementation practitioner and analytics consultant working at the intersection of LLM engineering, data architecture, and applied marketing research.

---

## Modules

### 01 — Automated Retail Intelligence: Multi-Site Web Scraping
**status: complete**

Structured, product-level scraping across three e-commerce sites (Olipop, Poppi, Coca-Cola Simply Pop) into one normalized schema for cross-brand comparison: pricing, live promotions, page position, image galleries, and nutritional composition. Includes a documented build-vs-buy call on scraping tooling and honest data-quality limitations where a site's template didn't cooperate.

→ [`task1-webscraping/`](./task1-webscraping) · [output](./task1-webscraping/output/products.csv) · [methodology](./task1-webscraping/README.md)

### 02 — Survey Instrumentation with Embedded AI Interaction
**status: complete**

Qualtrics survey design spanning ten distinct question types on a consumer decision-making topic tied to the same three beverage brands profiled in Module 01 (Olipop, Poppi, Coca-Cola Simply Pop), including a live Claude-enabled interactive question, testing both survey methodology range and AI-in-the-loop UX design.

→ [`task2-qualtrics/`](./task2-qualtrics) · [live survey](https://qualtricsxmwykl4q9jv.qualtrics.com/jfe/form/SV_cIOHHhcwcRLQCqi) · [methodology](./task2-qualtrics/README.md)

## 03 - AI Search Behavior Monitoring

**status: complete**

Programmatic, repeated retrieval of Claude API responses to a defensibly sourced set of 10 shopping intent prompts (grounded in WildChat, OpenAI's Shopping Research data, and the NBER "How People Use ChatGPT" study), pulled across 10 occasions each (100 total responses) to measure recommendation drift. Computes word count, brand count, and feature count per response, plus brand concentration (HHI) and cross occasion stability (Jaccard overlap) per prompt. Sharpest finding: closed category prompts (phone flagships, blender models) converge on near fixed brand answers, open ended prompts (fishing gifts, sneaker deals) barely repeat.

→ `task3-ai-scraping/` · [full results](task3-ai-scraping/README.md) · [methodology](task3-ai-scraping/task3_master_plan.md)

## 04 - Computational Biology Agent Deployment

**status:** complete

Stood up an AlphaGenome research agent via Paper2Agent, pivoted from a failed local build to the hosted remote MCP server after three isolated failures at the same build step, then ran a Mendelian randomization query (rs11174281, lifetime cannabis use) end to end. Output cross verified across two independent agent instances: chromosome, position, and allele lookup, variant effect prediction across 25,089 tracks and 11 modalities, brain tissue RNA seq ranking, regulatory element overlap, and 7 regulatory landscape plots.

-> [task4-ai-agents/](task4-ai-agents/)

### 05 — Applied Game Theory: Platform Badge Economics
**status: done**

Formal evaluation of a published platform badging game theoretic model against four empirical findings on demand, pricing, selective certification, and market concentration. Re derived the model's demand and price equilibria symbolically rather than taking the paper's stated closed forms at face value, surfacing a transcription correction in the process. Confirmed the model explains three of the four findings unconditionally, but the fourth (market concentration) holds only below an identifiable threshold on the green consumer segment size, a boundary the paper itself never states. Three modifications proposed, ordered by cost, to close the gap.

→ [`task5-game-theory/`](./task5-game-theory)

---

Each module folder carries its own README covering the approach taken, the judgment calls made, and any limitations encountered. The reasoning is treated as part of the deliverable, not an afterthought.
