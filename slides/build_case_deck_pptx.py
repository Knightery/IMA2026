from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Iterable

import pandas as pd
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SLIDES_DIR = ROOT / "slides"
OUT_DIR = ROOT / "outputs"
DEFAULT_OUTPUT = SLIDES_DIR / "case-deck.pptx"

from outputs.solve_case import load_data


@dataclass(frozen=True)
class Theme:
    bg: str = "F7F3EC"
    paper: str = "FCFAF5"
    panel: str = "FFFDF9"
    ink: str = "1F2621"
    muted: str = "5F6B63"
    primary: str = "355C47"
    primary_soft: str = "889A83"
    accent: str = "C58A2A"
    stress: str = "B5533A"
    compare: str = "3F728A"
    line: str = "D8D1C6"


THEME = Theme()
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN_X = Inches(0.6)
FONT_HEAD = "Aptos Display"
FONT_BODY = "Aptos"


def rgb(hex_color: str) -> RGBColor:
    return RGBColor.from_string(hex_color)


def fmt_money(value: float, digits: int = 1) -> str:
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.{digits}f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.{digits}f}k"
    return f"${value:,.0f}"


def fmt_pct(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}%"


def month_name(month_number: int) -> str:
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][month_number - 1]


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text: str,
    *,
    font_size: int = 18,
    color: str = THEME.ink,
    font_name: str = FONT_BODY,
    bold: bool = False,
    align: PP_ALIGN = PP_ALIGN.LEFT,
    valign: MSO_ANCHOR = MSO_ANCHOR.TOP,
    margin: float = 0.03,
) -> None:
    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = rgb(color)


def add_bullets(
    slide,
    left,
    top,
    width,
    height,
    bullets: Iterable[str],
    *,
    font_size: int = 16,
    color: str = THEME.ink,
    line_spacing: float = 1.15,
) -> None:
    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.03)
    tf.margin_right = Inches(0.03)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for idx, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        run = p.add_run()
        run.text = f"- {bullet}"
        run.font.name = FONT_BODY
        run.font.size = Pt(font_size)
        run.font.color.rgb = rgb(color)


def add_panel(
    slide,
    left,
    top,
    width,
    height,
    *,
    fill: str = THEME.panel,
    line: str = THEME.line,
    radius: MSO_AUTO_SHAPE_TYPE = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
) -> None:
    shape = slide.shapes.add_shape(radius, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.color.rgb = rgb(line)
    shape.line.width = Pt(1.0)


def add_badge(slide, text: str, left, top, width, *, fill: str, text_color: str = THEME.paper) -> None:
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.color.rgb = rgb(fill)
    add_textbox(
        slide,
        left + Inches(0.02),
        top + Inches(0.005),
        width - Inches(0.04),
        Inches(0.24),
        text.upper(),
        font_size=11,
        color=text_color,
        font_name=FONT_BODY,
        bold=True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )


def add_card(
    slide,
    left,
    top,
    width,
    height,
    *,
    header: str,
    metric: str,
    body: str,
    metric_color: str = THEME.ink,
) -> None:
    add_panel(slide, left, top, width, height)
    add_textbox(
        slide,
        left + Inches(0.16),
        top + Inches(0.15),
        width - Inches(0.32),
        Inches(0.24),
        header.upper(),
        font_size=11,
        color=THEME.muted,
        bold=True,
        font_name=FONT_BODY,
    )
    add_textbox(
        slide,
        left + Inches(0.16),
        top + Inches(0.42),
        width - Inches(0.32),
        Inches(0.55),
        metric,
        font_size=24,
        color=metric_color,
        bold=True,
        font_name=FONT_HEAD,
    )
    add_textbox(
        slide,
        left + Inches(0.16),
        top + Inches(0.96),
        width - Inches(0.32),
        height - Inches(1.12),
        body,
        font_size=15,
        color=THEME.ink,
        font_name=FONT_BODY,
    )


def add_background(slide, slide_number: int, *, section: str | None = None, footer: str = "Anonymized team submission") -> None:
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = rgb(THEME.bg)
    bg.line.fill.background()

    bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, Inches(10.1), Inches(0.14))
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(THEME.primary)
    bar.line.fill.background()

    accent_bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(10.1), 0, SLIDE_W - Inches(10.1), Inches(0.14))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = rgb(THEME.accent)
    accent_bar.line.fill.background()

    for size, line_color, transparency in [
        (Inches(2.6), THEME.line, 0.55),
        (Inches(1.95), THEME.primary_soft, 0.45),
        (Inches(1.15), THEME.accent, 0.72),
    ]:
        oval = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, Inches(10.35), Inches(0.02), size, size)
        oval.fill.background()
        oval.line.color.rgb = rgb(line_color)
        oval.line.width = Pt(4 if size > Inches(2) else 3)
        oval.line.transparency = transparency

    if section:
        add_textbox(
            slide,
            MARGIN_X,
            Inches(0.22),
            Inches(4.5),
            Inches(0.18),
            section.upper(),
            font_size=10,
            color=THEME.muted,
            bold=True,
            font_name=FONT_BODY,
        )

    add_textbox(
        slide,
        MARGIN_X,
        Inches(7.13),
        Inches(3.4),
        Inches(0.18),
        footer.upper(),
        font_size=9,
        color=THEME.muted,
        font_name=FONT_BODY,
    )
    add_textbox(
        slide,
        Inches(12.72),
        Inches(7.13),
        Inches(0.3),
        Inches(0.18),
        str(slide_number),
        font_size=9,
        color=THEME.muted,
        font_name=FONT_BODY,
        align=PP_ALIGN.RIGHT,
    )


