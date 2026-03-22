# West Valley Hass Avocado Pilot -- 36-Slide Deck Spec

This file is the single source of truth for slide content and story flow.
A rendering agent reads this and produces a rough PPTX using `build_case_deck_pptx.py` helpers.
Human reviewers handle final layout and positioning.

---

## Component Vocabulary

These map directly to `add_*` helper functions in `build_case_deck_pptx.py`.

### Standard Components (reusable across many slides)

| Component | Signature / Purpose |
|---|---|
| `title` | Action headline claim. Every slide has one. |
| `subtitle` | One-sentence elaboration below the title. |
| `badge` | Pill tag in top-right corner (e.g., "Context", "Inference", "Caveat"). |
| `stat_band` | Full-width horizontal row of 3-4 metric columns: label, big number, body text. |
| `stat_chip` | Single label + big value pair inside a panel. |
| `card` | Panel with header (muted label), metric (big text), and body (explanation). |
| `panel` | Rounded rectangle container. Used as a grouping boundary. |
| `bullets` | Bulleted list of 2-4 items. |
| `textbox` | Free-form text block for body copy or annotations. |
| `exhibit_footer` | Bottom bar with colored TAKEAWAY rail + optional methodology note. |
| `ranked_bar_list` | Horizontal bar chart: city label, colored bar, value. Good for rankings. |
| `long_bar_list` | Same as above, different sizing. Used for sensitivity drivers. |
| `generic_table` | Arbitrary table with headers, rows, column widths. |
| `city_metric_table` | Pre-formatted 5-column table: City, Miles, Price, Profit, Margin. |
| `two_series_profile` | Dual-line chart with months on x-axis (seasonality). |
| `multi_line_chart` | Multi-series line chart with years/periods on x-axis (trends). |
| `scatter_plot` | Scatter with auto-regression line, axis labels, optional legend. |
| `pilot_route_map` | Schematic West Coast map with hub + city dots + route lines. |

### Custom Components (one-off or slide-specific)

When a slide needs a visual that doesn't map to a standard helper, describe it as
`custom: <name>` with enough detail for the rendering agent to build it from primitives.

| Custom Component | Used On | Description |
|---|---|---|
| `winner_timeline` | Slide 5 | Horizontal chain of period badges, each with a winner-city badge below and share value. |
| `growth_bars_and_bridge` | Slide 6 | Left: indexed volume growth bars (2019=100). Right: organic share bridge chart. |
| `comparison_panels` | Slide 9 | Side-by-side panels (e.g., LA vs PNW) with metric rows + body paragraphs. |
| `formula_display` | Slide 10 | Centered equation in a highlighted panel. |
| `break_even_bars` | Slide 11 | Horizontal bars showing break-even units vs 20k screen with reference line + MOS labels. |
| `price_miles_scatter` | Slide 13 | Scatter of cities on price (y) vs miles (x) with labeled points and leader lines. |
| `multi_scenario_bars` | Slide 14 | Per-city grouped bars: base vs +50% vs -50% freight, with delta labels. |
| `rank_matrix` | Slide 15 | Table showing identical city rank across base/+50%/-50% scenarios. |
| `allocation_frontier` | Slide 17 | Vertical bars comparing single-city, 2-city, and 5-city allocation profit. |
| `seasonal_calendar_heatmap` | Slide 20 | 12-column month grid with colored zones and 3 annotation rows. |
| `seasonal_gantt` | Slide 21 | Horizontal lanes with month-span bars per operating posture. |
| `numbered_plays` | Slide 23 | Numbered ovals with label + description text per row. |
| `process_flow` | Slide 24 | Numbered step bubbles connected by arrows. |
| `timeline_roadmap` | Slide 25 | Year badges + phase lanes + gate-check panels. |
| `kpi_sidebar` | Slide 26 | Hero KPI list (colored bar + label + body) beside a detailed scorecard table. |
| `stage_gate_rows` | Slide 27 | Rows for each expansion phase with gate conditions and evidence required. |
| `risk_matrix_2x2` | Slide 28 | Probability (x) vs impact (y) grid with positioned risk bubbles. |

---

## Data References

Values in `{curly_braces}` are resolved at build time from the metrics dict produced by
`build_metrics()` in `build_case_deck_pptx.py` (which calls `outputs/solve_case.py`).

Common references:
- `{top5_profit_avg}` -- average profit across the recommended 5 cities
- `{top5_margin_avg}` -- average margin across the recommended 5 cities
- `{rank_gap}` -- profit gap between rank 5 and rank 6
- `{growth_org}` / `{growth_total}` -- organic vs total volume growth 2019-2024
- `{share_2019}` / `{share_2024}` -- organic share of total volume
- `{q1}` through `{q7r}` -- question-level DataFrames
- `{season_raw}` / `{seasonality}` -- seasonality analysis outputs
- `{entry_screen}` -- Q5 full city profitability screen
- `{q5_cvp}` -- break-even / CVP analysis per city
- `{q5_sens}` -- sensitivity analysis (price/volume/shipping drivers)
- `{q5_alloc}` -- allocation frontier scenarios
- `{conv_trend}` / `{org_trend}` -- yearly revenue trend by city

---

## Build Rules

1. Every slide title is an action claim, not a topic label.
2. Favor graph-first slides over text-first slides wherever possible.
3. Avoid duplicate exhibits across sections unless the second use adds a clearly different insight.
4. `badge: "Inference"` must appear on any slide that uses data or claims not in the case materials.
5. `exhibit_footer` should carry the single-sentence takeaway a judge remembers after moving on.

---

## Story Structure

**Main recommendation (stated on Slide 2, proven by Slides 4-30):**
West Valley should launch a 20,000-unit organic Hass avocado pilot in five cities --
Seattle, Boise, Portland, Spokane, and San Diego.

**Deck flow:**

| Section | Claim / Purpose | Slides | Case Questions |
|---|---|---|---|
| Market Context | The market is real but uneven -- size and premium diverge | 4-7 | Q1, Q2, Q3 |
| Pillar A | Premium pricing, not market size, picks the right cities | 8-12 | Q4, Q5 |
| Pillar B | The recommendation survives freight shocks | 13-17 | Q5, Q6, Q7 |
| Pillar C | Seasonality is an operating advantage, not just a risk | 18-24 | Q8, Q9 |
| Implementation + Risk | Concrete plan with gates, KPIs, and risk countermeasures | 25-29 | -- |
| Conclusion | Restate the recommendation with all pillars proven | 30-31 | -- |
| Appendix | Backup exhibits, caveats, and sources | 32-36 | -- |

