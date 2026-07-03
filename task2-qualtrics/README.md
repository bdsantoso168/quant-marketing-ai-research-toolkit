# Beverage Brand Choice: A 10 Method Survey Instrument

A Qualtrics instrument measuring how consumers weigh price, ingredients, and brand trust when choosing a functional soda, using Olipop, Poppi, and Coca Cola Simply Pop, the same three brands profiled in the webscraping module.

**Live survey:** https://qualtricsxmwykl4q9jv.qualtrics.com/jfe/form/SV_cIOHHhcwcRLQCqi

## Question types

Ten methodologically distinct question types, each chosen for what it can measure that the others can't.

| # | Type | Topic | Why this type fits what it's measuring |
|---|------|-------|------------------------------------------|
| 1 | Multiple choice | Brand purchase factors | Forces a single, top of mind answer on what actually drives the purchase decision, a clean baseline before any brand specific cues appear later in the survey. |
| 2 | Matrix table | Attribute importance ratings | Rates several attributes (price, taste, health claims, and so on) on the same scale in one grid, so importance scores are directly comparable without order effects from asking about each attribute separately. |
| 3 | Slider | Willingness to pay | Captures a continuous price point rather than forcing a respondent into a coarse bracket, which matters when the actual research question is a dollar figure, not a range. |
| 4 | Rank order | Purchase triggers | Forces a strict ordering of what triggers a purchase, which reveals relative priority in a way a rating scale can't, since ratings let everything cluster at "important." |
| 5 | Constant sum | Channel allocation | Allocates 100 points across purchase channels (in store, online, subscription, and so on), producing a real trade off instead of independent ratings that can all be high at once. |
| 6 | Text entry | Last new brand tried | Open ended recall left unstructured on purpose, so the brand named isn't primed by a predefined list, closer to genuine top of mind recall than a checkbox would give. |
| 7 | Net promoter score | Olipop recommend likelihood | Standard single number loyalty metric anchored to one specific brand, which lets the result sit against known category NPS benchmarks. |
| 8 | Side by side | Olipop vs Poppi can image comparison | Puts the actual scraped product images next to each other so the comparison is visual and immediate, not a comparison of brand names in text. |
| 9 | Multiple choice | Shelf attention priority | Asks which part of the can or label draws attention first, capturing visual attention priority as a ranked choice rather than requiring click coordinate capture. |
| 10 | Text entry | Claude AI interaction and purchase intent | Captures open ended reasoning generated through an actual live conversation with Claude, so the response reflects real dialogue instead of a scripted follow up question. |

## Build notes

Real constraints hit during the build, and the decision made for each.

**Willingness to pay slider.** Qualtrics slider increments don't support native decimal steps at the granularity a price question needs. I built the slider on a cents based integer scale, 0 to 200 in steps of 20, and relabeled the endpoints in dollar terms. The respondent sees a clean price slider; the backend just runs on integers Qualtrics can actually increment.

**Side by side image comparison.** The trial tier in use doesn't include the graphics library upload feature that side by side questions normally pull images from. I hosted the product images in this repo instead and pointed the question's image tool at the raw GitHub URLs. Same visual comparison, different image source, no loss of fidelity.

**Shelf attention priority.** Originally scoped as an image based click question. Same trial tier limitation killed that route: no graphics library upload path for that question type either. I switched it to multiple choice instead. It still captures the same construct, visual attention priority, just as a ranked choice among labeled regions of the can rather than click coordinates on an uploaded image. The measurement goal didn't change, only the input mechanic.

**Constant sum validation.** A constant sum question is only as good as its total. Rather than trust free text entry to sum to 100, I turned on Qualtrics' built in response validation so the question won't submit unless the allocation hits exactly 100 points. That moves the constraint into the platform instead of into the analysis stage.

**AI interactive question.** Building a Custom GPT for the ChatGPT route requires a paid ChatGPT plan. I used Claude instead: Claude's free tier supports a live, in survey conversation without that paywall, so the respondent still has a real AI interaction, not a scripted mockup standing in for one. The experimental goal, an actual conversation rather than a static exchange, is unchanged.

## What this demonstrates

Translating a business question, what actually drives a beverage purchase decision, into ten methodologically distinct instruments that each isolate a different part of that decision: purchase factors, attribute importance, price elasticity, trigger prioritization, channel trade offs, unprompted brand recall, loyalty benchmarking, visual comparison, shelf attention, and live reasoning through dialogue. Every platform constraint hit along the way, the slider increments, the missing graphics library behind two separate questions, the validation logic, the ChatGPT paywall, got solved without cutting what the underlying question was actually designed to measure.
