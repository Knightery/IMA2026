from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

from solve_case import (
    THEME,
    UNITS_ORDER,
    _fmt_millions,
    _new_chart,
    _save_chart,
    _style_axes,
    _style_legend,
    load_data,
)


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent
PERIOD_ORDER = [str(y) for y in range(2019, 2025)] + ["2025 H1"]
TOP5_PERIODS = [str(y) for y in range(2019, 2025)] + ["2025 H1"]
SERIES = {
    "Los Angeles": THEME["primary"],
    "New York": THEME["compare"],
    "Seattle": THEME["accent"],
    "DallasFtWorth": THEME["primary_soft"],
    "BaltimoreWashington": THEME["stress"],
    "San Francisco": "#718679",
    "Chicago": "#7a7f77",
}


def _periodize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Period"] = out["Date"].dt.year.astype(str)
    out.loc[(out["Date"] >= "2025-01-01") & (out["Date"] <= "2025-06-30"), "Period"] = "2025 H1"
    out = out[out["Period"].isin(PERIOD_ORDER)].copy()
    return out


def _lighten(hex_color: str, alpha: float) -> tuple[float, float, float, float]:
    return to_rgba(hex_color, alpha)


def plot_q1_winner_matrix() -> None:
    winners = pd.read_csv(OUT_DIR / "q1_winners_long.csv")
    winners["Period"] = pd.Categorical(winners["Period"], categories=PERIOD_ORDER, ordered=True)

    fig, ax = plt.subplots(figsize=(11.4, 3.8))
    fig.patch.set_facecolor(THEME["bg"])
    ax.set_facecolor(THEME["bg"])
    ax.set_xlim(0, len(PERIOD_ORDER))
    ax.set_ylim(0, len(UNITS_ORDER))
    ax.axis("off")

    for row_idx, prod_type in enumerate(UNITS_ORDER):
        row = (
            winners[winners["Type"] == prod_type]
            .sort_values("Period")
            .reset_index(drop=True)
        )
        min_rev = row["Sales_Dollars"].min()
        max_rev = row["Sales_Dollars"].max()
        base = THEME["compare"] if prod_type == "conventional" else THEME["primary"]

        for col_idx, rec in row.iterrows():
            ratio = 0.55 if max_rev == min_rev else 0.48 + 0.42 * (
                (rec["Sales_Dollars"] - min_rev) / (max_rev - min_rev)
            )
            rect = Rectangle(
                (col_idx + 0.03, len(UNITS_ORDER) - row_idx - 0.97),
                0.94,
                0.94,
                facecolor=_lighten(base, ratio),
                edgecolor=THEME["paper"],
                linewidth=1.4,
            )
            ax.add_patch(rect)
            ax.text(
                col_idx + 0.5,
                len(UNITS_ORDER) - row_idx - 0.58,
                rec["City"],
                ha="center",
                va="center",
                color=THEME["paper"],
                fontsize=13,
                fontweight="bold",
            )
            ax.text(
                col_idx + 0.5,
                len(UNITS_ORDER) - row_idx - 0.77,
                f"${rec['Sales_Dollars'] / 1_000_000:.1f}M",
                ha="center",
                va="center",
                color=THEME["paper"],
                fontsize=10,
            )

    for idx, period in enumerate(PERIOD_ORDER):
        ax.text(
            idx + 0.5,
            2.08,
            period,
            ha="center",
            va="bottom",
            fontsize=11,
            color=THEME["muted"],
            fontweight="bold",
        )

    ax.text(
        -0.08,
        1.5,
        "Conventional",
        ha="right",
        va="center",
        fontsize=12,
        color=THEME["compare"],
        fontweight="bold",
    )
    ax.text(
        -0.08,
        0.5,
        "Organic",
        ha="right",
        va="center",
        fontsize=12,
        color=THEME["primary"],
        fontweight="bold",
    )

    fig.text(
        0.06,
        0.95,
        "Los Angeles leads dollar sales in every required period and both types",
        fontsize=17,
        fontweight="bold",
        color=THEME["ink"],
    )
    fig.text(
        0.06,
        0.90,
        "Cell shading intensifies as winner revenue rises within each product type.",
        fontsize=10.5,
        color=THEME["muted"],
    )

    _save_chart(fig, OUT_DIR / "deck_q1_winner_matrix.png")