---

## Slides

---

### SLIDE 1 -- Cover

```yaml
section: ~
title: "A disciplined 5-city pilot is the right way to enter organic Hass avocados"
role: "First impression. One headline, one identity. The judge should absorb the recommendation in under three seconds."

elements:
  - type: textbox
    label: "WEST VALLEY FRESH DISTRIBUTION COMPANY"
    style: muted overline

  - type: textbox
    text: "A disciplined 5-city pilot is the right way to enter organic Hass avocados"
    style: hero headline

  - type: textbox
    text: "Prepared as an anonymized submission for the 2026 IMA Student Case Competition. The deck is designed to stand alone without speaker notes."
    style: muted footnote
```

---

### SLIDE 2 -- Executive Summary

```yaml
section: "Executive Summary"
title: "Launch a disciplined 5-city organic pilot"
role: "THE answer slide. A judge who reads only this slide should understand the full recommendation, the scope, and the three pillars that prove it."

elements:
  - type: panel
    label: "RECOMMENDATION"
    headline: "Launch Seattle, Boise, Portland, Spokane, and San Diego first."
    body: "These five cities combine premium June pricing, organic readiness, and manageable freight better than a broad national rollout."
    city_badges: [Seattle, Boise, Portland, Spokane, San Diego]

  - type: stat_chips
    items:
      - { label: "Avg profit", value: "{top5_profit_avg}", fmt: money }
      - { label: "Avg margin", value: "{top5_margin_avg}", fmt: percent }
      - { label: "Rank-5 gap", value: "{rank_gap}", fmt: money }

  - type: panel
    label: "DECISION TO PROVE"
    headline: "Win the right five cities first, then earn the right to scale."
    bullets:
      - "Price support beats raw market size."
      - "The top cities hold through freight shocks."
      - "Seasonality changes how the pilot should run."

  - type: cards
    items:
      - header: "Why these cities"
        metric: "Premium price markets"
        body: "The top five also rank as the strongest June organic price markets in the model."
        color: primary
      - header: "Why the list holds"
        metric: "Same 5 cities"
        body: "The city set does not change in the base, +50%, or -50% freight cases."
        color: compare
      - header: "How to operate it"
        metric: "Pilot before scale"
        body: "Launch narrowly, learn fast, then scale only where margin and service hold."
        color: accent

  - type: textbox
    text: "Scope: 20,000 organic units | 40 city markets screened | 2019-2025 HAB data | Model note: June 2025 price used as June 2026 proxy."
    style: muted footnote
```

---

### SLIDE 3 -- Roadmap

```yaml
section: "Roadmap"
title: "Four sections prove the recommendation"
role: "Preview the deck structure so the judge knows what is coming and why."

elements:
  - type: cards
    layout: horizontal, 4 columns
    items:
      - header: "Market Context"
        metric: "The market is real but uneven"
        body: "Q1-Q3: LA dominates total sales. Seattle leads organic penetration. Price is a signal but not sufficient by itself."
        color: muted
        slides: "4-7"
      - header: "Pillar A"
        metric: "Price picks the cities"
        body: "Q4-Q5: Demographics and channel fit explain why premium markets beat scale markets. The profitability model picks the top five."
        color: primary
        slides: "8-12"
      - header: "Pillar B"
        metric: "Freight doesn't change the answer"
        body: "Q6-Q7: The same five cities win at base, +50%, and -50% freight. Price leverage outweighs shipping by ~6:1."
        color: compare
        slides: "13-17"
      - header: "Pillar C"
        metric: "Seasonality is an advantage"
        body: "Q8-Q9: Volume peaks before price -- the duck curve. Three operating postures let the pilot exploit seasonal timing."
        color: accent
        slides: "18-24"

  - type: stat_band
    items:
      - { label: "Then", value: "Implementation", body: "Slides 25-29: timeline, KPIs, stage gates, risk map." }
      - { label: "Finally", value: "Conclusion", body: "Slides 30-31: full answer arc and strategic implications." }
      - { label: "Backup", value: "Appendix", body: "Slides 32-36: data tables, model caveats, sources." }
```

---

### SLIDE 4 -- Q1: LA leads, but organic competition is tighter

```yaml
section: "Market Context"
question: Q1
title: "Los Angeles leads dollar sales, but the organic race is much closer"
role: "Establish the scale leader, then immediately show the gap narrows in organic. This is the first signal that pilot choice can diverge from raw market size."

elements:
  - type: multi_line_chart
    layout: side-by-side
    left:
      data: "{conv_trend}"
      series: [Los Angeles, New York, DallasFtWorth, BaltimoreWashington, PhoenixTucson]
      subtitle: "Top 5 conventional revenue trend"
      y_axis: "$M"
    right:
      data: "{org_trend}"
      series: [Los Angeles, New York, Seattle, San Francisco, BaltimoreWashington]
      subtitle: "Top 5 organic revenue trend"
      y_axis: "$M"

  - type: stat_chips
    items:
      - { label: "Conv. winner cells", value: "14/14 LA" }
      - { label: "Org. 2024 LA-NY gap", value: "{la_2024_org - ny_2024_org}", fmt: money }
      - { label: "Seattle enters top 5", value: "Organic only" }

  - type: exhibit_footer
    takeaway: "LA dominates conventional. In organic, the lead shrinks and Seattle enters the picture -- first sign that size and premium diverge."
```

---

### SLIDE 5 -- Q2: Seattle leads organic penetration

```yaml
section: "Market Context"
question: Q2
title: "Seattle leads organic penetration in most periods"
role: "Introduce the real premium leader. Seattle's organic share leadership is the first quantitative signal that premium markets differ from scale markets."

elements:
  - type: custom:winner_timeline
    data: "{q2}"
    description: "Horizontal chain of 7 period badges (2019-2025H1), each with the winning city badge below and its organic share percentage. Seattle highlighted in primary color, others in compare/accent."

  - type: stat_band
    items:
      - { label: "Most frequent leader", value: "Seattle", body: "Wins 5 of the 7 measured periods and is the clearest indicator of organic readiness.", highlight: true }
      - { label: "Best one-year share", value: "Orlando 12.87%", body: "Orlando peaks in 2022, but it does not sustain the same multi-period lead." }
      - { label: "Current H1 leader", value: "Charlotte 9.45%", body: "Charlotte leads 2025 H1, showing that penetration leadership is not static." }
```

---

### SLIDE 6 -- Market context: organic growth

