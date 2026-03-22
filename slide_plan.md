# Detailed Slide Plan (Max 40 Slides)

## Working Answer the Deck Should Prove
- West Valley should enter the organic Hass avocado market through a **disciplined 5-city pilot**, not a broad rollout.
- The recommended cities are **Seattle, Boise, Portland, Spokane, and San Diego**.
- Under the current model, the top five remain unchanged in the base case, **shipping +50%**, and **shipping -50%** scenarios.
- The most important reason the ranking stays stable is that **local retail price support drives wholesale revenue more strongly than shipping swings change rank order**.
- The key seasonal issue is a real avocado "duck curve": **volume peaks before price peaks**, so timing matters for margin capture.

## Evidence We Already Have
- Filtered analysis window: **January 7, 2019 to June 29, 2025**
- Rows used in the cleaned analysis set: **27,120**
- Weekly timestamps: **339**
- Distinct city markets in the supplied data: **40**
- Product types: **conventional** and **organic**
- Case text says **41 metro regions**, but the supplied dataset resolves to **40 city markets** after cleaning. Treat this as a transparent data caveat, not something to hide.
- Q1: **Los Angeles wins every required period in both conventional and organic dollar sales**.
- Q2: **Seattle wins 5 of 7 periods** for organic share; **Orlando** wins 2022 and **Charlotte** wins 2025 H1.
- Q3: pooled price-volume relationship is **moderate negative** with **Pearson r = -0.427** and **R2 = 0.183**.
- Q3 nuance: within type, the relationship is weak:
  - Conventional: **r = -0.026**
  - Organic: **r = -0.044**
- Q5 base-case top five average profit: **$13,725.90**
- Q5 base-case top five average margin: **69.75%**
- Q5 base-case rank-5 vs rank-6 profit gap: **$1,007.00**
- Q6 top five average profit under shipping +50%: **$12,772.85**
- Q6 top five average margin under shipping +50%: **64.88%**
- Q6 top five average profit under shipping -50%: **$14,678.95**
- Q6 top five average margin under shipping -50%: **74.61%**
- Q8 seasonal anchors:
  - Conventional price peak: **July**
  - Organic price peak: **July**
  - Conventional volume peak: **May**
  - Organic volume peak: **January**
  - Low-volume month for both: **November**

## Non-Negotiable Build Rules
- Favor **graph-first slides** over text-first slides wherever possible.
- Use **charts as the main content**, with only a short takeaway sentence beside or below the chart.
- All figures must be rendered in the **Executive Avocado** palette. Do not use default plotting colors.
- Rebuild any legacy chart that still looks generic or disconnected from the theme.
- Avoid long blockquotes, long captions, or stacked text blocks that risk pushing content off-screen.
- Keep titles concise enough to preserve vertical space.
- Use conclusion-style slide titles whenever possible.
- Because the deck must stand alone without speaker notes, every slide should answer one clear question in a way that survives skimming.
- Do not let a generic markdown heading compete with a stronger chart title. Use **one dominant title system per slide**.
- Avoid duplicate exhibits across sections unless the second use adds a clearly different level of insight.
- Eliminate framework or process slides that do not carry evidence. If a slide is not proving something, it should probably be cut.
- Strip out non-essential chrome such as repeated footer labels, decorative pills, or quotes that do not add analysis.
- When a slide is qualitative, label it explicitly as **context** or **inference**, not measured output.
- Keep all stated facts consistent with the cleaned model, especially the **40-city dataset caveat** and the **2025 H1 partial-year caveat**.

## Learnings from `past_slide/` Reference Decks
- The strongest reference baseline for this case is **CBS + Team-2 Canada + Drake + 3A/3B**, not the more marketing-led decks. These references are better models for analytical, decision-led case storytelling.
- Use **EDGE / CCC / CRAK** selectively for visual energy, named-solution architecture, implementation packaging, and process/mockup slides, but do not let style outrun proof.
- Build the deck around **5-7 repeatable slide archetypes**, not bespoke one-off layouts on every page.
- The core archetypes we should support are:
  - `exec_summary`
  - `chart_plus_takeaway`
  - `split_chart_plus_screen`
  - `decision_matrix`
  - `proposal_table_with_assumptions`
  - `timeline_or_stage_gate`
  - `risk_matrix_with_owner`
  - `before_after_process`