def add_title(slide, title: str, *, top: float = 0.72, width: float = 11.3) -> None:
    add_textbox(
        slide,
        MARGIN_X,
        Inches(top),
        Inches(width),
        Inches(0.95),
        title,
        font_size=27,
        color=THEME.primary,
        font_name=FONT_HEAD,
        bold=True,
    )


def add_subtitle(slide, text: str, *, top: float, width: float = 10.5, color: str = THEME.muted) -> None:
    add_textbox(
        slide,
        MARGIN_X,
        Inches(top),
        Inches(width),
        Inches(0.35),
        text,
        font_size=13,
        color=color,
        font_name=FONT_BODY,
    )


def add_contained_picture(slide, image_path: Path, left, top, width, height) -> None:
    with Image.open(image_path) as img:
        img_w, img_h = img.size
    box_ratio = width / height
    img_ratio = img_w / img_h
    if img_ratio > box_ratio:
        final_w = width
        final_h = width / img_ratio
        offset_x = left
        offset_y = top + (height - final_h) / 2
    else:
        final_h = height
        final_w = height * img_ratio
        offset_x = left + (width - final_w) / 2
        offset_y = top
    slide.shapes.add_picture(str(image_path), offset_x, offset_y, width=final_w, height=final_h)


def add_chart_slide(slide, slide_number: int, image_path: Path, *, section: str, badge: tuple[str, str] | None = None) -> None:
    add_background(slide, slide_number, section=section)
    if badge:
        add_badge(slide, badge[0], Inches(11.25), Inches(0.28), Inches(1.35), fill=badge[1])
    add_contained_picture(slide, image_path, Inches(0.45), Inches(0.72), Inches(12.45), Inches(6.0))


def build_metrics() -> dict[str, object]:
    df = load_data(ROOT / "case_comp_data.csv")
    scoped = df[df["Date"].dt.year.between(2019, 2024)].copy()
    scoped["Year"] = scoped["Date"].dt.year
    annual = scoped.groupby(["Year", "Type"], as_index=False)["Total_Volume"].sum()
    pivot = annual.pivot(index="Year", columns="Type", values="Total_Volume")
    pivot["total"] = pivot["conventional"] + pivot["organic"]

    q2 = pd.read_csv(OUT_DIR / "q2_organic_share_winners.csv")
    q5 = pd.read_csv(OUT_DIR / "q5_city_profitability_base.csv")
    q6u = pd.read_csv(OUT_DIR / "q6_city_profitability_shipping_up_50.csv")
    q6d = pd.read_csv(OUT_DIR / "q6_city_profitability_shipping_down_50.csv")
    q7r = pd.read_csv(OUT_DIR / "q7_rank_comparison.csv")
    q7s = pd.read_csv(OUT_DIR / "q7_shipping_sensitivity.csv")
    season = pd.read_csv(OUT_DIR / "q8_monthly_seasonality.csv")

    def swing(series: pd.Series) -> float:
        return (series.max() / series.min() - 1) * 100

    season_by_type = {}
    for prod_type in ("conventional", "organic"):
        sub = season[season["Type"] == prod_type].sort_values("month")
        season_by_type[prod_type] = {
            "price_swing": swing(sub["mean_price"]),
            "volume_swing": swing(sub["mean_monthly_volume"]),
            "price_peak": month_name(int(sub.loc[sub["mean_price"].idxmax(), "month"])),
            "price_low": month_name(int(sub.loc[sub["mean_price"].idxmin(), "month"])),
            "volume_peak": month_name(int(sub.loc[sub["mean_monthly_volume"].idxmax(), "month"])),
            "volume_low": month_name(int(sub.loc[sub["mean_monthly_volume"].idxmin(), "month"])),
        }

    return {
        "q2": q2,
        "q5": q5,
        "q6u": q6u,
        "q6d": q6d,
        "q7r": q7r,
        "q7s": q7s,
        "growth_total": (pivot.loc[2024, "total"] / pivot.loc[2019, "total"] - 1) * 100,
        "growth_org": (pivot.loc[2024, "organic"] / pivot.loc[2019, "organic"] - 1) * 100,
        "share_2019": (pivot.loc[2019, "organic"] / pivot.loc[2019, "total"]) * 100,
        "share_2024": (pivot.loc[2024, "organic"] / pivot.loc[2024, "total"]) * 100,
        "top5_profit_avg": q5.head(5)["Profit"].mean(),
        "top5_margin_avg": q5.head(5)["Profit_Margin"].mean() * 100,
        "next5_profit_avg": q5.iloc[5:10]["Profit"].mean(),
        "rank_gap": q5.iloc[4]["Profit"] - q5.iloc[5]["Profit"],
        "up_profit_avg": q6u.head(5)["Profit"].mean(),
        "up_margin_avg": q6u.head(5)["Profit_Margin"].mean() * 100,
        "down_profit_avg": q6d.head(5)["Profit"].mean(),
        "down_margin_avg": q6d.head(5)["Profit_Margin"].mean() * 100,
        "stability_cities": q7r.head(5)["City"].tolist(),
        "top_sensitivity": q7s.sort_values("Profit_Impact_for_50pct_Shipping_Change", ascending=False).head(5),
        "seasonality": season_by_type,
    }


