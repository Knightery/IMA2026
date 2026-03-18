from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter


UNITS_ORDER = ["conventional", "organic"]
MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
THEME = {
    "bg": "#f7f3ec",
    "paper": "#fcfaf5",
    "panel": "#fffdf9",
    "ink": "#1f2621",
    "muted": "#5f6b63",
    "primary": "#355c47",
    "primary_soft": "#889a83",
    "accent": "#c58a2a",
    "stress": "#b5533a",
    "compare": "#3f728a",
    "line": "#d8d1c6",
}
SERIES_COLORS = {"conventional": THEME["compare"], "organic": THEME["primary"]}


def money(x: float) -> str:
    return f"${x:,.2f}"


def int_fmt(x: float) -> str:
    return f"{int(round(x)):,.0f}"


def pct(x: float) -> str:
    return f"{x:.2%}"


def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows_"
    header = "| " + " | ".join(df.columns) + " |"
    sep = "| " + " | ".join(["---"] * len(df.columns)) + " |"
    rows = []
    for _, row in df.iterrows():
        rows.append("| " + " | ".join(str(v) for v in row.values) + " |")
    return "\n".join([header, sep, *rows])


def _fmt_millions(x: float, pos: int | None = None) -> str:
    magnitude = abs(x)
    if magnitude >= 100_000_000:
        return f"{x / 1_000_000:.0f}M"
    if magnitude >= 10_000_000:
        return f"{x / 1_000_000:.1f}M"
    return f"{x / 1_000_000:.1f}M"


