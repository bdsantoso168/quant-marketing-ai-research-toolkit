# Beverage Brand Choice: A 10 Method Survey Instrument

A Qualtrics instrument measuring how consumers weigh price, ingredients, and brand trust when choosing a functional soda, using Olipop, Poppi, and Coca Cola Simply Pop, the same three brands profiled in the webscraping module.

**Live survey:** https://qualtricsxmwykl4q9jv.qualtrics.com/jfe/form/SV_cIOHHhcwcRLQCqi

## Question types

Ten methodologically distinct question types, each chosen for what it can measure that the others can't.

| # | Type | Why this type fits what it's measuring |
|---|------|------------------------------------------|
| 1 | Multiple choice | Screens for existing brand awareness before any brand cues are shown, so later answers can be read against a baseline. |
| 2 | Matrix table | Rates several brands against the same attribute set in one grid, which is the only way to get comparable, side by side attribute scores without order effects from asking one brand at a time. |
| 3 | Slider (willingness to pay) | Captures a continuous price point rather than forcing a respondent into a coarse price bracket, which matters when the actual research question is a dollar figure, not a range. |
| 4 | Rank order | Forces a strict ordering of purchase drivers (price, health claims, taste, sustainability), which reveals relative priority in a way a rating scale can't, since ratings let everything cluster at "important." |
| 5 | Constant sum | Allocates 100 points across decision factors, which produces a true zero sum tradeoff instead of independent ratings that can all be high at once. |
| 6 | Text entry | Open ended response on what would make a respondent switch brands, left unstructured on purpose so the answer isn't primed by a predefined list. |
| 7 | Net promoter score | Standard single number brand loyalty metric, included specifically because it's an industry benchmark and lets the results compare against known category NPS ranges. |
| 8 | Side by side comparison | Puts the actual scraped product images next to each other so the comparison is visual and immediate, not a comparison of brand names in text. |
| 9 | Heat map / hot spot | Has respondents click directly on the parts of an ingredient panel that catch their attention, which locates the specific claims driving a reaction instead of asking them to self report what they noticed. |
| 10 | AI interactive (Claude) | Gives the respondent an actual live conversation about their own reasoning, so the response is generated through real dialogue rather than a static follow up question. |

## Build notes

Real constraints hit during the build, and the decision made for each.

**Willingness to pay slider.** Qualtrics slider increments don't support native decimal steps at the granularity a price question needs. I built the slider on a cents based integer scale, 0 to 200 in steps of 20, and relabeled the endpoints in dollar terms. The respondent sees a clean price slider; the backend just runs on integers Qualtrics can actually increment.

**Side by side image comparison.** The account tier in use doesn't include the graphics library upload feature that side by side questions normally pull images from. I hosted the product images in this repo instead and pointed the question's image tool at the raw GitHub URLs. Same visual comparison, different image source, no loss of fidelity.

**Constant sum validation.** A constant sum question is only as good as its total. Rather than trust free text entry to sum to 100, I turned on Qualtrics' built in response validation so the question won't submit unless the allocation hits exactly 100 points. That moves the constraint into the platform instead of into the analysis stage.

**AI interactive question.** Building a Custom GPT for the ChatGPT route requires a paid ChatGPT plan. I used Claude instead: Claude's free tier supports a live, in survey conversation without that paywall, so the respondent still has a real AI interaction, not a scripted mockup standing in for one. The experimental goal, an actual conversation rather than a static exchange, is unchanged.

## What this demonstrates

Translating a business question, what actually drives a beverage purchase decision, into ten methodologically distinct instruments that each isolate a different part of that decision: awareness, comparative attribute scoring, price elasticity, priority ordering, tradeoff allocation, unprompted reasoning, loyalty benchmarking, visual comparison, attention location, and live reasoning through dialogue. Every platform constraint hit along the way, the slider increments, the missing graphics library, the validation logic, the ChatGPT paywall, got solved without cutting what the question was actually designed to measure.