- Most slides should have **one dominant object**: one chart, one matrix, one roadmap, one table, or one hero metric block. If a second object exists, its hierarchy must be obvious.
- Use **conclusion-first titles** on nearly every slide. Topic labels are weaker than direct claims.
- Keep a disciplined grid: **2-column layouts beat 4-quadrant clutter** for most main-deck pages.
- Support text should stay lean: **2-3 proof points** or a short takeaway box is usually enough.
- Add a compact **"how to read this" / assumptions / takeaway** panel on denser slides instead of surrounding the exhibit with paragraphs.
- Use **tables only when exact values matter**. If the point is ranking, comparison, or prioritization, prefer bars, matrices, or cards.
- Reserve accent color for the **recommended option, winning row, or one critical emphasis state**. Do not spread highlight styling everywhere.
- Use section chrome sparingly. A section band or breadcrumb is acceptable, but **logos, nav rails, footer labels, and decorative dividers must earn their space**.
- Use transition slides sparingly. If a divider does not add meaning, cut it.
- Executive summary slides should show the **recommendation, 3 proof pillars, and 2-4 anchor KPIs** in one scan.
- Implementation slides are strongest when they combine **timeline + KPIs + risks/mitigations** in one integrated page instead of splitting them into weak standalone slides.
- Risk slides should map **risk -> action -> owner**, not just list threats.
- Conclusion slides should restate the answer with **hard numbers, the proof pillars, and the operating discipline required to make the recommendation work**.
- Appendix slides should be curated and readable, not compressed dumps of every backup table.

## Reference Slide Examples Worth Borrowing
- `past_slide/3A-Kosciusko-Consulting.pdf` page 2: strong recommendation-first executive summary with impact visible immediately.
- `past_slide/3A-Kosciusko-Consulting.pdf` page 7: good winning-row decision matrix pattern.
- `past_slide/3B-Orama.pdf` page 6: strong table slide because the proposal banner and assumptions box explain how to read it.
- `past_slide/CBS_2025_Final_Cleaned_Up.pdf` pages 5-6: strong market-selection and allocation logic for recommendation slides.
- `past_slide/CBS_2025_Final_Cleaned_Up.pdf` page 12: good risk slide because mitigation is tied to structure, not left as an afterthought.
- `past_slide/CRAK.pdf` page 2: best-in-class executive summary layout among the references.
- `past_slide/CRAK.pdf` page 14: strong implementation page combining rollout logic and must-win battles.
- `past_slide/Drake-Consulting.pdf` page 4: good analysis-slide model with one main chart and short takeaways.
- `past_slide/EDGE-Consulting.pdf` page 2: useful reference for hero metrics and headline hierarchy, but not for quantitative rigor.
- `past_slide/Team-2_Canada-1.pdf` pages 13-15: good pattern for finance summary, implementation, and conclusion packaging.

## Lessons from Slides 1-25
- The deck reads best when the **visual itself carries the answer** and the caption only reinforces it.
- Early foundation slides should still be **data-led**, not methodology-led. Judges do not need a tour of the deck.
- For full-slide exhibit pages, the chart title is often enough; adding a second generic markdown title wastes vertical space.
- The strongest recommendation slides pair **exact economics** with one clean interpretation, rather than a stack of multiple claims.
- Qualitative matrices are acceptable for context, but they should never sit beside quantitative charts as if they are equally rigorous.
- Silent decks need each slide to survive a three-second skim: answer first, evidence second, caveat third.
- If a caveat matters for credibility, state it once clearly and keep it consistent everywhere rather than letting conflicting numbers appear.

## Modeling Caveats We Should State Explicitly
- **2025 is partial-year data (H1 only)** and should not be treated as a full-year comparison period.
- The Q5-Q7 profitability work uses **June 2025 organic retail price** as a simple forecast for **June 2026 retail price**.
- Planned wholesale price is modeled as **40% of forecast retail price**.
- Acquisition cost is modeled as **$0.20 per avocado**.
- Shipping is modeled as **$1,500 fixed + $50 per 100 miles**.
- The current city ranking logic uses a **comparable 20,000-unit city scorecard** for selection, which is useful for prioritization but is **not yet a full allocation model** for the single 20,000-unit order.
- Under the current assumptions, **all 40 city scenarios remain profitable even when shipping rises 50%**. That means the recommendation is about **optimizing city choice**, not proving only five markets are viable.
- Do **not** overclaim price elasticity. The pooled relationship is meaningful, but within-type relationships are weak.