def plot_sales_leader_trend(df: pd.DataFrame, prod_type: str, filename: str, title: str) -> None:
    scoped = _periodize(df.copy())
    scoped["Revenue"] = scoped["Average_price"] * scoped["Total_Volume"]
    annual = (
        scoped.groupby(["Period", "City", "Type"], as_index=False)["Revenue"]
        .sum()
    )
    annual["Period"] = pd.Categorical(annual["Period"], categories=TOP5_PERIODS, ordered=True)
    sub = annual[annual["Type"] == prod_type].copy()

    top_cities = (
        sub[sub["Period"] != "2025 H1"]
        .groupby("City")["Revenue"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .index
        .tolist()
    )
    plot_df = (
        sub[sub["City"].isin(top_cities)]
        .pivot(index="Period", columns="City", values="Revenue")
        .reindex(TOP5_PERIODS)
    )

    fig, ax = _new_chart(figsize=(10.0, 5.2))
    xs = np.arange(len(TOP5_PERIODS))
    ax.axvspan(5.5, 6.5, color=to_rgba(THEME["accent"], 0.07), zorder=0)

    for city in top_cities:
        color = SERIES.get(city, THEME["primary_soft"])
        linewidth = 3.0 if city == "Los Angeles" else 2.2
        alpha = 0.95 if city in {"Los Angeles", "New York", "Seattle"} else 0.75
        ax.plot(
            xs,
            plot_df[city].to_numpy(),
            marker="o",
            markersize=5.5,
            linewidth=linewidth,
            color=color,
            alpha=alpha,
            label=city,
        )
        last_val = plot_df.loc["2024", city]
        ax.text(
            5.08,
            last_val,
            f" {city}",
            color=color,
            fontsize=9.5,
            va="center",
        )

    _style_axes(ax, title, "Period", "Sales revenue ($)", grid_axis="y")
    ax.set_xticks(xs)
    ax.set_xticklabels(TOP5_PERIODS)
    ax.yaxis.set_major_formatter(FuncFormatter(_fmt_millions))
    ax.text(
        0.985,
        0.03,
        "2025 H1 is shaded because it is a partial year.",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color=THEME["muted"],
    )
    _style_legend(ax, loc="upper left", ncol=2)
    _save_chart(fig, OUT_DIR / filename)


def plot_q2_winner_timeline() -> None:
    q2 = pd.read_csv(OUT_DIR / "q2_organic_share_winners_raw.csv")
    q2["Organic Share"] = q2["Organic Share"] * 100
    colors = {"Seattle": THEME["primary"], "Orlando": THEME["accent"], "Charlotte": THEME["stress"]}

    fig, ax = _new_chart(figsize=(9.8, 4.8))
    xs = np.arange(len(PERIOD_ORDER))
    ys = q2["Organic Share"].to_numpy()

    ax.plot(xs, ys, color=THEME["primary_soft"], linewidth=2.2, alpha=0.8, zorder=1)

    for i, row in q2.iterrows():
        color = colors.get(row["City"], THEME["compare"])
        ax.scatter(
            xs[i],
            row["Organic Share"],
            s=130,
            color=color,
            edgecolor=THEME["paper"],
            linewidth=1.2,
            zorder=3,
        )
        ax.text(
            xs[i],
            row["Organic Share"] + 0.22,
            f"{row['City']}\n{row['Organic Share']:.2f}%",
            ha="center",
            va="bottom",
            fontsize=9.2,
            color=THEME["ink"],
        )

    _style_axes(
        ax,
        "Seattle leads organic penetration in five of the seven required periods",
        "Period",
        "Organic share of city volume (%)",
        grid_axis="y",
    )
    ax.set_xticks(xs)
    ax.set_xticklabels(PERIOD_ORDER)
    ax.set_ylim(8.2, 13.5)
    _save_chart(fig, OUT_DIR / "deck_q2_winner_timeline.png")


def plot_q2_growth_share(df: pd.DataFrame) -> None:
    scoped = df[df["Date"].dt.year.between(2019, 2024)].copy()
    scoped["Year"] = scoped["Date"].dt.year
    annual = scoped.groupby(["Year", "Type"], as_index=False)["Total_Volume"].sum()
    pivot = annual.pivot(index="Year", columns="Type", values="Total_Volume")
    pivot["total"] = pivot["conventional"] + pivot["organic"]

    idx_total = (pivot.loc[2024, "total"] / pivot.loc[2019, "total"]) * 100
    idx_org = (pivot.loc[2024, "organic"] / pivot.loc[2019, "organic"]) * 100
    share_2019 = (pivot.loc[2019, "organic"] / pivot.loc[2019, "total"]) * 100
    share_2024 = (pivot.loc[2024, "organic"] / pivot.loc[2024, "total"]) * 100
    delta_share = share_2024 - share_2019

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.8))
    fig.patch.set_facecolor(THEME["bg"])
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.14, top=0.76, wspace=0.24)

    for ax in (ax1, ax2):
        ax.set_facecolor(THEME["panel"])
        for side in ["top", "right"]:
            ax.spines[side].set_visible(False)
        for side in ["left", "bottom"]:
            ax.spines[side].set_color(THEME["line"])
            ax.spines[side].set_linewidth(1.1)
        ax.tick_params(colors=THEME["muted"], labelsize=10)
        ax.set_axisbelow(True)

    bars = ax1.bar(
        ["Total market", "Organic"],
        [idx_total, idx_org],
        color=[THEME["compare"], THEME["primary"]],
        width=0.58,
    )
    ax1.axhline(100, color=THEME["line"], linewidth=1.2, linestyle="--")
    ax1.set_ylim(0, 210)
    ax1.grid(axis="y", color=THEME["line"], linewidth=0.9, alpha=0.75)
    ax1.set_title("Indexed volume growth\n2019 = 100", loc="left", fontsize=13, fontweight="bold", color=THEME["ink"])
    ax1.set_ylabel("Index", color=THEME["muted"], fontsize=11)
    for bar, val in zip(bars, [idx_total, idx_org]):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
            color=THEME["ink"],
            fontweight="bold",
        )

    x = np.arange(3)
    bottoms = [0, share_2019, 0]
    heights = [share_2019, delta_share, share_2024]
    colors = [THEME["compare"], THEME["accent"], THEME["primary"]]
    labels = ["2019 share", "share gain", "2024 share"]
    ax2.bar(x[0], heights[0], color=colors[0], width=0.58)
    ax2.bar(x[1], heights[1], bottom=bottoms[1], color=colors[1], width=0.58)
    ax2.bar(x[2], heights[2], color=colors[2], width=0.58)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.set_ylim(0, 7.4)
    ax2.grid(axis="y", color=THEME["line"], linewidth=0.9, alpha=0.75)
    ax2.set_title("Organic share bridge", loc="left", fontsize=13, fontweight="bold", color=THEME["ink"])
    ax2.set_ylabel("Share of total volume (%)", color=THEME["muted"], fontsize=11)
    ax2.text(x[0], heights[0] + 0.15, f"{share_2019:.2f}%", ha="center", va="bottom", fontsize=10, color=THEME["ink"], fontweight="bold")
    ax2.text(x[1], bottoms[1] + heights[1] + 0.15, f"+{delta_share:.2f} pts", ha="center", va="bottom", fontsize=10, color=THEME["ink"], fontweight="bold")
    ax2.text(x[2], heights[2] + 0.15, f"{share_2024:.2f}%", ha="center", va="bottom", fontsize=10, color=THEME["ink"], fontweight="bold")

    fig.suptitle(
        "Organic volume nearly doubled from 2019 to 2024 while share rose 1.77 points",
        x=0.06,
        y=0.955,
        ha="left",
        fontsize=15,
        fontweight="bold",
        color=THEME["ink"],
    )
    fig.text(0.06, 0.875, "Organic volume growth outpaced total market growth by a wide margin.", fontsize=10, color=THEME["muted"])
    _save_chart(fig, OUT_DIR / "deck_q2_growth_share.png")