```yaml
section: "Market Context"
title: "Organic is growing fast but still niche"
role: "Bridge between market observation and city selection. Growth justifies entry; small share justifies being selective about where."

elements:
  - type: custom:growth_bars_and_bridge
    description: "Left panel: indexed volume growth bars (2019=100, total vs organic, showing organic nearly doubling). Right panel: organic share bridge chart (2019 share + share gain = 2024 share)."

  - type: stat_band
    items:
      - { label: "Organic volume growth", value: "+{growth_org}%", body: "Organic nearly doubled from 2019 to 2024.", highlight: true }
      - { label: "Total volume growth", value: "+{growth_total}%", body: "Overall Hass market expanded at a much slower pace." }
      - { label: "2019 organic share", value: "{share_2019}%", body: "Started from a small base." }
      - { label: "2024 organic share", value: "{share_2024}%", body: "Direction is clear, but share is still modest." }

  - type: exhibit_footer
    takeaway: "Growth is real enough to justify entry. Scale is still small enough that city choice matters. That favors a pilot, not a broad launch."
```

---

### SLIDE 7 -- Q3: Price-volume relationship

```yaml
section: "Market Context"
question: Q3
title: "Price matters at the market level but explains little within each type"
role: "Close market context by showing price is a signal but not a sufficient selection criterion. This sets up Pillar A: we need something beyond price to choose cities."

elements:
  - type: scatter_plot
    layout: side-by-side
    left:
      data: "{q3_points}"
      label: "ALL OBSERVATIONS (POOLED)"
      x: avg_price
      y: total_volume
      color_by: Type (conventional = primary, organic = compare)
      regression: true
      stat_chips: [{ label: "Pearson r", value: "{q3_all_r}" }, { label: "R-squared", value: "{q3_all_r2}" }]
    right:
      data: "{q3_points}"
      label: "WITHIN-TYPE (CONV | ORG)"
      description: "Two regressions overlaid -- conventional and organic separately -- both nearly flat."
      stat_chips: [{ label: "Conv r", value: "{q3_conv_r}" }, { label: "Org r", value: "{q3_org_r}" }]

  - type: exhibit_footer
    takeaway: "Q3 answer: a correlation of about -0.43 pooled means higher-priced markets sell fewer units, but within each type the relationship is nearly flat. Local market structure does the rest."
```

---

### SLIDE 8 -- Q4: Demand drivers

```yaml
section: "Pillar A -- Price Picks the Cities"
question: Q4
badge: "Context"
title: "Demand depends on demographics, channel fit, proximity, and competitive intensity"
role: "Qualitative framework explaining why the quantitative results from Q1-Q3 cluster the way they do."

elements:
  - type: custom:driver_grid
    layout: 2x2 grid of panels
    items:
      - title: "Demographics + income"
        body: "Higher-income, wellness-oriented households are more likely to treat organic avocados as a premium grocery choice rather than a commodity staple."
        color: primary
      - title: "Retail + foodservice infrastructure"
        body: "Whole Foods-style organic retail, co-ops, prepared foods, and food-service pull all raise the odds that organic turns quickly at premium price points."
        color: compare
      - title: "Proximity + freshness perception"
        body: "Nearness to California and Mexican supply can help availability, but it can also make avocados feel ubiquitous and price-competitive instead of premium."
        color: primary_soft
      - title: "Competition + market saturation"
        body: "Large incumbent avocado markets can be harder first-entry markets because competitive density compresses price even when category demand is high."
        color: accent

  - type: textbox
    text: "Q4 answer: Los Angeles proves scale, but premium demand depends on who buys organic, where they shop, how supply is perceived, and how crowded the market already is."
    style: bold panel
```

---

### SLIDE 9 -- Q4: Biggest market != best first market

```yaml
section: "Pillar A -- Price Picks the Cities"
question: Q4
badge: "Inference"
title: "The biggest market is not the best first market"
role: "The punchline of Pillar A's market analysis. LA vs PNW head-to-head proves the principle."

elements:
  - type: custom:comparison_panels
    left:
      label: "WHY LA LOSES THE PILOT"
      fill: warm
      metrics:
        - { label: "June price", value: "${la.forecast_retail_price}", color: stress }
        - { label: "Organic share", value: "{la.organic_share}%", color: compare }
        - { label: "Revenue on 20K", value: "${la.Revenue}", color: stress }
        - { label: "Profit on 20K", value: "${la.Profit}", color: stress }
        - { label: "Profit rank", value: "{la.profit_rank} of 40", color: stress }
      body: "Los Angeles sells more avocados than any other U.S. city. But that scale compresses pricing. Avocados are a commodity in LA, ubiquitous in retail and foodservice, supported by massive nearby supply. The same competitive density that creates volume prevents premium pricing for a new entrant."
    right:
      label: "WHY THE PACIFIC NORTHWEST WINS"
      fill: cool
      metrics:
        - { label: "June price", value: "${sea.forecast_retail_price} (Seattle)", color: primary }
        - { label: "Organic share", value: "{sea.organic_share}% (Seattle)", color: compare }
        - { label: "Revenue on 20K", value: "${sea.Revenue}", color: primary }
        - { label: "Profit on 20K", value: "${sea.Profit}", color: primary }
        - { label: "Profit rank", value: "{sea.profit_rank} of 40", color: primary }
      body: "Seattle and the PNW treat organic avocados as a premium choice, not a staple. Higher household incomes, strong organic retail infrastructure (co-ops, Whole Foods density), and consistent organic share leadership from Q2 create a buyer who specifically seeks organic and will pay more."

  - type: textbox
    text: "You do not launch a premium product in the city with the highest total consumption. You launch where buyers already pay a premium and actively seek it out."
    style: bold takeaway
```

---

### SLIDE 10 -- Q5: Special-order framing

```yaml
section: "Pillar A -- Price Picks the Cities"
question: Q5
title: "This is a special-order decision, not a full P&L"
role: "Frame the accounting logic. Judges at an IMA competition need to see you understand relevant-cost analysis."

elements:
  - type: custom:formula_display
    formula: "Profit(Q) = Q x (0.40 x retail price - $0.20) - ($1,500 + $50 x miles / 100)"

  - type: cards
    layout: horizontal, 3 columns
    items:
      - { header: "RELEVANT REVENUE", metric: "40% of retail", body: "The case gives one June price proxy, so revenue is modeled consistently across cities.", color: primary }
      - { header: "VARIABLE COST", metric: "$0.20 / avocado", body: "Acquisition is the true per-unit cost in the screen.", color: compare }
      - { header: "ROUTE-FIXED COST", metric: "$1,500 + distance", body: "Shipping behaves like a route cost paid once per destination.", color: accent }

  - type: textbox
    text: "Because the case assumes idle capacity and no extra overhead, this is a textbook special-order screen: accept if incremental contribution covers route cost, then optimize city choice."

  - type: stat_chips
    items:
      - { label: "City screens positive", value: "{all_positive}/40" }
      - { label: "Lowest profit", value: "{min_profit}", fmt: money }
      - { label: "Decision rule", value: "Optimize city mix" }

  - type: bullets
    items:
      - "All 40 cities clear the special-order hurdle, so the question is not whether to sell. It is where the economics are strongest."
      - "Idle capacity makes existing overhead irrelevant, which is why this is a relevant-cost screen rather than a full absorption-costing exercise."
```