## Revised Narrative
1. Start with the decision.
2. Frame the market as large, growing, seasonal, and uneven across cities.
3. Show that Los Angeles dominates sales, while Seattle dominates organic penetration.
4. Show that price matters at the market level, but market mix matters more than simple price alone.
5. Prove that the Pacific Northwest plus San Diego is the best disciplined pilot set.
6. Show that the recommendation survives freight volatility.
7. End with seasonality, implementation discipline, risk management, and what data would improve the next decision.

## Section 1: Foundation (Slides 1-5)

| # | Draft Headline | Why This Slide Exists | Primary Visual | Data / Files | Must Show / Caution |
| --- | --- | --- | --- | --- | --- |
| 1 | Entering the Organic Hass Avocado Market With Disciplined Pilot Economics | Establish the case, tone, and anonymity requirements immediately. | Cover slide with abstract avocado-ring / contour motif only. | Case brief only. | No school name or logo. Keep this clean and premium. |
| 2 | A 5-City Pilot Offers High Margins and Survives Freight Shocks | Put the answer first so the rest of the deck feels like proof, not exploration. | Executive summary slide with 3 proof pillars and the 5-city list. | `outputs/question_5.md`, `outputs/question_6.md`, `outputs/question_7.md` | Mention the exact cities and the fact that the top five do not change across base, +50%, and -50% shipping scenarios. |
| 3 | Seasonality Creates a Timing Gap Between Volume and Price | Define the core seasonal problem visually, not verbally. | Dual chart slide: monthly volume on left, monthly price on right. | `outputs/q8_seasonality_volume.png`, `outputs/q8_seasonality_price.png`, `outputs/q8_seasonality_peaks.csv` | The key message is simple: organic volume peaks in January, conventional in May, but price peaks in July for both. Keep the text short and avoid jargon-heavy labeling. |
| 4 | Organic Is Growing Faster Than the Total Hass Market, but It Is Still a Small Share | Give the market opportunity slide real quantitative weight. | New themed stacked bar, indexed line, or waterfall showing 2019 vs 2024 organic vs total volume growth. | Build from `outputs/cleaned_data_2019_to_2025H1.csv` or directly from `case_comp_data.csv` via the same logic in `outputs/solve_case.py` | Use the actual numbers: total volume +32.8%, organic volume +89.3%, organic share 4.15% to 5.91% from 2019 to 2024. |
| 5 | The Pilot Screen Should Be Price Support, Organic Readiness, and Route Efficiency | End the foundation section by showing the three filters that the evidence will test. | Three-card or three-metric proof slide using already-established numbers. | Pull from `outputs/question_5.md`, `outputs/question_6.md`, `outputs/question_7.md`, and `outputs/q2_organic_share_winners.csv` | This should be evidence-backed, not a generic process slide. Use exact metrics, not broad bullet points. |

## Section 2: Data Exploration & Market Analysis (Slides 6-15)