def _new_chart(figsize: Tuple[float, float] = (8.2, 5.2)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(THEME["bg"])
    ax.set_facecolor(THEME["panel"])
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(THEME["line"])
        ax.spines[side].set_linewidth(1.1)
    ax.tick_params(colors=THEME["muted"], labelsize=10)
    ax.set_axisbelow(True)
    return fig, ax


def _style_axes(
    ax,
    title: str,
    xlabel: str,
    ylabel: str,
    *,
    grid_axis: str = "y",
) -> None:
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", color=THEME["ink"], pad=10)
    ax.set_xlabel(xlabel, color=THEME["muted"], fontsize=11, labelpad=8)
    ax.set_ylabel(ylabel, color=THEME["muted"], fontsize=11, labelpad=8)
    ax.grid(axis=grid_axis, color=THEME["line"], linewidth=0.9, alpha=0.75)


def _style_legend(ax, *, loc: str = "best", ncol: int = 1):
    legend = ax.legend(loc=loc, ncol=ncol, frameon=True, fontsize=10)
    if legend is not None:
        frame = legend.get_frame()
        frame.set_facecolor(THEME["paper"])
        frame.set_edgecolor(THEME["line"])
        frame.set_linewidth(0.9)
        for text in legend.get_texts():
            text.set_color(THEME["ink"])
    return legend


def _save_chart(fig, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def load_data(csv_path: Path) -> pd.DataFrame:
    raw = pd.read_csv(csv_path)
    raw.columns = [c.strip() for c in raw.columns]

    price_col = [c for c in raw.columns if "Average_price" in c][0]
    vol_col = [c for c in raw.columns if "Total_Volume" in c][0]

    df = raw.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Type"] = df["Type"].astype(str).str.strip().str.lower()
    df["City"] = df["City"].astype(str).str.strip()
    df["State"] = df["State"].astype(str).str.strip()
    df["Average_price"] = (
        df[price_col].astype(str).str.replace(r"[\$,]", "", regex=True).astype(float)
    )
    df["Total_Volume"] = pd.to_numeric(df[vol_col], errors="coerce")
    df["Mileage_miles"] = pd.to_numeric(df["Mileage (miles)"], errors="coerce")

    mask_window = (df["Date"] >= "2019-01-01") & (df["Date"] <= "2025-06-30")
    df = df.loc[mask_window].copy()
    df = df[df["Type"].isin(UNITS_ORDER)].copy()
    df["Revenue"] = df["Average_price"] * df["Total_Volume"]

    return df


def periods(df: pd.DataFrame) -> List[Tuple[str, pd.Series]]:
    out: List[Tuple[str, pd.Series]] = []
    for year in range(2019, 2025):
        out.append((str(year), df["Date"].dt.year == year))
    out.append(("2025 H1", (df["Date"] >= "2025-01-01") & (df["Date"] <= "2025-06-30")))
    return out


def solve_q1(df: pd.DataFrame, out_dir: Path) -> Dict[str, pd.DataFrame]:
    recs = []
    for label, mask in periods(df):
        sub = df.loc[mask]
        by_city_type = (
            sub.groupby(["City", "Type"], as_index=False)["Revenue"].sum().copy()
        )
        for t in UNITS_ORDER:
            t_sub = by_city_type[by_city_type["Type"] == t]
            winner = t_sub.loc[t_sub["Revenue"].idxmax()]
            recs.append(
                {
                    "Period": label,
                    "Type": t,
                    "City": winner["City"],
                    "Sales_Dollars": winner["Revenue"],
                }
            )

    winners_long = pd.DataFrame(recs)
    winners_long.to_csv(out_dir / "q1_winners_long.csv", index=False)

    rows = []
    ordered_periods = [str(y) for y in range(2019, 2025)] + ["2025 H1"]
    for p in ordered_periods:
        conv = winners_long[(winners_long["Period"] == p) & (winners_long["Type"] == "conventional")].iloc[0]
        org = winners_long[(winners_long["Period"] == p) & (winners_long["Type"] == "organic")].iloc[0]
        rows.append(
            {
                "Period": p,
                "Conventional Winner": conv["City"],
                "Conventional Sales ($)": money(conv["Sales_Dollars"]),
                "Organic Winner": org["City"],
                "Organic Sales ($)": money(org["Sales_Dollars"]),
            }
        )
    winners = pd.DataFrame(rows)
    winners.to_csv(out_dir / "q1_winners.csv", index=False)

    md = []
    md.append("# Question 1")
    md.append("")
    md.append("## Method")
    md.append("- Filtered data to 2019-01-01 through 2025-06-30.")
    md.append("- Computed dollar sales as `Average_price * Total_Volume` for each row.")
    md.append("- For each period, aggregated sales by `City x Type` and selected the top city separately for conventional and organic.")
    md.append("")
    md.append("## Key Output")
    md.append(md_table(winners))
    md.append("")
    md.append("Supporting CSVs: `q1_winners.csv`, `q1_winners_long.csv`.")

    (out_dir / "question_1.md").write_text("\n".join(md), encoding="utf-8")
    return {"q1_winners": winners_long}


def solve_q2(df: pd.DataFrame, out_dir: Path) -> Dict[str, pd.DataFrame]:
    recs = []
    for label, mask in periods(df):
        sub = df.loc[mask]
        vol = sub.groupby(["City", "Type"], as_index=False)["Total_Volume"].sum()
        pivot = vol.pivot(index="City", columns="Type", values="Total_Volume").fillna(0)
        pivot["total"] = pivot.get("organic", 0) + pivot.get("conventional", 0)
        pivot["organic_share"] = np.where(pivot["total"] > 0, pivot.get("organic", 0) / pivot["total"], 0)
        winner_city = pivot["organic_share"].idxmax()
        w = pivot.loc[winner_city]
        recs.append(
            {
                "Period": label,
                "City": winner_city,
                "Organic Units": w.get("organic", 0),
                "Total Units": w["total"],
                "Organic Share": w["organic_share"],
            }
        )

    winners = pd.DataFrame(recs)
    winners.to_csv(out_dir / "q2_organic_share_winners_raw.csv", index=False)

    show = winners.copy()
    show["Organic Units"] = show["Organic Units"].map(int_fmt)
    show["Total Units"] = show["Total Units"].map(int_fmt)
    show["Organic Share"] = show["Organic Share"].map(pct)
    show.to_csv(out_dir / "q2_organic_share_winners.csv", index=False)

    md = []
    md.append("# Question 2")
    md.append("")
    md.append("## Method")
    md.append("- For each period, summed units by city and type.")
    md.append("- Calculated `organic_share = organic_units / (organic_units + conventional_units)`.")
    md.append("- Selected the city with the highest organic share in each period.")
    md.append("")
    md.append("## Key Output")
    md.append(md_table(show))
    md.append("")
    md.append("Supporting CSVs: `q2_organic_share_winners.csv`, `q2_organic_share_winners_raw.csv`.")

    (out_dir / "question_2.md").write_text("\n".join(md), encoding="utf-8")
    return {"q2_winners": winners}


def _corr(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 2:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


def _relation_label(r: float) -> str:
    if np.isnan(r):
        return "insufficient"
    strength = abs(r)
    if strength < 0.10:
        s = "negligible"
    elif strength < 0.30:
        s = "weak"
    elif strength < 0.50:
        s = "moderate"
    else:
        s = "strong"
    direction = "positive" if r > 0 else "negative"
    return f"{s} {direction}"


def solve_q3(df: pd.DataFrame, out_dir: Path) -> Dict[str, pd.DataFrame]:
    annual = df[df["Date"].dt.year.between(2019, 2024)].copy()
    annual["Price_x_Volume"] = annual["Average_price"] * annual["Total_Volume"]
    agg = (
        annual.groupby(["Year", "City", "Type"], as_index=False)
        .agg(total_volume=("Total_Volume", "sum"), sum_price_x_volume=("Price_x_Volume", "sum"))
        .copy()
    )
    agg["avg_price"] = np.where(agg["total_volume"] > 0, agg["sum_price_x_volume"] / agg["total_volume"], np.nan)
    agg.to_csv(out_dir / "q3_city_year_type_agg.csv", index=False)

    def metrics(data: pd.DataFrame, label: str) -> Dict[str, float]:
        x = data["avg_price"].to_numpy()
        y = data["total_volume"].to_numpy()
        pear = _corr(x, y)
        spear = float(data["avg_price"].rank().corr(data["total_volume"].rank(), method="pearson"))

        if len(x) > 1:
            slope, intercept = np.polyfit(x, y, 1)
            y_hat = slope * x + intercept
            ss_res = np.sum((y - y_hat) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else np.nan
        else:
            slope = intercept = r2 = np.nan

        valid = (x > 0) & (y > 0)
        if valid.sum() > 1:
            elasticity, _ = np.polyfit(np.log(x[valid]), np.log(y[valid]), 1)
        else:
            elasticity = np.nan
        return {
            "Segment": label,
            "N": len(data),
            "Pearson_r": pear,
            "Spearman_rho": spear,
            "Linear_slope_units_per_$": slope,
            "Linear_R2": r2,
            "LogLog_Elasticity": float(elasticity),
        }

    m = [
        metrics(agg, "All"),
        metrics(agg[agg["Type"] == "conventional"], "Conventional"),
        metrics(agg[agg["Type"] == "organic"], "Organic"),
    ]
    mdf = pd.DataFrame(m)
    mdf.to_csv(out_dir / "q3_price_volume_metrics_raw.csv", index=False)

    show = mdf.copy()
    show["N"] = show["N"].astype(int).astype(str)
    for col in ["Pearson_r", "Spearman_rho", "Linear_R2", "LogLog_Elasticity"]:
        show[col] = show[col].map(lambda v: f"{v:.3f}")
    show["Linear_slope_units_per_$"] = show["Linear_slope_units_per_$"].map(lambda v: f"{v:,.0f}")
    show.to_csv(out_dir / "q3_price_volume_metrics.csv", index=False)

    all_r = mdf.loc[mdf["Segment"] == "All", "Pearson_r"].iloc[0]
    all_r2 = mdf.loc[mdf["Segment"] == "All", "Linear_R2"].iloc[0]

    # Scatter chart
    fig, ax = _new_chart(figsize=(8.6, 5.3))
    for t in UNITS_ORDER:
        sub = agg[agg["Type"] == t]
        ax.scatter(
            sub["avg_price"],
            sub["total_volume"],
            s=42,
            alpha=0.75,
            color=SERIES_COLORS[t],
            edgecolor=THEME["paper"],
            linewidth=0.6,
            label=t.title(),
        )

    slope, intercept = np.polyfit(agg["avg_price"], agg["total_volume"], 1)
    x_line = np.linspace(agg["avg_price"].min(), agg["avg_price"].max(), 200)
    y_line = np.maximum(slope * x_line + intercept, 0)
    ax.plot(x_line, y_line, color=THEME["accent"], linewidth=2.6, label="All-market trend")

    _style_axes(
        ax,
        "Price increases generally coincide with lower annual volume",
        "Average annual price ($ / unit)",
        "Annual volume (units)",
        grid_axis="both",
    )
    ax.yaxis.set_major_formatter(FuncFormatter(_fmt_millions))
    ax.set_ylim(bottom=0)
    ax.text(
        0.98,
        0.06,
        f"Pearson r = {all_r:.3f}\nR² = {all_r2:.3f}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color=THEME["ink"],
        fontsize=9.5,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": THEME["paper"],
            "edgecolor": THEME["line"],
            "linewidth": 0.9,
        },
    )
    _style_legend(ax, loc="upper right")
    fig_path = out_dir / "q3_price_volume_scatter.png"
    _save_chart(fig, fig_path)

    interpretation = _relation_label(all_r)

    md = []
    md.append("# Question 3")
    md.append("")
    md.append("## Method")
    md.append("- Used full-year observations for 2019-2024 (to avoid partial-year bias from 2025 H1).")
    md.append("- Built city-year-type points with **volume-weighted** annual price and total annual volume.")
    md.append("- Measured association with Pearson/Spearman correlation, linear fit (`R^2`), and log-log elasticity.")
    md.append("")
    md.append("## Key Output")
    md.append(md_table(show))
    md.append("")
    md.append(f"Overall relationship (`All`, Pearson r = {all_r:.3f}) is **{interpretation}**.")
    md.append("This indicates higher prices are generally associated with lower annual volume, but strength varies by type.")
    md.append("")
    md.append("Figure: `q3_price_volume_scatter.png`")
    md.append("Supporting CSVs: `q3_city_year_type_agg.csv`, `q3_price_volume_metrics.csv`, `q3_price_volume_metrics_raw.csv`.")

    (out_dir / "question_3.md").write_text("\n".join(md), encoding="utf-8")
    return {"q3_metrics": mdf}


def solve_q4(df: pd.DataFrame, q1_winners: pd.DataFrame, out_dir: Path) -> None:
    annual = df[df["Date"].dt.year.between(2019, 2024)].copy()
    q3_agg = (
        annual.groupby(["Year", "City", "Type"], as_index=False)
        .agg(avg_price=("Average_price", "mean"), total_volume=("Total_Volume", "sum"))
    )
    price_volume_corr = q3_agg["avg_price"].corr(q3_agg["total_volume"])

    winner_counts = q1_winners.groupby("City", as_index=False).size().sort_values("size", ascending=False)
    winner_counts.to_csv(out_dir / "q4_q1_winner_counts.csv", index=False)
    top_cities = ", ".join(winner_counts.head(5)["City"].tolist())

    md = []
    md.append("# Question 4")
    md.append("")
    md.append("## Method")
    md.append("- Used Q1 winner history and the Q3 price-volume relationship as evidence.")
    md.append("- Added market-demand drivers based on standard produce retail dynamics.")
    md.append("")
    md.append("## Key Factors Likely Driving Demand")
    md.append(f"- **Market size and density:** Q1 winner cities are concentrated in large metros ({top_cities}), where baseline produce demand is higher.")
    md.append("- **Retail price level and price sensitivity:** Q3 shows a negative price-volume association, so demand is likely price elastic in many markets.")
    md.append("- **Consumer mix (income + health orientation):** Organic penetration tends to be stronger in markets with higher health-conscious and premium-paying segments.")
    md.append("- **Distribution distance/logistics:** Distance from West Valley affects cost and freshness risk, which can influence local price competitiveness and demand realization.")
    md.append("- **Seasonality and promotions:** Recurring intra-year patterns in volume/pricing indicate seasonal availability and retail promotion timing matter.")
    md.append("- **Local competition and channel mix:** Presence of large grocery chains, club stores, and food-service buyers can materially shift city-level demand.")
    md.append("")
    md.append(f"Data point: overall annual price-volume Pearson correlation (2019-2024 city-year-type) = {price_volume_corr:.3f}.")
    md.append("Supporting CSV: `q4_q1_winner_counts.csv`.")

    (out_dir / "question_4.md").write_text("\n".join(md), encoding="utf-8")


def city_profitability(june_prices: pd.DataFrame, shipping_multiplier: float = 1.0) -> pd.DataFrame:
    units = 20_000
    acquisition_cost = 0.20 * units

    out = june_prices.copy()
    out["forecast_retail_price_jun2026"] = out["avg_retail_price_jun2025"]
    out["planned_wholesale_price"] = 0.40 * out["forecast_retail_price_jun2026"]
    out["Revenue"] = out["planned_wholesale_price"] * units
    out["Base_Shipping_Cost"] = 1500 + 50 * (out["Mileage_miles"] / 100.0)
    out["Shipping_Cost"] = out["Base_Shipping_Cost"] * shipping_multiplier
    out["Acquisition_Cost"] = acquisition_cost
    out["Total_Cost"] = out["Shipping_Cost"] + out["Acquisition_Cost"]
    out["Profit"] = out["Revenue"] - out["Total_Cost"]
    out["Profit_Margin"] = np.where(out["Revenue"] > 0, out["Profit"] / out["Revenue"], np.nan)
    return out.sort_values("Profit", ascending=False).reset_index(drop=True)


def solve_q5_q6_q7(df: pd.DataFrame, out_dir: Path) -> Dict[str, pd.DataFrame]:
    june = df[
        (df["Type"] == "organic")
        & (df["Date"].dt.year == 2025)
        & (df["Date"].dt.month == 6)
    ].copy()

    june_prices = (
        june.groupby(["City", "State", "Mileage_miles"], as_index=False)
        .agg(avg_retail_price_jun2025=("Average_price", "mean"))
        .sort_values("City")
    )
    june_prices.to_csv(out_dir / "q5_june2025_city_prices.csv", index=False)

    base = city_profitability(june_prices, shipping_multiplier=1.0)
    up = city_profitability(june_prices, shipping_multiplier=1.5)
    down = city_profitability(june_prices, shipping_multiplier=0.5)

    base.to_csv(out_dir / "q5_city_profitability_base.csv", index=False)
    up.to_csv(out_dir / "q6_city_profitability_shipping_up_50.csv", index=False)
    down.to_csv(out_dir / "q6_city_profitability_shipping_down_50.csv", index=False)

    top5_base = base.head(5).copy()
    top5_up = up.head(5).copy()
    top5_down = down.head(5).copy()

    top5_base.to_csv(out_dir / "q5_top5_cities.csv", index=False)
    top5_up.to_csv(out_dir / "q6_top5_cities_shipping_up_50.csv", index=False)
    top5_down.to_csv(out_dir / "q6_top5_cities_shipping_down_50.csv", index=False)

    display_cols = [
        "City",
        "State",
        "Mileage_miles",
        "forecast_retail_price_jun2026",
        "planned_wholesale_price",
        "Revenue",
        "Shipping_Cost",
        "Acquisition_Cost",
        "Total_Cost",
        "Profit",
        "Profit_Margin",
    ]

    def prep_show(d: pd.DataFrame) -> pd.DataFrame:
        s = d[display_cols].copy()
        s = s.rename(
            columns={
                "Mileage_miles": "Mileage (miles)",
                "forecast_retail_price_jun2026": "Forecast Retail Price ($/unit)",
                "planned_wholesale_price": "Planned Wholesale Price ($/unit)",
                "Profit_Margin": "Profit Margin",
            }
        )
        s["Mileage (miles)"] = s["Mileage (miles)"].map(int_fmt)
        for c in [
            "Forecast Retail Price ($/unit)",
            "Planned Wholesale Price ($/unit)",
            "Revenue",
            "Shipping_Cost",
            "Acquisition_Cost",
            "Total_Cost",
            "Profit",
        ]:
            s[c] = s[c].map(money)
        s["Profit Margin"] = s["Profit Margin"].map(pct)
        return s

    show_base = prep_show(top5_base)
    show_up = prep_show(top5_up)
    show_down = prep_show(top5_down)

    show_base.to_csv(out_dir / "q5_top5_cities_display.csv", index=False)
    show_up.to_csv(out_dir / "q6_top5_cities_shipping_up_50_display.csv", index=False)
    show_down.to_csv(out_dir / "q6_top5_cities_shipping_down_50_display.csv", index=False)

    # Q5 writeup
    md5 = []
    md5.append("# Question 5")
    md5.append("")
    md5.append("## Method")
    md5.append("- Used each city's simple average organic retail price from June 2025 as the June 2026 retail forecast.")
    md5.append("- Planned wholesale price = `40% * forecast retail price`.")
    md5.append("- Assumed 20,000 units sold per candidate city (as a comparable city-selection scenario).")
    md5.append("- Cost model: acquisition (`$0.20 * 20,000`) + shipping (`$1,500 + $50 per 100 miles`).")
    md5.append("- Ranked cities by expected profit and selected top five.")
    md5.append("")
    md5.append("## Recommended 5 Cities (Base Case)")
    md5.append(md_table(show_base))
    md5.append("")
    md5.append("Rationale: these cities maximize expected profit by combining higher local price support (higher wholesale revenue) with manageable logistics cost.")
    md5.append("")
    md5.append("Supporting CSVs: `q5_june2025_city_prices.csv`, `q5_city_profitability_base.csv`, `q5_top5_cities.csv`.")
    (out_dir / "question_5.md").write_text("\n".join(md5), encoding="utf-8")

    # Q6 writeup
    md6 = []
    md6.append("# Question 6")
    md6.append("")
    md6.append("## Method")
    md6.append("- Reused Q5 base assumptions and modified only shipping/logistics expense.")
    md6.append("- Scenario (a): shipping cost multiplier = `1.5`.")
    md6.append("- Scenario (b): shipping cost multiplier = `0.5`.")
    md6.append("- Ranked cities by scenario profit.")
    md6.append("")
    md6.append("## (a) Shipping +50%: Recommended 5 Cities")
    md6.append(md_table(show_up))
    md6.append("")
    md6.append("## (b) Shipping -50%: Recommended 5 Cities")
    md6.append(md_table(show_down))
    md6.append("")
    md6.append("Supporting CSVs: `q6_city_profitability_shipping_up_50.csv`, `q6_city_profitability_shipping_down_50.csv`, `q6_top5_cities_shipping_up_50.csv`, `q6_top5_cities_shipping_down_50.csv`.")
    (out_dir / "question_6.md").write_text("\n".join(md6), encoding="utf-8")

    # Q7 comparison
    base_set = list(top5_base["City"])
    up_set = list(top5_up["City"])
    down_set = list(top5_down["City"])

    rank = (
        base[["City", "Profit"]]
        .merge(up[["City", "Profit"]], on="City", suffixes=("_base", "_up50"))
        .merge(down[["City", "Profit"]], on="City")
        .rename(columns={"Profit": "Profit_down50"})
    )
    rank["Rank_base"] = rank["Profit_base"].rank(ascending=False, method="min").astype(int)
    rank["Rank_up50"] = rank["Profit_up50"].rank(ascending=False, method="min").astype(int)
    rank["Rank_down50"] = rank["Profit_down50"].rank(ascending=False, method="min").astype(int)
    rank["Rank_change_up50"] = rank["Rank_up50"] - rank["Rank_base"]
    rank["Rank_change_down50"] = rank["Rank_down50"] - rank["Rank_base"]
    rank.to_csv(out_dir / "q7_rank_comparison.csv", index=False)

    sensitivity = base[["City", "Base_Shipping_Cost"]].copy()
    sensitivity["Profit_Impact_for_50pct_Shipping_Change"] = 0.5 * sensitivity["Base_Shipping_Cost"]
    sensitivity.to_csv(out_dir / "q7_shipping_sensitivity.csv", index=False)

    top_compare = pd.DataFrame(
        {
            "Base (Q5)": base_set,
            "Shipping +50% (Q6a)": up_set,
            "Shipping -50% (Q6b)": down_set,
        }
    )

    same_recommendations = base_set == up_set == down_set
    if same_recommendations:
        compare_text = (
            "- Recommendations are unchanged across Q5 and both Q6 scenarios (the same five cities remain top-ranked)."
        )
        important_factor = (
            "Local retail price (and therefore wholesale revenue) dominates ranking outcomes; shipping changes affect profit levels but not the top-5 order here."
        )
    else:
        compare_text = (
            "- Recommendations change across scenarios because shipping multipliers penalize longer-distance cities more heavily."
        )
        important_factor = (
            "Distance-driven shipping sensitivity (mileage) is the key driver of ranking changes across scenarios."
        )

    md7 = []
    md7.append("# Question 7")
    md7.append("")
    md7.append("## Comparison of Recommendations")
    md7.append(md_table(top_compare))
    md7.append("")
    md7.append("## Interpretation")
    md7.append(compare_text)
    md7.append(f"- Most important factor behind differences: **{important_factor}**")
    md7.append("- Cities with higher mileage experience larger absolute profit shifts when shipping changes by +/-50%.")
    md7.append("")
    md7.append("Supporting CSVs: `q7_rank_comparison.csv`, `q7_shipping_sensitivity.csv`.")
    (out_dir / "question_7.md").write_text("\n".join(md7), encoding="utf-8")

    return {"q5_base": base, "q6_up": up, "q6_down": down}


def solve_q8(df: pd.DataFrame, out_dir: Path) -> Dict[str, pd.DataFrame]:
    monthly = df[df["Date"].dt.year.between(2019, 2024)].copy()
    monthly["year_month"] = monthly["Date"].dt.to_period("M").dt.to_timestamp()
    month_agg = (
        monthly.groupby(["year_month", "Type"], as_index=False)
        .agg(avg_price=("Average_price", "mean"), total_volume=("Total_Volume", "sum"))
    )
    month_agg["month"] = month_agg["year_month"].dt.month
    month_coverage = (
        month_agg.groupby(["month", "Type"], as_index=False)
        .size()
        .rename(columns={"size": "n_year_month_obs"})
        .sort_values(["Type", "month"])
    )
    month_coverage.to_csv(out_dir / "q8_month_coverage.csv", index=False)

    seasonal = (
        month_agg.groupby(["month", "Type"], as_index=False)
        .agg(mean_price=("avg_price", "mean"), mean_monthly_volume=("total_volume", "mean"))
        .sort_values(["Type", "month"])
    )
    seasonal.to_csv(out_dir / "q8_monthly_seasonality.csv", index=False)

    months = np.arange(1, 13)

    fig1, ax1 = _new_chart(figsize=(8.6, 5.1))
    for t in UNITS_ORDER:
        sub = seasonal[seasonal["Type"] == t].set_index("month").reindex(months).reset_index()
        ax1.plot(
            sub["month"],
            sub["mean_price"],
            marker="o",
            markersize=5.5,
            linewidth=2.8,
            color=SERIES_COLORS[t],
            label=t.title(),
        )
        ax1.fill_between(
            sub["month"],
            sub["mean_price"],
            sub["mean_price"].min(),
            color=SERIES_COLORS[t],
            alpha=0.06 if t == "conventional" else 0.1,
        )
        peak_idx = sub["mean_price"].idxmax()
        low_idx = sub["mean_price"].idxmin()
        ax1.scatter(sub.loc[peak_idx, "month"], sub.loc[peak_idx, "mean_price"], s=54, color=THEME["accent"], zorder=5)
        ax1.scatter(sub.loc[low_idx, "month"], sub.loc[low_idx, "mean_price"], s=44, color=THEME["stress"], zorder=5)
    ax1.set_xticks(months)
    ax1.set_xticklabels(MONTH_LABELS)
    _style_axes(
        ax1,
        "Prices crest in July after the strongest volume months",
        "Month",
        "Average price ($ / unit)",
    )
    _style_legend(ax1, loc="upper left")
    fig1_path = out_dir / "q8_seasonality_price.png"
    _save_chart(fig1, fig1_path)

    fig2, ax2 = _new_chart(figsize=(8.6, 5.1))
    for t in UNITS_ORDER:
        sub = seasonal[seasonal["Type"] == t].set_index("month").reindex(months).reset_index()
        ax2.plot(
            sub["month"],
            sub["mean_monthly_volume"],
            marker="o",
            markersize=5.5,
            linewidth=2.8,
            color=SERIES_COLORS[t],
            label=t.title(),
        )
        peak_idx = sub["mean_monthly_volume"].idxmax()
        low_idx = sub["mean_monthly_volume"].idxmin()
        ax2.scatter(
            sub.loc[peak_idx, "month"],
            sub.loc[peak_idx, "mean_monthly_volume"],
            s=54,
            color=THEME["accent"],
            zorder=5,
        )
        ax2.scatter(
            sub.loc[low_idx, "month"],
            sub.loc[low_idx, "mean_monthly_volume"],
            s=44,
            color=THEME["stress"],
            zorder=5,
        )
    ax2.set_xticks(months)
    ax2.set_xticklabels(MONTH_LABELS)
    ax2.yaxis.set_major_formatter(FuncFormatter(_fmt_millions))
    _style_axes(
        ax2,
        "Volume peaks earlier than price, creating a seasonal timing gap",
        "Month",
        "Average monthly volume (units)",
    )
    _style_legend(ax2, loc="upper right")
    fig2_path = out_dir / "q8_seasonality_volume.png"
    _save_chart(fig2, fig2_path)

    peaks = []
    for t in UNITS_ORDER:
        s = seasonal[seasonal["Type"] == t]
        pmax = s.loc[s["mean_price"].idxmax()]
        pmin = s.loc[s["mean_price"].idxmin()]
        vmax = s.loc[s["mean_monthly_volume"].idxmax()]
        vmin = s.loc[s["mean_monthly_volume"].idxmin()]
        peaks.append(
            {
                "Type": t.title(),
                "Peak Price Month": MONTH_LABELS[int(pmax["month"]) - 1],
                "Low Price Month": MONTH_LABELS[int(pmin["month"]) - 1],
                "Peak Volume Month": MONTH_LABELS[int(vmax["month"]) - 1],
                "Low Volume Month": MONTH_LABELS[int(vmin["month"]) - 1],
            }
        )
    peaks_df = pd.DataFrame(peaks)
    peaks_df.to_csv(out_dir / "q8_seasonality_peaks.csv", index=False)

    md = []
    md.append("# Question 8")
    md.append("")
    md.append("## Method")
    md.append("- Used complete years only (2019-2024) to avoid partial-year seasonality bias from 2025 H1.")
    md.append("- Aggregated weekly data into monthly city totals/averages by type.")
    md.append("- Computed average month-of-year seasonality profiles for price and volume.")
    md.append("- Identified peak/low months for each type.")
    md.append("")
    md.append("## Key Output")
    md.append(md_table(peaks_df))
    md.append("")
    md.append("## Graphical Depictions")
    md.append("- `q8_seasonality_price.png`")
    md.append("- `q8_seasonality_volume.png`")
    md.append("")
    md.append("Supporting CSVs: `q8_monthly_seasonality.csv`, `q8_seasonality_peaks.csv`, `q8_month_coverage.csv`.")

    (out_dir / "question_8.md").write_text("\n".join(md), encoding="utf-8")
    return {"q8_seasonality": seasonal}


def solve_q9(out_dir: Path) -> None:
    md = []
    md.append("# Question 9")
    md.append("")
    md.append("## Recommendations to Manage Seasonality")
    md.append("- Use **contract tiers** with growers and retailers (base volume + seasonal flex volume) so supply can expand in high-demand months without overcommitting year-round.")
    md.append("- Shift to **seasonal pricing and promotion calendars**: promote aggressively in low-volume months and protect margin when demand is naturally high.")
    md.append("- Build a **city-level allocation model** that routes supply toward markets with the highest expected margin each month.")
    md.append("- Improve **cold-chain and transit reliability** in peak months to reduce spoilage and stockouts when velocity is highest.")
    md.append("- Expand **demand smoothing channels** (food-service contracts, subscription boxes, institutional buyers) to absorb excess in weaker months.")
    md.append("- Coordinate with trade associations on **consumer education campaigns** (recipes, health messaging) timed to historically soft months.")
    md.append("- Run monthly **S&OP reviews** (forecast vs actual price/volume) and adjust purchase commitments and distribution plans quickly.")

    (out_dir / "question_9.md").write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir.parent / "case_comp_data.csv"
    df = load_data(csv_path)
    df.to_csv(out_dir / "cleaned_data_2019_to_2025H1.csv", index=False)

    q1 = solve_q1(df, out_dir)
    solve_q2(df, out_dir)
    solve_q3(df, out_dir)
    solve_q4(df, q1["q1_winners"], out_dir)
    solve_q5_q6_q7(df, out_dir)
    solve_q8(df, out_dir)
    solve_q9(out_dir)

    index_lines = [
        "# Outputs Index",
        "",
        "Generated files:",
    ]
    for p in sorted(out_dir.glob("*")):
        if p.name == Path(__file__).name:
            continue
        index_lines.append(f"- `{p.name}`")
    (out_dir / "README.md").write_text("\n".join(index_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