def slide_1(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 1, footer="Anonymized team submission")
    add_textbox(
        slide,
        MARGIN_X,
        Inches(1.55),
        Inches(7.4),
        Inches(2.2),
        "Entering the Organic Hass\nAvocado Market With Disciplined\nPilot Economics",
        font_size=31,
        color=THEME.primary,
        font_name=FONT_HEAD,
        bold=True,
    )
    add_textbox(
        slide,
        MARGIN_X,
        Inches(3.78),
        Inches(5.8),
        Inches(0.78),
        "West Valley Fresh Distribution Company\n2026 IMA Student Case Competition",
        font_size=17,
        color=THEME.ink,
        font_name=FONT_BODY,
    )
    pill_y = Inches(4.72)
    pills = [
        ("20,000 organic units", 1.95),
        ("40 city markets in supplied data", 3.1),
        ("2019 to June 2025 HAB data", 2.65),
    ]
    current_x = MARGIN_X
    for text, width in pills:
        shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, current_x, pill_y, Inches(width), Inches(0.33))
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(THEME.paper)
        shape.line.color.rgb = rgb(THEME.line)
        add_textbox(
            slide,
            current_x + Inches(0.04),
            pill_y + Inches(0.01),
            Inches(width) - Inches(0.08),
            Inches(0.25),
            text.upper(),
            font_size=10,
            color=THEME.primary,
            font_name=FONT_BODY,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
        current_x += Inches(width + 0.14)

    add_textbox(
        slide,
        MARGIN_X,
        Inches(5.35),
        Inches(5.8),
        Inches(0.62),
        "Prepared as an anonymized submission. The deck is designed to stand alone without speaker notes and focuses on profitability, volatility, and disciplined market entry.",
        font_size=14,
        color=THEME.muted,
        font_name=FONT_BODY,
    )


def slide_2(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 2, section="Executive Summary")
    add_title(slide, "A selective 5-city pilot is the strongest entry path for the 20,000-unit organic order")
    cards = [
        (
            "Recommendation",
            "5-city launch",
            "Seattle, Boise, Portland, Spokane, and San Diego maximize expected profit under the June 2026 pricing assumption.",
            THEME.primary,
        ),
        (
            "Base-case economics",
            f"{fmt_money(m['top5_profit_avg'])} avg profit",
            f"The selected cities pair premium June pricing with manageable miles, producing a top-five average margin of {fmt_pct(m['top5_margin_avg'])}.",
            THEME.ink,
        ),
        (
            "Why it is resilient",
            "Same 5 cities",
            "The recommendation does not change when shipping costs move up 50% or down 50%.",
            THEME.compare,
        ),
    ]
    x_positions = [Inches(0.6), Inches(4.35), Inches(8.1)]
    for idx, card in enumerate(cards):
        add_card(
            slide,
            x_positions[idx],
            Inches(2.18),
            Inches(3.15),
            Inches(2.25),
            header=card[0],
            metric=card[1],
            body=card[2],
            metric_color=card[3],
        )
    add_subtitle(
        slide,
        "Model note: each city is scored as a comparable 20,000-unit scenario using June 2025 retail price as the June 2026 proxy.",
        top=4.62,
        width=11.9,
    )


def slide_3(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 3, section="Foundation")
    add_title(slide, "Seasonality creates a timing gap between volume and price")
    add_contained_picture(slide, OUT_DIR / "q8_seasonality_volume.png", Inches(0.62), Inches(1.55), Inches(5.9), Inches(3.1))
    add_contained_picture(slide, OUT_DIR / "q8_seasonality_price.png", Inches(6.82), Inches(1.55), Inches(5.9), Inches(3.1))
    add_textbox(
        slide,
        Inches(0.62),
        Inches(4.82),
        Inches(5.85),
        Inches(0.46),
        "Volume arrives early. Organic volume peaks in January, conventional peaks in May, and both soften into November.",
        font_size=13,
        color=THEME.ink,
    )
    add_textbox(
        slide,
        Inches(6.82),
        Inches(4.82),
        Inches(5.85),
        Inches(0.46),
        "Price crests later. Both organic and conventional prices peak in July and bottom in February.",
        font_size=13,
        color=THEME.ink,
    )
    add_textbox(
        slide,
        Inches(0.62),
        Inches(5.38),
        Inches(11.85),
        Inches(0.56),
        "The market absorbs more units before it offers peak pricing, so timing affects margin capture, promotions, and inventory allocation.",
        font_size=17,
        color=THEME.muted,
        font_name=FONT_BODY,
    )


def slide_4(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chart_slide(slide, 4, OUT_DIR / "deck_q2_growth_share.png", section="Foundation")


def slide_5(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 5, section="Foundation")
    add_title(slide, "The pilot screen should be price support, organic readiness, and route efficiency")
    q2 = m["q2"]
    seattle_wins = int((q2["City"] == "Seattle").sum())
    top5 = m["q5"].head(5)
    shipping_low = m["q7r"].head(5)["Profit_base"].min() - m["q6u"].head(5)["Profit"].min()
    shipping_high = m["q7r"].head(5)["Profit_base"].max() - m["q6u"].head(5)["Profit"].max()

    cards = [
        (
            "Price support",
            f"${top5['forecast_retail_price_jun2026'].min():.2f} to ${top5['forecast_retail_price_jun2026'].max():.2f}",
            "The selected five cities are also the five highest-price June 2025 organic markets in the model.",
            THEME.primary,
        ),
        (
            "Organic readiness",
            f"Seattle leads {seattle_wins} of 7",
            "Organic adoption is uneven by city, so total sales scale alone is not enough to pick the best launch markets.",
            THEME.compare,
        ),
        (
            "Route efficiency",
            f"{fmt_money(shipping_low)} to {fmt_money(shipping_high)}",
            "Even after a 50% freight increase, the recommended cities lose only about $0.8k to $1.0k each and keep the same ranking.",
            THEME.stress,
        ),
    ]
    x_positions = [Inches(0.78), Inches(4.52), Inches(8.26)]
    for idx, card in enumerate(cards):
        add_card(
            slide,
            x_positions[idx],
            Inches(2.02),
            Inches(3.05),
            Inches(2.22),
            header=card[0],
            metric=card[1],
            body=card[2],
            metric_color=card[3],
        )
    add_subtitle(
        slide,
        "This deck tests those three filters against sales leadership, organic mix, profitability, freight sensitivity, and seasonality.",
        top=4.56,
        width=11.8,
    )


def add_market_analysis_slides(prs: Presentation) -> None:
    slides = [
        (6, OUT_DIR / "deck_q1_winner_matrix.png", "Market Analysis"),
        (7, OUT_DIR / "deck_q1_conventional_top5_trends.png", "Market Analysis"),
        (8, OUT_DIR / "deck_q1_organic_top5_trends.png", "Market Analysis"),
        (9, OUT_DIR / "deck_q2_winner_timeline.png", "Market Analysis"),
        (10, OUT_DIR / "deck_q2_growth_share.png", "Market Analysis"),
        (11, OUT_DIR / "q3_price_volume_scatter.png", "Market Analysis"),
        (12, OUT_DIR / "deck_q3_within_type_metrics.png", "Market Analysis"),
        (13, OUT_DIR / "deck_q4_macro_driver_heatmap.png", "Market Analysis"),
        (14, OUT_DIR / "deck_q4_city_micro_heatmap.png", "Market Analysis"),
        (15, OUT_DIR / "deck_q5_price_vs_miles.png", "Market Analysis"),
        (16, OUT_DIR / "deck_q5_unit_economics_waterfall.png", "Recommendation"),
        (17, OUT_DIR / "deck_q5_price_ranking.png", "Recommendation"),
        (18, OUT_DIR / "deck_q5_profit_ranking.png", "Recommendation"),
        (19, OUT_DIR / "deck_q5_selection_matrix.png", "Recommendation"),
        (20, OUT_DIR / "deck_q5_frontier_zoom.png", "Recommendation"),
        (21, OUT_DIR / "deck_q6_up50_compare.png", "Recommendation"),
        (22, OUT_DIR / "deck_q6_down50_compare.png", "Recommendation"),
        (23, OUT_DIR / "deck_q7_rank_stability_matrix.png", "Recommendation"),
        (24, OUT_DIR / "deck_q7_shipping_tornado.png", "Recommendation"),
        (25, OUT_DIR / "deck_q7_price_vs_sensitivity.png", "Recommendation"),
        (26, OUT_DIR / "q8_seasonality_price.png", "Seasonality"),
        (27, OUT_DIR / "q8_seasonality_volume.png", "Seasonality"),
    ]
    for slide_number, image_path, section in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        badge = ("Context", THEME.compare) if slide_number in {13, 14} else None
        add_chart_slide(slide, slide_number, image_path, section=section, badge=badge)


def slide_28(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 28, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "Seasonality should change when West Valley pushes volume and when it protects margin")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_left = Inches(0.75)
    month_top = Inches(2.18)
    month_w = Inches(0.91)
    for idx, month in enumerate(months):
        fill = THEME.paper
        if idx <= 4:
            fill = THEME.primary_soft
        elif 6 <= idx <= 8:
            fill = THEME.accent
        elif idx >= 10 or idx <= 1:
            fill = THEME.compare
        elif idx == 9:
            fill = THEME.line
        box = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, month_left + idx * month_w, month_top, Inches(0.78), Inches(0.48))
        box.fill.solid()
        box.fill.fore_color.rgb = rgb(fill)
        box.line.color.rgb = rgb(fill)
        add_textbox(
            slide,
            month_left + idx * month_w,
            month_top + Inches(0.1),
            Inches(0.78),
            Inches(0.2),
            month,
            font_size=11,
            color=THEME.paper if fill in {THEME.primary_soft, THEME.accent, THEME.compare} else THEME.ink,
            font_name=FONT_BODY,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
    add_card(
        slide,
        Inches(0.78),
        Inches(3.15),
        Inches(3.65),
        Inches(2.0),
        header="Push volume",
        metric="Jan to May",
        body="Prioritize service, retailer availability, and flow discipline while market volume is naturally strongest.",
        metric_color=THEME.primary,
    )
    add_card(
        slide,
        Inches(4.84),
        Inches(3.15),
        Inches(3.65),
        Inches(2.0),
        header="Protect margin",
        metric="Jul to Sep",
        body="Hold pricing discipline and allocate the strongest fruit to the best-paying markets while price support is highest.",
        metric_color=THEME.accent,
    )
    add_card(
        slide,
        Inches(8.9),
        Inches(3.15),
        Inches(3.65),
        Inches(2.0),
        header="Stimulate demand",
        metric="Nov to Feb",
        body="Use promotions, alternate channels, and tighter inventory planning when both types face softer volume months.",
        metric_color=THEME.compare,
    )
    add_subtitle(
        slide,
        f"Organic volume peaks in {m['seasonality']['organic']['volume_peak']} while price peaks in {m['seasonality']['organic']['price_peak']}; that gap is the operating lever.",
        top=5.55,
        width=11.8,
    )


def slide_29(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 29, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "A monthly operating calendar can convert seasonality from risk into advantage")
    row_labels = ["Commercial posture", "Supply posture", "Operating focus"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    values = [
        ["Stimulate", "Stimulate", "Support", "Support", "Service", "Balance", "Protect", "Protect", "Protect", "Rebalance", "Stimulate", "Stimulate"],
        ["Flex up", "Flex up", "Flex up", "Flex up", "Peak flow", "Normalize", "Tighten mix", "Tighten mix", "Tighten mix", "Reset", "Flex down", "Flex down"],
        ["Forecast", "Promote", "Allocate", "Allocate", "Service", "Audit", "Margin", "Margin", "Margin", "Plan", "Clear", "Review"],
    ]
    color_map = {
        "Stimulate": THEME.compare,
        "Support": THEME.primary_soft,
        "Service": THEME.primary,
        "Balance": THEME.line,
        "Protect": THEME.accent,
        "Rebalance": THEME.stress,
        "Flex up": THEME.primary_soft,
        "Peak flow": THEME.primary,
        "Normalize": THEME.line,
        "Tighten mix": THEME.accent,
        "Reset": THEME.stress,
        "Flex down": THEME.compare,
        "Forecast": THEME.primary_soft,
        "Promote": THEME.compare,
        "Allocate": THEME.primary,
        "Audit": THEME.line,
        "Margin": THEME.accent,
        "Plan": THEME.stress,
        "Clear": THEME.compare,
        "Review": THEME.primary_soft,
    }
    table = slide.shapes.add_table(4, 13, Inches(0.7), Inches(1.7), Inches(12.0), Inches(3.55)).table
    table.columns[0].width = Inches(1.65)
    for col in range(1, 13):
        table.columns[col].width = Inches(0.82)
    for row in range(4):
        table.rows[row].height = Inches(0.87)
    table.cell(0, 0).text = ""
    for idx, month in enumerate(months, start=1):
        cell = table.cell(0, idx)
        cell.text = month
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(THEME.paper)
    for row_idx, label in enumerate(row_labels, start=1):
        cell = table.cell(row_idx, 0)
        cell.text = label
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(THEME.paper)
        for col_idx, value in enumerate(values[row_idx - 1], start=1):
            cell = table.cell(row_idx, col_idx)
            cell.text = value
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(color_map[value])
    dark_fills = {rgb(THEME.primary), rgb(THEME.primary_soft), rgb(THEME.compare), rgb(THEME.accent), rgb(THEME.stress)}
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(11)
                    run.font.bold = True
                    run.font.color.rgb = rgb(THEME.paper if cell.fill.fore_color.rgb in dark_fills else THEME.ink)
    add_subtitle(
        slide,
        "Suggested cadence: Jan-May prioritize service and flow, Jul-Sep protect margin, and Nov-Feb stimulate demand while tightening inventory.",
        top=5.52,
        width=11.7,
    )


def slide_30(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 30, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "Growers need flexible contracts, better cold-chain readiness, and alternate lanes")
    cards = [
        ("Contract tiers", "Base + flex volume", "Lock a stable base volume, then add seasonal flex tiers so supply expands without overcommitting year-round.", THEME.primary),
        ("Cold-chain readiness", "Protect service", "Use better storage, transit monitoring, and receiving discipline during peak months to cut spoilage and stockouts.", THEME.compare),
        ("Alternate lanes", "Reduce disruption", "Build backup carriers and routes so freight volatility or lane disruption does not force reactive city choices.", THEME.stress),
    ]
    for idx, card in enumerate(cards):
        add_card(
            slide,
            Inches(0.82 + idx * 4.03),
            Inches(2.0),
            Inches(3.45),
            Inches(2.65),
            header=card[0],
            metric=card[1],
            body=card[2],
            metric_color=card[3],
        )
    add_subtitle(slide, "These actions translate Q9 into supply-side discipline rather than generic risk language.", top=4.92, width=11.5)


def slide_31(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 31, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "Trade associations should smooth demand in off-peak months")
    cards = [
        ("Consumer messaging", "Recipes + health", "Use recipe content and health messaging in softer months to keep avocados visible in weekly shopping decisions.", THEME.primary),
        ("Channel mix", "Food-service + institutional", "Shift more volume through restaurants, prepared foods, and institutional buyers when retail pull weakens.", THEME.compare),
        ("Promo timing", "Promote when the market is soft", "Reserve the strongest promotional calendar for low-volume months instead of discounting away naturally strong demand.", THEME.accent),
        ("Trade support", "Joint campaigns", "Coordinate with trade associations on seasonal education campaigns so promotions align with the month-by-month operating calendar.", THEME.stress),
    ]
    positions = [(0.8, 1.95), (6.76, 1.95), (0.8, 4.05), (6.76, 4.05)]
    for card, (x, y) in zip(cards, positions):
        add_card(slide, Inches(x), Inches(y), Inches(5.1), Inches(1.65), header=card[0], metric=card[1], body=card[2], metric_color=card[3])


def slide_32(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 32, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "A shared monthly S&OP cadence can align growers, West Valley, and retail partners")
    stakeholder_cards = [
        ("Growers", "Supply commitment", "Set base volume, flex volume, and harvest timing updates by month.", THEME.primary),
        ("West Valley", "Control tower", "Translate price, demand, and freight signals into allocation decisions.", THEME.compare),
        ("Retailers", "Demand signal", "Provide promo calendars, replenishment risk, and reorder visibility.", THEME.accent),
    ]
    for idx, card in enumerate(stakeholder_cards):
        add_card(slide, Inches(0.85 + idx * 4.1), Inches(2.0), Inches(3.35), Inches(1.85), header=card[0], metric=card[1], body=card[2], metric_color=card[3])
    for x in [4.25, 8.35]:
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(2.95), Inches(x + 0.45), Inches(2.95))
        line.line.color.rgb = rgb(THEME.line)
        line.line.width = Pt(2.0)
    add_panel(slide, Inches(1.35), Inches(4.35), Inches(10.65), Inches(1.55), fill=THEME.paper)
    add_textbox(slide, Inches(1.6), Inches(4.6), Inches(10.15), Inches(0.28), "Monthly cadence: Forecast demand -> lock commitments -> allocate by city -> review realized margin and service", font_size=17, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(
        slide,
        Inches(1.62),
        Inches(4.98),
        Inches(10.0),
        Inches(0.7),
        [
            "Run the review monthly, not quarterly, because the volume-price gap changes within the season.",
            "Use the same cycle to adjust grower commitments, routing, and retailer promotion timing.",
        ],
        font_size=14,
        color=THEME.ink,
    )


def slide_33(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 33, section="Implementation")
    add_title(slide, "Launch the 2026 pilot first, then scale what the market confirms")
    phases = [
        ("2026", "Pilot", "Launch the five-city test, validate realized margin, and refine routing assumptions.", THEME.primary),
        ("2027", "Expand", "Add retailer coverage only where realized economics and service levels hold.", THEME.compare),
        ("2028", "Optimize", "Tighten contracts, allocation logic, and seasonal operating rules.", THEME.accent),
    ]
    for idx, phase in enumerate(phases):
        x = Inches(0.85 + idx * 4.1)
        circle = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, x + Inches(1.05), Inches(2.0), Inches(1.0), Inches(1.0))
        circle.fill.solid()
        circle.fill.fore_color.rgb = rgb(phase[3])
        circle.line.color.rgb = rgb(phase[3])
        add_textbox(slide, x + Inches(1.1), Inches(2.25), Inches(0.9), Inches(0.2), phase[0], font_size=16, color=THEME.paper, font_name=FONT_HEAD, bold=True, align=PP_ALIGN.CENTER)
        add_card(slide, x, Inches(3.15), Inches(3.15), Inches(1.85), header=phase[1], metric=phase[0], body=phase[2], metric_color=phase[3])
        if idx < 2:
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x + Inches(3.18), Inches(2.5), x + Inches(4.06), Inches(2.5))
            connector.line.color.rgb = rgb(THEME.line)
            connector.line.width = Pt(2.0)


def slide_34(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 34, section="Implementation")
    add_title(slide, "Pilot KPIs should focus on margin, service, spoilage, and repeat orders")
    kpis = [
        ("Margin", "Realized gross margin", "Confirms whether forecast economics survive execution.", THEME.primary),
        ("Freight", "Freight per unit", "Shows whether routing and lane discipline are improving.", THEME.compare),
        ("Service", "Fill rate", "Measures retailer execution quality during seasonal peaks.", THEME.primary_soft),
        ("Shrink", "Spoilage rate", "Captures cold-chain and freshness failures directly.", THEME.stress),
        ("Demand", "Reorder rate", "Tests whether pilot demand is repeatable, not one-off.", THEME.accent),
        ("Planning", "Forecast accuracy", "Shows whether monthly S&OP is improving allocation decisions.", THEME.compare),
    ]
    for idx, kpi in enumerate(kpis):
        row = idx // 3
        col = idx % 3
        add_card(
            slide,
            Inches(0.82 + col * 4.05),
            Inches(1.85 + row * 2.15),
            Inches(3.4),
            Inches(1.72),
            header=kpi[0],
            metric=kpi[1],
            body=kpi[2],
            metric_color=kpi[3],
        )


def slide_35(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 35, section="Implementation")
    add_title(slide, "Expansion should follow stage gates, not automatic geography growth")
    stages = [
        ("Gate 1", "Pilot live", "Launch and collect clean economics by city."),
        ("Gate 2", "Economics verified", "Confirm realized margin and freight per unit."),
        ("Gate 3", "Service verified", "Confirm fill rate, spoilage control, and retailer reorder behavior."),
        ("Decision", "Scale selectively", "Expand only where pilot evidence remains strong."),
    ]
    for idx, stage in enumerate(stages):
        x = Inches(0.7 + idx * 3.1)
        add_card(slide, x, Inches(2.25), Inches(2.55), Inches(2.2), header=stage[0], metric=stage[1], body=stage[2], metric_color=THEME.primary if idx < 2 else THEME.compare if idx == 2 else THEME.accent)
        if idx < len(stages) - 1:
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x + Inches(2.58), Inches(3.32), x + Inches(3.02), Inches(3.32))
            connector.line.color.rgb = rgb(THEME.line)
            connector.line.width = Pt(2.0)
    add_subtitle(slide, "This avoids pretending the current model can allocate the full 20,000-unit order with exact retailer-level precision.", top=5.18, width=11.7)