| # | Draft Headline | Why This Slide Exists | Primary Visual | Data / Files | Must Show / Caution |
| --- | --- | --- | --- | --- | --- |
| 6 | Los Angeles Leads Dollar Sales in Every Required Period and in Both Types | Q1 should open with the clearest possible answer. | Rebuilt winner matrix or heatmap showing all 14 winner cells. | `outputs/q1_winners_long.csv`, `outputs/q1_winners.csv` | Los Angeles wins all required periods in both conventional and organic. This is the cleanest Q1 proof slide. |
| 7 | Conventional Sales Leadership Is Structural, Not a One-Year Spike | Show that Los Angeles is not just a one-off leader in conventional. | New top-5 city line or clustered bar chart by year for conventional sales. | Build from `outputs/cleaned_data_2019_to_2025H1.csv` and `outputs/q1_winners_long.csv` | Call out that Los Angeles beats New York by roughly $46M to $70M in full-year conventional revenue, and by $22.5M in 2025 H1. |
| 8 | Organic Sales Leadership Is Consistent, but the Gap Is Much Narrower | Separate the organic story from conventional rather than merging both into an unreadable chart. | New top-5 city line or clustered bar chart by year for organic sales. | Build from `outputs/cleaned_data_2019_to_2025H1.csv` and `outputs/q1_winners_long.csv` | Los Angeles still leads, but the gap to New York is much smaller than in conventional: about $0.2M to $3.1M depending on year. |
| 9 | Seattle Leads Organic Penetration in Most Periods | Q2 is not about total sales; it is about organic mix. | Dot plot, ranked strip, or compact timeline of the Q2 winners. | `outputs/q2_organic_share_winners_raw.csv`, `outputs/q2_organic_share_winners.csv` | Seattle wins 5 of 7 periods. Orlando leads 2022 at 12.87%. Charlotte leads 2025 H1 at 9.45%. |
| 10 | Organic Share Has Expanded Even Though It Remains a Niche Slice of the Total Market | Use the requested organic-vs-total growth visual here, where it supports Q2 better than the foundation section. | Waterfall, stacked columns, or share bridge showing organic volume growth relative to total volume growth from 2019 to 2024. | Build from `outputs/cleaned_data_2019_to_2025H1.csv` | Keep this on share growth, not raw scale alone. The important numbers are +89.3% organic volume growth and organic share rising from 4.15% to 5.91%. |
| 11 | At the Market Level, Higher Prices Generally Coincide With Lower Volume | This is the main Q3 visual answer. | Reuse the themed scatter with regression line. | `outputs/q3_price_volume_scatter.png`, `outputs/q3_price_volume_metrics.csv` | State the relationship clearly: moderate inverse, not perfect. |
| 12 | Within Product Type, Price Alone Explains Very Little | This is the nuance slide that protects us from overclaiming elasticity. | New coefficient comparison, two-panel scatter, or compact stats visual. | `outputs/q3_price_volume_metrics_raw.csv`, `outputs/q3_city_year_type_agg.csv` | Use the actual numbers: conventional `r = -0.026`, organic `r = -0.044`. This slide should explicitly say that mix and market structure matter more than price alone. |
| 13 | Four Risks Run Through the Profit Model and Three Are Tested Later | Begin Q4 with a macro frame that ties directly to the accounting model rather than feeling like a generic PESTLE slide. | Four-card risk bridge tied to modeled inputs and later tests. | `case_context.md`, `case_full.md`, `outputs/question_4.md`, `outputs/question_6.md`, `outputs/question_8.md` | Each card should say whether the risk is directly modeled, tested later, or still a disclosed limitation. |
| 14 | The Biggest Market Is Not the Best First Market | Turn Q4 into the LA paradox slide: why Los Angeles proves demand exists but still loses to Seattle / the Pacific Northwest in the pilot model. | Two-panel comparison: LA loses the pilot vs PNW wins. | `outputs/question_4.md`, `outputs/q5_city_profitability_base.csv`, `outputs/q5_june2025_city_prices.csv`, `outputs/q2_organic_share_winners.csv` | Use model outputs plus clearly labeled inference. The point is not that LA is weak; it is that premium pricing and organic readiness matter more than raw scale for first entry. |
| 15 | The Best Entry Markets Need Price Power, Organic Readiness, and Manageable Miles | Bridge from analysis into recommendation. | Entry leaderboard table with explicit LA paradox bridge sentence in the side panel. | `outputs/q5_city_profitability_base.csv`, `outputs/q5_june2025_city_prices.csv` | The slide must explicitly say that Los Angeles ranks only 8th despite being nearby because price support is too weak. |

## Section 3: Strategic Recommendations (Slides 16-25)

