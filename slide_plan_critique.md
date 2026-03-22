# Critical Review: [new_slide_plan.md](file:///c:/Users/nyter/Downloads/IMA2026/slides/new_slide_plan.md)

This review assumes limited prior case knowledge. Every claim is backed by a quote or line reference from the slide plan.

---

## 1. Slide 1 is doing the work of three slides and will overwhelm on first glance

The cover carries a hero headline, a three-chip stat band, a "DECISION TO PROVE" panel with three bullets, AND a body paragraph AND a footnote:

> ```yaml
> - type: textbox
>   text: "A disciplined 5-city pilot is the right way to enter organic Hass avocados"
>   style: hero headline
> - type: stat_chips  (3 items)
> - type: panel
>   label: "DECISION TO PROVE"
>   bullets: (3 items)
> - type: textbox  (footnote)
> ```
> *(Lines 112–140)*

A judge flipping through 40 slides will spend **3-5 seconds on the cover**. You're asking them to absorb a headline, three stat chips, three proof bullets, and fine-print context in that window. Compare to the reference you cited yourself:

> `past_slide/CRAK.pdf` page 2: best-in-class executive summary layout among the references.
> *(slide_plan.md, line 87)*

CRAK's page 1 is *sparse* — logo, title, one line. The exec summary is page 2. You're collapsing both into one slide.

**Fix:** Strip Slide 1 down to company name + hero headline + one-line scope. Move the stat chips and "DECISION TO PROVE" panel into Slide 2, which is already the exec summary. The cover should make exactly one impression: *"These people are going to tell me to do a disciplined pilot."*

---

## 2. Pillar A is 11 slides (4–14) for what is really two beats — too much real estate for "price picks the cities"

| Section | Slides | Count |
|---------|--------|-------|
| Pillar A | 4–14 | **11** |
| Pillar B | 15–20 | 6 |
| Pillar C | 21–27 | 7 |
| Implementation + Risk | 28–32 | 5 |
| Conclusion | 33–34 | 2 |
| Appendix | 35–40 | 6 |

Pillar A consumes **27.5% of your deck**. The actual analytical work in Pillar A boils down to:
1. LA wins on scale, Seattle wins on penetration (Q1+Q2 — could be 2 slides)
2. Price-volume is moderate pooled, flat within-type (Q3 — 1 slide, maybe 2)
3. Demand drivers are qualitative (Q4 — 1 slide)
4. The profitability model picks the top 5 (Q5 — 2 slides)

That's 6–7 slides of real content, not 11. The bloat comes from:
- **Slide 7** (organic growth context) is a market-framing slide that belongs in the Foundation, not inside a pillar that's supposed to prove "price picks cities." It's actually *moved to the appendix* as Slide 39 AND kept here.
- **Slide 12** (special-order framing) and **Slide 13** (break-even bars) are both proving the same point: "our accounting is sound." One slide with the formula + the break-even bars would be cleaner.
- **Slide 14** (route map) is a nice visual but doesn't advance a new argument — it re-visualizes what Slide 13 already proved.

**Fix:** Compress Pillar A to 7-8 slides. Merge 12+13 into one slide. Move 7 out of the pillar flow (or cut it — Slide 39 in appendix covers the same content). Consider merging 4+5 (both are Q1).

---

## 3. The LA Paradox (Slide 11) makes a demographic claim with no sourced data

> ```yaml
> body: "Seattle and the PNW treat organic avocados as a premium choice, not a staple.
>   Higher household incomes (~$121k median), over 60% college attainment, and
>   concentrated organic retail infrastructure create a buyer who specifically seeks
>   organic and will pay more."
> ```
> *(Lines 451)*

