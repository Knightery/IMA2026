# Slide Specification Format Options

Three candidate formats for specifying every slide in a way an AI agent can parse and turn into actual PowerPoint slides. Each option shows the same three example slides so you can compare directly.

---

## Anatomy of a Slide (from the current deck)

Every slide in the existing deck has a subset of these elements:

| Element | Purpose |
|---|---|
| **section** | Chapter label shown in header (e.g., "Recommendation") |
| **question** | Case question this slide addresses (e.g., "Q5") |
| **badge** | Optional pill tag in top-right (e.g., "Context", "Inference") |
| **title** | Action headline / claim the slide proves |
| **subtitle** | One-sentence elaboration below the title |
| **stat_band** | Horizontal row of 3-4 metric chips spanning the width |
| **panels** | Rectangular content zones (left/right split, cards, etc.) |
| **chart** | Data visualization: line profile, bar, bridge, scatter, risk matrix, timeline |
| **stat_chips** | Label + big-number pairs inside panels |
| **bullets** | Supporting bullet points |
| **table** | Rows x columns with typed cells |
| **cards** | Stacked summary boxes (header + metric + body) |
| **comparison** | Side-by-side panels contrasting two options |
| **exhibit_footer** | Bottom bar with takeaway + methodology note |

---

## OPTION A: YAML Blocks in Markdown

Each slide is a fenced YAML block. Properties are flat where possible, nested where layout demands it. Charts reference data by key name (resolved at build time from the metrics dict). An agent reads top-to-bottom, left-to-right.

### Example: Executive Summary

```yaml
slide: 2
section: "Executive Summary"
title: "Launch a disciplined 5-city organic pilot"
narrative_role: "This is THE answer slide. Everything after it exists to prove it."

recommendation:
  text: "Launch Seattle, Boise, Portland, Spokane, and San Diego first."
  supporting: "These five cities combine premium June pricing, organic readiness, and manageable freight better than a broad national rollout."
  cities: [Seattle, Boise, Portland, Spokane, San Diego]

stats:
  - label: "Avg profit"
    value: "{top5_profit_avg}"
    format: money
  - label: "Avg margin"
    value: "{top5_margin_avg}"
    format: percent
  - label: "Rank-5 gap"
    value: "{rank_gap}"
    format: money

proof_cards:
  - header: "Why these cities"
    metric: "Premium price markets"
    body: "The top five also rank as the strongest June organic price markets in the model."
  - header: "Why the list holds"
    metric: "Same 5 cities"
    body: "The city set does not change in the base, +50%, or -50% freight cases."
  - header: "How to operate it"
    metric: "Pilot before scale"
    body: "Launch narrowly, learn fast, then scale only where margin and service hold."

footer_note: "Model note: each city is scored on the same 20,000-unit scenario using June 2025 price as the June 2026 proxy."
```

### Example: Risk Matrix

```yaml
slide: 35
section: "Risks"
badge: "Inference"
title: "Top risks are freight, competitors, import disruption, and forecast error"
narrative_role: "Show the judge that every threat has been anticipated and ranked."

layout: split
left:
  type: risk_matrix
  axes:
    x: { label: "Probability", low: "Low prob.", high: "High prob." }
    y: { label: "Impact", low: "Low impact", high: "High impact" }
  items:
    - label: "Freight spikes"
      quadrant: high_impact_high_prob
      severity: critical
    - label: "Import disruption"
      quadrant: high_impact_moderate_prob
      severity: critical
    - label: "Forecast error"
      quadrant: moderate_impact_high_prob
      severity: warning
    - label: "Retailer uptake"
      quadrant: moderate_impact_high_prob
      severity: info
    - label: "Spoilage"
      quadrant: moderate_impact_moderate_prob
      severity: info
    - label: "Competitor response"
      quadrant: low_impact_low_prob
      severity: warning

right:
  type: watchlist
  items:
    - risk: "Freight spikes"
      response: "Pre-book core lanes and keep alternates ready before peak season."
    - risk: "Competitor response"
      response: "The 20,000-unit pilot is less than 1% of any target city's organic volume. Monitor but do not overweight."
    - risk: "Import disruption"
      response: "Use flexible grower commitments and staggered sourcing windows."
    - risk: "Forecast error"
      response: "Re-run allocation monthly using realized pilot demand."
```

### Example: Implementation Roadmap