| # | Draft Headline | Why This Slide Exists | Primary Visual | Data / Files | Must Show / Caution |
| --- | --- | --- | --- | --- | --- |
| 16 | This Is a Special-Order Decision, Not a Full P&L | Before ranking cities, frame the case correctly as a relevant-cost / idle-capacity screen rather than a generic profit table. | Relevant-cost formula slide with contribution logic and decision rule. | `case_context.md`, `outputs/question_5.md`, `outputs/q5_city_profitability_base.csv` | Make the accounting explicit: relevant revenue, variable acquisition cost, route-fixed shipping cost, and the fact that all 40 city screens are profitable. |
| 17 | Top-Five Markets Break Even at Only 12%-14% of Planned Volume | Add real CVP logic so the recommendation has break-even and margin-of-safety support, not just ranking support. | Break-even volume bars vs the 20,000-unit screen. | `outputs/q5_cvp_metrics.csv` | Show that the top five clear route-fixed cost very early and have 86%+ margin of safety under the screen assumptions. |
| 18 | All 40 Cities Pass the Special-Order Test; the Top Five Maximize Profit | Show that the recommendation is an optimization decision, not an arbitrary pass/fail screen. | Horizontal bar ranking of all cities by base-case profit. | `outputs/q5_city_profitability_base.csv` | Use the exact numbers: top-five average profit $13,725.90, next-five average profit $9,218.90, and rank-5 vs rank-6 gap $1,007.00. The key sentence is that all 40 screens are positive, but the top five maximize contribution. |
| 19 | Seattle, Boise, Portland, Spokane, and San Diego Maximize Base-Case Profitability | This is the formal Q5 answer slide. | Selection matrix or compact comparison table for the chosen five. | `outputs/q5_top5_cities.csv`, `outputs/q5_top5_cities_display.csv` | Keep the five-city list visible. Use price, miles, profit, and margin in one place. |
| 20 | The Chosen Five Win on Price Support, Not Just Distance | Explain why these five beat nearby California markets and distant East Coast markets. | Price vs mileage bubble chart with profit as size and top five highlighted. | `outputs/q5_city_profitability_base.csv`, `outputs/q5_june2025_city_prices.csv` | Important comparison: San Diego acts as the low-mileage hedge, while San Francisco, Sacramento, and Los Angeles lose because price support is lower. |
| 21 | Shipping +50% Compresses Profit but Does Not Change the Recommendation | This is Q6(a). | Scenario comparison bars for the top five or top ten. | `outputs/q6_city_profitability_shipping_up_50.csv`, `outputs/q6_top5_cities_shipping_up_50_display.csv` | Use the exact averages: top-five average profit $12,772.85 and average margin 64.88%. |
| 22 | Shipping -50% Expands Profit but Still Does Not Change the Recommendation | This is Q6(b). | Scenario comparison bars for the top five or top ten. | `outputs/q6_city_profitability_shipping_down_50.csv`, `outputs/q6_top5_cities_shipping_down_50_display.csv` | Use the exact averages: top-five average profit $14,678.95 and average margin 74.61%. |
| 23 | The Same Five Cities Stay Top-Ranked in Every Modeled Scenario | This is the clean Q7 answer before the explanation slide. | Rank matrix or scenario heatmap. | `outputs/q7_rank_comparison.csv`, `outputs/question_7.md` | The message is simple and should be unmistakable: same cities, same order, three scenarios. |
| 24 | Freight Is Not the Main City-Screen Risk; Split Allocation Makes It Matter More | Replace the narrow freight-only read with a true management-accounting sensitivity view. | Two-panel tornado / sensitivity bars: Seattle city screen vs 5-city equal pilot. | `outputs/q5_multi_variable_sensitivity.csv` | Show that price and volume dominate the one-city screen, while repeated route-fixed shipping becomes more material once volume is split across five destinations. |
| 25 | City Selection and Unit Allocation Are Different Accounting Decisions | Close Section 3 by separating the market-selection decision from the one-order allocation decision. | Allocation frontier / scenario bars for 1-city, 2-city, and 5-city deployment. | `outputs/q5_allocation_scenarios.csv` | Quantify the trade-off: concentration maximizes profit, while a multi-city pilot buys learning and diversification at the cost of duplicated route-fixed shipping. |

## Section 4: Advanced Seasonality & Sustainability (Slides 26-32)

| # | Draft Headline | Why This Slide Exists | Primary Visual | Data / Files | Must Show / Caution |
| --- | --- | --- | --- | --- | --- |
| 26 | Prices Reach Their High Point in July | Show the pricing side of seasonality in a clean, single-idea slide. | Reuse the themed monthly price chart. | `outputs/q8_seasonality_price.png`, `outputs/q8_monthly_seasonality.csv` | Call out the actual swing sizes: conventional about +21.4% from February low to July peak; organic about +20.5%. |
| 27 | Volumes Peak Earlier and Trough in November | Show the volume side of seasonality as a separate operational problem. | Reuse the themed monthly volume chart. | `outputs/q8_seasonality_volume.png`, `outputs/q8_monthly_seasonality.csv` | Call out the actual swing sizes: conventional about +29.1% from November low to May peak; organic about +30.9% from November low to January peak. |
| 28 | Seasonality Should Change When West Valley Pushes Volume and When It Protects Margin | Turn the seasonality analysis into an operating decision. | New normalized overlay or seasonal calendar combining price and volume logic. | `outputs/q8_monthly_seasonality.csv`, `outputs/q8_seasonality_peaks.csv` | This is the clearest "duck curve" interpretation slide. Keep it very visual. |
| 29 | A Monthly Operating Calendar Can Convert Seasonality From Risk Into Advantage | Translate the duck curve into a practical calendar. | Month-by-month operating playbook or heatmap. | Build from `outputs/q8_monthly_seasonality.csv` and `outputs/question_9.md` | Suggested structure: Jan-May prioritize service and flow, Jul-Sep protect margin, Nov-Feb stimulate and rebalance. |
| 30 | Growers Need Flexible Contracts, Better Cold-Chain Readiness, and Alternate Lanes | This is the first Q9 action slide. | 2x2 action matrix or impact/effort cards. | `outputs/question_9.md` | Use the actual recommendation set: contract tiers, cold storage, transit reliability, seasonal flex volume. |
| 31 | Trade Associations Should Smooth Demand in Off-Peak Months | Cover the demand-side response to seasonality. | Action playbook or campaign calendar. | `outputs/question_9.md` | Use recipes, health messaging, food-service channels, and promotion timing to absorb low-month softness. |
| 32 | A Shared Monthly S&OP Cadence Can Align Growers, West Valley, and Retail Partners | Close Section 4 by integrating stakeholders into one operating model. | Ecosystem diagram or monthly control-tower workflow. | `outputs/question_9.md`, `outputs/question_8.md` | Tie the actions back to margin capture, spoilage control, and seasonal reallocation. |