---

### SLIDE 11 -- Q5: Top 5 ranking + break-even

```yaml
section: "Pillar A -- Price Picks the Cities"
question: Q5
title: "Top-five markets break even at only 12%-14% of planned volume"
role: "Show both the ranking result AND the margin of safety in one slide. Combines the most important outputs of Q5."

elements:
  - type: custom:break_even_bars
    data: "{q5_cvp}.head(5)"
    description: "Horizontal bars showing break-even units per city vs the 20,000-unit screen, with a vertical reference line at 20k. Each bar labeled with MOS %."

  - type: stat_chips
    items:
      - { label: "Best break-even", value: "{min_break_even_units}", fmt: units }
      - { label: "Worst break-even", value: "{max_break_even_units}", fmt: units }
      - { label: "Break-even retail range", value: "${min_be_price}-${max_be_price}" }

  - type: bullets
    items:
      - "Seattle breaks even at roughly 2.3k units; Spokane, the weakest of the five, still breaks even at only 2.7k."
      - "That means every recommended city has an 86%+ margin of safety under the screen assumptions."
```

---

### SLIDE 12 -- Q5: West Coast cluster + route map

```yaml
section: "Pillar A -- Price Picks the Cities"
question: Q5
title: "The recommendation is a West Coast cluster"
role: "Visualize the geography. Show this is one coherent logistics system, not five disconnected bets."

elements:
  - type: badge_row
    cities: [Seattle, Boise, Portland, Spokane, San Diego]

  - type: pilot_route_map
    cities:
      - { name: "Seattle", x_pct: 0.18, y_pct: 0.14 }
      - { name: "Portland", x_pct: 0.22, y_pct: 0.34 }
      - { name: "Spokane", x_pct: 0.70, y_pct: 0.22 }
      - { name: "Boise", x_pct: 0.62, y_pct: 0.42 }
      - { name: "San Diego", x_pct: 0.36, y_pct: 0.86 }

  - type: stat_chips
    items:
      - { label: "Avg miles", value: "{top5_avg_miles}" }
      - { label: "Avg price", value: "${top5_avg_price}" }
      - { label: "Low-mile hedge", value: "San Diego" }

  - type: bullets
    items:
      - "This is one coherent western lane system, not five disconnected bets."
      - "The Northwest supplies the premium; San Diego supplies the short-haul hedge."
      - "That makes the recommendation operational, not just analytical."
```

---

### SLIDE 13 -- Q5 bridge to Pillar B: Price beats proximity

```yaml
section: "Pillar B -- Freight Doesn't Change the Answer"
question: Q5
title: "Price support beats proximity"
role: "Bridge slide. Transitions from 'which cities' to 'how robust is this under freight stress' by showing the selected cities are NOT the closest ones."

elements:
  - type: custom:price_miles_scatter
    data: "{entry_screen} -- selected 5 cities + 4 nearest non-selected"
    x: Mileage_miles
    y: forecast_retail_price_jun2026
    color: primary for selected, compare for nearby alternatives
    description: "Scatter with city labels and leader lines. Selected cities cluster top-right (far but expensive). Nearby alternatives cluster bottom-left (close but cheap)."

  - type: stat_chips
    items:
      - { label: "Selected avg price", value: "${selected_avg_price}" }
      - { label: "Nearby alt. avg price", value: "${nearby_avg_price}" }

  - type: bullets
    items:
      - "The winners are not simply the closest cities."
      - "Nearby alternatives give back the freight edge through weaker pricing."
      - "San Diego is the hedge that keeps the cluster grounded."
```

---

### SLIDE 14 -- Q6: Freight shocks change margin, not the city set

```yaml
section: "Pillar B -- Freight Doesn't Change the Answer"
question: Q6
title: "Freight shocks change margin, not the city set"
role: "Both stress tests in one view. The judge sees +50% and -50% freight alongside the base case and concludes the same five cities survive."

elements:
  - type: custom:multi_scenario_bars
    data: "{q7r}.head(5)"
    columns:
      - { key: Profit_base, label: "Base case", color: primary }
      - { key: Profit_up50, label: "+50% freight", color: stress }
      - { key: Profit_down50, label: "-50% freight", color: compare }
    description: "Per-city grouped bars (3 bars per city) for the top 5 cities. Delta labels between base and each scenario."

  - type: stat_chips
    items:
      - { label: "Base avg margin", value: "{base_margin_avg}", fmt: percent }
      - { label: "+50% avg margin", value: "{up_margin_avg}", fmt: percent }
      - { label: "-50% avg margin", value: "{down_margin_avg}", fmt: percent }
      - { label: "City set change", value: "None" }

  - type: bullets
    items:
      - "+50% freight compresses average margin from ~70% to ~65%. The pilot still holds because price support outruns the freight shock."
      - "-50% freight lifts margin to ~75%. Use that upside to fund service and trade support, not to chase more cities."
      - "In both cases the same five cities win in the same order."
```

---

### SLIDE 15 -- Q6-Q7: Rank matrix

```yaml
section: "Pillar B -- Freight Doesn't Change the Answer"
title: "The same five cities win in every freight case"
role: "Visual proof of robustness. Zero rank changes across three scenarios."

elements:
  - type: custom:rank_matrix
    data: "{q7r}.head(5)"
    columns: ["Rank", "Base", "+50%", "-50%"]
    description: "All three scenario columns show the same city in the same order: Seattle, Boise, Portland, Spokane, San Diego."

  - type: stat_chips
    items:
      - { label: "Rank changes", value: "0" }
      - { label: "Selected set", value: "Same 5 cities" }

  - type: bullets
    items:
      - "Base, upside, and downside freight all return the same five cities in the same order."
      - "That is the cleanest proof that the recommendation is structurally stable."
      - "The next slide shows why: price support wins the tie-break."
```

