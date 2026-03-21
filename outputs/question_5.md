# Question 5

## Method
- Used each city's simple average organic retail price from June 2025 as the June 2026 retail forecast.
- Planned wholesale price = `40% * forecast retail price`.
- Treated this as a **special-order / relevant-cost** decision: the case says there is idle capacity and no added overhead beyond the modeled inputs.
- Assumed 20,000 units sold per candidate city as a **comparable city-selection scorecard**, not as the final allocation plan.
- Cost model: acquisition (`$0.20 * 20,000`) + shipping (`$1,500 + $50 per 100 miles`).
- Ranked cities by incremental profit and selected top five.

## Recommended 5 Cities (Base Case)
| City | State | Mileage (miles) | Forecast Retail Price ($/unit) | Planned Wholesale Price ($/unit) | Revenue | Shipping_Cost | Acquisition_Cost | Total_Cost | Profit | Profit Margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seattle | WA | 1,029 | $2.66 | $1.06 | $21,280.00 | $2,014.50 | $4,000.00 | $6,014.50 | $15,265.50 | 71.74% |
| Boise | ID | 827 | $2.59 | $1.04 | $20,752.00 | $1,913.50 | $4,000.00 | $5,913.50 | $14,838.50 | 71.50% |
| Portland | OR | 855 | $2.54 | $1.02 | $20,336.00 | $1,927.50 | $4,000.00 | $5,927.50 | $14,408.50 | 70.85% |
| Spokane | WA | 1,097 | $2.38 | $0.95 | $19,040.00 | $2,048.50 | $4,000.00 | $6,048.50 | $12,991.50 | 68.23% |
| San Diego | CA | 253 | $2.09 | $0.84 | $16,752.00 | $1,626.50 | $4,000.00 | $5,626.50 | $11,125.50 | 66.41% |

## Management-Accounting Interpretation
- All **40** city scorecards are profitable, so the decision is **optimization**, not simple accept/reject. Lowest modeled profit is $4,343.00.
- The top-five break-even volumes are only **2,285 to 2,724 units**, which means the pilot clears route fixed costs well below the 20,000-unit screen.
- A true 5-city equal split of the 20,000-unit order still earns $6,101.50, but it sacrifices $9,164.00 versus concentrating all volume in Seattle. That trade-off buys market learning.

Supporting CSVs: `q5_june2025_city_prices.csv`, `q5_city_profitability_base.csv`, `q5_top5_cities.csv`, `q5_cvp_metrics.csv`, `q5_allocation_scenarios.csv`, `q5_multi_variable_sensitivity.csv`.