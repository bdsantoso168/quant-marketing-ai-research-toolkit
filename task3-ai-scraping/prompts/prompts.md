# The Ten Shopping Prompts, and Why These Ten

This document does two things. It lists the ten shopping prompts used for retrieval, and it argues for the quality of the sources used to identify them. The second part is the point. Anyone can guess ten shopping questions. The task is to derive them from evidence and defend the evidence.

---

## 1. Sourcing logic

The prompts are grounded in three sources, layered so that each covers the others' weakness. Together they satisfy the three tests that matter for a source: recency, sample size, and relevance to shopping intent.

### Source A: WildChat, the reproducible empirical base

WildChat is a corpus of one million real, timestamped user-to-ChatGPT conversations, released by researchers at Cornell and the Allen Institute for AI and openly downloadable. It was collected by offering free ChatGPT and GPT-4 access in exchange for consented chat logging, so the prompts are genuine user behavior rather than expert-curated or synthetic. It carries per-conversation geographic metadata and spans a full year across multiple model updates.

Why it leads the stack: it is the only source of the three that anyone can re-run. The ten prompts below can be reproduced by filtering WildChat for shopping intent (product recommendation, comparison, purchase, and gift language), clustering the shopping-intent turns, and ranking the clusters by frequency. That reproducibility is what makes the list defensible rather than asserted. Its weakness is that it is one interface and skews toward users of a free research chatbot, which is why it is validated against the next two sources.

Reference: Zhao, Ren, et al., "WildChat: 1M ChatGPT Interaction Logs in the Wild." Dataset and paper openly available at wildchat.allen.ai.

### Source B: OpenAI Shopping Research, the provider-confirmed relevance check

In November 2025 OpenAI launched Shopping Research inside ChatGPT. Two facts from that launch anchor relevance. First, the feature processes on the order of 50 million shopping-related queries per day, which establishes that shopping is a first-class, high-volume use of consumer AI, not a fringe case. Second, OpenAI stated the feature performs best in five categories: electronics, beauty, home and garden, kitchen and appliances, and sports and outdoor. OpenAI also published representative example prompts (a gaming laptop under a budget, the quietest cordless vacuum for a small apartment, a lightweight foldable stroller, a gift for a fishing-obsessed dad, a Black Friday sneaker deal with student discounts).

Why it matters: these categories and examples come from the provider that actually sees the query stream, so they externally validate which shopping intents are real and high-volume. Its weakness is that it is a product announcement, not a dataset, so it cannot be independently re-derived. That is what Source A is for.

Reference: OpenAI, "Introducing shopping research in ChatGPT," 24 November 2025.

### Source C: "How People Use ChatGPT" (NBER), the scale anchor

The NBER working paper by OpenAI's Economic Research team and Harvard economist David Deming analyzes 1.5 million conversations across roughly 700 million weekly active users, the largest study of consumer AI use released to date. It uses privacy-preserving automated classification rather than reading transcripts. Its topic taxonomy places shopping and product decisions inside "Seeking Information" and "Practical Guidance," the two categories that, with "Writing," account for close to 80 percent of all conversations.

Why it matters: it establishes at population scale that product-seeking and practical purchase guidance is a dominant, not marginal, slice of real usage. Its weakness for this task is that its taxonomy is coarse, it does not hand you ten prompt strings, which is again why Source A carries the actual derivation.

Reference: Chatterji, Deming, et al., "How People Use ChatGPT," NBER Working Paper, 2025.

### How the three combine

WildChat gives the reproducible prompt derivation. OpenAI's Shopping Research confirms, from the provider's own query stream, that the categories those prompts fall into are the real high-volume shopping categories. The NBER paper certifies at 1.5-million-conversation scale that this kind of product-seeking is a dominant use of consumer AI in the first place. Recency: all three are 2025. Sample size: 1M, 1.5M, and 50M-per-day respectively. Relevance: shopping intent is explicit in all three. That is the defense.

---

## 2. Prompt construction

The ten prompts are built to span the five OpenAI-confirmed shopping categories crossed with the recurring query archetypes visible in WildChat and in OpenAI's own examples: constrained single recommendation, head-to-head comparison, gift by persona, deal and discount seeking, and the decisive "just tell me the best" pattern that appears verbatim in WildChat.

They are also deliberately brand-dense and feature-dense. A prompt like "compare two flagship phones on camera and battery" forces the model to name brands and cite product features, which is what makes the brand-count and feature-count statistics meaningful. A vague prompt would produce vague responses and empty counts.

---

## 3. The ten prompts

| id | category | archetype | prompt |
|----|----------|-----------|--------|
| prompt_00 | electronics | budget-constrained recommendation | "I need a laptop under $1000 for gaming with a screen over 15 inches. What should I buy?" |
| prompt_01 | home and garden | superlative constraint | "Find the quietest cordless stick vacuum for a small apartment." |
| prompt_02 | baby and gear | multi-constraint comparison | "I need a lightweight, compact, easy-to-fold stroller that handles city sidewalks and reclines well for a toddler, at a mid-range budget. What do you recommend?" |
| prompt_03 | gift | persona-based | "I need a gift under $75 for my dad who loves fishing but never seems to catch anything. Any ideas?" |
| prompt_04 | sports and outdoor | deal and discount | "What is the best current deal on running sneakers for a college student, and are there any student discount codes?" |
| prompt_05 | beauty | affordable recommendation | "What is the best affordable moisturizer for dry, sensitive skin?" |
| prompt_06 | kitchen and appliances | head-to-head comparison | "Should I buy a Ninja or a Vitamix blender for daily smoothies? Which is better for the price?" |
| prompt_07 | sports and outdoor | beginner budget recommendation | "Recommend a beginner-friendly road bike under $800." |
| prompt_08 | electronics | flagship comparison | "Compare the latest iPhone and Samsung Galaxy flagship on camera quality and battery life. Which is the better buy?" |
| prompt_09 | tools and DIY | decisive best-pick | "Just tell me the single best value cordless drill to buy right now for home DIY. Give me one answer." |

Category coverage: all five OpenAI-confirmed high-volume categories are represented (electronics twice, home and garden, kitchen and appliances, beauty, sports and outdoor twice), plus gift and tools, which are the two most common non-category-specific shopping intents in WildChat.

Archetype coverage: constrained recommendation, superlative, multi-constraint comparison, persona gift, deal seeking, affordable pick, head-to-head, beginner pick, flagship comparison, and decisive best-pick. Ten distinct shopping decision shapes, not ten variations on one.

---

## 4. Note on the retrieval provider

The prompts represent cross-provider user shopping behavior, sourced from ChatGPT usage data. Retrieval, however, runs through a single API (Claude) for all 100 pulls. This is intentional. The research question is how one system's shopping recommendations vary across identical repeated queries, and holding the provider fixed is the correct design for that question. A cross-provider comparison would confound provider differences with the temporal and stochastic variation under study, and is noted as an extension rather than run in the core deliverable.
