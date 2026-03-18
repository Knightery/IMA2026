# Question 3

## Method
- Used full-year observations for 2019-2024 (to avoid partial-year bias from 2025 H1).
- Built city-year-type points with **volume-weighted** annual price and total annual volume.
- Measured association with Pearson/Spearman correlation, linear fit (`R^2`), and log-log elasticity.

## Key Output
| Segment | N | Pearson_r | Spearman_rho | Linear_slope_units_per_$ | Linear_R2 | LogLog_Elasticity |
| --- | --- | --- | --- | --- | --- | --- |
| All | 480 | -0.427 | -0.673 | -30,505,466 | 0.183 | -4.956 |
| Conventional | 240 | -0.026 | -0.014 | -4,304,994 | 0.001 | -0.393 |
| Organic | 240 | -0.044 | -0.151 | -223,882 | 0.002 | -0.807 |

Overall relationship (`All`, Pearson r = -0.427) is **moderate negative**.
This indicates higher prices are generally associated with lower annual volume, but strength varies by type.

Figure: `q3_price_volume_scatter.png`
Supporting CSVs: `q3_city_year_type_agg.csv`, `q3_price_volume_metrics.csv`, `q3_price_volume_metrics_raw.csv`.