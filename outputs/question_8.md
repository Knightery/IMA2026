# Question 8

## Method
- Used complete years only (2019-2024) to avoid partial-year seasonality bias from 2025 H1.
- Aggregated weekly data into monthly city totals/averages by type.
- Computed average month-of-year seasonality profiles for price and volume.
- Identified peak/low months for each type.

## Key Output
| Type | Peak Price Month | Low Price Month | Peak Volume Month | Low Volume Month |
| --- | --- | --- | --- | --- |
| Conventional | Jul | Feb | May | Nov |
| Organic | Jul | Feb | Jan | Nov |

## Graphical Depictions
- `q8_seasonality_price.png`
- `q8_seasonality_volume.png`

Supporting CSVs: `q8_monthly_seasonality.csv`, `q8_seasonality_peaks.csv`, `q8_month_coverage.csv`.