```yaml
slide: 32
section: "Implementation"
title: "Launch in 2026, then scale only what the pilot proves"
subtitle: "Treat year one as a live test of economics, service, and demand quality, not a commitment to broad expansion."
narrative_role: "Convert the analytical recommendation into a concrete time-phased plan."

layout: split
left:
  type: timeline
  label: "ROLLOUT ROADMAP"
  phases:
    - year: "2026"
      name: "Pilot"
      description: "Launch the five-city test and prove realized margin, fill rate, and spoilage control."
      gate: "City economics hold in live execution."
    - year: "2027"
      name: "Expand selectively"
      description: "Add retailer doors only in markets where reorder behavior and service levels remain strong."
      gate: "Economics survive broader coverage."
    - year: "2028"
      name: "Optimize system"
      description: "Tighten grower contracts, allocation logic, and seasonal playbooks around what the pilot confirms."
      gate: "Process gains are repeatable."

right:
  type: checklist
  label: "SCALE ONLY IF"
  items:
    - name: "Margin"
      detail: "Realized margin beats the base case after freight and spoilage."
    - name: "Service"
      detail: "Fill rate holds through peak-season pressure."
    - name: "Demand"
      detail: "Retailers reorder because demand is repeatable, not launch noise."
```

### Pros
- Extremely machine-parseable; any LLM can consume structured YAML without ambiguity.
- Explicit field names mean the rendering agent never guesses what something is.
- Easy to validate: a schema checker can flag missing required fields.

### Cons
- Verbose for simple text-heavy slides.
- Less natural to read/edit for a human collaborating live.
- Chart data references (`{top5_profit_avg}`) require a separate data contract.

---

## OPTION B: Directive Markdown (Zone Blocks)

Each slide uses markdown headings for structure and `:::` fenced blocks (inspired by MyST/Docusaurus) to define typed zones. Properties are inline key-value pairs. Content is natural markdown inside the zone. The rendering agent maps each `:::` block type to a visual element.

### Example: Executive Summary

## Slide 2 | Executive Summary
<!-- narrative_role: This is THE answer slide. Everything after it exists to prove it. -->

### Launch a disciplined 5-city organic pilot

::: recommendation
Launch **Seattle, Boise, Portland, Spokane, and San Diego** first.

These five cities combine premium June pricing, organic readiness, and manageable freight better than a broad national rollout.
:::

::: stats {layout="row"}
- **Avg profit** = `{top5_profit_avg | money}`
- **Avg margin** = `{top5_margin_avg | percent}`
- **Rank-5 gap** = `{rank_gap | money}`
:::

::: card-stack {position="right"}
| Header | Metric | Body |
|---|---|---|
| Why these cities | Premium price markets | The top five also rank as the strongest June organic price markets in the model. |
| Why the list holds | Same 5 cities | The city set does not change in the base, +50%, or -50% freight cases. |
| How to operate it | Pilot before scale | Launch narrowly, learn fast, then scale only where margin and service hold. |
:::

::: footer
Model note: each city is scored on the same 20,000-unit scenario using June 2025 price as the June 2026 proxy.
:::

---

### Example: Risk Matrix

## Slide 35 | Risks | badge: Inference

### Top risks are freight, competitors, import disruption, and forecast error
<!-- narrative_role: Show the judge that every threat has been anticipated and ranked. -->

::: risk-matrix {position="left", x_axis="Probability", y_axis="Impact"}
| Risk | Quadrant | Severity |
|---|---|---|
| Freight spikes | high-impact / high-prob | critical |
| Import disruption | high-impact / mid-prob | critical |
| Forecast error | mid-impact / high-prob | warning |
| Retailer uptake | mid-impact / high-prob | info |
| Spoilage | mid-impact / mid-prob | info |
| Competitor response | low-impact / low-prob | warning |
:::

::: watchlist {position="right"}
- **Freight spikes** -- Pre-book core lanes and keep alternates ready before peak season.
- **Competitor response** -- The 20,000-unit pilot is less than 1% of any target city's organic volume. Monitor but do not overweight.
- **Import disruption** -- Use flexible grower commitments and staggered sourcing windows.
- **Forecast error** -- Re-run allocation monthly using realized pilot demand.
:::

---

### Example: Implementation Roadmap

## Slide 32 | Implementation

### Launch in 2026, then scale only what the pilot proves

