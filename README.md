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

### 03 — AI Search Behavior Monitoring
**status: not started**

Programmatic, scheduled retrieval of AI assistant responses to a defensibly-sourced set of shopping-intent prompts, repeated over time to observe response drift, with word/brand/feature-mention statistics computed per response.

→ [`task3-ai-scraping/`](./task3-ai-scraping)

### 04 — Computational Biology Agent Deployment
**status: not started**

Standing up a domain-specific research agent from the AlphaGenome paper via the Paper2Agent framework, then running a Mendelian randomization query (rs11174281, lifetime cannabis use) through it end to end.

→ [`task4-ai-agents/`](./task4-ai-agents)

### 05 — Applied Game Theory: Platform Badge Economics
**status: not started**

Formal evaluation of whether a published platform-badging game-theoretic model can jointly explain four empirical findings on demand, pricing, selective certification, and market concentration — with structural modifications proposed where the model falls short.

→ [`task5-game-theory/`](./task5-game-theory)

---

Each module folder carries its own README covering the approach taken, the judgment calls made, and any limitations encountered. The reasoning is treated as part of the deliverable, not an afterthought.