def plot_q3_within_type_metrics() -> None:
    metrics = pd.read_csv(OUT_DIR / "q3_price_volume_metrics_raw.csv")
    order = ["All", "Conventional", "Organic"]
    metrics["Segment"] = pd.Categorical(metrics["Segment"], categories=order, ordered=True)
    metrics = metrics.sort_values("Segment")
    colors = [THEME["accent"], THEME["compare"], THEME["primary"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.7))
    fig.patch.set_facecolor(THEME["bg"])

    for ax in (ax1, ax2):
        ax.set_facecolor(THEME["panel"])
        for side in ["top", "right"]:
            ax.spines[side].set_visible(False)
        for side in ["left", "bottom"]:
            ax.spines[side].set_color(THEME["line"])
            ax.spines[side].set_linewidth(1.1)
        ax.tick_params(colors=THEME["muted"], labelsize=10)
        ax.set_axisbelow(True)
        ax.grid(axis="x", color=THEME["line"], linewidth=0.9, alpha=0.75)

    y = np.arange(len(metrics))
    ax1.barh(y, metrics["Pearson_r"], color=colors, height=0.54)
    ax1.set_yticks(y)
    ax1.set_yticklabels(metrics["Segment"])
    ax1.set_xlim(-0.5, 0.05)
    ax1.axvline(0, color=THEME["line"], linewidth=1.0)
    ax1.set_title("Pearson correlation", loc="left", fontsize=13, fontweight="bold", color=THEME["ink"])
    for i, val in enumerate(metrics["Pearson_r"]):
        ax1.text(val - 0.01 if val < 0 else val + 0.01, i, f"{val:.3f}", va="center", ha="right" if val < 0 else "left", fontsize=10, color=THEME["ink"])

    ax2.barh(y, metrics["Linear_R2"], color=colors, height=0.54)
    ax2.set_yticks(y)
    ax2.set_yticklabels([])
    ax2.set_xlim(0, 0.21)
    ax2.set_title("Linear R²", loc="left", fontsize=13, fontweight="bold", color=THEME["ink"])
    for i, val in enumerate(metrics["Linear_R2"]):
        ax2.text(val + 0.006, i, f"{val:.3f}", va="center", ha="left", fontsize=10, color=THEME["ink"])

    fig.suptitle(
        "Within product type, price alone explains very little variation in volume",
        x=0.06,
        y=0.97,
        ha="left",
        fontsize=16,
        fontweight="bold",
        color=THEME["ink"],
    )
    fig.text(0.06, 0.91, "The pooled market signal is meaningful, but type-specific relationships are weak.", fontsize=10, color=THEME["muted"])
    _save_chart(fig, OUT_DIR / "deck_q3_within_type_metrics.png")


