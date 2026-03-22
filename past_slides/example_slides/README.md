# Slides That Need a Human Designer

These slides from our 36-slide deck will improve **2x** with human layout work. Each entry names the problem, then points to an example PNG in this folder that shows the target quality level.

---

## Slide 2 — Executive Summary

**Problem:** Currently a stack of disconnected panels (Recommendation panel, stat chips, Decision to Prove panel, 3 cards, footnote). A judge scanning this slide sees 5 separate boxes and has to figure out which one matters most. There's no visual flow connecting recommendation → evidence → impact.

**Reference:** `cbs_exec_summary.png`

CBS chains Challenge → Question → Solution → Impact as one connected vertical flow with arrows. Each box leads visually into the next. The Impact row uses hero KPIs (1705 MWs, 15% IRR, €400M NPV) as the payoff. Our slide needs that same connected-flow treatment instead of floating panels.

Also reference: `kosciusko_exec_summary.png` — shows how to pack recommendation + two named strategy pillars + impact KPIs into one dense-but-scannable slide using clear visual hierarchy (big text for the answer, smaller text for the support).

---

## Slide 6 — Organic Growth Context

**Problem:** The `growth_bars_and_bridge` custom chart is a good idea, but the auto-generated version will likely produce a basic bar chart without the visual storytelling (indexed bars with 2019=100 baseline, bridge chart with 2019 share + gain = 2024 share). The stat band below also repeats the exact numbers the chart shows. A human can make the chart the hero and cut redundant stats.

**Reference:** `cbs_market_selection.png`

CBS uses a donut chart as the visual anchor with radiating callout boxes. For our slide, the human should make the growth/bridge chart the dominant visual (60%+ of the slide area), then use 2 stat chips max as accent, not 4.

---

## Slide 9 — LA vs PNW (The LA Paradox)

**Problem:** This is the most important persuasion slide in Pillar A, but comparison_panels rendered by code will be two flat rectangles with metric lists. The impact comes from the *visual contrast* between the two panels — warm/stress colors on the left (LA losing), cool/primary colors on the right (PNW winning). A human designer can make the contrast visceral: different background fills, metric sizing that draws the eye to the profit gap, and body text that reads like a narrative, not a data dump.

**Reference:** `crak_exec_summary.png`

CRAK's exec summary shows how to use visual weight and color contrast to make the eye go to the right answer first. The "Solution" and "Impact" boxes are larger and bolder than the "Case Ask" box. Our LA panel should feel visually *diminished* while the PNW panel feels *elevated*.

---

## Slide 10 — Special-Order Framing (Profit Formula)

**Problem:** The formula display + 3 cards + textbox + stat chips + bullets is too many elements. A human should turn this into a clean **Inputs → Formula → Output** flow diagram where the formula is the visual centerpiece and the three cost components feed into it like a pipeline.

**Reference:** `crak_tech_explanation.png`

CRAK explains a complex AI system with a simple Inputs → Process → Outputs diagram. Our slide should steal this: Retail Price and Mileage feed in on the left, the profit formula sits in the center as a highlighted box, and the output (city profit ranking) comes out on the right.

---

## Slide 12 — West Coast Cluster Route Map

**Problem:** The `pilot_route_map` auto-generated from x/y coordinates will produce basic dots and lines. A human can turn this into a strategic geography visual like CBS's portfolio allocation slide — the map in the center with city callout boxes radiating outward, each showing the city's key metric (price, margin, role in the cluster).

**Reference:** `cbs_market_selection.png`

CBS surrounds a donut chart with country-specific strategy callouts. Our map should do the same: Seattle callout ("premium price leader, organic share #1"), San Diego callout ("short-haul hedge, 267 miles"), Boise callout ("near-PNW margin, $2.58 retail"), etc. Make the geography carry the strategy.

---

## Slide 14 — Freight Scenarios (Multi-Scenario Bars)

**Problem:** Grouped bars (3 per city × 5 cities = 15 bars) will be dense and hard to read at auto-generated sizing. The key insight is *all bars are essentially the same height* — that's the point. A human can make the visual punchline obvious: minimal height variation across scenarios, with delta labels that are tiny (reinforcing "small change").

**Reference:** `kosciusko_decision_matrix.png`

Kosciusko's decision matrix uses clean column alignment with highlighted cells to make the "winner" obvious at a glance. Our bars should use the same principle: mute the visual variation (because the story is stability, not change) and make the "Same 5" label the hero element.

---

## Slide 20 — The Avocado Duck Curve (Seasonal Calendar Heatmap)

**Problem:** The `seasonal_calendar_heatmap` (12-column month grid, 3 annotation rows, colored zones) is the slide that should be the most *memorable* in the deck. Auto-generated, it'll be a colored table. A human can make it feel like an operational calendar: distinct zone backgrounds, clear posture labels, and a visual "duck curve" shape overlaid on the grid showing the volume-before-price timing gap.

**Reference:** `crak_market_context.png`

CRAK's market landscape uses icons + colored panels in columns to make a contextual overview scannable and visually distinct. Our seasonal calendar should feel equally purposeful — each zone (Volume Build, Price Premium, Off-Peak) should have a distinct visual identity, not just a different shade.

---

## Slide 28 — Risk Matrix

**Problem:** Our 2x2 matrix with 6 risk bubbles will look basic when auto-generated. The reference decks use gradient-colored grids, precisely positioned bubbles, and an adjacent mitigation table — that level of polish requires manual layout.