---

### SLIDE 16 -- Q7: Price leverage vs freight leverage

```yaml
section: "Pillar B -- Freight Doesn't Change the Answer"
question: Q7
title: "Price leverage outweighs freight leverage by roughly 6:1"
role: "The analytical explanation for WHY the cities don't change: revenue delta between Seattle and LA dwarfs the freight delta."

elements:
  - type: long_bar_list
    layout: side-by-side
    left:
      data: "{q5_sens} filtered to Seattle city screen"
      subtitle: "Seattle 20k city screen"
      description: "Bars showing profit impact per sensitivity driver (price, volume, shipping, acquisition)"
    right:
      data: "{q5_sens} filtered to 5-city equal pilot"
      subtitle: "5-city equal pilot"

  - type: stat_chips
    items:
      - { label: "Seattle-LA revenue gap", value: "{price_gap_revenue}", fmt: money }
      - { label: "Seattle freight hit", value: "{shipping_hit}", fmt: money }

  - type: textbox
    text: "Q7 answer: price beats freight by {leverage_ratio}x, so shipping shocks compress margin without reordering the top five."
    style: bold

  - type: exhibit_footer
    takeaway: "Price leverage dominates because the revenue gap between premium and commodity markets is structurally larger than any plausible freight swing."
    note: "Ratio = profit impact of ±10% retail price / profit impact of ±50% shipping cost, from the Q5 sensitivity model."
```

---

### SLIDE 17 -- Q7: City selection vs allocation

```yaml
section: "Pillar B -- Freight Doesn't Change the Answer"
question: Q7
title: "City selection and unit allocation are different accounting decisions"
role: "Close Pillar B by distinguishing the city screen (where to go) from the allocation question (how to split units). Shows the learning premium."

elements:
  - type: custom:allocation_frontier
    data: "{q5_alloc}"
    description: "3 vertical bars: max-profit single market, balanced 2-city split, 5-city learning pilot. Shows declining profit but increasing learning value."

  - type: stat_chips
    items:
      - { label: "Single-city max", value: "{max_case_profit}", fmt: money }
      - { label: "5-city pilot", value: "{learning_profit}", fmt: money }
      - { label: "Learning premium", value: "-{max - learning}", fmt: money }

  - type: bullets
    items:
      - "A balanced Seattle-Boise split still earns strong economics with less concentration risk."
      - "The five-city pilot is a learning investment: lower profit than one city, but more retailer signal and less single-market exposure."
      - "That is why city screening and exact unit allocation should be presented as separate accounting decisions."
```

---

### SLIDE 18 -- Q8: Prices peak in July

```yaml
section: "Pillar C -- Seasonality Is an Advantage"
title: "Prices reach their high point in July"
role: "Open Pillar C with the price seasonality finding. Summer is when premium markets pay the most."

elements:
  - type: two_series_profile
    data: "{season_raw}"
    metric: mean_price
    series_a: Conventional
    series_b: Organic
    y_label: "Mean monthly price"
    value_fmt: "${:.2f}"

  - type: stat_chips
    items:
      - { label: "Conventional peak", value: "{seasonality.conventional.price_peak}" }
      - { label: "Organic peak", value: "{seasonality.organic.price_peak}" }

  - type: bullets
    items:
      - "Conventional price peaks in October while organic peaks in July."
      - "The gap means timing strategy must differ by product type."
      - "Organic's summer premium is the window West Valley should protect."
```

---

### SLIDE 19 -- Q8: Volume peaks in January

```yaml
section: "Pillar C -- Seasonality Is an Advantage"
title: "Volume peaks months before price does"
role: "Show the timing mismatch that creates the duck-curve operating problem."

elements:
  - type: two_series_profile
    data: "{season_raw}"
    metric: mean_volume
    series_a: Conventional
    series_b: Organic
    y_label: "Volume"
    value_fmt: "{:,.0f}"

  - type: stat_chips
    items:
      - { label: "Conventional peak", value: "{seasonality.conventional.volume_peak}" }
      - { label: "Organic peak", value: "{seasonality.organic.volume_peak}" }

  - type: bullets
    items:
      - "Organic volume peaks in January while conventional peaks in May."
      - "Both soften into November, which is why off-peak demand support matters."
      - "Volume timing and price timing do not line up, creating the duck-curve operating problem."
```

---

### SLIDE 20 -- Q8: The Avocado Duck Curve

```yaml
section: "Pillar C -- Seasonality Is an Advantage"
question: Q8
badge: "Inference"
title: "The Avocado Duck Curve: volume arrives before price"
subtitle: "Organic volume peaks in {seasonality.organic.volume_peak} while price peaks in {seasonality.organic.price_peak}; that gap is the operating lever."
role: "Synthesize price and volume seasonality into a branded, memorable decision framework."

elements:
  - type: custom:seasonal_calendar_heatmap
    months: [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
    zones:
      - { months: "Jan-May", color: primary_soft, label: "Volume build" }
      - { months: "Jun-Sep", color: accent, label: "Price premium" }
      - { months: "Oct-Dec", color: compare, label: "Off-peak" }
    rows:
      - { label: "Volume signal", description: "seasonal flow annotation per month" }
      - { label: "Price signal", description: "seasonal price annotation per month" }
      - { label: "Operating posture", description: "action per season" }
    description: "12-column month grid with 3 rows, each cell colored by season zone. Shows when to push volume, protect margin, or stimulate demand."
```

---

### SLIDE 21 -- Q9: The duck curve requires three operating postures

```yaml
section: "Pillar C -- Seasonality Is an Advantage"
question: Q9
badge: "Inference"
title: "The duck curve requires three distinct operating postures"
role: "Prescriptive answer to Q9. Translate the timing data into clear operational rules."

elements:
  - type: custom:seasonal_gantt
    months: [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
    lanes:
      - name: "Push volume"
        period: "Jan-May"
        color: primary
        note: "Keep shelves full while baseline demand is strongest."
      - name: "Protect margin"
        period: "Jul-Sep"
        color: accent
        note: "Hold price in the summer premium window."
      - name: "Stimulate demand"
        period: "Nov-Feb"
        color: compare
        note: "Use trade support when demand and price soften."

  - type: exhibit_footer
    takeaway: "Q9 answer starts with timing: assign one clear commercial job to each season so weak months do not get misread as weak markets."
```

---

### SLIDE 22 -- Q9: Grower contracts

