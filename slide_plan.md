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
| 13 | Macro Drivers Include Freight, Fuel, Inflation, and Cross-Border Supply Risk | Begin Q4 with a macro frame that ties directly to the case context. | Macro driver map or force diagram. | `case_context.md`, `case_full.md`, `outputs/question_4.md` | Tie this to imported supply, labor pressure, and freight volatility. |
| 14 | Micro Drivers Explain Why Los Angeles Sells, Seattle Penetrates, and the Pacific Northwest Prices Higher | Turn Q4 from generic business-school bullets into city-specific logic. | City evidence matrix comparing Los Angeles, Seattle, and the selected top five. | `outputs/question_4.md`, `outputs/q1_winners.csv`, `outputs/q2_organic_share_winners.csv`, `outputs/q5_june2025_city_prices.csv` | Make the distinction between market size, organic readiness, and local willingness to support premium pricing. |
| 15 | The Best Entry Markets Need Price Power, Organic Readiness, and Manageable Miles | Bridge from analysis into recommendation. | New scatter or bubble chart: June 2025 price vs mileage with selected cities highlighted. | `outputs/q5_june2025_city_prices.csv` | The biggest cities are not automatically the best pilot cities. This slide should prepare the audience for why Seattle beats Los Angeles in the entry model. |

## Section 3: Strategic Recommendations (Slides 16-25)

| # | Draft Headline | Why This Slide Exists | Primary Visual | Data / Files | Must Show / Caution |
| --- | --- | --- | --- | --- | --- |
| 16 | The Profit Model Is Simple, Transparent, and Easy to Audit | Before ranking cities, show the mechanics so judges trust the result. | Formula slide or waterfall of revenue minus acquisition and shipping. | `case_context.md`, `outputs/question_5.md` | Use the exact assumptions: 20,000 units, 40% of retail, $0.20 acquisition, shipping formula. |
| 17 | June 2025 Retail Prices Point to the Pacific Northwest as the Premium Opportunity | Show the revenue side of the selection clearly. | Ranked bar chart of forecast June 2026 retail prices by city. | `outputs/q5_june2025_city_prices.csv` | Important insight: the selected top five are also the top five June 2025 price markets. That supports the Q7 result that price dominates rank. |
| 18 | Base-Case Profit Ranking Produces a Clear Top Five Cut Line | Show that the recommendation is not arbitrary. | Horizontal bar ranking of all cities by base-case profit. | `outputs/q5_city_profitability_base.csv` | Use the exact numbers: top-five average profit $13,725.90, next-five average profit $9,218.90, and rank-5 vs rank-6 gap $1,007.00. |
| 19 | Seattle, Boise, Portland, Spokane, and San Diego Maximize Base-Case Profitability | This is the formal Q5 answer slide. | Selection matrix or compact comparison table for the chosen five. | `outputs/q5_top5_cities.csv`, `outputs/q5_top5_cities_display.csv` | Keep the five-city list visible. Use price, miles, profit, and margin in one place. |
| 20 | The Chosen Five Win on Price Support, Not Just Distance | Explain why these five beat nearby California markets and distant East Coast markets. | Price vs mileage bubble chart with profit as size and top five highlighted. | `outputs/q5_city_profitability_base.csv`, `outputs/q5_june2025_city_prices.csv` | Important comparison: San Diego acts as the low-mileage hedge, while San Francisco, Sacramento, and Los Angeles lose because price support is lower. |
| 21 | Shipping +50% Compresses Profit but Does Not Change the Recommendation | This is Q6(a). | Scenario comparison bars for the top five or top ten. | `outputs/q6_city_profitability_shipping_up_50.csv`, `outputs/q6_top5_cities_shipping_up_50_display.csv` | Use the exact averages: top-five average profit $12,772.85 and average margin 64.88%. |
| 22 | Shipping -50% Expands Profit but Still Does Not Change the Recommendation | This is Q6(b). | Scenario comparison bars for the top five or top ten. | `outputs/q6_city_profitability_shipping_down_50.csv`, `outputs/q6_top5_cities_shipping_down_50_display.csv` | Use the exact averages: top-five average profit $14,678.95 and average margin 74.61%. |
| 23 | The Same Five Cities Stay Top-Ranked in Every Modeled Scenario | This is the clean Q7 answer before the explanation slide. | Rank matrix or scenario heatmap. | `outputs/q7_rank_comparison.csv`, `outputs/question_7.md` | The message is simple and should be unmistakable: same cities, same order, three scenarios. |
| 24 | Shipping Sensitivity Is Highest in Distant Northeast Markets, Not in the Recommended Set | Show where freight actually bites hardest. | Tornado chart or ranked delta-profit bars. | `outputs/q7_shipping_sensitivity.csv` | Call out that Boston, HartfordSpringfield, and Albany have the biggest absolute +/-50% shipping profit swings, while the selected top five move by about $813 to $1,024. |
| 25 | Local Retail Price Is the Main Lever Behind Rank Stability | Close Section 3 with the real interpretation, not just the mechanics. | Quadrant or comparison chart: forecast price rank vs shipping sensitivity or profit rank. | `outputs/q5_june2025_city_prices.csv`, `outputs/q7_rank_comparison.csv`, `outputs/q7_shipping_sensitivity.csv` | Also mention that all 40 modeled cities remain profitable even at +50% shipping, so the issue is city optimization rather than simple survival. |

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
| 36 | The Highest-Risk Threats Are Freight Spikes, Import Disruptions, and Forecast Error | This is the main risk map. | 4-quadrant probability vs impact chart. | `case_context.md`, `case_full.md`, `outputs/question_6.md`, `outputs/question_8.md` | Include freight spikes, Mexico/import disruption, labor pressure, forecast error, spoilage, and retailer uptake risk. |
| 37 | Each Major Risk Has a Specific Operational Countermeasure | Pair every major risk with an action and owner. | Risk mitigation matrix. | Build from `outputs/question_9.md` and the implementation section. | Tie mitigations to transport contracts, alternate lanes, cold-chain controls, monthly S&OP, and flexible retailer/grower agreements. |
| 38 | The Current Model Is Strong Enough for City Selection but Not Yet for Exact Allocation | This slide earns credibility by being transparent about model limits. | Assumptions / limitations table. | `case_context.md`, `outputs/question_5.md`, `outputs/question_6.md`, `outputs/question_7.md` | Explicitly mention: 40 vs 41 market discrepancy, 2025 H1 partial year, comparable 20,000-unit city scorecards, no retailer-specific demand, no spoilage shrink, and limited cost stack. |
| 39 | West Valley Should Pursue a 5-City Organic Entry With Structured Discipline | This is the final conclusion slide. | Final recommendation banner with the 5 cities and the three proof pillars. | Pull from Q5-Q9 outputs. | End on the decision, the resilience result, and the seasonal operating discipline required to make it work. |
| 40 | Q&A / Backup: Sources, Assumptions, and Supporting Tables | Give the deck a clean close and a logical bridge to backup discussion. | Sources + appendix index slide. | `outputs/README.md`, key CSVs, case files | Include the source list and which backup tables are available if judges ask. |

## Slides That Are Worth Rebuilding, Not Reusing
- `outputs/q1_winner_matrix.png`
- `outputs/q1_sales_trend_los_angeles.png`
- Any other legacy chart that still looks like a default matplotlib export

## Optional Compression If the Main Story Needs to Be Tighter
- Move Slides **10, 14, 24, 35, 38, and 40** to backup if the main deck starts to feel long.
- Protect Slides **2, 3, 5, 6, 9, 11, 18, 19, 21, 23, 26, 27, 33, and 39**. Those are the highest-signal story beats.