def slide_36(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 36, section="Risks")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.stress)
    add_title(slide, "The highest-risk threats are freight spikes, import disruptions, and forecast error")
    add_panel(slide, Inches(1.05), Inches(1.75), Inches(9.7), Inches(4.4), fill=THEME.paper)
    v_line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(5.9), Inches(1.95), Inches(5.9), Inches(5.92))
    h_line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(1.3), Inches(3.95), Inches(10.45), Inches(3.95))
    for line in [v_line, h_line]:
        line.line.color.rgb = rgb(THEME.line)
        line.line.width = Pt(1.6)
    add_textbox(slide, Inches(4.65), Inches(1.83), Inches(2.5), Inches(0.2), "High impact", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(4.65), Inches(5.95), Inches(2.5), Inches(0.2), "Low impact", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(0.9), Inches(3.65), Inches(0.9), Inches(0.4), "Low\nprob.", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(10.55), Inches(3.65), Inches(0.9), Inches(0.4), "High\nprob.", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)

    risks = [
        ("Freight spikes", 8.6, 2.6, THEME.stress),
        ("Import disruption", 6.8, 2.35, THEME.stress),
        ("Forecast error", 7.9, 3.3, THEME.accent),
        ("Retailer uptake", 7.2, 4.4, THEME.compare),
        ("Spoilage", 6.0, 4.2, THEME.compare),
        ("Labor pressure", 5.2, 3.2, THEME.primary_soft),
    ]
    for label, x, y, color in risks:
        bubble = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, Inches(x), Inches(y), Inches(0.82), Inches(0.82))
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = rgb(color)
        bubble.line.color.rgb = rgb(color)
        add_textbox(slide, Inches(x - 0.3), Inches(y + 0.84), Inches(1.45), Inches(0.4), label, font_size=11, color=THEME.ink, align=PP_ALIGN.CENTER)