def plot_macro_driver_heatmap() -> None:
    scores = pd.DataFrame(
        {
            "Consumer demand": [5, 2, 3, 1, 3],
            "Margin pressure": [4, 5, 4, 4, 4],
            "Service reliability": [1, 4, 5, 4, 5],
        },
        index=[
            "Inflation",
            "Freight + fuel",
            "Import dependence",
            "Labor costs",
            "Supply chain disruption",
        ],
    )

    cmap = LinearSegmentedColormap.from_list(
        "executive_avocado_heat",
        [THEME["paper"], THEME["primary_soft"], THEME["accent"], THEME["stress"]],
    )

    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    fig.patch.set_facecolor(THEME["bg"])
    ax.set_facecolor(THEME["panel"])
    im = ax.imshow(scores.to_numpy(), cmap=cmap, vmin=1, vmax=5, aspect="auto")

    ax.set_xticks(np.arange(scores.shape[1]))
    ax.set_yticks(np.arange(scores.shape[0]))
    ax.set_xticklabels(scores.columns, color=THEME["muted"], fontsize=10)
    ax.set_yticklabels(scores.index, color=THEME["ink"], fontsize=10)
    ax.set_title(
        "Freight, import dependence, and inflation are the main macro pressures on demand and margin",
        loc="left",
        fontsize=15,
        fontweight="bold",
        color=THEME["ink"],
        pad=12,
    )
    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)

    labels = {1: "Low", 2: "Low-Med", 3: "Medium", 4: "High", 5: "Very High"}
    for r in range(scores.shape[0]):
        for c in range(scores.shape[1]):
            val = int(scores.iloc[r, c])
            ax.text(c, r, labels[val], ha="center", va="center", color=THEME["ink"], fontsize=9, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cbar.outline.set_edgecolor(THEME["line"])
    cbar.ax.tick_params(colors=THEME["muted"], labelsize=9)
    cbar.set_label("Qualitative impact score", color=THEME["muted"], fontsize=10)
    fig.text(
        0.06,
        0.91,
        "Qualitative assessment inferred from the case context and produce-market operating logic.",
        fontsize=10,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q4_macro_driver_heatmap.png")


def plot_city_micro_heatmap(df: pd.DataFrame) -> None:
    focus = ["Los Angeles", "Seattle", "Boise", "Portland", "Spokane", "San Diego"]

    year_2024 = df[df["Date"].dt.year == 2024].copy()
    year_2024["Revenue"] = year_2024["Average_price"] * year_2024["Total_Volume"]
    market_scale = year_2024.groupby("City", as_index=False)["Revenue"].sum().rename(columns={"Revenue": "Market scale ($M)"})
    market_scale["Market scale ($M)"] = market_scale["Market scale ($M)"] / 1_000_000

    vol_2024 = year_2024.groupby(["City", "Type"], as_index=False)["Total_Volume"].sum()
    share = vol_2024.pivot(index="City", columns="Type", values="Total_Volume").fillna(0)
    share["Organic share (%)"] = (share.get("organic", 0) / (share.get("organic", 0) + share.get("conventional", 0))) * 100
    share = share.reset_index()[["City", "Organic share (%)"]]

    june_prices = pd.read_csv(OUT_DIR / "q5_june2025_city_prices.csv")[["City", "avg_retail_price_jun2025", "Mileage_miles"]]
    june_prices = june_prices.rename(
        columns={
            "avg_retail_price_jun2025": "June 2025 price ($)",
            "Mileage_miles": "Miles from West Valley",
        }
    )

    merged = market_scale.merge(share, on="City").merge(june_prices, on="City")
    merged = merged[merged["City"].isin(focus)].copy().set_index("City").loc[focus]

    color_df = merged.copy()
    color_df["Miles from West Valley"] = color_df["Miles from West Valley"].max() - color_df["Miles from West Valley"]
    color_scaled = (color_df - color_df.min()) / (color_df.max() - color_df.min())

    cmap = LinearSegmentedColormap.from_list(
        "city_heat",
        [THEME["paper"], THEME["primary_soft"], THEME["primary"]],
    )

    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    fig.patch.set_facecolor(THEME["bg"])
    ax.set_facecolor(THEME["panel"])
    ax.imshow(color_scaled.to_numpy(), cmap=cmap, vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(np.arange(merged.shape[1]))
    ax.set_yticks(np.arange(merged.shape[0]))
    ax.set_xticklabels(merged.columns, fontsize=10, color=THEME["muted"])
    ax.set_yticklabels(merged.index, fontsize=10, color=THEME["ink"])
    ax.set_title(
        "City micro-drivers differ across scale, organic readiness, price support, and route efficiency",
        loc="left",
        fontsize=15,
        fontweight="bold",
        color=THEME["ink"],
        pad=12,
    )

    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)

    for r in range(merged.shape[0]):
        for c, col in enumerate(merged.columns):
            val = merged.iloc[r, c]
            if "scale" in col.lower():
                label = f"${val:.1f}M"
            elif "share" in col.lower():
                label = f"{val:.1f}%"
            elif "price" in col.lower():
                label = f"${val:.2f}"
            else:
                label = f"{int(round(val))}"
            ax.text(c, r, label, ha="center", va="center", fontsize=9.2, color=THEME["ink"], fontweight="bold")

    fig.text(
        0.06,
        0.91,
        "Heatmap shading is normalized by column. Lower miles are treated as better route efficiency for coloring.",
        fontsize=10,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q4_city_micro_heatmap.png")


def plot_price_vs_miles() -> None:
    prices = pd.read_csv(OUT_DIR / "q5_june2025_city_prices.csv")
    base = pd.read_csv(OUT_DIR / "q5_city_profitability_base.csv")[["City", "Profit"]]
    data = prices.merge(base, on="City")
    selected = {"Seattle", "Boise", "Portland", "Spokane", "San Diego"}
    compare_cities = {"Los Angeles", "San Francisco", "Sacramento"}

    fig, ax = _new_chart(figsize=(10.0, 5.1))
    ax.scatter(
        data[~data["City"].isin(selected | compare_cities)]["Mileage_miles"],
        data[~data["City"].isin(selected | compare_cities)]["avg_retail_price_jun2025"],
        s=(data[~data["City"].isin(selected | compare_cities)]["Profit"] / 90),
        color=to_rgba(THEME["primary_soft"], 0.35),
        edgecolor=THEME["paper"],
        linewidth=0.6,
        zorder=1,
    )

    peer = data[data["City"].isin(compare_cities)]
    ax.scatter(
        peer["Mileage_miles"],
        peer["avg_retail_price_jun2025"],
        s=(peer["Profit"] / 70),
        color=to_rgba(THEME["compare"], 0.75),
        edgecolor=THEME["paper"],
        linewidth=0.8,
        zorder=3,
        label="California comparison markets",
    )

    chosen = data[data["City"].isin(selected)]
    ax.scatter(
        chosen["Mileage_miles"],
        chosen["avg_retail_price_jun2025"],
        s=(chosen["Profit"] / 55),
        color=to_rgba(THEME["primary"], 0.92),
        edgecolor=THEME["accent"],
        linewidth=1.4,
        zorder=4,
        label="Recommended top five",
    )

    for _, row in chosen.iterrows():
        ax.text(
            row["Mileage_miles"] + 18,
            row["avg_retail_price_jun2025"] + 0.015,
            row["City"],
            fontsize=9.3,
            color=THEME["ink"],
        )
    for _, row in peer.iterrows():
        ax.text(
            row["Mileage_miles"] + 15,
            row["avg_retail_price_jun2025"] - 0.03,
            row["City"],
            fontsize=8.8,
            color=THEME["compare"],
        )

    ax.axvline(data["Mileage_miles"].median(), color=THEME["line"], linewidth=1.1, linestyle="--")
    ax.axhline(data["avg_retail_price_jun2025"].median(), color=THEME["line"], linewidth=1.1, linestyle="--")
    _style_axes(
        ax,
        "Best entry markets combine premium price support with acceptable shipping distance",
        "Mileage from West Valley",
        "Average organic retail price in June 2025 ($ / unit)",
        grid_axis="both",
    )
    _style_legend(ax, loc="lower right")
    _save_chart(fig, OUT_DIR / "deck_q5_price_vs_miles.png")


def plot_q5_unit_economics_waterfall() -> None:
    top5 = pd.read_csv(OUT_DIR / "q5_top5_cities.csv")
    revenue = top5["Revenue"].mean()
    shipping = top5["Shipping_Cost"].mean()
    acquisition = top5["Acquisition_Cost"].mean()
    profit = top5["Profit"].mean()

    steps = [
        ("Revenue", revenue, THEME["primary"]),
        ("Shipping", -shipping, THEME["stress"]),
        ("Acquisition", -acquisition, THEME["compare"]),
    ]
    running = 0
    starts = []
    heights = []
    for _, value, _ in steps:
        starts.append(running if value >= 0 else running + value)
        heights.append(abs(value))
        running += value

    fig, ax = _new_chart(figsize=(9.8, 5.0))
    x = np.arange(len(steps) + 1)
    width = 0.62

    for i, ((_, value, color), start, height) in enumerate(zip(steps, starts, heights)):
        ax.bar(i, height, bottom=start, width=width, color=color)
        ax.text(
            i,
            start + height + (400 if value >= 0 else -650),
            f"${abs(value):,.0f}",
            ha="center",
            va="bottom" if value >= 0 else "top",
            color=THEME["ink"],
            fontsize=10,
            fontweight="bold",
        )

    ax.bar(len(steps), profit, width=width, color=THEME["accent"])
    ax.text(
        len(steps),
        profit + 450,
        f"${profit:,.0f}",
        ha="center",
        va="bottom",
        color=THEME["ink"],
        fontsize=10.5,
        fontweight="bold",
    )

    ax.axhline(0, color=THEME["line"], linewidth=1.0)
    _style_axes(
        ax,
        "Average top-five city economics remain strongly positive under base assumptions",
        "",
        "Average dollars per 20,000-unit city scenario",
        grid_axis="y",
    )
    ax.set_xticks(x)
    ax.set_xticklabels([label for label, _, _ in steps] + ["Profit"])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"${v/1000:.0f}k"))
    ax.text(
        0.985,
        0.03,
        "Model uses June 2025 price as the June 2026 forecast, 40% wholesale pricing,\n$0.20 acquisition cost, and shipping = $1,500 + $50 per 100 miles.",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q5_unit_economics_waterfall.png")


def plot_q5_price_ranking() -> None:
    prices = (
        pd.read_csv(OUT_DIR / "q5_june2025_city_prices.csv")
        .sort_values("avg_retail_price_jun2025", ascending=False)
        .head(15)
    )
    selected = {"Seattle", "Boise", "Portland", "Spokane", "San Diego"}
    colors = [THEME["primary"] if c in selected else THEME["primary_soft"] for c in prices["City"]]

    fig, ax = _new_chart(figsize=(9.8, 5.3))
    y = np.arange(len(prices))
    ax.barh(y, prices["avg_retail_price_jun2025"], color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(prices["City"])
    ax.invert_yaxis()
    _style_axes(
        ax,
        "The recommended top five are also the five highest June 2025 organic price markets",
        "",
        "Average organic retail price in June 2025 ($ / unit)",
        grid_axis="x",
    )
    for i, (_, row) in enumerate(prices.iterrows()):
        ax.text(
            row["avg_retail_price_jun2025"] + 0.02,
            i,
            f"${row['avg_retail_price_jun2025']:.2f}",
            va="center",
            ha="left",
            fontsize=9.3,
            color=THEME["ink"],
        )
    ax.axvline(prices["avg_retail_price_jun2025"].median(), color=THEME["line"], linewidth=1.1, linestyle="--")
    ax.text(
        0.985,
        0.04,
        "San Diego is the fifth price market at $2.09; San Francisco is next at $1.97.",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q5_price_ranking.png")


def plot_q5_profit_ranking() -> None:
    base = pd.read_csv(OUT_DIR / "q5_city_profitability_base.csv").copy()
    focus = base.head(12).copy()
    selected = set(base.head(5)["City"])
    colors = [THEME["primary"] if c in selected else THEME["compare"] for c in focus["City"]]

    fig, ax = _new_chart(figsize=(9.9, 5.4))
    y = np.arange(len(focus))
    ax.barh(y, focus["Profit"], color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(focus["City"])
    ax.invert_yaxis()
    _style_axes(
        ax,
        "Base-case profit ranking shows a clear top-five cut line",
        "",
        "Expected profit per 20,000-unit city scenario ($)",
        grid_axis="x",
    )
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"${v/1000:.0f}k"))
    for i, (_, row) in enumerate(focus.iterrows()):
        ax.text(row["Profit"] + 120, i, f"${row['Profit']:,.0f}", va="center", ha="left", fontsize=9.2, color=THEME["ink"])
    ax.axhline(4.5, color=THEME["accent"], linewidth=1.6, linestyle="--")
    ax.text(
        0.985,
        0.06,
        "Top-five avg profit = $13.7k\nNext-five avg profit = $9.2k\nAll 40 modeled cities remain profitable in the base case.",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q5_profit_ranking.png")


def plot_q5_selection_matrix() -> None:
    top5 = pd.read_csv(OUT_DIR / "q5_top5_cities.csv").copy()
    show = top5[["City", "forecast_retail_price_jun2026", "Mileage_miles", "Profit", "Profit_Margin"]].copy()
    show = show.rename(
        columns={
            "forecast_retail_price_jun2026": "Forecast price ($)",
            "Mileage_miles": "Miles",
            "Profit": "Profit ($)",
            "Profit_Margin": "Margin (%)",
        }
    )
    show["Margin (%)"] = show["Margin (%)"] * 100
    numeric = show.set_index("City")
    color_df = numeric.copy()
    color_df["Miles"] = color_df["Miles"].max() - color_df["Miles"]
    scaled = (color_df - color_df.min()) / (color_df.max() - color_df.min())
    cmap = LinearSegmentedColormap.from_list("selection_matrix", [THEME["paper"], THEME["primary_soft"], THEME["primary"]])

    fig, ax = plt.subplots(figsize=(9.4, 4.9))
    fig.patch.set_facecolor(THEME["bg"])
    ax.set_facecolor(THEME["panel"])
    ax.imshow(scaled.to_numpy(), cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(np.arange(numeric.shape[1]))
    ax.set_yticks(np.arange(numeric.shape[0]))
    ax.set_xticklabels(numeric.columns, fontsize=10, color=THEME["muted"])
    ax.set_yticklabels(numeric.index, fontsize=10, color=THEME["ink"])
    ax.set_title(
        "Seattle, Boise, Portland, Spokane, and San Diego form the best selection matrix",
        loc="left",
        fontsize=15,
        fontweight="bold",
        color=THEME["ink"],
        pad=12,
    )
    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)
    for r in range(numeric.shape[0]):
        for c, col in enumerate(numeric.columns):
            val = numeric.iloc[r, c]
            if "price" in col.lower():
                label = f"${val:.2f}"
            elif "margin" in col.lower():
                label = f"{val:.1f}%"
            elif "profit" in col.lower():
                label = f"${val:,.0f}"
            else:
                label = f"{int(round(val))}"
            ax.text(c, r, label, ha="center", va="center", fontsize=9.3, color=THEME["ink"], fontweight="bold")
    fig.text(
        0.06,
        0.91,
        "Higher shading is better by column. Miles are inverted for coloring so lower distance scores stronger.",
        fontsize=10,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q5_selection_matrix.png")


def plot_q5_frontier_zoom() -> None:
    prices = pd.read_csv(OUT_DIR / "q5_june2025_city_prices.csv")
    base = pd.read_csv(OUT_DIR / "q5_city_profitability_base.csv")[["City", "Profit"]]
    data = prices.merge(base, on="City").sort_values("Profit", ascending=False).head(12)
    selected = {"Seattle", "Boise", "Portland", "Spokane", "San Diego"}

    fig, ax = _new_chart(figsize=(9.8, 5.1))
    others = data[~data["City"].isin(selected)]
    chosen = data[data["City"].isin(selected)]

    ax.scatter(
        others["Mileage_miles"],
        others["avg_retail_price_jun2025"],
        s=others["Profit"] / 18,
        color=to_rgba(THEME["compare"], 0.7),
        edgecolor=THEME["paper"],
        linewidth=0.7,
        label="Next-best alternatives",
    )
    ax.scatter(
        chosen["Mileage_miles"],
        chosen["avg_retail_price_jun2025"],
        s=chosen["Profit"] / 14,
        color=to_rgba(THEME["primary"], 0.95),
        edgecolor=THEME["accent"],
        linewidth=1.3,
        label="Recommended top five",
    )

    for _, row in chosen.iterrows():
        ax.text(row["Mileage_miles"] + 16, row["avg_retail_price_jun2025"] + 0.013, row["City"], fontsize=9.2, color=THEME["ink"])
    for _, row in others.iterrows():
        ax.text(row["Mileage_miles"] + 16, row["avg_retail_price_jun2025"] - 0.03, row["City"], fontsize=8.6, color=THEME["compare"])

    _style_axes(
        ax,
        "The chosen five win because price support outweighs pure proximity",
        "Mileage from West Valley",
        "Average organic retail price in June 2025 ($ / unit)",
        grid_axis="both",
    )
    _style_legend(ax, loc="lower right")
    _save_chart(fig, OUT_DIR / "deck_q5_frontier_zoom.png")


def plot_q6_scenario_compare(scenario: str, filename: str, title: str) -> None:
    base = pd.read_csv(OUT_DIR / "q5_city_profitability_base.csv")
    scenario_df = pd.read_csv(
        OUT_DIR / ("q6_city_profitability_shipping_up_50.csv" if scenario == "up" else "q6_city_profitability_shipping_down_50.csv")
    )
    top5 = base.head(5)[["City", "Profit"]].merge(scenario_df[["City", "Profit"]], on="City", suffixes=("_base", "_scenario"))
    cities = top5["City"].tolist()
    x = np.arange(len(cities))
    width = 0.34
    scenario_color = THEME["stress"] if scenario == "up" else THEME["compare"]
    scenario_label = "Shipping +50%" if scenario == "up" else "Shipping -50%"

    fig, ax = _new_chart(figsize=(9.8, 5.0))
    ax.bar(x - width / 2, top5["Profit_base"], width=width, color=THEME["primary"], label="Base case")
    ax.bar(x + width / 2, top5["Profit_scenario"], width=width, color=scenario_color, label=scenario_label)
    _style_axes(
        ax,
        title,
        "Recommended city",
        "Profit per 20,000-unit city scenario ($)",
        grid_axis="y",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(cities)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"${v/1000:.0f}k"))
    for i, row in top5.iterrows():
        delta = row["Profit_scenario"] - row["Profit_base"]
        ax.text(
            i,
            max(row["Profit_base"], row["Profit_scenario"]) + 250,
            f"{delta:+.0f}",
            ha="center",
            va="bottom",
            fontsize=9.2,
            color=scenario_color,
            fontweight="bold",
        )
    _style_legend(ax, loc="upper right")
    _save_chart(fig, OUT_DIR / filename)


def plot_q7_rank_stability_matrix() -> None:
    rank = pd.read_csv(OUT_DIR / "q7_rank_comparison.csv").head(5).copy()
    matrix = rank.set_index("City")[["Rank_base", "Rank_up50", "Rank_down50"]]
    matrix.columns = ["Base", "+50% shipping", "-50% shipping"]

    fig, ax = plt.subplots(figsize=(8.6, 4.5))
    fig.patch.set_facecolor(THEME["bg"])
    ax.set_facecolor(THEME["panel"])
    ax.imshow(
        np.ones_like(matrix, dtype=float),
        cmap=LinearSegmentedColormap.from_list("rankstable", [THEME["paper"], THEME["primary_soft"]]),
        vmin=0,
        vmax=1,
        aspect="auto",
    )
    ax.set_xticks(np.arange(matrix.shape[1]))
    ax.set_yticks(np.arange(matrix.shape[0]))
    ax.set_xticklabels(matrix.columns, fontsize=10, color=THEME["muted"])
    ax.set_yticklabels(matrix.index, fontsize=10, color=THEME["ink"])
    ax.set_title(
        "The same five cities keep the same rank order in every modeled scenario",
        loc="left",
        fontsize=15,
        fontweight="bold",
        color=THEME["ink"],
        pad=12,
    )
    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            ax.text(c, r, f"#{int(matrix.iloc[r, c])}", ha="center", va="center", fontsize=12, color=THEME["ink"], fontweight="bold")
    fig.text(
        0.06,
        0.91,
        "Rank changes are zero for all five recommended cities under both freight scenarios.",
        fontsize=10,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q7_rank_stability_matrix.png")


def plot_q7_shipping_tornado() -> None:
    sens = pd.read_csv(OUT_DIR / "q7_shipping_sensitivity.csv").sort_values("Profit_Impact_for_50pct_Shipping_Change", ascending=False).head(12)
    selected = {"Seattle", "Boise", "Portland", "Spokane", "San Diego"}
    colors = [THEME["stress"] if c not in selected else THEME["primary"] for c in sens["City"]]

    fig, ax = _new_chart(figsize=(10.0, 5.2))
    y = np.arange(len(sens))
    ax.barh(y, sens["Profit_Impact_for_50pct_Shipping_Change"], color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(sens["City"])
    ax.invert_yaxis()
    _style_axes(
        ax,
        "Freight sensitivity is largest in distant Northeast markets, not in the recommended set",
        "",
        "Profit change from a ±50% shipping swing ($)",
        grid_axis="x",
    )
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"${v:,.0f}"))
    ax.text(
        0.985,
        0.04,
        "Boston, HartfordSpringfield, and Albany have the biggest absolute freight swings.\nRecommended cities shift by about $813 to $1,024 instead.",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color=THEME["muted"],
    )
    _save_chart(fig, OUT_DIR / "deck_q7_shipping_tornado.png")


def plot_q7_price_vs_sensitivity() -> None:
    prices = pd.read_csv(OUT_DIR / "q5_june2025_city_prices.csv")
    profit = pd.read_csv(OUT_DIR / "q5_city_profitability_base.csv")[["City", "Profit"]]
    sens = pd.read_csv(OUT_DIR / "q7_shipping_sensitivity.csv")
    data = prices.merge(sens, on="City").merge(profit, on="City")
    selected = {"Seattle", "Boise", "Portland", "Spokane", "San Diego"}
    comparison = {"Boston", "HartfordSpringfield", "Albany", "New York", "Philadelphia"}

    fig, ax = _new_chart(figsize=(9.8, 5.1))
    background = data[~data["City"].isin(selected | comparison)]
    ax.scatter(
        background["Profit_Impact_for_50pct_Shipping_Change"],
        background["avg_retail_price_jun2025"],
        s=background["Profit"] / 22,
        color=to_rgba(THEME["primary_soft"], 0.35),
        edgecolor=THEME["paper"],
        linewidth=0.5,
    )

    comp = data[data["City"].isin(comparison)]
    ax.scatter(
        comp["Profit_Impact_for_50pct_Shipping_Change"],
        comp["avg_retail_price_jun2025"],
        s=comp["Profit"] / 18,
        color=to_rgba(THEME["stress"], 0.8),
        edgecolor=THEME["paper"],
        linewidth=0.7,
        label="High-sensitivity East / Northeast markets",
    )

    chosen = data[data["City"].isin(selected)]
    ax.scatter(
        chosen["Profit_Impact_for_50pct_Shipping_Change"],
        chosen["avg_retail_price_jun2025"],
        s=chosen["Profit"] / 14,
        color=to_rgba(THEME["primary"], 0.95),
        edgecolor=THEME["accent"],
        linewidth=1.2,
        label="Recommended top five",
    )

    for _, row in chosen.iterrows():
        ax.text(row["Profit_Impact_for_50pct_Shipping_Change"] + 16, row["avg_retail_price_jun2025"] + 0.015, row["City"], fontsize=9.1, color=THEME["ink"])
    for _, row in comp.iterrows():
        ax.text(row["Profit_Impact_for_50pct_Shipping_Change"] + 10, row["avg_retail_price_jun2025"] - 0.025, row["City"], fontsize=8.5, color=THEME["stress"])

    ax.axvline(data["Profit_Impact_for_50pct_Shipping_Change"].median(), color=THEME["line"], linewidth=1.1, linestyle="--")
    ax.axhline(data["avg_retail_price_jun2025"].median(), color=THEME["line"], linewidth=1.1, linestyle="--")
    _style_axes(
        ax,
        "Local price support matters more than freight sensitivity in preserving the top-five ranking",
        "Profit impact from a ±50% shipping change ($)",
        "Average organic retail price in June 2025 ($ / unit)",
        grid_axis="both",
    )
    _style_legend(ax, loc="lower left")
    _save_chart(fig, OUT_DIR / "deck_q7_price_vs_sensitivity.png")


def main() -> None:
    df = load_data(ROOT / "case_comp_data.csv")

    plot_q1_winner_matrix()
    plot_sales_leader_trend(
        df,
        "conventional",
        "deck_q1_conventional_top5_trends.png",
        "Los Angeles' conventional sales lead is structural, not a one-year spike",
    )
    plot_sales_leader_trend(
        df,
        "organic",
        "deck_q1_organic_top5_trends.png",
        "Los Angeles leads organic sales too, but the gap is much tighter",
    )
    plot_q2_winner_timeline()
    plot_q2_growth_share(df)
    plot_q3_within_type_metrics()
    plot_macro_driver_heatmap()
    plot_city_micro_heatmap(df)
    plot_price_vs_miles()
    plot_q5_unit_economics_waterfall()
    plot_q5_price_ranking()
    plot_q5_profit_ranking()
    plot_q5_selection_matrix()
    plot_q5_frontier_zoom()
    plot_q6_scenario_compare(
        "up",
        "deck_q6_up50_compare.png",
        "A 50% freight increase compresses profit but does not change the top-five recommendation",
    )
    plot_q6_scenario_compare(
        "down",
        "deck_q6_down50_compare.png",
        "A 50% freight decrease expands profit, but the same cities still lead",
    )
    plot_q7_rank_stability_matrix()
    plot_q7_shipping_tornado()
    plot_q7_price_vs_sensitivity()


if __name__ == "__main__":
    main()
