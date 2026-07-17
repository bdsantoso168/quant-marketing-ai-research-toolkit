# Applied Game Theory: Platform Badge Economics
 
A formal audit of a published game theoretic model of Amazon's Climate Pledge Friendly badge, checking whether the model's own equilibrium conditions actually support all four of its claimed empirical findings simultaneously, and finding a boundary condition the paper itself never states.
 
**Paper:** Feng, Liu, Zhang, and Srinivasan, "Sustainability and Competition on Amazon"
 
## What this demonstrates
 
Reading a formal economic model critically means re deriving it, not summarizing it. This project rebuilt the paper's demand and price equilibrium expressions directly from the underlying consumer utility functions using symbolic computation, checked them against the paper's own stated baseline case, and used that to surface a transcription inconsistency in one of the paper's key formulas before running the actual numerical check nobody, including the paper's own authors, had run.
 
## The question
 
Can a three stage game (platform sets badge threshold, sellers set prices, consumers purchase) simultaneously explain:
1. The badge increases demand
2. The badge increases price
3. The platform prefers badging only a fraction of sellers
4. The badge decreases market concentration

## Method
 
1. Derived the three stage game's equilibrium prices and demand functions directly from the consumer utility functions, using symbolic computation (sympy), rather than transcribing the paper's stated closed forms as given
2. Cross checked the derivation against the paper's own baseline case (no badge scenario) to validate correctness, which surfaced a likely OCR transcription error in one of the paper's key formulas
3. Ran the market concentration comparison numerically across a range of parameter values inside the paper's own stated example, rather than relying on its single illustrative case
4. Proposed three structural modifications, ordered by implementation cost, that would close the gap

## The finding
 
Three of the four hold unconditionally across the model's relevant parameter space. The fourth, market concentration, only holds below an identifiable threshold on the size of the green consumer segment, a boundary that exists in the model's own algebra but is never stated or checked in the paper. Verified with a full symbolic re derivation rather than accepting the paper's single numerical illustration at face value.

### Verdict
The model, as written, does not jointly explain all four findings for every parameter value. Findings 1, 2, and 3 hold throughout Proposition 3's own parameter band regardless of the green consumer segment size (k), since none of those conditions involve k at all. Finding 4 holds only on a sub region of that same band, bounded by k. Above roughly k = 0.5 to 0.7 (tightening further as the baseline utility parameter rises), the model's own algebra predicts market concentration rises instead of falls. The paper never states or derives this restriction. Full derivation, numerical check, and the proposed modifications (ordered by cost) are in `analysis.pdf`.

### Judgment call worth flagging
The demand and price formulas as transcribed from the paper (via OCR in the source PDF) show the badge premium term as a function of z, the substitutability parameter. Deriving the model from its own stated utility functions and checking the result against the paper's clean Situation 1 closed form shows this is inconsistent: the term must instead be a function of k, the green consumer segment size. The z reading does not reduce correctly to the paper's own baseline case, the k reading does. This is treated as a transcription error in the source material, not an error in the paper's actual model, and the analysis proceeds on the k reading throughout. This distinction is the reason the HHI result above is stated as a function of k rather than z, flagging it here since it is a deviation from a literal read of the transcribed equations.


## Output
`analysis.pdf`: full derivation, finding by finding evaluation, the verified boundary condition, and proposed modifications.