def slide_37(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 37, section="Risks")
    add_title(slide, "Each major risk has a specific operational countermeasure")
    table = slide.shapes.add_table(6, 3, Inches(0.72), Inches(1.75), Inches(11.85), Inches(4.3)).table
    headers = ["Risk", "Countermeasure", "Owner"]
    rows = [
        ("Freight spikes", "Lock core carrier capacity and maintain alternate lanes.", "Logistics lead"),
        ("Import or supply disruption", "Use flexible grower contracts and staggered commitments.", "Sourcing lead"),
        ("Spoilage / service failures", "Tighten cold-chain controls and receiving discipline.", "Operations lead"),
        ("Forecast error", "Run monthly S&OP and reallocate by city using realized demand.", "Commercial lead"),
        ("Retailer uptake risk", "Require stage gates before expanding beyond the pilot.", "General manager"),
    ]
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(THEME.primary)
    for row_idx, row in enumerate(rows, start=1):
        for col_idx, value in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = value
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(THEME.paper if row_idx % 2 else THEME.bg)
    widths = [2.4, 7.0, 2.45]
    for idx, width in enumerate(widths):
        table.columns[idx].width = Inches(width)
    for row in table.rows:
        row.height = Inches(0.72)
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(12)
                    run.font.bold = row == table.rows[0]
                    run.font.color.rgb = rgb(THEME.paper if row == table.rows[0] else THEME.ink)


