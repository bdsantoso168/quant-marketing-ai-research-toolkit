# Quant Marketing AI Research Toolkit

**Benedict Daxell Santoso**

Five self contained projects spanning the core methodology of applied marketing research: web scraping and data pipelines, experimental survey design, programmatic AI response collection and analysis, agentic AI systems built from a research paper, and formal game theoretic modeling verified with symbolic computation.

Each folder is independent, with its own README, code, and output. Built as a demonstration of range across the full research stack: from scraping raw data off the web, to designing instruments that collect it directly from people, to building AI agents that operate research tools autonomously, to formally auditing a published economic model's internal consistency.

---

## Projects

### 01 — Multi Site Web Scraping Pipeline
Extracts structured product data (pricing, position, ingredients, nutrition, imagery) from three e-commerce sites with materially different front end architectures, normalized into a single schema despite each site requiring a different scraping strategy.
→ [`task1-webscraping/`](./task1-webscraping)

### 02 — Experimental Survey Design with Embedded AI Interaction
A Qualtrics instrument spanning ten distinct question types, including a live, participant facing AI chat interaction embedded directly in the survey flow, not a static question about AI.
→ [`task2-qualtrics/`](./task2-qualtrics) · [Live survey link](#) <!-- add your Qualtrics link here -->

### 03 — Programmatic AI Response Collection and Analysis
A repeated measurement pipeline: ten shopping relevant prompts, each queried via API across ten separate sessions, producing a structured dataset of AI generated shopping guidance with word, brand, and feature level statistics computed per response.
→ [`task3-ai-scraping/`](./task3-ai-scraping)

### 04 — Research Agent from a Published Paper
Stood up a functioning AI agent directly from AlphaGenome, a DeepMind genomics research paper, using the Paper2Agent framework, then ran a full Mendelian randomization analysis prompt through it end to end, with cross verified output.
→ [`task4-ai-agents/`](./task4-ai-agents)

### 05 — Applied Game Theory: Platform Badge Economics
Formal evaluation of a published platform badging game theoretic model against four empirical findings on demand, pricing, selective certification, and market concentration. Re derived the model's equilibrium conditions symbolically rather than relying on the paper's stated closed forms, surfacing a transcription correction in the process, and identified an explicit, previously unstated boundary condition under which one of the four findings holds.
→ [`task5-game-theory/`](./task5-game-theory)

---

## Stack

Python, pandas, Apify, Qualtrics, Anthropic Claude API, sympy, Paper2Agent, AlphaGenome, Word/OMML for equation rendering.

## Contact

[[LinkedIn](https://www.linkedin.com/in/benedictdaxellsantoso/)](#) · [benedict.d.santoso@gmail.com](#) <!-- add your links -->