> Treat year one as a live test of economics, service, and demand quality, not a commitment to broad expansion.

::: timeline {position="left"}
**2026 -- Pilot**
Launch the five-city test and prove realized margin, fill rate, and spoilage control.
*Gate: City economics hold in live execution.*

**2027 -- Expand selectively**
Add retailer doors only in markets where reorder behavior and service levels remain strong.
*Gate: Economics survive broader coverage.*

**2028 -- Optimize system**
Tighten grower contracts, allocation logic, and seasonal playbooks around what the pilot confirms.
*Gate: Process gains are repeatable.*
:::

::: checklist {position="right", label="SCALE ONLY IF"}
- **Margin** -- Realized margin beats the base case after freight and spoilage.
- **Service** -- Fill rate holds through peak-season pressure.
- **Demand** -- Retailers reorder because demand is repeatable, not launch noise.
:::

---

### Pros
- Most readable for human collaborators; feels like writing a document.
- `:::` block types give the agent clear rendering instructions without leaving markdown.
- Easy to iterate on content without touching structure.

### Cons
- Less strict than YAML; ambiguity possible if a human drifts from conventions.
- The rendering agent needs to parse both markdown and the directive syntax.
- Position/layout is implicit rather than explicit pixel-level.

---

## OPTION C: Layered Specification (Narrative + Blueprint)

Each slide has TWO sections: a **Narrative** layer (what and why -- written in plain English for story flow) and a **Blueprint** layer (exact visual spec in structured format). The narrative layer ensures the story is right before layout is even considered. The blueprint layer gives the rendering agent deterministic instructions.

### Example: Executive Summary

---

### SLIDE 2

**Section:** Executive Summary
**Question:** --
**Narrative Role:** The single most important slide. A judge who reads only this slide should understand the full recommendation and know what evidence follows.

#### NARRATIVE

**Claim:** West Valley should launch organic Hass avocados in five specific cities -- Seattle, Boise, Portland, Spokane, and San Diego -- as a disciplined pilot, not a broad rollout.

**Why it matters:** These cities were selected because premium retail pricing drives more profit than proximity to West Valley's warehouse. The same five cities win under all three freight scenarios (+50%, base, -50%), which means the recommendation is robust. Seasonality gives the pilot a timing advantage if operated correctly.

**What the judge should take away:** The recommendation is specific, data-backed, and stress-tested. It is not "enter the avocado market" -- it is "enter these five cities first, measure, then earn the right to scale."

#### BLUEPRINT

```
layout: left-panel (60%) + right-stack (40%)

LEFT PANEL:
  [label] RECOMMENDATION
  [headline] "Launch Seattle, Boise, Portland, Spokane, and San Diego first."
  [body] "These five cities combine premium June pricing, organic readiness, and manageable freight better than a broad national rollout."
  [badge-row] Seattle | Boise | Portland | Spokane | San Diego
  [stat-row]
    - "Avg profit" = {top5_profit_avg | money}
    - "Avg margin" = {top5_margin_avg | percent}
    - "Rank-5 gap" = {rank_gap | money}

RIGHT STACK (3 cards):
  Card 1: header="Why these cities" metric="Premium price markets"
    "The top five also rank as the strongest June organic price markets in the model."
  Card 2: header="Why the list holds" metric="Same 5 cities"
    "The city set does not change in the base, +50%, or -50% freight cases."
  Card 3: header="How to operate it" metric="Pilot before scale"
    "Launch narrowly, learn fast, then scale only where margin and service hold."

FOOTER:
  "Model note: each city is scored on the same 20,000-unit scenario using June 2025 price as the June 2026 proxy."
```

---

### Example: Risk Matrix

---

### SLIDE 35

**Section:** Risks
**Badge:** Inference
**Narrative Role:** Preempt the judge's skepticism. Show every major threat is catalogued and has a named owner.

#### NARRATIVE

**Claim:** The four biggest risks to the pilot are freight spikes, competitor response, import disruption, and forecast error -- and each already has a countermeasure.

**Why it matters:** A no-speaking deck that presents a recommendation without addressing risk looks naive. The 2x2 matrix ranks threats by probability and impact so the judge sees the team thought about what could go wrong. The watchlist on the right converts each risk into an action.

**What the judge should take away:** This team is not just optimistic about the pilot. They have a contingency playbook.

#### BLUEPRINT