```yaml
section: "Pillar C -- Seasonality Is an Advantage"
question: Q9
badge: "Inference"
title: "Growers need flex contracts, cold-chain discipline, and backup lanes"
subtitle: "Build seasonality discipline into contracts and execution rules before the pilot scales."
role: "First of three Q9 stakeholder prescriptions. Grower-facing."

elements:
  - type: generic_table
    headers: ["Lever", "How it should work", "Critical operating move", "Why it matters"]
    col_widths: [1.9, 1.9, 4.15, 3.47]
    rows:
      - ["Contract tiers", "Base + flex volume", "Lock a stable base commitment, then layer in seasonal flex volume so supply can expand without year-round overcommitment.", "Prevents the pilot from buying peak-season optionality with permanent fixed cost."]
      - ["Cold-chain readiness", "Protect service", "Tighten transit monitoring, storage discipline, and receiving checks during the months when flow is highest.", "Spoilage and service misses can erase good city economics faster than freight swings do."]
      - ["Alternate lanes", "Reduce disruption", "Pre-qualify backup carriers and routes before the peak season so lane shocks do not force reactive reallocations.", "The pilot should never have to choose between service and margin because a lane fails."]

  - type: textbox
    text: "Contract base volume, protect the cold chain, and pre-book fallback lanes before peak flow starts."
    style: bold operating rule
```

---

### SLIDE 23 -- Q9: Trade associations

```yaml
section: "Pillar C -- Seasonality Is an Advantage"
question: Q9
badge: "Inference"
title: "Trade associations should protect off-peak retailer demand"
subtitle: "Aim off-peak support at buyers, trade calendars, and food-service pull, not generic consumer messaging alone."
role: "Second Q9 stakeholder prescription. Trade-association and retailer-facing."

elements:
  - type: custom:numbered_plays
    items:
      - { number: "1", label: "Retail promo calendar", body: "Concentrate retailer ads, features, and display support in Nov-Feb when baseline turns are softest.", color: primary }
      - { number: "2", label: "Food-service channels", body: "Lean harder on restaurants, prepared foods, and institutional buyers when retail pull weakens.", color: compare }
      - { number: "3", label: "Trade funds + slotting", body: "Use trade dollars, temporary allowances, and slotting support to win attention in soft months.", color: accent }
      - { number: "4", label: "Shelf discipline", body: "Coordinate assortment, facing, and freshness standards so promotions convert to repeat orders.", color: stress }

  - type: stat_chips
    items:
      - { label: "Softest months", value: "Nov to Feb" }
      - { label: "Primary buyer", value: "Retail + FS" }

  - type: bullets
    items:
      - "Do not mistake seasonal softness for launch failure."
      - "Push through buyer calendars, not just consumer media."
      - "Separate repeat demand from promo-driven lift."

  - type: card
    header: "Execution rule"
    metric: "Front-load trade support"
    body: "Spend trade dollars and retailer attention in Nov-Feb, not when summer demand is already doing the work."
```

---

### SLIDE 24 -- Q9: Monthly S&OP

```yaml
section: "Pillar C -- Seasonality Is an Advantage"
question: Q9
badge: "Inference"
title: "Monthly S&OP should align growers, West Valley, and retailers"
subtitle: "One monthly forum should translate market signals into volume, routing, and promotion decisions."
role: "Close Pillar C with the coordination mechanism. Third Q9 stakeholder prescription."

elements:
  - type: cards
    layout: horizontal, 3 columns
    items:
      - { header: "Growers", metric: "Supply commitment", body: "Provide base volume, flex capacity, and harvest timing updates.", color: primary }
      - { header: "West Valley", metric: "Control tower", body: "Convert price, freight, and demand signals into city allocation decisions.", color: compare }
      - { header: "Retailers", metric: "Demand signal", body: "Feed promo calendars, replenishment risk, and reorder visibility into the review.", color: accent }

  - type: custom:process_flow
    steps:
      - { number: "1", label: "Forecast demand" }
      - { number: "2", label: "Lock commitments" }
      - { number: "3", label: "Allocate by city" }
      - { number: "4", label: "Review margin + service" }

  - type: stat_band
    items:
      - { label: "Cadence", value: "Monthly", body: "Update commitments and allocations every month, not quarterly." }
      - { label: "Decision output", value: "Commit + allocate", body: "Reset grower volume, lanes, and promo timing in the same review." }
      - { label: "Success signal", value: "Margin and service", body: "Higher realized margin should not come with fill-rate or freshness slippage." }
```

---

### SLIDE 25 -- Implementation: Rollout roadmap

```yaml
section: "Implementation"
title: "Launch in 2026, then scale only what the pilot proves"
subtitle: "Treat year one as a live test of economics, service, and demand quality, not a commitment to broad expansion."
role: "Concrete time-phased execution plan with go/no-go gates."

elements:
  - type: custom:timeline_roadmap
    phases:
      - year: "2026"
        name: "Pilot"
        description: "Launch the five-city test and prove realized margin, fill rate, and spoilage control."
        gate: "City economics hold in live execution."
        color: primary
      - year: "2027"
        name: "Expand selectively"
        description: "Add retailer doors only in markets where reorder behavior and service levels remain strong."
        gate: "Economics survive broader coverage."
        color: compare
      - year: "2028"
        name: "Optimize system"
        description: "Tighten grower contracts, allocation logic, and seasonal playbooks around what the pilot confirms."
        gate: "Process gains are repeatable."
        color: accent

  - type: panel
    label: "SCALE ONLY IF"
    checklist:
      - { name: "Margin", detail: "Realized margin beats the base case after freight and spoilage." }
      - { name: "Service", detail: "Fill rate holds through peak-season pressure." }
      - { name: "Demand", detail: "Retailers reorder because demand is repeatable, not launch noise." }
```

---

### SLIDE 26 -- Implementation: KPIs

```yaml
section: "Implementation"
title: "Pilot KPIs should prove margin, service, spoilage, and repeat orders"
role: "Define what success looks like. Judges want to see measurement discipline."

elements:
  - type: custom:kpi_sidebar
    hero_kpis:
      - { name: "Gross margin", body: "Proof that premium pricing survives live execution.", color: primary }
      - { name: "Fill rate", body: "Proof that service can scale without breaking.", color: compare }
      - { name: "Reorder rate", body: "Proof that demand repeats after launch week.", color: accent }

  - type: generic_table
    label: "PILOT SCORECARD"
    headers: ["KPI", "Why it matters", "Cadence / owner"]
    col_widths: [2.0, 3.35, 1.6]
    rows:
      - ["Realized gross margin", "Confirms whether forecast economics survive live execution.", "Weekly / finance"]
      - ["Freight per unit", "Shows whether routing and carrier discipline are improving.", "Weekly / logistics"]
      - ["Fill rate", "Measures retailer execution quality during seasonal peaks.", "Weekly / operations"]
      - ["Spoilage rate", "Captures cold-chain and freshness failures directly.", "Weekly / operations"]
      - ["Reorder rate", "Tests whether demand is repeatable beyond launch.", "Monthly / commercial"]
      - ["Forecast accuracy", "Shows whether monthly S&OP is improving allocation decisions.", "Monthly / planning"]
```