## Section 5: Implementation, Risks, & Impact (Slides 33-40)

| # | Draft Headline | Why This Slide Exists | Primary Visual | Data / Files | Must Show / Caution |
| --- | --- | --- | --- | --- | --- |
| 33 | Launch the 2026 Pilot First, Then Scale What the Market Confirms | Start implementation with discipline rather than ambition. | 3-year roadmap or Gantt. | Build from the recommendation logic in `outputs/question_5.md` through `outputs/question_9.md` | 2026 = pilot, 2027 = expand where economics hold, 2028 = optimize contracts and routing. |
| 34 | Pilot KPIs Should Focus on Margin, Service, Spoilage, and Repeat Orders | Tell judges how success will be measured. | KPI dashboard mockup. | Derived from the case economics and seasonality logic. | Suggested KPIs: realized gross margin, freight per unit, fill rate, spoilage rate, retailer reorder rate, and service-level consistency. |
| 35 | Expansion Should Follow Stage Gates, Not Automatic Geography Growth | Prevent the implementation section from becoming vague. | Stage-gate decision tree. | Derived from the recommendation and risk logic. | Avoid false precision on exact 20,000-unit allocation. Use retailer commitments and realized pilot economics before scaling. |
| 36 | Top Risks Are Freight, Competitors, Import Disruption, and Forecast Error | This is the main risk map. | 4-quadrant probability vs impact chart. | `case_context.md`, `case_full.md`, `outputs/question_6.md`, `outputs/question_8.md` | Competitor response should be shown as low-probability / low-impact for the 20,000-unit pilot, not as a major destabilizing force. |
| 37 | Each Major Risk Has a Specific Operational Countermeasure | Pair every major risk with an action and owner. | Risk mitigation matrix. | Build from `outputs/question_9.md` and the implementation section. | Tie mitigations to transport contracts, alternate lanes, cold-chain controls, monthly S&OP, and flexible retailer/grower agreements. |
| 38 | The Model Can Now Separate City Choice From Allocation Economics | This slide earns credibility by showing what the upgraded accounting model can defend today and what still requires more data. | Two-panel assumptions / limitations table. | `case_context.md`, `outputs/question_5.md`, `outputs/question_6.md`, `outputs/question_7.md`, `outputs/q5_allocation_scenarios.csv` | Explicitly mention: 40 vs 41 market discrepancy, 2025 H1 partial year, comparable 20,000-unit city screens, split-allocation logic now quantified, but no retailer-level demand, shrink, or route-level service costs yet. |
| 39 | West Valley Should Pursue a 5-City Organic Entry With Structured Discipline | This is the final conclusion slide. | Final recommendation banner with the 5 cities and the three proof pillars. | Pull from Q5-Q9 outputs. | End on the decision, the resilience result, and the seasonal operating discipline required to make it work. |
| 40 | Q&A / Backup: Sources, Assumptions, and Supporting Tables | Give the deck a clean close and a logical bridge to backup discussion. | Sources + appendix index slide. | `outputs/README.md`, key CSVs, case files | Include the source list and which backup tables are available if judges ask. |

## Slides That Are Worth Rebuilding, Not Reusing
- `outputs/q1_winner_matrix.png`
- `outputs/q1_sales_trend_los_angeles.png`
- Any other legacy chart that still looks like a default matplotlib export

## Optional Compression If the Main Story Needs to Be Tighter
- Move Slides **10, 14, 24, 35, 38, and 40** to backup if the main deck starts to feel long.
- Protect Slides **2, 3, 5, 6, 9, 11, 18, 19, 21, 23, 26, 27, 33, and 39**. Those are the highest-signal story beats.