```
layout: split (left 60%, right 40%)

LEFT PANEL:
  [type] risk_matrix (2x2 grid)
  [x-axis] Probability: "Low prob." to "High prob."
  [y-axis] Impact: "Low impact" to "High impact"
  [bubbles]
    "Freight spikes"       -> high-impact, high-prob (critical)
    "Import disruption"    -> high-impact, mid-prob (critical)
    "Forecast error"       -> mid-impact, high-prob (warning)
    "Retailer uptake"      -> mid-impact, high-prob (info)
    "Spoilage"             -> mid-impact, mid-prob (info)
    "Competitor response"  -> low-impact, low-prob (warning)

RIGHT PANEL:
  [label] WATCHLIST
  [items]
    "Freight spikes" -- "Pre-book core lanes and keep alternates ready before peak season."
    "Competitor response" -- "The 20,000-unit pilot is <1% of any target city's organic volume. Monitor but do not overweight."
    "Import disruption" -- "Use flexible grower commitments and staggered sourcing windows."
    "Forecast error" -- "Re-run allocation monthly using realized pilot demand."
```

---

### Example: Implementation Roadmap

---

### SLIDE 32

**Section:** Implementation
**Narrative Role:** Convert the analytical recommendation into a phased execution plan with explicit go/no-go gates.

#### NARRATIVE

**Claim:** The pilot should launch in 2026 and scale only if live data -- margin, service, and reorder behavior -- confirms the model's predictions.

**Why it matters:** Judges want to see that the team does not confuse "the model says yes" with "we should bet everything now." The stage gates force discipline: each phase earns the right to the next.

**What the judge should take away:** This is a learning-first strategy, not a blind expansion plan.

#### BLUEPRINT

```
layout: split (left 70%, right 30%)

LEFT PANEL:
  [label] ROLLOUT ROADMAP
  [timeline - 3 phases, vertical stack]
    Phase 1: year="2026" name="Pilot"
      "Launch the five-city test and prove realized margin, fill rate, and spoilage control."
      Gate: "City economics hold in live execution."
    Phase 2: year="2027" name="Expand selectively"
      "Add retailer doors only in markets where reorder behavior and service levels remain strong."
      Gate: "Economics survive broader coverage."
    Phase 3: year="2028" name="Optimize system"
      "Tighten grower contracts, allocation logic, and seasonal playbooks around what the pilot confirms."
      Gate: "Process gains are repeatable."

RIGHT PANEL:
  [label] SCALE ONLY IF
  [checklist - 3 items]
    "Margin" -- "Realized margin beats the base case after freight and spoilage."
    "Service" -- "Fill rate holds through peak-season pressure."
    "Demand" -- "Retailers reorder because demand is repeatable, not launch noise."
```

---

### Pros
- Forces the author to articulate *why* a slide exists before specifying *what* it shows. This is the strongest storytelling guardrail.
- The narrative layer is a quality check: if you can't write a compelling claim/why/takeaway, the slide shouldn't exist.
- The blueprint layer gives the rendering agent everything it needs without ambiguity.
- The two layers can be reviewed independently: story people review narrative, design people review blueprint.

### Cons
- Most verbose of the three options. Every slide has two full sections.
- Requires discipline to keep narrative and blueprint in sync after edits.
- Overkill for simple appendix/source slides.

---

## Comparison Matrix

| Criterion | A: YAML | B: Directives | C: Narrative + Blueprint |
|---|---|---|---|
| Machine parseability | Best | Good | Good (blueprint is structured) |
| Human readability | Moderate | Best | Good (narrative is prose) |
| Story quality control | None built-in | Minimal (comments) | Built-in (narrative layer) |
| Layout precision | High | Moderate | High (blueprint layer) |
| Editing speed | Moderate | Fast | Slow (two layers per slide) |
| Rendering agent clarity | Best | Good | Best (separate intent from spec) |
| Scales to 40 slides | Clean | Clean | Verbose but thorough |
| Catches bad slides early | No | No | Yes (narrative forces justification) |

## Recommendation

For a **perfect deck with infinite time**, Option C is the right call. The narrative layer is the thing that prevents "slide 17 exists because Q5 has a part (b)" -- instead, every slide must justify itself with a claim, a reason, and a takeaway. The blueprint layer then gives an agent deterministic build instructions.

If you want speed over perfection, Option A is the most agent-friendly. Option B is the best compromise for live human-AI collaboration.