The `$121k median household income` and `60% college attainment` are specific quantitative claims that appear nowhere in [case_comp_data.csv](file:///c:/Users/nyter/Downloads/IMA2026/case_comp_data.csv), [case_full.md](file:///c:/Users/nyter/Downloads/IMA2026/case_full.md), or any question output. Your own [human_required.md](file:///c:/Users/nyter/Downloads/IMA2026/human_required.md) flagged this exact risk:

> *"if you use claims like demographics, food culture, or health orientation, either source them or label them as informed inference so they do not read like hallucinations."*
> *(human_required.md, line 51)*

This slide *does not* carry a badge. The Q4 driver grid on Slide 10 correctly has `badge: "Context"`, but Slide 11 — the slide with the hardest claims — does not.

**Fix:** Either (a) source the income/education figures with a footnote citing Census/ACS data, (b) add a `badge: "Inference"` and soften to "higher household incomes and college attainment" without specific numbers, or (c) replace with data you *do* have — organic share from Q2 and retail price from Q5, which already prove the point without outside data.

---

## 4. The "6:1 price leverage" claim (Slide 19) is presented as a proven ratio but never derived

> ```yaml
> title: "Price leverage outweighs freight leverage by roughly 6:1"
> ```
> *(Line 684)*

> ```yaml
> text: "Q7 answer: price beats freight by {leverage_ratio}x"
> ```
> *(Line 704)*

This ratio is used as a key claim — it appears in the Pillar B card on the roadmap slide too:

> ```yaml
> body: "Q6-Q7: The same five cities win at base, +50%, and -50% freight.
>   Price leverage outweighs shipping by 6:1."
> ```
> *(Line 205)*

But `{leverage_ratio}` is a build-time variable that presumably comes from `q5_sens`. The slide plan never explains what this ratio actually measures. Is it:
- Seattle revenue - LA revenue vs. Seattle shipping - LA shipping?
- Marginal profit impact of 10% price change vs. 10% freight change from the sensitivity analysis?
- Something else?

If a judge asks "where does 6:1 come from?" and your slide says `{leverage_ratio}x`, the answer better be airtight. Right now the slide plan doesn't define the methodology — it just asserts the number.

**Fix:** Add a methodology note to the slide spec or the exhibit footer. Something like: *"Ratio = profit impact of ±10% retail price / profit impact of ±50% shipping, from the sensitivity model."* Even if the rendering agent fills in the variable, the *plan* should show how the claim is constructed.

---

## 5. The "duck curve" is never actually called a duck curve in the final slides

The old [slide_plan.md](file:///c:/Users/nyter/Downloads/IMA2026/slide_plan.md) coined a memorable metaphor:

> *"The key seasonal issue is a real avocado 'duck curve': volume peaks before price peaks"*
> *(slide_plan.md, line 8)*

The new plan's Slide 23 describes the concept in detail:

> ```yaml
> title: "Seasonality should change when West Valley pushes volume vs margin"
> subtitle: "Organic volume peaks in {seasonality.organic.volume_peak} while price
>   peaks in {seasonality.organic.price_peak}; that gap is the operating lever."
> ```
> *(Lines 804-805)*

But the term "duck curve" — which is instantly memorable and gives judges a shorthand to remember your seasonality argument — is never used in any slide title, body, or takeaway. The subtitle describes the timing gap generically instead of branding it.

In a **no-speaking, 40-slide format**, you need language that sticks. A judge reading slide 38 should recall "oh, the duck curve team." Generic operational phrasing won't do that.

**Fix:** Use the term explicitly. Slide 23 title → *"The Avocado Duck Curve: Volume Arrives Before Price"* or similar. Then reference it by name in the seasonal gantt (Slide 24) and the conclusion (Slide 33).

---

## 6. Pillar B (Slides 15-20) is structurally repetitive — three slides say "same 5 cities"

| Slide | Title |
|-------|-------|
| 16 | "+50% freight cuts margin, not the city set" |
| 17 | "-50% freight lifts margin, not the city set" |
| 18 | "The same five cities win in every freight case" |

Slides 16 and 17 each end with `{ label: "Result", value: "Same 5" }`. Then Slide 18 restates the same conclusion with a rank matrix. A judge who understood Slide 16 already knows the punchline of slides 17 and 18.

The information is correct, but the repetition violates your own build rule:

> *"Avoid duplicate exhibits across sections unless the second use adds a clearly different level of insight."*
> *(slide_plan.md, line 47)*

**Fix:** Merge 16+17 into one slide with two scenario columns (base vs. +50% vs. -50%) — the `paired_bar_compare` component already supports multi-scenario visuals. Then Slide 18 becomes the "why" slide (price leverage), and you save a slide for something else or tighten the whole section.

---

## 7. Competitor response is conspicuously underweighted given the case text

The case explicitly says:

> *"The industry is highly competitive, particularly in California's Central Valley"*
> *(case_full.md, line 25)*

Yet in your risk matrix (Slide 31), competitors are placed at:

> ```yaml
> - { label: "Competitor response", quadrant: "low-impact / low-prob", severity: warning }
> ```
> *(Line 1061)*

And the watchlist justification is:

> ```yaml
> - { risk: "Competitor response", response: "The 20,000-unit pilot is less than 1% of
>   any target city's organic volume. Monitor but do not overweight." }
> ```
> *(Line 1067)*

The "less than 1%" argument is valid for volume disruption, but it ignores the *pricing response*. If an incumbent notices a new organic distributor in Seattle and drops their wholesale price by $0.05/unit, your Q5 model breaks — because your model's revenue is based on `40% of forecast retail price`, and retail price is the single variable that matters most in your ranking.

Your own sensitivity analysis (Slide 19) says price leverage outweighs freight 6:1. If price is that dominant, a competitor adjusting prices should be the *highest*-impact risk, not the lowest.

**Fix:** Move competitor response to at least "mid-impact / low-prob" or "mid-impact / mid-prob." Acknowledge the pricing vulnerability and tie your countermeasure to the sensitivity analysis: *"Because price is our dominant variable, West Valley should monitor competitor pricing weekly and have a plan to compete on service and certification, not on price."*

---

## 8. Conclusion Slide 33 re-summarizes Q1-Q9 sequentially — violating the Pyramid Principle you declared

Slide 33's "FINAL ANSWER ARC" panel lists:

> ```yaml
> rows:
>   - { questions: "Q1-Q2", answer: "Los Angeles proves category scale..." }
>   - { questions: "Q3-Q4", answer: "Price matters at market level..." }
>   - { questions: "Q5-Q7", answer: "Seattle, Boise, Portland, Spokane..." }
>   - { questions: "Q8-Q9", answer: "Seasonality changes when..." }
> ```
> *(Lines 1107-1110)*

This is literally "here are the answers to Q1-Q9 in order." Your own [human_required.md](file:///c:/Users/nyter/Downloads/IMA2026/human_required.md) explicitly warned against this:

> *"The winning story is not: 'Here are the answers to nine homework questions.' It is: 'West Valley can enter organic Hass avocados profitably, but only if it treats this as a disciplined learning pilot.'"*
> *(human_required.md, lines 23-29)*

A conclusion slide should restate the **recommendation**, the **three pillars** (in your pillar language, not Q-numbers), and the **key condition**. Referencing Q-numbers in the conclusion is student-assignment framing, not executive framing.

**Fix:** Rewrite the "FINAL ANSWER ARC" rows using pillar language, not Q-numbers:
- "Premium markets, not the biggest markets, generate the strongest pilot economics."
- "That result holds across three freight scenarios because price leverage dominates shipping."
- "A seasonal operating calendar converts timing risk into margin discipline."

Then the DECISION panel (which is already good) closes the slide.

---

## 9. The slide plan has no visual proof of the organic growth market opportunity

Slides 4-5 show revenue trend charts for Q1 (conventional and organic line charts). Slide 7 shows organic growth stats. But **nowhere in the main deck** is there a visual showing organic volume growing faster than total — one of the strongest "why enter now" proof points.

> ```yaml
> # Slide 7
> elements:
>   - type: stat_band  (4 stat chips with text)
>   - type: panel (3 bullets)
>   - type: panel (1 body paragraph)
> ```
> *(Lines 308-324)*

This is 100% text. No chart. No visual at all. The appendix version (Slide 39) has a `custom:growth_bars_and_bridge` visual:

> ```yaml
> - type: custom:growth_bars_and_bridge
>   description: "Left panel: indexed volume growth bars... Right panel: organic share bridge chart..."
> ```
> *(Lines 1287-1288)*

But it's buried in the **appendix**. The market opportunity visual — which should be one of the most compelling visuals in the deck — is in backup while the main deck gets stat chips and bullets.

Your own build rules say:

> *"Favor graph-first slides over text-first slides wherever possible."*
> *(slide_plan.md, line 38)*

**Fix:** Move the `growth_bars_and_bridge` visual into Slide 7 (main deck) and demote the stat chips to supporting elements, or replace Slide 7 with a simple stacked bar (organic vs. conventional volume by year) that makes the growth trajectory obvious in 3 seconds.

---

## Summary: Priority fixes

| # | Issue | Severity | Effort |
|---|-------|----------|--------|
| 1 | Slide 1 overloaded | High | Low — just move elements to Slide 2 |
| 2 | Pillar A bloat (11 slides) | High | Medium — merge 2-3 slides |
| 3 | LA Paradox unsourced demographics | **Critical** — judges will challenge | Low — add badge or remove numbers |
| 4 | 6:1 ratio methodology undefined | Medium | Low — add a footnote |
| 5 | "Duck curve" branding dropped | Medium | Low — add term to titles |
| 6 | Pillar B repetition (3x "same 5") | Medium | Medium — merge slides 16+17 |
| 7 | Competitor risk underweighted | High | Low — adjust risk matrix quadrant |
| 8 | Conclusion uses Q-numbers | **Critical** — violates stated principle | Low — rewrite 4 rows |
| 9 | Market growth has no visual in main deck | High | Low — move appendix chart up |
