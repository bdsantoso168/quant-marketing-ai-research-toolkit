# Task 5: Game Theory Model Proof

**Paper:** Feng, Liu, Zhang, and Srinivasan, "Sustainability and Competition on Amazon" (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4958107)

**Task:** evaluate the paper's three stage game theory model. Determine whether it can simultaneously explain four empirical findings. If not, propose modifications.

**Deliverable:** `analysis.pdf` (also available as `.docx` on request), full write up with equations rendered natively.

## The four findings

1. CPF badge increases demand and sales
2. CPF badge increases price
3. Platform prefers selective badging (badge only a fraction of sellers)
4. CPF badge decreases market concentration (HHI)

## What was done

Read the paper's theoretical model (Sections 3.1 to 3.4) and empirical results (Section 6) in full. Worked through the consumer utility functions, the three Lemmas, and Propositions 1 through 5 directly rather than taking the paper's summary claims at face value. Re derived the demand and price equilibrium expressions from the underlying utility functions using symbolic computation (sympy), then checked them against the paper's own stated closed forms.

## Verdict

The model, as written, does not jointly explain all four findings for every parameter value. Findings 1, 2, and 3 hold throughout Proposition 3's own parameter band regardless of the green consumer segment size (k), since none of those conditions involve k at all. Finding 4 holds only on a sub region of that same band, bounded by k. Above roughly k = 0.5 to 0.7 (tightening further as the baseline utility parameter rises), the model's own algebra predicts market concentration rises instead of falls. The paper never states or derives this restriction. Full derivation, numerical check, and the proposed modifications (ordered by cost) are in `analysis.pdf`.

## Judgment call worth flagging

The demand and price formulas as transcribed from the paper (via OCR in the source PDF) show the badge premium term as a function of z, the substitutability parameter. Deriving the model from its own stated utility functions and checking the result against the paper's clean Situation 1 closed form shows this is inconsistent: the term must instead be a function of k, the green consumer segment size. The z reading does not reduce correctly to the paper's own baseline case, the k reading does. This is treated as a transcription error in the source material, not an error in the paper's actual model, and the analysis proceeds on the k reading throughout. This distinction is the reason the HHI result above is stated as a function of k rather than z, flagging it here since it is a deviation from a literal read of the transcribed equations.

## Files

- `analysis.pdf` (or `.docx`): full evaluation, finding by finding derivation, consistency verdict, and three modifications ordered by cost