---

### SLIDE 27 -- Implementation: Stage gates

```yaml
section: "Implementation"
title: "Scale should follow stage gates, not geography ambition"
subtitle: "The model can choose where to test, but scale should still depend on live pilot evidence."
role: "Reinforce that the pilot earns the right to expand, not the other way around."

elements:
  - type: custom:stage_gate_rows
    description: "Rows for each expansion phase with gate conditions and evidence required."
    gates:
      - { phase: "Pilot cities", condition: "Live margin matches or exceeds model forecast", evidence: "Weekly P&L by city" }
      - { phase: "Add doors in pilot cities", condition: "Reorder rate proves demand is repeatable", evidence: "Monthly retailer scorecards" }
      - { phase: "New cities", condition: "Service and margin hold at broader coverage", evidence: "Quarterly review with grower and logistics partners" }

  - type: exhibit_footer
    takeaway: "Use the pilot to validate economics and service before adding geography."
    note: "The model is strong enough to choose where to test, not yet strong enough to dictate exact retailer-level allocation."
```

---

### SLIDE 28 -- Risk: Impact/probability map

```yaml
section: "Risks"
badge: "Inference"
title: "Top risks are freight, competitors, import disruption, and forecast error"
role: "Preempt the judge's skepticism. Show every major threat is catalogued and ranked."

elements:
  - type: custom:risk_matrix_2x2
    axes:
      x: { label: "Probability", low: "Low prob.", high: "High prob." }
      y: { label: "Impact", low: "Low impact", high: "High impact" }
    risks:
      - { label: "Freight spikes", quadrant: "high-impact / high-prob", severity: critical }
      - { label: "Import disruption", quadrant: "high-impact / mid-prob", severity: critical }
      - { label: "Competitor response", quadrant: "mid-impact / mid-prob", severity: warning }
      - { label: "Forecast error", quadrant: "mid-impact / high-prob", severity: warning }
      - { label: "Retailer uptake", quadrant: "mid-impact / high-prob", severity: info }
      - { label: "Spoilage", quadrant: "mid-impact / mid-prob", severity: info }

  - type: panel
    label: "WATCHLIST"
    items:
      - { risk: "Freight spikes", response: "Pre-book core lanes and keep alternates ready before peak season." }
      - { risk: "Competitor response", response: "Because price is the dominant profit driver (~6:1 over freight), West Valley should monitor competitor pricing weekly and compete on service and certification, not on price." }
      - { risk: "Import disruption", response: "Use flexible grower commitments and staggered sourcing windows." }
      - { risk: "Forecast error", response: "Re-run allocation monthly using realized pilot demand." }
```

---

### SLIDE 29 -- Risk: Countermeasure table

```yaml
section: "Risks"
title: "Each major risk already has a countermeasure"
subtitle: "Every major threat should already have a response and owner before West Valley scales."
role: "Convert the risk map into an actionable response plan."

elements:
  - type: generic_table
    headers: ["Risk", "Trigger", "Countermeasure", "Owner"]
    col_widths: [2.2, 2.8, 4.0, 2.85]
    rows:
      - ["Freight spikes", "Fuel surcharges or carrier capacity shortage during peak season", "Pre-book core lanes 60 days out; maintain 2 alternate carriers per route", "Logistics"]
      - ["Competitor entry", "National distributor undercuts pricing in pilot cities", "Compete on service and organic certification, not on price; monitor competitor pricing weekly", "Commercial"]
      - ["Import disruption", "Tariff, border delay, or phytosanitary hold on Mexican supply", "Stagger sourcing windows; maintain local California grower fallback", "Supply chain"]
      - ["Forecast error", "Demand materially above or below the 20k screen", "Re-run allocation model monthly with realized demand data", "Finance / planning"]
      - ["Spoilage", "Cold-chain failure or transit damage exceeds 3% threshold", "Tighten receiving standards; add real-time temperature logging", "Operations"]
```

---

### SLIDE 30 -- Conclusion: Full answer arc

```yaml
section: "Conclusion"
title: "The full case supports a disciplined 5-city pilot, not a broad organic rollout"
role: "Restate the recommendation with all three pillars proven. This is the slide a judge reads last before scoring."

elements:
  - type: panel
    label: "FINAL ANSWER ARC"
    rows:
      - { pillar: "Market reality", answer: "Los Angeles proves category scale, while Seattle proves organic readiness. The biggest market is not the best first market." }
      - { pillar: "City selection", answer: "Premium pricing, demographics, and channel fit pick the top five. The profitability model confirms Seattle, Boise, Portland, Spokane, and San Diego." }
      - { pillar: "Freight resilience", answer: "The same five cities win at base, +50%, and -50% freight because price leverage dominates shipping by ~6:1." }
      - { pillar: "The duck curve", answer: "Seasonality changes when West Valley should push volume, protect margin, and stimulate demand. The pilot needs a coordinated seasonal operating calendar." }

  - type: panel
    label: "DECISION"
    headline: "Launch Seattle, Boise, Portland, Spokane, and San Diego first."
    stat_chips:
      - { label: "Avg profit", value: "{top5_profit_avg}", fmt: money }
      - { label: "Freight result", value: "Same 5 cities" }
    body: "This is a learning-first pilot with positive economics, explicit sensitivities, and a seasonal operating plan. Scale only if live margin, service, and reorder data confirm the screen."

  - type: textbox
    text: "Do not treat the city screen as a full allocation plan. Use the pilot to earn that next decision."
    style: bold callout
```

---

### SLIDE 31 -- Conclusion: Strategic implications