def slide_38(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 38, section="Limitations")
    add_badge(slide, "Caveat", Inches(11.28), Inches(0.28), Inches(1.28), fill=THEME.stress)
    add_title(slide, "The current model is strong enough for city selection but not yet for exact allocation")
    left_items = [
        "The case text references 41 metro regions, but the cleaned dataset resolves to 40 city markets.",
        "2025 data is partial year only and should not be read as a full-year comparison period.",
        "The city ranking uses comparable 20,000-unit scorecards for selection, not a retailer-level allocation model.",
    ]
    right_items = [
        "The model uses June 2025 retail price as the simple forecast for June 2026 retail price.",
        "It does not include spoilage shrink, retailer-specific demand curves, or a fully expanded operating cost stack.",
        "All 40 city scenarios remain profitable even at +50% shipping, so the choice is about optimization, not survival.",
    ]
    add_panel(slide, Inches(0.8), Inches(1.9), Inches(5.7), Inches(3.95))
    add_panel(slide, Inches(6.85), Inches(1.9), Inches(5.7), Inches(3.95))
    add_textbox(slide, Inches(1.0), Inches(2.12), Inches(2.0), Inches(0.25), "What the model does well", font_size=15, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(slide, Inches(1.0), Inches(2.45), Inches(5.1), Inches(3.0), left_items, font_size=15)
    add_textbox(slide, Inches(7.05), Inches(2.12), Inches(2.3), Inches(0.25), "What it does not do yet", font_size=15, color=THEME.stress, font_name=FONT_HEAD, bold=True)
    add_bullets(slide, Inches(7.05), Inches(2.45), Inches(5.1), Inches(3.0), right_items, font_size=15)


def slide_39(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 39, section="Conclusion")
    add_title(slide, "West Valley should pursue a 5-city organic entry with structured discipline")
    add_panel(slide, Inches(0.82), Inches(1.9), Inches(4.2), Inches(3.8), fill=THEME.paper)
    add_textbox(slide, Inches(1.05), Inches(2.18), Inches(3.7), Inches(0.3), "RECOMMENDATION", font_size=11, color=THEME.muted, font_name=FONT_BODY, bold=True)
    add_textbox(slide, Inches(1.05), Inches(2.52), Inches(3.5), Inches(0.55), "Launch the 5-city pilot", font_size=24, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(
        slide,
        Inches(1.05),
        Inches(3.18),
        Inches(3.55),
        Inches(1.8),
        [
            "Seattle, Boise, Portland, Spokane, and San Diego maximize expected profit.",
            "The same five remain top-ranked in the base, +50%, and -50% shipping scenarios.",
            "Seasonality requires monthly operating discipline, not a static annual plan.",
        ],
        font_size=15,
    )
    proof_cards = [
        ("Economics", fmt_money(m["top5_profit_avg"]) + " avg profit", "Base case", THEME.primary),
        ("Resilience", "Same 5 cities", "All three shipping scenarios", THEME.compare),
        ("Operating discipline", "Volume before price", "Plan by month, not by annual average", THEME.accent),
    ]
    for idx, card in enumerate(proof_cards):
        add_card(slide, Inches(5.48), Inches(2.0 + idx * 1.25), Inches(6.0), Inches(1.05), header=card[0], metric=card[1], body=card[2], metric_color=card[3])
    add_subtitle(slide, "Next decision: run the pilot, measure realized economics, and scale only where the pilot confirms the model.", top=6.08, width=11.7)


def slide_40(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 40, section="Appendix", footer="Sources and backup")
    add_title(slide, "Q&A / backup: sources, assumptions, and supporting tables")
    add_panel(slide, Inches(0.78), Inches(1.88), Inches(5.7), Inches(4.2))
    add_panel(slide, Inches(6.85), Inches(1.88), Inches(5.7), Inches(4.2))
    add_textbox(slide, Inches(1.0), Inches(2.12), Inches(2.6), Inches(0.24), "Primary sources", font_size=15, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(
        slide,
        Inches(1.0),
        Inches(2.45),
        Inches(5.0),
        Inches(3.1),
        [
            "case_full.md and case_context.md",
            "case_comp_data.csv",
            "outputs/question_1.md through outputs/question_9.md",
            "outputs/q5_city_profitability_base.csv and scenario variants",
            "outputs/q8_monthly_seasonality.csv and supporting charts",
        ],
        font_size=15,
    )
    add_textbox(slide, Inches(7.08), Inches(2.12), Inches(2.8), Inches(0.24), "Backup exhibits available", font_size=15, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(
        slide,
        Inches(7.08),
        Inches(2.45),
        Inches(5.0),
        Inches(3.1),
        [
            "Winner matrix and city trend lines",
            "Growth/share bridge and elasticity visuals",
            "Selection matrix, frontier zoom, and freight sensitivity",
            "Seasonality price and volume charts",
            "Model caveats and implementation stage gates",
        ],
        font_size=15,
    )


def build_deck(output_path: Path = DEFAULT_OUTPUT) -> Path:
    metrics = build_metrics()
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_1(prs)
    slide_2(prs, metrics)
    slide_3(prs)
    slide_4(prs)
    slide_5(prs, metrics)
    add_market_analysis_slides(prs)
    slide_28(prs, metrics)
    slide_29(prs)
    slide_30(prs)
    slide_31(prs)
    slide_32(prs)
    slide_33(prs)
    slide_34(prs)
    slide_35(prs)
    slide_36(prs)
    slide_37(prs)
    slide_38(prs)
    slide_39(prs, metrics)
    slide_40(prs)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)
    return output_path


if __name__ == "__main__":
    path = build_deck()
    print(path)