**Reference:** `kosciusko_risk_heatmap.png`

Kosciusko uses a full 5×5 gradient grid (green → yellow → red) with numbered bubbles. A human should upgrade our 2×2 to at least a 3×3 and position the bubbles precisely. The adjacent watchlist panel needs to align visually with the matrix.

Also reference: `cbs_risk_conclusion.png` — CBS pairs their risk heatmap with a takeaway box that ties risk back to the strategy. Our risk slide should do the same: *"The pilot's small scale (20,000 units) is itself the primary risk mitigant."*

---

## Slide 30 — Conclusion (Final Answer Arc)

**Problem:** The "FINAL ANSWER ARC" panel with 4 rows of pillar/answer pairs is a text table. For the last slide a judge reads before scoring, it needs to feel like a culmination, not a summary table. A human should make the pillar names visually distinct (colored badges or icons), make the DECISION panel dominant, and ensure the stat chips (avg profit, same 5 cities) are the visual payoff.

**Reference:** `cbs_risk_conclusion.png`

CBS's conclusion slide pairs an NPV chart with hero KPIs and 3 strategy callout boxes. The combination of *visual proof* + *numbers* + *strategic framing* is what makes a conclusion stick. Our Slide 30 should pair the rank stability matrix or profit bars with the recommendation restatement, not just list text rows.

---

## Slide 3 — Roadmap / Table of Contents

**Problem:** The 4-column cards layout works textually, but it lacks a visual flow that shows *how* the four sections fit together. A human designer can build this as a "Strategy Map" where the challenges map directly to the four pillars, which then feed into the KPIs.

**Reference:** `ccc_exec_summary.png`

CCC maps "Key Challenges" directly to a "Core Strategy" and right into "KPI Targets." It turns a table of contents into a logical argument. Our Slide 3 should look like a visual equation: Market Reality + City Economics + Freight Hedge + Seasonal Timing = The 5-City Pilot.

---

## Slide 15 — Rank Matrix (Scenario Stability)

**Problem:** A `rank_matrix` generated from our data will literally just be a table saying "Seattle, Boise..." three times across columns. To make the "stability" argument land, it needs check-mark/status styling where the visual repetition *is* the insight.

**Reference:** `orama_comparison_matrix.png`

Orama uses a clean matrix with check-marks and subtle shading to compare initiatives. For our slide, we want the cities down the left, the scenarios (Base, +50%, -50%) across the top, and solid check-marks in every cell to visually hammer home that "Nothing changes."

---

## Slide 21 — Operating Postures (Seasonal Gantt)

**Problem:** Auto-generated timeline lanes can look clunky. We need a clean, professional Jan–Dec monthly calendar view that clearly phases out the "Push Volume," "Protect Margin," and "Stimulate Demand" postures without overwhelming the slide with gridlines.

**Reference:** `edge_implementation_timeline.png`

EDGE's timeline slide uses a very clean top header for months/quarters and precise, colored pill-shapes for the phases. We should steal this exact styling for our seasonal operating Gantt.

---

## Slide 25 — Implementation Roadmap

**Problem:** The 3-year rollout plan (Pilot → Expand → Optimize) needs to look like a committed corporate timeline, not just a list of years. A human designer can integrate the years directly into a "stepping stone" or arrow progression.

**Reference:** `ccc_three_step_solution.png`

CCC uses a phased approach graphic that physically steps up from left to right. Our 3-stage pilot roll-out should use a similar "staircase" or "arrow" visual to show progression from the 2026 test to 2028 optimization.

---

## Slide 26 — Pilot Scorecard

**Problem:** The scorecard is a dense 6-row table mapping KPIs to owners. If not styled well, it will look like an Excel screenshot. It needs clean lines, plenty of whitespace, and subtle row shading to be readable on a screen.

**Reference:** `orama_scorecard_table.png`

Orama's scorecard table is a masterclass in clean table design — no vertical borders, muted header texts, and bolding only the most important values. Our KPI table needs this exact bespoke formatting.

---

## Summary

| Our Slide | What Needs Human Work | Reference Deck |
|-----------|----------------------|----------------|
| **2** (Exec Summary) | Connected visual flow instead of floating panels | CBS / 3A-Kosciusko |
| **3** (Roadmap) | Visual strategy map linking challenges to pillars | CCC Global |
| **6** (Organic Growth) | Chart as hero visual, cut redundant stat band | CBS |
| **9** (LA vs PNW) | Visual contrast — LA diminished, PNW elevated | CRAK |
| **10** (Profit Formula) | Inputs → Formula → Output flow diagram | CRAK |
| **12** (Route Map) | Map with radiating strategy callouts per city | CBS |
| **14** (Freight Scenarios) | Muted variation to emphasize stability | 3A-Kosciusko |
| **15** (Rank Matrix) | Clean check-mark matrix to prove stability | 3B-Orama |
| **20** (Duck Curve Calendar) | Memorable branded visual, distinct zones | CRAK |
| **21** (Operating Gantt) | Clean Jan-Dec month headers with pill timelines | EDGE |
| **25** (Implementation) | Stepping-stone or phased arrow progression | CCC Global |
| **26** (Scorecard) | Ultra-clean table formatting (no vertical borders) | 3B-Orama |
| **28** (Risk Matrix) | Upgrade to gradient grid with precise positioning | 3A-Kosciusko / CBS |
| **30** (Conclusion) | Visual proof paired with KPIs, not a text summary | CBS |