```yaml
section: "Conclusion"
title: "What this pilot teaches West Valley applies to every new product line"
role: "Elevate beyond avocados. Show the judge this team thinks strategically, not just analytically."

elements:
  - type: cards
    layout: horizontal, 3 columns
    items:
      - header: "Analytical discipline"
        metric: "Screen, then pilot"
        body: "Use comparable-unit screens to choose markets, then use live pilots to validate before scaling. This approach works for any perishable product."
        color: primary
      - header: "Accounting rigor"
        metric: "Relevant costs only"
        body: "Special-order framing, sensitivity analysis, and CVP give West Valley a repeatable toolkit for incremental product decisions."
        color: compare
      - header: "Operational readiness"
        metric: "Seasonal S&OP"
        body: "The monthly review cadence, stage gates, and KPI framework can be reused for any product with seasonal supply-demand timing gaps."
        color: accent

  - type: textbox
    text: "West Valley does not just enter avocados. It builds the decision-making infrastructure to evaluate and launch any new produce line with the same rigor."
    style: bold takeaway
```

---

### SLIDE 32 -- Appendix: Full 40-city ranking

```yaml
section: "Appendix"
question: Q5
title: "All 40 cities pass the special-order test; the top five maximize profit"
role: "Backup exhibit for judges who want to see the full ranking."

elements:
  - type: ranked_bar_list
    data: "{q5}.sort_values('Profit', ascending=False).head(10)"
    subtitle: "Top 10 city profit ranking"
    description: "Top 5 in primary color, next 5 in muted. Bar width proportional to profit."

  - type: stat_chips
    items:
      - { label: "Top-5 avg", value: "{top5_profit_avg}", fmt: money }
      - { label: "Next-5 avg", value: "{next5_profit_avg}", fmt: money }
      - { label: "Rank-5 vs rank-6 gap", value: "{rank_gap}", fmt: money }

  - type: bullets
    items:
      - "All 40 markets are positive; the cut line chooses the best five."
      - "Top-five profit averages $13.7k versus $9.2k for the next tier."
      - "That makes the recommendation an optimization call, not a generic yes."
```

---

### SLIDE 33 -- Appendix: Entry screen leaderboard

```yaml
section: "Appendix"
question: Q5
title: "Seattle screens first because premium pricing outweighs Los Angeles's freight edge"
role: "Detailed table for judges who want to see the city-level math."

elements:
  - type: generic_table
    label: "ENTRY SCREEN LEADERBOARD"
    headers: ["City", "Price", "Organic share", "Miles", "Profit", "Pilot"]
    data: "{entry_screen}.sort_values('Profit', ascending=False).head(8)"
    description: "Top 8 cities with all key metrics. Selected cities marked."

  - type: panel
    label: "WORKED CITY EXAMPLE"
    description: "Seattle step-by-step calculation: Revenue, Acquisition, Shipping, Profit."
    lines:
      - { label: "Revenue", value: "20,000 x (40% x ${seattle.price}) = ${seattle.Revenue}" }
      - { label: "Acquisition", value: "20,000 x $0.20 = $4,000" }
      - { label: "Shipping", value: "$1,500 + ($50 x {seattle.miles} / 100) = ${seattle.Shipping}" }
      - { label: "Profit", value: "${seattle.Revenue} - $4,000 - ${seattle.Shipping} = ${seattle.Profit}" }

  - type: textbox
    text: "Los Angeles ranks 8th at only 111 miles because its $1.87 retail price cannot close the revenue gap."
    style: callout
```

---

### SLIDE 34 -- Appendix: Sensitivity detail

```yaml
section: "Appendix"
question: Q7
title: "Price leverage outweighs freight leverage by roughly 6:1"
role: "Backup for the Q7 answer showing the full sensitivity bars."

elements:
  - type: long_bar_list
    layout: side-by-side
    left:
      data: "{q5_sens} filtered to Seattle city screen"
      subtitle: "Seattle 20k city screen"
    right:
      data: "{q5_sens} filtered to 5-city equal pilot"
      subtitle: "5-city equal pilot"

  - type: textbox
    text: "For the one-city screen, a volume miss is the biggest downside. Once West Valley splits 20,000 units across five destinations, repeated route-fixed shipping makes freight much more material."
```

---

### SLIDE 35 -- Appendix: Model caveats

```yaml
section: "Appendix"
badge: "Caveat"
title: "The model can now separate city choice from allocation economics"
role: "Intellectual honesty. Show what the model can and cannot defend."

elements:
  - type: panel
    label: "What we can defend now"
    bullets:
      - "The cleaned dataset resolves to 40 city markets even though the case text references 41 metro regions."
      - "The comparable 20,000-unit city screen is still the right way to choose where to test because every market is evaluated on the same basis."
      - "All 40 city screens remain profitable even at +50% shipping, so the recommendation is an optimization problem, not a survival problem."

  - type: panel
    label: "What still needs more data"
    bullets:
      - "2025 is partial-year data only and June 2025 retail price is used as the simple proxy for June 2026 retail price."
      - "The model now quantifies split-allocation trade-offs, but it still does not include shrink, retailer-level demand curves, or route-level service costs."
      - "That means the deck can defend city selection and portfolio logic now, but not exact retailer-by-retailer allocation yet."

  - type: textbox
    label: "NEXT DATA TO COLLECT"
    text: "Pilot reorder behavior, lane-level spoilage, and retailer response would move West Valley from screen-level economics to exact allocation and account-level planning."
```

---

### SLIDE 36 -- Appendix: Sources and assumptions

```yaml
section: "Appendix"
title: "Appendix: sources, assumptions, and backup exhibits"
role: "Credibility and transparency. Standard appendix close."

elements:
  - type: panel
    label: "Primary sources"
    bullets:
      - "case_full.md and case_context.md (IMA 2026 case materials)"
      - "case_comp_data.csv (HAB weekly sales data, Jan 2019 - Jun 2025)"
      - "outputs/question_1.md through outputs/question_9.md"
      - "Q5-Q7 profitability scenario CSVs"
      - "Q8 seasonality CSVs and charts"

  - type: panel
    label: "Core assumptions"
    bullets:
      - "20,000-unit comparable city scorecards"
      - "June 2025 retail price used as June 2026 proxy"
      - "Wholesale price modeled at 40% of retail"
      - "$0.20 acquisition cost per avocado"
      - "Shipping = $1,500 fixed + $50 per 100 miles"

  - type: panel
    label: "Backup exhibits available"
    bullets:
      - "Winner matrix and city trend lines"
      - "Growth/share bridge and elasticity visuals"
      - "Selection matrix, frontier zoom, and freight sensitivity"
      - "Seasonality price and volume charts"
      - "Model caveats and implementation stage gates"

  - type: textbox
    text: "Use this appendix to answer questions on data scope, scenario assumptions, seasonality, or why the five-city recommendation stays stable under freight stress."
    style: muted footnote
```
