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


def emu(value) -> int:
    return int(round(float(value)))


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


def add_stat_chip(
    slide,
    left,
    top,
    width,
    height,
    *,
    label: str,
    value: str,
    fill: str = THEME.paper,
    line: str = THEME.line,
    value_color: str = THEME.primary,
    align: PP_ALIGN = PP_ALIGN.LEFT,
) -> None:
    add_panel(slide, left, top, width, height, fill=fill, line=line)
    add_textbox(
        slide,
        left + Inches(0.14),
        top + Inches(0.12),
        width - Inches(0.28),
        Inches(0.18),
        label.upper(),
        font_size=10,
        color=THEME.muted,
        font_name=FONT_BODY,
        bold=True,
        align=align,
    )
    add_textbox(
        slide,
        left + Inches(0.14),
        top + Inches(0.34),
        width - Inches(0.28),
        height - Inches(0.46),
        value,
        font_size=19,
        color=value_color,
        font_name=FONT_HEAD,
        bold=True,
        align=align,
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
    compact = height <= Inches(1.15)
    header_top = Inches(0.15)
    header_height = Inches(0.24)
    metric_top = Inches(0.42)
    metric_height = Inches(0.55)
    metric_font_size = 24
    body_top = Inches(0.96)
    body_height = height - Inches(1.12)
    body_font_size = 15

    if compact:
        header_top = Inches(0.1)
        header_height = Inches(0.18)
        metric_top = Inches(0.3)
        metric_height = Inches(0.28)
        metric_font_size = 18
        body_top = Inches(0.6)
        body_height = height - Inches(0.72)
        body_font_size = 11

    add_textbox(
        slide,
        left + Inches(0.16),
        top + header_top,
        width - Inches(0.32),
        header_height,
        header.upper(),
        font_size=10 if compact else 11,
        color=THEME.muted,
        bold=True,
        font_name=FONT_BODY,
    )
    add_textbox(
        slide,
        left + Inches(0.16),
        top + metric_top,
        width - Inches(0.32),
        metric_height,
        metric,
        font_size=metric_font_size,
        color=metric_color,
        bold=True,
        font_name=FONT_HEAD,
    )
    if body_height > 0:
        add_textbox(
            slide,
            left + Inches(0.16),
            top + body_top,
            width - Inches(0.32),
            body_height,
            body,
            font_size=body_font_size,
            color=THEME.ink,
            font_name=FONT_BODY,
        )


def add_stat_band(
    slide,
    left,
    top,
    width,
    height,
    items: list[tuple[str, str, str]],
    *,
    highlight_idx: int | None = None,
) -> None:
    add_panel(slide, left, top, width, height, fill=THEME.paper)
    col_w = emu(width / len(items))
    accent_cycle = [THEME.primary, THEME.compare, THEME.accent, THEME.stress]
    compact = height <= Inches(0.95)
    label_top = Inches(0.14 if not compact else 0.1)
    label_height = Inches(0.18 if not compact else 0.14)
    metric_top = Inches(0.34 if not compact else 0.26)
    metric_height = Inches(0.34 if not compact else 0.24)
    metric_font_size = 21 if not compact else 17
    body_top = Inches(0.72 if not compact else 0.56)
    body_height = emu(height - Inches(0.88 if not compact else 0.64))
    body_font_size = 12 if not compact else 10
    for idx, (label, metric, body) in enumerate(items):
        x = emu(left + idx * col_w)
        if idx:
            divider = slide.shapes.add_connector(
                MSO_CONNECTOR.STRAIGHT,
                emu(x),
                emu(top + Inches(0.18)),
                emu(x),
                emu(top + height - Inches(0.18)),
            )
            divider.line.color.rgb = rgb(THEME.line)
            divider.line.width = Pt(1.0)
        accent = THEME.primary if highlight_idx == idx else accent_cycle[idx % len(accent_cycle)]
        add_textbox(
            slide,
            emu(x + Inches(0.14)),
            emu(top + label_top),
            emu(col_w - Inches(0.28)),
            label_height,
            label.upper(),
            font_size=10,
            color=THEME.muted,
            font_name=FONT_BODY,
            bold=True,
        )
        add_textbox(
            slide,
            emu(x + Inches(0.14)),
            emu(top + metric_top),
            emu(col_w - Inches(0.28)),
            metric_height,
            metric,
            font_size=metric_font_size,
            color=accent,
            font_name=FONT_HEAD,
            bold=True,
        )
        if body_height > 0:
            add_textbox(
                slide,
                emu(x + Inches(0.14)),
                emu(top + body_top),
                emu(col_w - Inches(0.28)),
                body_height,
                body,
                font_size=body_font_size,
                color=THEME.ink,
                font_name=FONT_BODY,
            )


def add_exhibit_footer(
    slide,
    left,
    top,
    width,
    height,
    *,
    takeaway: str,
    note: str | None = None,
    accent: str = THEME.primary,
) -> None:
    add_panel(slide, left, top, width, height, fill=THEME.paper)
    rail = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, left + Inches(0.14), top + Inches(0.12), Inches(1.15), height - Inches(0.24))
    rail.fill.solid()
    rail.fill.fore_color.rgb = rgb(accent)
    rail.line.color.rgb = rgb(accent)
    add_textbox(
        slide,
        left + Inches(0.2),
        top + Inches(0.18),
        Inches(1.03),
        height - Inches(0.36),
        "TAKEAWAY",
        font_size=10,
        color=THEME.paper,
        font_name=FONT_BODY,
        bold=True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_textbox(
        slide,
        left + Inches(1.5),
        top + Inches(0.1),
        width - Inches(4.15 if note else 1.72),
        height - Inches(0.2),
        takeaway,
        font_size=12,
        color=THEME.ink,
        font_name=FONT_BODY,
        bold=True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    if note:
        divider_x = emu(left + width - Inches(2.55))
        divider = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            emu(divider_x),
            emu(top + Inches(0.14)),
            emu(divider_x),
            emu(top + height - Inches(0.14)),
        )
        divider.line.color.rgb = rgb(THEME.line)
        divider.line.width = Pt(1.0)
        add_textbox(
            slide,
            emu(divider_x + Inches(0.18)),
            emu(top + Inches(0.1)),
            Inches(2.12),
            emu(height - Inches(0.2)),
            note,
            font_size=10,
            color=THEME.muted,
            font_name=FONT_BODY,
            valign=MSO_ANCHOR.MIDDLE,
        )


def add_ranked_bar_list(
    slide,
    items: list[tuple[str, float, str]],
    *,
    left,
    top,
    width,
    row_h,
    max_value: float | None = None,
    value_fmt: str = "${:,.0f}",
    subtitle: str | None = None,
) -> None:
    if not items:
        return
    max_val = max_value or max(value for _, value, _ in items)
    if subtitle:
        add_textbox(
            slide,
            left,
            emu(top - Inches(0.22)),
            width,
            Inches(0.16),
            subtitle.upper(),
            font_size=10,
            color=THEME.muted,
            font_name=FONT_BODY,
            bold=True,
        )
    for idx, (label, value, color) in enumerate(items):
        y = emu(top + idx * row_h)
        add_textbox(slide, left, emu(y + Inches(0.04)), Inches(1.7), Inches(0.18), label, font_size=11, color=THEME.ink, font_name=FONT_BODY, bold=idx < 5)
        track_w = emu(width - Inches(3.0))
        track = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, emu(left + Inches(1.82)), emu(y + Inches(0.05)), track_w, Inches(0.18))
        track.fill.solid()
        track.fill.fore_color.rgb = rgb(THEME.bg)
        track.line.color.rgb = rgb(THEME.bg)
        bar_w = max(emu(track_w * (value / max_val if max_val else 0)), 1)
        bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, emu(left + Inches(1.82)), emu(y + Inches(0.05)), bar_w, Inches(0.18))
        bar.fill.solid()
        bar.fill.fore_color.rgb = rgb(color)
        bar.line.color.rgb = rgb(color)
        add_textbox(slide, emu(left + width - Inches(1.0)), y, Inches(0.95), Inches(0.2), value_fmt.format(value), font_size=11, color=color, font_name=FONT_BODY, bold=True, align=PP_ALIGN.RIGHT)


def add_city_metric_table(
    slide,
    rows: list[tuple[str, str, float, float, float, float]],
    *,
    left,
    top,
    width,
    height,
) -> None:
    table = slide.shapes.add_table(len(rows) + 1, 5, left, top, width, height).table
    headers = ["City", "Miles", "Price", "Profit", "Margin"]
    widths = [2.2, 1.1, 1.15, 1.35, 1.0]
    for idx, val in enumerate(widths):
        table.columns[idx].width = Inches(val)
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(THEME.primary)
    for row_idx, row in enumerate(rows, start=1):
        values = [
            f"{row[0]}, {row[1]}",
            f"{int(row[2]):,}",
            f"${row[3]:.2f}",
            f"${row[4]:,.0f}",
            f"{row[5] * 100:.1f}%",
        ]
        for col_idx, value in enumerate(values):
            cell = table.cell(row_idx, col_idx)
            cell.text = value
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(THEME.paper if row_idx % 2 else THEME.bg)
    for row in table.rows:
        row.height = Inches(0.46)
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(11)
                    run.font.bold = row == table.rows[0]
                    run.font.color.rgb = rgb(THEME.paper if row == table.rows[0] else THEME.ink)


def add_generic_table(
    slide,
    headers: list[str],
    rows: list[list[str]],
    *,
    left,
    top,
    width,
    height,
    col_widths: list[float],
    font_size: int = 11,
) -> None:
    table = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, width, height).table
    for idx, col_width in enumerate(col_widths):
        table.columns[idx].width = Inches(col_width)
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
    for row in table.rows:
        row.height = Inches(height.inches / (len(rows) + 1))
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(font_size)
                    run.font.bold = row == table.rows[0]
                    run.font.color.rgb = rgb(THEME.paper if row == table.rows[0] else THEME.ink)


def add_two_series_profile(
    slide,
    *,
    left,
    top,
    width,
    height,
    months: list[str],
    series_a: list[float],
    series_b: list[float],
    label_a: str,
    label_b: str,
    color_a: str = THEME.primary,
    color_b: str = THEME.accent,
    y_label: str = "",
) -> None:
    x0 = emu(left + Inches(0.45))
    y0 = emu(top + height - Inches(0.45))
    x_axis = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x0, y0, emu(left + width - Inches(0.15)), y0)
    y_axis = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x0, emu(top + Inches(0.18)), x0, y0)
    for axis in [x_axis, y_axis]:
        axis.line.color.rgb = rgb(THEME.line)
        axis.line.width = Pt(1.2)
    min_v = min(series_a + series_b)
    max_v = max(series_a + series_b)
    span = max(max_v - min_v, 0.0001)
    points = len(months)
    plot_w = emu(width - Inches(0.8))
    plot_h = emu(height - Inches(0.8))

    def plot_series(values: list[float], color: str) -> None:
        coords = []
        for idx, value in enumerate(values):
            x = emu(x0 + plot_w * (idx / max(1, points - 1)))
            y = emu(y0 - plot_h * ((value - min_v) / span))
            coords.append((x, y))
        for idx, (x, y) in enumerate(coords):
            dot = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, emu(x - Inches(0.06)), emu(y - Inches(0.06)), Inches(0.12), Inches(0.12))
            dot.fill.solid()
            dot.fill.fore_color.rgb = rgb(color)
            dot.line.color.rgb = rgb(color)
            if idx < len(coords) - 1:
                nx, ny = coords[idx + 1]
                line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, emu(x), emu(y), emu(nx), emu(ny))
                line.line.color.rgb = rgb(color)
                line.line.width = Pt(2.0)

    plot_series(series_a, color_a)
    plot_series(series_b, color_b)
    for idx, month in enumerate(months):
        x = emu(x0 + plot_w * (idx / max(1, points - 1)))
        add_textbox(slide, emu(x - Inches(0.24)), emu(y0 + Inches(0.08)), Inches(0.48), Inches(0.16), month, font_size=9, color=THEME.muted, align=PP_ALIGN.CENTER)
    if y_label:
        add_textbox(slide, emu(left - Inches(0.02)), emu(top + height / 2 - Inches(0.15)), Inches(0.4), Inches(0.3), y_label, font_size=9, color=THEME.muted, align=PP_ALIGN.CENTER)
    add_textbox(slide, emu(left + Inches(0.18)), emu(top - Inches(0.16)), Inches(1.25), Inches(0.14), label_a.upper(), font_size=10, color=color_a, bold=True)
    add_textbox(slide, emu(left + Inches(1.52)), emu(top - Inches(0.16)), Inches(1.25), Inches(0.14), label_b.upper(), font_size=10, color=color_b, bold=True)


def add_background(slide, slide_number: int, *, section: str | None = None, footer: str = "") -> None:
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = rgb(THEME.bg)
    bg.line.fill.background()

    bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, SLIDE_W, Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(THEME.primary)
    bar.line.fill.background()

    accent_bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(10.55), 0, Inches(2.78), Inches(0.08))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = rgb(THEME.accent)
    accent_bar.line.fill.background()

    if section:
        tag = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, MARGIN_X, Inches(0.22), Inches(1.7), Inches(0.28))
        tag.fill.solid()
        tag.fill.fore_color.rgb = rgb(THEME.paper)
        tag.line.color.rgb = rgb(THEME.line)
        add_textbox(slide, MARGIN_X + Inches(0.02), Inches(0.245), Inches(1.66), Inches(0.2), section.upper(), font_size=10, color=THEME.primary, bold=True, font_name=FONT_BODY, align=PP_ALIGN.CENTER)

    if footer:
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


def add_chart_slide(
    slide,
    slide_number: int,
    image_path: Path,
    *,
    section: str,
    badge: tuple[str, str] | None = None,
    takeaway: str | None = None,
    note: str | None = None,
    accent: str = THEME.primary,
) -> None:
    add_background(slide, slide_number, section=section)
    if badge:
        add_badge(slide, badge[0], Inches(11.25), Inches(0.28), Inches(1.35), fill=badge[1])
    add_panel(slide, Inches(0.42), Inches(0.74), Inches(12.5), Inches(5.55), fill=THEME.paper, line=THEME.line)
    add_contained_picture(slide, image_path, Inches(0.6), Inches(0.92), Inches(12.1), Inches(5.18))
    if takeaway:
        add_exhibit_footer(slide, Inches(0.68), Inches(6.02), Inches(12.0), Inches(0.72), takeaway=takeaway, note=note, accent=accent)


def build_metrics() -> dict[str, object]:
    df = load_data(ROOT / "case_comp_data.csv")
    scoped = df[df["Date"].dt.year.between(2019, 2024)].copy()
    scoped["Year"] = scoped["Date"].dt.year
    df_period = df.copy()
    df_period["Period"] = df_period["Date"].dt.year.astype(str)
    df_period.loc[df_period["Date"].dt.year.eq(2025), "Period"] = "2025 H1"
    period_order = ["2019", "2020", "2021", "2022", "2023", "2024", "2025 H1"]
    annual = scoped.groupby(["Year", "Type"], as_index=False)["Total_Volume"].sum()
    pivot = annual.pivot(index="Year", columns="Type", values="Total_Volume")
    pivot["total"] = pivot["conventional"] + pivot["organic"]

    q1 = pd.read_csv(OUT_DIR / "q1_winners.csv")
    q2 = pd.read_csv(OUT_DIR / "q2_organic_share_winners.csv")
    q3 = pd.read_csv(OUT_DIR / "q3_price_volume_metrics_raw.csv")
    q5 = pd.read_csv(OUT_DIR / "q5_city_profitability_base.csv")
    q6u = pd.read_csv(OUT_DIR / "q6_city_profitability_shipping_up_50.csv")
    q6d = pd.read_csv(OUT_DIR / "q6_city_profitability_shipping_down_50.csv")
    q7r = pd.read_csv(OUT_DIR / "q7_rank_comparison.csv")
    q7s = pd.read_csv(OUT_DIR / "q7_shipping_sensitivity.csv")
    june_prices = pd.read_csv(OUT_DIR / "q5_june2025_city_prices.csv")
    season = pd.read_csv(OUT_DIR / "q8_monthly_seasonality.csv")

    period_city_type = df_period.groupby(["Period", "Type", "City"], as_index=False)["Revenue"].sum()
    period_city_type["Period"] = pd.Categorical(period_city_type["Period"], categories=period_order, ordered=True)

    top_conv_cities = (
        period_city_type[period_city_type["Type"] == "conventional"]
        .groupby("City", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(5)["City"]
        .tolist()
    )
    top_org_cities = (
        period_city_type[period_city_type["Type"] == "organic"]
        .groupby("City", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(5)["City"]
        .tolist()
    )
    conv_trend = (
        period_city_type[(period_city_type["Type"] == "conventional") & (period_city_type["City"].isin(top_conv_cities))]
        .pivot(index="Period", columns="City", values="Revenue")
        .reindex(period_order)
        .fillna(0)
    )
    org_trend = (
        period_city_type[(period_city_type["Type"] == "organic") & (period_city_type["City"].isin(top_org_cities))]
        .pivot(index="Period", columns="City", values="Revenue")
        .reindex(period_order)
        .fillna(0)
    )

    share_2024 = (
        df[df["Date"].dt.year == 2024]
        .groupby(["City", "Type"], as_index=False)["Total_Volume"]
        .sum()
        .pivot(index="City", columns="Type", values="Total_Volume")
        .fillna(0)
    )
    share_2024["organic_share"] = share_2024["organic"] / (share_2024["organic"] + share_2024["conventional"])
    share_2024 = share_2024.reset_index()[["City", "organic_share"]]
    entry_screen = q5.merge(share_2024, on="City", how="left").merge(june_prices[["City", "avg_retail_price_jun2025"]], on="City", how="left")
    entry_screen["profit_rank"] = entry_screen["Profit"].rank(ascending=False, method="dense")
    entry_screen["price_rank"] = entry_screen["forecast_retail_price_jun2026"].rank(ascending=False, method="dense")
    entry_screen["share_rank"] = entry_screen["organic_share"].rank(ascending=False, method="dense")
    entry_screen["miles_rank"] = entry_screen["Mileage_miles"].rank(ascending=True, method="dense")

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
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q5": q5,
        "q6u": q6u,
        "q6d": q6d,
        "q7r": q7r,
        "q7s": q7s,
        "june_prices": june_prices,
        "season_raw": season,
        "conv_trend": conv_trend,
        "org_trend": org_trend,
        "top_conv_cities": top_conv_cities,
        "top_org_cities": top_org_cities,
        "entry_screen": entry_screen,
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


CHART_SLIDE_META: dict[int, dict[str, str]] = {
    4: {
        "takeaway": "Organic is still a niche share of the total market, but it is growing materially faster than the overall Hass category.",
        "note": "Use this as market context, not as a launch recommendation by itself.",
        "accent": THEME.primary,
    },
    6: {
        "takeaway": "Los Angeles dominates dollar sales in every required period and in both product types.",
        "note": "This answers Q1 on market scale, not on pilot attractiveness.",
        "accent": THEME.primary,
    },
    7: {
        "takeaway": "Conventional sales leadership is structural: Los Angeles leads every full year and 2025 H1 by a wide margin.",
        "note": "The gap to New York stays large rather than collapsing over time.",
        "accent": THEME.primary,
    },
    8: {
        "takeaway": "Los Angeles also leads organic dollar sales, but the gap is much narrower than in conventional.",
        "note": "Organic leadership and organic readiness are not the same thing.",
        "accent": THEME.compare,
    },
    9: {
        "takeaway": "Seattle leads organic penetration in most periods, which makes it more relevant for pilot fit than raw sales alone.",
        "note": "Seattle wins 5 of 7 measured periods.",
        "accent": THEME.compare,
    },
    10: {
        "takeaway": "Organic volume has grown much faster than the total market, but it still represents a relatively small share of total Hass demand.",
        "note": "Use this to justify opportunity size without overstating maturity.",
        "accent": THEME.primary,
    },
    11: {
        "takeaway": "At the market level, higher prices generally coincide with lower volume, but the relationship is only moderately strong.",
        "note": "This is useful context, not a full elasticity model.",
        "accent": THEME.compare,
    },
    12: {
        "takeaway": "Within product type, price alone explains very little, so city mix and market structure matter more than simple price moves.",
        "note": "Protects the deck from overclaiming elasticity.",
        "accent": THEME.compare,
    },
    13: {
        "takeaway": "Freight, fuel, inflation, labor, and cross-border supply risk all shape the launch environment around the pilot.",
        "note": "Context slide: these are directional drivers rather than model outputs.",
        "accent": THEME.stress,
    },
    14: {
        "takeaway": "City-level micro drivers explain why Los Angeles wins scale, Seattle wins penetration, and the Pacific Northwest supports premium pricing.",
        "note": "Context slide: use it to interpret the recommendation rather than prove it alone.",
        "accent": THEME.compare,
    },
    15: {
        "takeaway": "The best pilot cities need price power, organic readiness, and manageable miles at the same time.",
        "note": "This is the bridge from market analysis into city selection.",
        "accent": THEME.primary,
    },
    16: {
        "takeaway": "The profit model is simple enough to audit: revenue is driven by local price support, then reduced by acquisition and freight.",
        "note": "Keep this transparent so later rankings feel defensible.",
        "accent": THEME.primary,
    },
    17: {
        "takeaway": "June retail pricing points toward the Pacific Northwest as the premium revenue opportunity.",
        "note": "The selected five are also the five strongest June price markets.",
        "accent": THEME.accent,
    },
    18: {
        "takeaway": "Base-case profitability creates a clear top-five cut line rather than a crowded cluster of nearly identical options.",
        "note": "The rank-5 to rank-6 gap matters because it makes the recommendation more defensible.",
        "accent": THEME.primary,
    },
    19: {
        "takeaway": "Seattle, Boise, Portland, Spokane, and San Diego are the cleanest five-city set under the base-case model.",
        "note": "This is the formal selection slide for the recommendation.",
        "accent": THEME.primary,
    },
    20: {
        "takeaway": "The chosen five win on price support, not just proximity, which is why nearby large California markets do not automatically make the cut.",
        "note": "San Diego acts as the low-mile hedge inside a price-led set.",
        "accent": THEME.accent,
    },
    21: {
        "takeaway": "A 50% freight increase compresses profit, but it does not change the five recommended cities.",
        "note": "This is resilience, not immunity: margins fall, ranking does not.",
        "accent": THEME.stress,
    },
    22: {
        "takeaway": "A 50% freight decrease expands profit, but it still does not change the five recommended cities.",
        "note": "The recommendation is stable because price support dominates the order.",
        "accent": THEME.compare,
    },
    23: {
        "takeaway": "The same five cities stay top-ranked in every modeled freight scenario.",
        "note": "This is the cleanest single-slide answer to the rank-stability question.",
        "accent": THEME.primary,
    },
    24: {
        "takeaway": "Freight sensitivity is highest in distant Northeast markets, not in the recommended set.",
        "note": "The pilot cities move, but far less than the most exposed long-haul markets.",
        "accent": THEME.stress,
    },
    25: {
        "takeaway": "Local retail price support is the main reason the recommendation stays stable under freight stress.",
        "note": "All 40 modeled cities remain profitable even at +50% shipping.",
        "accent": THEME.accent,
    },
    26: {
        "takeaway": "Price peaks in July, which creates the best annual window for margin protection rather than pure volume push.",
        "note": "Both conventional and organic follow this summer price crest.",
        "accent": THEME.accent,
    },
    27: {
        "takeaway": "Volume peaks earlier and softens into November, so service and demand support need different timing than pricing decisions.",
        "note": "Organic peaks in January; conventional peaks in May.",
        "accent": THEME.compare,
    },
}


def slide_1(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 1, footer="Anonymized team submission")
    add_badge(slide, "Decision Deck", Inches(10.96), Inches(0.28), Inches(1.48), fill=THEME.primary)
    add_textbox(
        slide,
        MARGIN_X,
        Inches(0.94),
        Inches(5.85),
        Inches(0.2),
        "WEST VALLEY FRESH DISTRIBUTION COMPANY",
        font_size=11,
        color=THEME.muted,
        font_name=FONT_BODY,
        bold=True,
    )
    add_textbox(
        slide,
        MARGIN_X,
        Inches(1.24),
        Inches(7.2),
        Inches(1.9),
        "A disciplined 5-city pilot is the right way to enter organic Hass avocados",
        font_size=29,
        color=THEME.primary,
        font_name=FONT_HEAD,
        bold=True,
    )
    add_textbox(
        slide,
        MARGIN_X,
        Inches(3.18),
        Inches(6.9),
        Inches(0.64),
        "This deck argues for a selective launch, not a broad rollout, by testing price support, organic readiness, freight resilience, and seasonality in the supplied city data.",
        font_size=15,
        color=THEME.ink,
        font_name=FONT_BODY,
    )
    chip_top = Inches(4.18)
    for idx, (label, value, width) in enumerate(
        [
            ("Pilot order", "20,000 organic units", 2.2),
            ("Market scope", "40 city markets", 2.0),
            ("History", "2019 to Jun 2025", 2.15),
        ]
    ):
        add_stat_chip(
            slide,
            MARGIN_X + Inches(idx * 2.38),
            chip_top,
            Inches(width),
            Inches(0.92),
            label=label,
            value=value,
            value_color=THEME.primary if idx < 2 else THEME.compare,
        )

    add_panel(slide, Inches(8.55), Inches(1.28), Inches(3.95), Inches(4.72), fill=THEME.paper)
    add_textbox(
        slide,
        Inches(8.82),
        Inches(1.58),
        Inches(2.8),
        Inches(0.2),
        "DECISION TO PROVE",
        font_size=11,
        color=THEME.muted,
        font_name=FONT_BODY,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(8.82),
        Inches(1.9),
        Inches(3.28),
        Inches(0.86),
        "Enter through a disciplined 5-city pilot, then scale only where realized economics hold.",
        font_size=21,
        color=THEME.primary,
        font_name=FONT_HEAD,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(8.82),
        Inches(2.95),
        Inches(3.15),
        Inches(0.18),
        "THIS DECK TESTS",
        font_size=10,
        color=THEME.muted,
        font_name=FONT_BODY,
        bold=True,
    )
    add_bullets(
        slide,
        Inches(8.82),
        Inches(3.2),
        Inches(3.12),
        Inches(1.42),
        [
            "Whether local price support outweighs simple market size.",
            "Whether the top-ranked cities survive freight volatility.",
            "Whether seasonality changes how the pilot should operate.",
        ],
        font_size=13,
    )

    add_textbox(
        slide,
        MARGIN_X,
        Inches(5.5),
        Inches(7.0),
        Inches(0.45),
        "Prepared as an anonymized submission for the 2026 IMA Student Case Competition. The deck is designed to stand alone without speaker notes.",
        font_size=12,
        color=THEME.muted,
        font_name=FONT_BODY,
    )


def slide_2(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 2, section="Executive Summary")
    add_title(slide, "West Valley should launch a disciplined 5-city organic pilot")
    add_panel(slide, Inches(0.72), Inches(1.78), Inches(7.15), Inches(4.78), fill=THEME.paper)
    add_textbox(slide, Inches(1.0), Inches(2.08), Inches(2.4), Inches(0.2), "RECOMMENDATION", font_size=11, color=THEME.muted, font_name=FONT_BODY, bold=True)
    add_textbox(
        slide,
        Inches(1.0),
        Inches(2.42),
        Inches(6.1),
        Inches(0.78),
        "Launch Seattle, Boise, Portland, Spokane, and San Diego first.",
        font_size=25,
        color=THEME.primary,
        font_name=FONT_HEAD,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(1.0),
        Inches(3.16),
        Inches(5.95),
        Inches(0.52),
        "These five cities combine premium June pricing, organic readiness, and manageable freight better than a broad national rollout.",
        font_size=15,
        color=THEME.ink,
    )
    city_specs = [
        ("Seattle", 1.0, 3.95, 1.15),
        ("Boise", 2.24, 3.95, 1.05),
        ("Portland", 3.37, 3.95, 1.23),
        ("Spokane", 4.68, 3.95, 1.18),
        ("San Diego", 5.94, 3.95, 1.42),
    ]
    for city, x, y, width in city_specs:
        add_badge(slide, city, Inches(x), Inches(y), Inches(width), fill=THEME.primary, text_color=THEME.paper)
    for idx, (label, value, color) in enumerate(
        [
            ("Avg profit", fmt_money(m["top5_profit_avg"]), THEME.primary),
            ("Avg margin", fmt_pct(m["top5_margin_avg"]), THEME.compare),
            ("Rank-5 gap", fmt_money(m["rank_gap"], 0), THEME.accent),
        ]
    ):
        add_stat_chip(
            slide,
            Inches(0.98 + idx * 2.24),
            Inches(4.72),
            Inches(2.0),
            Inches(1.08),
            label=label,
            value=value,
            value_color=color,
        )

    proof_cards = [
        ("Why these cities", "Highest June price support", "The selected five are also the five highest-price June 2025 organic markets in the model.", THEME.primary),
        ("Why the list holds", "Same 5 cities", "The recommendation is unchanged in the base, +50%, and -50% shipping cases.", THEME.compare),
        ("How to operate it", "Pilot before scale", "Run a tight launch first and use seasonality to shift from volume protection to margin protection by month.", THEME.accent),
    ]
    for idx, card in enumerate(proof_cards):
        add_card(slide, Inches(8.18), Inches(1.9 + idx * 1.52), Inches(4.4), Inches(1.28), header=card[0], metric=card[1], body=card[2], metric_color=card[3])
    add_subtitle(slide, "Model note: each city is scored as a comparable 20,000-unit scenario using June 2025 retail price as the June 2026 proxy.", top=6.1, width=12.0)


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
    meta = CHART_SLIDE_META[4]
    add_chart_slide(
        slide,
        4,
        OUT_DIR / "deck_q2_growth_share.png",
        section="Foundation",
        takeaway=meta["takeaway"],
        note=meta["note"],
        accent=meta["accent"],
    )


def slide_5(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 5, section="Foundation")
    add_title(slide, "The pilot screen should be price support, organic readiness, and route efficiency")
    q2 = m["q2"]
    seattle_wins = int((q2["City"] == "Seattle").sum())
    top5 = m["q5"].head(5)
    shipping_low = m["q7r"].head(5)["Profit_base"].min() - m["q6u"].head(5)["Profit"].min()
    shipping_high = m["q7r"].head(5)["Profit_base"].max() - m["q6u"].head(5)["Profit"].max()

    add_panel(slide, Inches(0.78), Inches(1.84), Inches(11.8), Inches(3.7), fill=THEME.paper)
    headers = [("Filter", 1.6), ("What good looks like", 3.05), ("Evidence in the model", 5.25), ("Why it matters", 2.1)]
    x = Inches(1.0)
    for label, width in headers:
        add_textbox(slide, x, Inches(2.08), Inches(width), Inches(0.18), label.upper(), font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
        x += Inches(width + 0.12)

    rows = [
        ("Price support", f"${top5['forecast_retail_price_jun2026'].min():.2f} to ${top5['forecast_retail_price_jun2026'].max():.2f} June pricing", "The selected five are also the five highest-price June 2025 organic markets.", "High local price support matters more than raw market size.", THEME.primary),
        ("Organic readiness", f"Seattle leads {seattle_wins} of 7 periods", "Organic penetration varies by city, so launch markets must show willingness to support premium mix.", "Total avocado scale alone is not enough to choose the right pilot.", THEME.compare),
        ("Route efficiency", f"{fmt_money(shipping_low)} to {fmt_money(shipping_high)} profit loss at +50% freight", "The recommended cities keep the same ranking even after a large shipping shock.", "Freight changes margin, but it does not overturn the top-five order.", THEME.stress),
    ]
    for idx, row in enumerate(rows):
        top = Inches(2.46 + idx * 0.96)
        band = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(1.0), top, Inches(1.38), Inches(0.74))
        band.fill.solid()
        band.fill.fore_color.rgb = rgb(row[4])
        band.line.color.rgb = rgb(row[4])
        add_textbox(slide, Inches(1.08), top + Inches(0.17), Inches(1.18), Inches(0.28), row[0], font_size=13, color=THEME.paper, font_name=FONT_HEAD, bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(slide, Inches(2.68), top + Inches(0.08), Inches(2.9), Inches(0.56), row[1], font_size=14, color=row[4], font_name=FONT_HEAD, bold=True)
        add_textbox(slide, Inches(5.78), top + Inches(0.06), Inches(4.95), Inches(0.6), row[2], font_size=12, color=THEME.ink)
        add_textbox(slide, Inches(10.95), top + Inches(0.06), Inches(1.2), Inches(0.6), row[3], font_size=12, color=THEME.ink)
    add_subtitle(slide, "These three filters explain why the Pacific Northwest plus San Diego survives the market, mix, and freight tests that follow.", top=5.78, width=11.9)


def slide_6(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 6, section="Market Analysis")
    add_title(slide, "Los Angeles leads dollar sales in every required period and in both types")
    q1 = m["q1"]
    rows = q1[["Period", "Conventional Winner", "Conventional Sales ($)", "Organic Winner", "Organic Sales ($)"]].values.tolist()
    add_panel(slide, Inches(0.78), Inches(1.78), Inches(8.45), Inches(4.78), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.02), Inches(2.4), Inches(0.18), "WINNER MATRIX", font_size=10, color=THEME.muted, bold=True)
    add_generic_table(
        slide,
        ["Period", "Conventional", "Sales", "Organic", "Sales"],
        rows,
        left=Inches(1.0),
        top=Inches(2.36),
        width=Inches(7.95),
        height=Inches(3.8),
        col_widths=[1.0, 1.9, 1.45, 1.9, 1.45],
        font_size=10,
    )
    add_panel(slide, Inches(9.48), Inches(1.78), Inches(3.1), Inches(4.78), fill=THEME.paper)
    add_stat_chip(slide, Inches(9.78), Inches(2.12), Inches(1.18), Inches(0.96), label="Winner cells", value="14/14", value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(11.06), Inches(2.12), Inches(1.18), Inches(0.96), label="Winning city", value="LA", value_color=THEME.accent, align=PP_ALIGN.CENTER)
    add_bullets(
        slide,
        Inches(9.78),
        Inches(3.45),
        Inches(2.5),
        Inches(1.8),
        [
            "Los Angeles is the clear scale leader in both conventional and organic revenue.",
            "This answers the sales question cleanly, but it does not mean Los Angeles is the best pilot market.",
            "The pilot recommendation still depends on price support, organic readiness, and freight.",
        ],
        font_size=13,
    )


def slide_7(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 7, section="Market Analysis")
    add_title(slide, "Conventional sales leadership is structural, not a one-year spike")
    conv = m["conv_trend"].copy()
    rows = []
    for period in conv.index.tolist():
        vals = [f"${conv.loc[period, city] / 1_000_000:.1f}M" for city in conv.columns.tolist()]
        rows.append([period] + vals)
    add_panel(slide, Inches(0.78), Inches(1.8), Inches(8.55), Inches(4.76), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.02), Inches(2.9), Inches(0.18), "TOP 5 CONVENTIONAL CITIES", font_size=10, color=THEME.muted, bold=True)
    add_generic_table(
        slide,
        ["Period"] + [city.replace("BaltimoreWashington", "Balt/Wash").replace("DallasFtWorth", "Dallas/FW").replace("PhoenixTucson", "Phoenix/Tucson") for city in conv.columns.tolist()],
        rows,
        left=Inches(1.0),
        top=Inches(2.34),
        width=Inches(8.0),
        height=Inches(3.9),
        col_widths=[1.0, 1.45, 1.3, 1.45, 1.35, 1.45],
        font_size=10,
    )
    add_panel(slide, Inches(9.58), Inches(1.8), Inches(3.0), Inches(4.76), fill=THEME.paper)
    la_2024 = conv.loc["2024", "Los Angeles"]
    ny_2024 = conv.loc["2024", "New York"]
    la_2025 = conv.loc["2025 H1", "Los Angeles"]
    ny_2025 = conv.loc["2025 H1", "New York"]
    add_stat_chip(slide, Inches(9.88), Inches(2.12), Inches(2.4), Inches(0.96), label="2024 lead vs NY", value=fmt_money(la_2024 - ny_2024), value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(9.88), Inches(3.28), Inches(2.4), Inches(0.96), label="2025 H1 lead vs NY", value=fmt_money(la_2025 - ny_2025), value_color=THEME.accent, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(9.88), Inches(4.72), Inches(2.35), Inches(0.75), "Los Angeles is not just the winner. It leads by a structurally larger revenue base across every measured period.", font_size=13, color=THEME.ink)


def slide_8(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 8, section="Market Analysis")
    add_title(slide, "Organic sales leadership is consistent, but the gap is much narrower")
    org = m["org_trend"].copy()
    rows = []
    for period in org.index.tolist():
        vals = [f"${org.loc[period, city] / 1_000_000:.1f}M" for city in org.columns.tolist()]
        rows.append([period] + vals)
    add_panel(slide, Inches(0.78), Inches(1.8), Inches(8.55), Inches(4.76), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.02), Inches(2.7), Inches(0.18), "TOP 5 ORGANIC CITIES", font_size=10, color=THEME.muted, bold=True)
    add_generic_table(
        slide,
        ["Period"] + [city.replace("BaltimoreWashington", "Balt/Wash").replace("San Francisco", "San Fran") for city in org.columns.tolist()],
        rows,
        left=Inches(1.0),
        top=Inches(2.34),
        width=Inches(8.0),
        height=Inches(3.9),
        col_widths=[1.0, 1.45, 1.45, 1.35, 1.35, 1.4],
        font_size=10,
    )
    add_panel(slide, Inches(9.58), Inches(1.8), Inches(3.0), Inches(4.76), fill=THEME.paper)
    la_2024 = org.loc["2024", "Los Angeles"]
    ny_2024 = org.loc["2024", "New York"]
    add_stat_chip(slide, Inches(9.88), Inches(2.12), Inches(2.4), Inches(0.96), label="2024 lead vs NY", value=fmt_money(la_2024 - ny_2024), value_color=THEME.compare, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(9.88), Inches(3.28), Inches(2.4), Inches(0.96), label="Seattle in top tier", value="Top 5", value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(9.88), Inches(4.72), Inches(2.35), Inches(0.75), "Organic scale is less concentrated than conventional, which leaves more room for pilot-market selection to differ from simple size rankings.", font_size=13, color=THEME.ink)


def slide_9(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 9, section="Market Analysis")
    add_title(slide, "Seattle leads organic penetration in most periods")
    q2 = m["q2"].copy()
    add_panel(slide, Inches(0.78), Inches(1.86), Inches(11.8), Inches(4.7), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.08), Inches(2.6), Inches(0.18), "WINNER TIMELINE", font_size=10, color=THEME.muted, bold=True)
    for idx, (_, row) in enumerate(q2.iterrows()):
        x = Inches(1.0 + idx * 1.63)
        top = Inches(2.58)
        period_box = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, top, Inches(1.35), Inches(0.36))
        period_box.fill.solid()
        period_box.fill.fore_color.rgb = rgb(THEME.bg)
        period_box.line.color.rgb = rgb(THEME.line)
        add_textbox(slide, x, top + Inches(0.08), Inches(1.35), Inches(0.16), str(row["Period"]), font_size=10, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)
        winner_fill = THEME.primary if row["City"] == "Seattle" else THEME.compare if row["City"] == "Charlotte" else THEME.accent
        add_badge(slide, str(row["City"]), x, Inches(3.12), Inches(1.35), fill=winner_fill)
        add_textbox(slide, x, Inches(3.62), Inches(1.35), Inches(0.18), str(row["Organic Share"]), font_size=12, color=winner_fill, font_name=FONT_HEAD, bold=True, align=PP_ALIGN.CENTER)
        if idx < len(q2) - 1:
            line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, emu(x + Inches(1.38)), emu(Inches(3.28)), emu(x + Inches(1.58)), emu(Inches(3.28)))
            line.line.color.rgb = rgb(THEME.line)
            line.line.width = Pt(1.6)
    add_stat_band(
        slide,
        Inches(1.02),
        Inches(4.5),
        Inches(11.15),
        Inches(1.0),
        [
            ("Most frequent leader", "Seattle", "Wins 5 of the 7 measured periods and is the clearest indicator of organic readiness."),
            ("Best one-year share", "Orlando 12.87%", "Orlando peaks in 2022, but it does not sustain the same multi-period lead."),
            ("Current H1 leader", "Charlotte 9.45%", "Charlotte leads 2025 H1, showing that penetration leadership is not static."),
        ],
        highlight_idx=0,
    )


def slide_10(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 10, section="Market Analysis")
    add_title(slide, "Organic share has expanded even though it remains a niche slice of the total market")
    add_stat_band(
        slide,
        Inches(0.82),
        Inches(1.86),
        Inches(11.75),
        Inches(1.25),
        [
            ("2019 organic share", f"{m['share_2019']:.2f}%", "Organic started from a small base inside the total Hass market."),
            ("2024 organic share", f"{m['share_2024']:.2f}%", "The share has risen, but it is still a minority slice of total demand."),
            ("Organic volume growth", f"+{m['growth_org']:.1f}%", "Organic volume grew much faster than the total category from 2019 to 2024."),
            ("Total volume growth", f"+{m['growth_total']:.1f}%", "The overall market also expanded, but at a much slower pace."),
        ],
        highlight_idx=2,
    )
    add_panel(slide, Inches(0.82), Inches(3.46), Inches(5.55), Inches(2.8), fill=THEME.paper)
    add_textbox(slide, Inches(1.08), Inches(3.76), Inches(1.8), Inches(0.18), "WHAT THIS MEANS", font_size=10, color=THEME.muted, bold=True)
    add_bullets(
        slide,
        Inches(1.08),
        Inches(4.1),
        Inches(4.8),
        Inches(1.6),
        [
            "The category is growing fast enough to justify entry.",
            "But the share is still small enough that city selection matters more than national scale ambition.",
            "That supports a pilot rather than a broad first-year rollout.",
        ],
        font_size=13,
    )
    add_panel(slide, Inches(6.7), Inches(3.46), Inches(5.87), Inches(2.8), fill=THEME.paper)
    add_textbox(slide, Inches(6.96), Inches(3.76), Inches(2.0), Inches(0.18), "INTERPRETATION", font_size=10, color=THEME.muted, bold=True)
    add_textbox(slide, Inches(6.96), Inches(4.16), Inches(5.2), Inches(1.35), "Organic is attractive because it is growing faster than the total Hass market. It still needs a disciplined launch because the category is not yet large enough to reward undifferentiated market entry.", font_size=14, color=THEME.ink)


def slide_11(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 11, section="Market Analysis")
    add_title(slide, "At the market level, higher prices generally coincide with lower volume")
    q3 = m["q3"]
    all_row = q3[q3["Segment"] == "All"].iloc[0]
    add_panel(slide, Inches(0.82), Inches(1.84), Inches(6.2), Inches(4.72), fill=THEME.paper)
    add_textbox(slide, Inches(1.08), Inches(2.08), Inches(2.4), Inches(0.18), "MARKET-LEVEL RELATIONSHIP", font_size=10, color=THEME.muted, bold=True)
    add_stat_chip(slide, Inches(1.08), Inches(2.42), Inches(1.55), Inches(1.0), label="Pearson r", value=f"{all_row['Pearson_r']:.3f}", value_color=THEME.compare, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(2.78), Inches(2.42), Inches(1.55), Inches(1.0), label="R2", value=f"{all_row['Linear_R2']:.3f}", value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(4.48), Inches(2.42), Inches(2.12), Inches(1.0), label="Elasticity", value=f"{all_row['LogLog_Elasticity']:.2f}", value_color=THEME.accent, align=PP_ALIGN.CENTER)
    add_bullets(
        slide,
        Inches(1.08),
        Inches(4.0),
        Inches(5.3),
        Inches(1.55),
        [
            "The overall relationship is moderately negative, not flat.",
            "That means higher-price markets often sell fewer units, but not in a mechanically perfect way.",
            "The recommendation still needs city-level nuance before turning this into a decision rule.",
        ],
        font_size=13,
    )
    add_panel(slide, Inches(7.3), Inches(1.84), Inches(5.28), Inches(4.72), fill=THEME.paper)
    add_textbox(slide, Inches(7.58), Inches(2.08), Inches(1.9), Inches(0.18), "READ IT THIS WAY", font_size=10, color=THEME.muted, bold=True)
    add_textbox(slide, Inches(7.58), Inches(2.46), Inches(4.7), Inches(0.5), "Price matters at the market level.", font_size=20, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_textbox(slide, Inches(7.58), Inches(3.1), Inches(4.65), Inches(1.05), "But it does not tell the whole story. Market mix, organic readiness, and local structure still explain why some cities are better pilot markets than others.", font_size=14, color=THEME.ink)
    add_textbox(slide, Inches(7.58), Inches(4.58), Inches(4.6), Inches(0.5), "This is why the deck separates scale leadership, penetration leadership, and entry-market economics instead of collapsing them into one rule.", font_size=12, color=THEME.muted)


def slide_12(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 12, section="Market Analysis")
    add_title(slide, "Within product type, price alone explains very little")
    q3 = m["q3"]
    conv = q3[q3["Segment"] == "Conventional"].iloc[0]
    org = q3[q3["Segment"] == "Organic"].iloc[0]
    cards = [
        ("Conventional", conv, THEME.primary),
        ("Organic", org, THEME.compare),
    ]
    for idx, (label, row, color) in enumerate(cards):
        left = Inches(0.92 + idx * 5.95)
        add_panel(slide, left, Inches(1.94), Inches(5.55), Inches(3.95), fill=THEME.paper)
        add_textbox(slide, left + Inches(0.26), Inches(2.2), Inches(2.0), Inches(0.22), label.upper(), font_size=11, color=THEME.muted, bold=True)
        add_stat_chip(slide, left + Inches(0.26), Inches(2.62), Inches(1.5), Inches(0.96), label="Pearson r", value=f"{row['Pearson_r']:.3f}", value_color=color, align=PP_ALIGN.CENTER)
        add_stat_chip(slide, left + Inches(1.92), Inches(2.62), Inches(1.4), Inches(0.96), label="R2", value=f"{row['Linear_R2']:.3f}", value_color=THEME.accent, align=PP_ALIGN.CENTER)
        add_stat_chip(slide, left + Inches(3.46), Inches(2.62), Inches(1.55), Inches(0.96), label="Elasticity", value=f"{row['LogLog_Elasticity']:.2f}", value_color=THEME.compare if idx == 0 else THEME.primary, align=PP_ALIGN.CENTER)
        add_textbox(slide, left + Inches(0.26), Inches(4.02), Inches(4.8), Inches(1.2), "Inside each type, the observed relationship between price and volume is very weak. That means city mix and local market structure matter more than price alone once the product type is fixed.", font_size=13, color=THEME.ink)
    add_panel(slide, Inches(1.08), Inches(6.18), Inches(11.0), Inches(0.56), fill=THEME.paper)
    add_textbox(slide, Inches(1.3), Inches(6.36), Inches(10.6), Inches(0.18), "Implication: do not overclaim elasticity. The pooled relationship is useful context, but pilot selection still requires city-level economics and penetration evidence.", font_size=12, color=THEME.ink, bold=True)


def slide_13(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 13, section="Market Analysis")
    add_badge(slide, "Context", Inches(11.25), Inches(0.28), Inches(1.35), fill=THEME.compare)
    add_title(slide, "Macro drivers include freight, fuel, inflation, and cross-border supply risk")
    drivers = [
        ("Freight + fuel", "Affects landed cost and changes the margin penalty on long-haul markets.", THEME.stress),
        ("Imported supply risk", "Mexico and cross-border flow disruptions can tighten availability and raise uncertainty.", THEME.compare),
        ("Labor + inflation", "Raises operating pressure throughout sourcing, distribution, and retail execution.", THEME.primary_soft),
        ("Seasonality + promotions", "Changes when the market wants volume and when it supports price.", THEME.accent),
    ]
    for idx, (title, body, color) in enumerate(drivers):
        row = idx // 2
        col = idx % 2
        add_card(slide, Inches(0.92 + col * 5.92), Inches(2.0 + row * 2.0), Inches(5.45), Inches(1.62), header="Driver", metric=title, body=body, metric_color=color)
    add_panel(slide, Inches(1.08), Inches(6.18), Inches(11.0), Inches(0.56), fill=THEME.paper)
    add_textbox(slide, Inches(1.3), Inches(6.36), Inches(10.6), Inches(0.18), "These are context drivers, not modeled outputs. They explain why a selective pilot with freight resilience and seasonal discipline is safer than a broad first-year rollout.", font_size=12, color=THEME.ink, bold=True)


def slide_14(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 14, section="Market Analysis")
    add_badge(slide, "Context", Inches(11.25), Inches(0.28), Inches(1.35), fill=THEME.compare)
    add_title(slide, "Micro drivers explain why Los Angeles sells, Seattle penetrates, and the Pacific Northwest prices higher")
    entry = m["entry_screen"]
    la = entry[entry["City"] == "Los Angeles"].iloc[0]
    sea = entry[entry["City"] == "Seattle"].iloc[0]
    selected = entry[entry["City"].isin(m["q7r"].head(5)["City"].tolist())]
    rows = [
        ["Los Angeles", "Largest sales base", f"{la['organic_share']*100:.1f}%", f"${la['forecast_retail_price_jun2026']:.2f}", "Great scale, weaker pilot economics"],
        ["Seattle", "Strong organic leader", f"{sea['organic_share']*100:.1f}%", f"${sea['forecast_retail_price_jun2026']:.2f}", "Best mix of readiness and pricing"],
        ["Selected 5 avg", "Pilot set", f"{selected['organic_share'].mean()*100:.1f}%", f"${selected['forecast_retail_price_jun2026'].mean():.2f}", "Best overall entry screen"],
    ]
    add_panel(slide, Inches(0.82), Inches(1.9), Inches(11.75), Inches(4.62), fill=THEME.paper)
    add_textbox(slide, Inches(1.06), Inches(2.14), Inches(2.8), Inches(0.18), "CITY EVIDENCE MATRIX", font_size=10, color=THEME.muted, bold=True)
    add_generic_table(
        slide,
        ["Market", "What it wins", "2024 organic share", "June price", "Why it matters"],
        rows,
        left=Inches(1.02),
        top=Inches(2.5),
        width=Inches(11.0),
        height=Inches(2.2),
        col_widths=[1.5, 2.2, 1.65, 1.2, 4.0],
        font_size=11,
    )
    add_stat_band(
        slide,
        Inches(1.02),
        Inches(5.08),
        Inches(11.0),
        Inches(0.9),
        [
            ("Los Angeles", "Scale", "Shows where baseline demand is largest."),
            ("Seattle", "Penetration", "Shows where organic adoption is strongest."),
            ("Pacific NW + San Diego", "Price support", "Shows where the pilot can monetize organic units best."),
        ],
        highlight_idx=2,
    )


def slide_15(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 15, section="Market Analysis")
    add_title(slide, "The best entry markets need price power, organic readiness, and manageable miles")
    screen = m["entry_screen"].sort_values("Profit", ascending=False).head(8).copy()
    rows = []
    selected = set(m["q7r"].head(5)["City"].tolist())
    for _, row in screen.iterrows():
        rows.append([
            row["City"],
            f"${row['forecast_retail_price_jun2026']:.2f}",
            f"{row['organic_share']*100:.1f}%",
            f"{int(row['Mileage_miles']):,}",
            f"${row['Profit']:,.0f}",
            "Selected" if row["City"] in selected else "Not selected",
        ])
    add_panel(slide, Inches(0.78), Inches(1.86), Inches(8.55), Inches(4.66), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.08), Inches(2.8), Inches(0.18), "ENTRY SCREEN LEADERBOARD", font_size=10, color=THEME.muted, bold=True)
    add_generic_table(
        slide,
        ["City", "Price", "Organic share", "Miles", "Profit", "Pilot"],
        rows,
        left=Inches(1.0),
        top=Inches(2.42),
        width=Inches(8.0),
        height=Inches(3.8),
        col_widths=[1.5, 1.0, 1.3, 1.0, 1.25, 0.95],
        font_size=10,
    )
    add_panel(slide, Inches(9.58), Inches(1.86), Inches(3.02), Inches(4.66), fill=THEME.paper)
    add_bullets(
        slide,
        Inches(9.86),
        Inches(2.18),
        Inches(2.45),
        Inches(1.9),
        [
            "Price power filters out large but lower-value markets.",
            "Organic readiness helps separate premium-fit cities from simple scale leaders.",
            "Miles still matter, but they do not overturn a strong local price advantage.",
        ],
        font_size=13,
    )
    add_stat_chip(slide, Inches(9.86), Inches(4.62), Inches(2.36), Inches(0.96), label="Bridge to recommendation", value="Best pilot set = top 5", value_color=THEME.primary, align=PP_ALIGN.CENTER)


def slide_16(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 16, section="Recommendation")
    add_title(slide, "The profit model is simple, transparent, and easy to audit")
    top5 = m["q5"].head(5)
    avg_revenue = float(top5["Revenue"].mean())
    avg_shipping = float(top5["Shipping_Cost"].mean())
    avg_acq = float(top5["Acquisition_Cost"].mean())
    avg_profit = float(top5["Profit"].mean())
    add_panel(slide, Inches(0.82), Inches(1.84), Inches(7.0), Inches(4.72), fill=THEME.paper)
    add_textbox(slide, Inches(1.06), Inches(2.08), Inches(2.3), Inches(0.18), "AVERAGE UNIT ECONOMICS", font_size=10, color=THEME.muted, bold=True)
    steps = [
        ("Revenue", avg_revenue, THEME.primary),
        ("Acquisition", -avg_acq, THEME.stress),
        ("Shipping", -avg_shipping, THEME.compare),
        ("Profit", avg_profit, THEME.accent),
    ]
    base_x = emu(Inches(1.25))
    y = emu(Inches(3.2))
    cursor = base_x
    scale = emu(Inches(4.8)) / avg_revenue
    for idx, (label, value, color) in enumerate(steps):
        width = max(emu(abs(value) * scale), 1)
        bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, emu(cursor if value >= 0 else cursor - width), y, width, Inches(0.42))
        bar.fill.solid()
        bar.fill.fore_color.rgb = rgb(color)
        bar.line.color.rgb = rgb(color)
        add_textbox(slide, emu(cursor - Inches(0.15)), emu(y - Inches(0.28)), Inches(1.5), Inches(0.18), label.upper(), font_size=10, color=THEME.muted, bold=True)
        add_textbox(slide, emu(cursor - Inches(0.1)), emu(y + Inches(0.48)), Inches(1.4), Inches(0.18), fmt_money(value, 1), font_size=11, color=color, bold=True)
        cursor = cursor + width if value >= 0 else cursor - width
        if idx < len(steps) - 1:
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, emu(cursor), emu(y + Inches(0.21)), emu(cursor + Inches(0.3)), emu(y + Inches(0.21)))
            connector.line.color.rgb = rgb(THEME.line)
            connector.line.width = Pt(1.6)
            cursor += emu(Inches(0.3))
    add_textbox(slide, Inches(1.06), Inches(4.58), Inches(6.2), Inches(0.62), "Each city is scored using the same 20,000-unit assumption: planned wholesale revenue minus acquisition cost and the freight formula. The simplicity is a feature because judges can audit the math quickly.", font_size=14, color=THEME.ink)
    add_panel(slide, Inches(8.12), Inches(1.84), Inches(4.46), Inches(4.72), fill=THEME.paper)
    add_stat_band(
        slide,
        Inches(8.38),
        Inches(2.14),
        Inches(3.9),
        Inches(2.28),
        [
            ("Units", "20,000", "Comparable scorecard for each city."),
            ("Wholesale price", "40% of retail", "Revenue proxy used consistently across markets."),
            ("Freight", "$1,500 + $50 / 100 miles", "Makes distance visible without overcomplicating the model."),
        ],
        highlight_idx=1,
    )
    add_textbox(slide, Inches(8.4), Inches(4.9), Inches(3.8), Inches(0.52), "This is not a full allocation model yet. It is a transparent city-selection model.", font_size=13, color=THEME.ink)


def slide_17(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 17, section="Recommendation")
    add_title(slide, "June retail prices point to the Pacific Northwest as the premium opportunity")
    prices = m["june_prices"].sort_values("avg_retail_price_jun2025", ascending=False).head(10).reset_index(drop=True)
    selected = set(m["q7r"].head(5)["City"].tolist())
    items = [(row["City"], float(row["avg_retail_price_jun2025"]), THEME.primary if row["City"] in selected else THEME.primary_soft) for _, row in prices.iterrows()]
    add_panel(slide, Inches(0.82), Inches(1.84), Inches(7.5), Inches(4.72), fill=THEME.paper)
    add_ranked_bar_list(
        slide,
        items,
        left=Inches(1.08),
        top=Inches(2.24),
        width=Inches(6.8),
        row_h=Inches(0.38),
        max_value=float(prices["avg_retail_price_jun2025"].max()),
        value_fmt="${:.2f}",
        subtitle="Top June 2025 organic retail prices",
    )
    add_panel(slide, Inches(8.56), Inches(1.84), Inches(4.02), Inches(4.72), fill=THEME.paper)
    add_stat_chip(slide, Inches(8.84), Inches(2.14), Inches(1.74), Inches(0.96), label="Selected cities in top 5", value="5/5", value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(10.72), Inches(2.14), Inches(1.56), Inches(0.96), label="Top price", value=f"${prices.iloc[0]['avg_retail_price_jun2025']:.2f}", value_color=THEME.accent, align=PP_ALIGN.CENTER)
    add_bullets(
        slide,
        Inches(8.84),
        Inches(3.44),
        Inches(3.2),
        Inches(1.7),
        [
            "The selected five cities are also the five highest-price June organic markets.",
            "That is why price support keeps overpowering freight changes later in the analysis.",
            "Price is the strongest revenue-side reason the pilot set wins.",
        ],
        font_size=13,
    )


def slide_18(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 18, section="Recommendation")
    add_title(slide, "Base-case profitability produces a clear top-five cut line")
    q5 = m["q5"].sort_values("Profit", ascending=False).head(10).reset_index(drop=True)
    bar_items = [
        (row["City"], float(row["Profit"]), THEME.primary if idx < 5 else THEME.primary_soft)
        for idx, (_, row) in enumerate(q5.iterrows())
    ]
    add_panel(slide, Inches(0.78), Inches(1.72), Inches(7.2), Inches(4.82), fill=THEME.paper)
    add_ranked_bar_list(
        slide,
        bar_items,
        left=Inches(1.02),
        top=Inches(2.18),
        width=Inches(6.55),
        row_h=Inches(0.37),
        max_value=float(q5["Profit"].max()),
        subtitle="Top 10 city profit ranking",
    )
    add_panel(slide, Inches(8.28), Inches(1.72), Inches(4.3), Inches(4.82), fill=THEME.paper)
    add_textbox(slide, Inches(8.56), Inches(2.0), Inches(2.8), Inches(0.18), "WHY THE CUT LINE IS DEFENSIBLE", font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
    add_stat_chip(slide, Inches(8.56), Inches(2.34), Inches(1.9), Inches(1.0), label="Top-5 avg", value=fmt_money(m["top5_profit_avg"]), value_color=THEME.primary)
    add_stat_chip(slide, Inches(10.56), Inches(2.34), Inches(1.72), Inches(1.0), label="Next-5 avg", value=fmt_money(m["next5_profit_avg"]), value_color=THEME.compare)
    add_stat_chip(slide, Inches(8.56), Inches(3.52), Inches(3.72), Inches(0.96), label="Rank-5 vs rank-6 gap", value=fmt_money(m["rank_gap"], 0), value_color=THEME.accent)
    add_bullets(
        slide,
        Inches(8.56),
        Inches(4.72),
        Inches(3.4),
        Inches(1.35),
        [
            "The top five form a distinct profit tier rather than a noisy tie.",
            "All five are premium-price markets, not simply the nearest destinations.",
            "That makes the selection more robust to small assumption error.",
        ],
        font_size=13,
    )


def slide_19(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 19, section="Recommendation")
    add_title(slide, "Seattle, Boise, Portland, Spokane, and San Diego maximize base-case profitability")
    top5 = m["q5"].sort_values("Profit", ascending=False).head(5).reset_index(drop=True)
    for idx, row in top5.iterrows():
        add_badge(slide, row["City"], Inches(0.82 + idx * 2.37), Inches(1.72), Inches(1.85 if len(row["City"]) > 8 else 1.55), fill=THEME.primary, text_color=THEME.paper)
    rows = [
        (
            row["City"],
            row["State"],
            float(row["Mileage_miles"]),
            float(row["forecast_retail_price_jun2026"]),
            float(row["Profit"]),
            float(row["Profit_Margin"]),
        )
        for _, row in top5.iterrows()
    ]
    add_panel(slide, Inches(0.78), Inches(2.16), Inches(7.55), Inches(4.32), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.4), Inches(2.3), Inches(0.18), "SELECTED CITY SCORECARD", font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
    add_city_metric_table(slide, rows, left=Inches(1.0), top=Inches(2.72), width=Inches(7.05), height=Inches(3.3))
    add_panel(slide, Inches(8.6), Inches(2.16), Inches(3.98), Inches(4.32), fill=THEME.paper)
    add_textbox(slide, Inches(8.86), Inches(2.4), Inches(2.2), Inches(0.18), "WHY THIS SET WINS", font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
    add_stat_band(
        slide,
        Inches(8.86),
        Inches(2.72),
        Inches(3.42),
        Inches(2.2),
        [
            ("Price support", "Top 5 price markets", "The selected cities are the strongest June organic price markets in the model."),
            ("Freight", "Manageable miles", "San Diego provides a low-mile hedge while the Northwest still supports premium pricing."),
            ("Result", "Best profit set", "The five-city list wins on expected profit without requiring broad national complexity."),
        ],
        highlight_idx=2,
    )
    add_textbox(slide, Inches(8.88), Inches(5.24), Inches(3.2), Inches(0.58), "This is the formal Q5 answer: a disciplined five-city pilot beats a broad rollout because the premium-price cities still produce the best economics after freight.", font_size=12, color=THEME.ink)


def slide_20(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 20, section="Recommendation")
    add_title(slide, "The chosen five win on price support, not just distance")
    q5 = m["q5"].copy()
    selected = set(m["q7r"].head(5)["City"].tolist())
    compare = q5[~q5["City"].isin(selected)].nsmallest(4, "Mileage_miles")
    plot_df = pd.concat([q5[q5["City"].isin(selected)], compare], ignore_index=True)
    add_panel(slide, Inches(0.82), Inches(1.82), Inches(7.45), Inches(4.65), fill=THEME.paper)
    add_textbox(slide, Inches(1.05), Inches(2.04), Inches(2.2), Inches(0.18), "PRICE VS MILES", font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
    plot_left = Inches(1.22)
    plot_top = Inches(2.45)
    plot_w = Inches(6.45)
    plot_h = Inches(3.35)
    x0 = plot_left + Inches(0.45)
    y0 = plot_top + plot_h - Inches(0.4)
    x_axis = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x0, y0, plot_left + plot_w - Inches(0.18), y0)
    y_axis = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x0, plot_top + Inches(0.15), x0, y0)
    for axis in [x_axis, y_axis]:
        axis.line.color.rgb = rgb(THEME.line)
        axis.line.width = Pt(1.4)
    min_miles, max_miles = float(plot_df["Mileage_miles"].min()), float(plot_df["Mileage_miles"].max())
    min_price, max_price = float(plot_df["forecast_retail_price_jun2026"].min()), float(plot_df["forecast_retail_price_jun2026"].max())
    for _, row in plot_df.iterrows():
        x = x0 + (plot_w - Inches(0.9)) * ((float(row["Mileage_miles"]) - min_miles) / max(1.0, (max_miles - min_miles)))
        y = y0 - (plot_h - Inches(0.75)) * ((float(row["forecast_retail_price_jun2026"]) - min_price) / max(0.01, (max_price - min_price)))
        color = THEME.primary if row["City"] in selected else THEME.compare
        bubble = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, x - Inches(0.09), y - Inches(0.09), Inches(0.18), Inches(0.18))
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = rgb(color)
        bubble.line.color.rgb = rgb(color)
        add_textbox(slide, x + Inches(0.06), y - Inches(0.08), Inches(1.2), Inches(0.16), row["City"], font_size=10, color=color if row["City"] in selected else THEME.ink, font_name=FONT_BODY, bold=row["City"] in selected)
    add_textbox(slide, plot_left + Inches(2.4), Inches(5.92), Inches(2.0), Inches(0.16), "Higher mileage", font_size=10, color=THEME.muted, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(0.92), Inches(4.0), Inches(0.6), Inches(0.35), "Higher\nprice", font_size=10, color=THEME.muted, align=PP_ALIGN.CENTER)
    add_panel(slide, Inches(8.58), Inches(1.82), Inches(4.0), Inches(4.65), fill=THEME.paper)
    selected_avg_price = q5[q5["City"].isin(selected)]["forecast_retail_price_jun2026"].mean()
    nearby_avg_price = compare["forecast_retail_price_jun2026"].mean()
    add_stat_chip(slide, Inches(8.86), Inches(2.12), Inches(1.72), Inches(0.96), label="Selected avg price", value=f"${selected_avg_price:.2f}", value_color=THEME.primary)
    add_stat_chip(slide, Inches(10.68), Inches(2.12), Inches(1.62), Inches(0.96), label="Nearby alt.", value=f"${nearby_avg_price:.2f}", value_color=THEME.compare)
    add_bullets(
        slide,
        Inches(8.86),
        Inches(3.34),
        Inches(3.18),
        Inches(1.9),
        [
            "The winning cities are not the shortest-haul options; they are the strongest price-support markets.",
            "Nearby alternatives lose because lower local pricing gives back the mileage advantage.",
            "San Diego is the low-mile hedge inside an otherwise premium-price set.",
        ],
        font_size=13,
    )


def slide_21(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 21, section="Recommendation")
    add_title(slide, "Shipping +50% compresses profit but does not change the recommendation")
    q7r = m["q7r"].head(5).copy()
    add_panel(slide, Inches(0.78), Inches(1.82), Inches(7.55), Inches(4.7), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.06), Inches(2.7), Inches(0.18), "BASE VS +50% FREIGHT", font_size=10, color=THEME.muted, bold=True)
    max_profit = float(q7r["Profit_base"].max())
    for idx, (_, row) in enumerate(q7r.iterrows()):
        y = Inches(2.52 + idx * 0.74)
        add_textbox(slide, Inches(1.02), y, Inches(1.3), Inches(0.18), row["City"], font_size=11, color=THEME.ink, bold=True)
        base_w = Inches(2.8) * (float(row["Profit_base"]) / max_profit)
        up_w = Inches(2.8) * (float(row["Profit_up50"]) / max_profit)
        base_bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(2.42), y + Inches(0.02), base_w, Inches(0.16))
        base_bar.fill.solid()
        base_bar.fill.fore_color.rgb = rgb(THEME.primary_soft)
        base_bar.line.color.rgb = rgb(THEME.primary_soft)
        up_bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(2.42), y + Inches(0.22), up_w, Inches(0.16))
        up_bar.fill.solid()
        up_bar.fill.fore_color.rgb = rgb(THEME.stress)
        up_bar.line.color.rgb = rgb(THEME.stress)
        add_textbox(slide, Inches(5.45), y - Inches(0.02), Inches(1.0), Inches(0.16), fmt_money(float(row["Profit_base"]), 1), font_size=10, color=THEME.primary, align=PP_ALIGN.RIGHT)
        add_textbox(slide, Inches(5.45), y + Inches(0.19), Inches(1.0), Inches(0.16), fmt_money(float(row["Profit_up50"]), 1), font_size=10, color=THEME.stress, align=PP_ALIGN.RIGHT)
        add_textbox(slide, Inches(6.55), y + Inches(0.08), Inches(0.92), Inches(0.16), f"-{fmt_money(float(row['Profit_base'] - row['Profit_up50']), 1)}", font_size=10, color=THEME.stress, bold=True, align=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(2.42), Inches(5.92), Inches(1.2), Inches(0.16), "Base case", font_size=10, color=THEME.primary)
    add_textbox(slide, Inches(3.58), Inches(5.92), Inches(1.4), Inches(0.16), "+50% freight", font_size=10, color=THEME.stress)
    add_panel(slide, Inches(8.58), Inches(1.82), Inches(4.0), Inches(4.7), fill=THEME.paper)
    add_stat_chip(slide, Inches(8.86), Inches(2.12), Inches(1.8), Inches(0.96), label="Top-5 avg profit", value=fmt_money(m["up_profit_avg"]), value_color=THEME.stress)
    add_stat_chip(slide, Inches(10.78), Inches(2.12), Inches(1.48), Inches(0.96), label="Avg margin", value=fmt_pct(m["up_margin_avg"]), value_color=THEME.compare)
    add_stat_chip(slide, Inches(8.86), Inches(3.3), Inches(3.4), Inches(0.96), label="Result", value="Same 5 cities", value_color=THEME.primary)
    add_bullets(slide, Inches(8.86), Inches(4.55), Inches(3.16), Inches(1.4), ["Profit compresses in every selected city.", "The ranking does not change because local price support still dominates freight.", "This is a resilience test, not a claim that shipping does not matter."], font_size=13)


def slide_22(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 22, section="Recommendation")
    add_title(slide, "Shipping -50% expands profit but still does not change the recommendation")
    q7r = m["q7r"].head(5).copy()
    add_panel(slide, Inches(0.78), Inches(1.82), Inches(7.55), Inches(4.7), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.06), Inches(2.7), Inches(0.18), "BASE VS -50% FREIGHT", font_size=10, color=THEME.muted, bold=True)
    max_profit = float(q7r["Profit_down50"].max())
    for idx, (_, row) in enumerate(q7r.iterrows()):
        y = Inches(2.52 + idx * 0.74)
        add_textbox(slide, Inches(1.02), y, Inches(1.3), Inches(0.18), row["City"], font_size=11, color=THEME.ink, bold=True)
        base_w = Inches(2.8) * (float(row["Profit_base"]) / max_profit)
        down_w = Inches(2.8) * (float(row["Profit_down50"]) / max_profit)
        base_bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(2.42), y + Inches(0.02), base_w, Inches(0.16))
        base_bar.fill.solid()
        base_bar.fill.fore_color.rgb = rgb(THEME.primary_soft)
        base_bar.line.color.rgb = rgb(THEME.primary_soft)
        down_bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(2.42), y + Inches(0.22), down_w, Inches(0.16))
        down_bar.fill.solid()
        down_bar.fill.fore_color.rgb = rgb(THEME.compare)
        down_bar.line.color.rgb = rgb(THEME.compare)
        add_textbox(slide, Inches(5.45), y - Inches(0.02), Inches(1.0), Inches(0.16), fmt_money(float(row["Profit_base"]), 1), font_size=10, color=THEME.primary, align=PP_ALIGN.RIGHT)
        add_textbox(slide, Inches(5.45), y + Inches(0.19), Inches(1.0), Inches(0.16), fmt_money(float(row["Profit_down50"]), 1), font_size=10, color=THEME.compare, align=PP_ALIGN.RIGHT)
        add_textbox(slide, Inches(6.55), y + Inches(0.08), Inches(0.92), Inches(0.16), f"+{fmt_money(float(row['Profit_down50'] - row['Profit_base']), 1)}", font_size=10, color=THEME.compare, bold=True, align=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(2.42), Inches(5.92), Inches(1.2), Inches(0.16), "Base case", font_size=10, color=THEME.primary)
    add_textbox(slide, Inches(3.58), Inches(5.92), Inches(1.4), Inches(0.16), "-50% freight", font_size=10, color=THEME.compare)
    add_panel(slide, Inches(8.58), Inches(1.82), Inches(4.0), Inches(4.7), fill=THEME.paper)
    add_stat_chip(slide, Inches(8.86), Inches(2.12), Inches(1.8), Inches(0.96), label="Top-5 avg profit", value=fmt_money(m["down_profit_avg"]), value_color=THEME.compare)
    add_stat_chip(slide, Inches(10.78), Inches(2.12), Inches(1.48), Inches(0.96), label="Avg margin", value=fmt_pct(m["down_margin_avg"]), value_color=THEME.primary)
    add_stat_chip(slide, Inches(8.86), Inches(3.3), Inches(3.4), Inches(0.96), label="Result", value="Same 5 cities", value_color=THEME.primary)
    add_bullets(slide, Inches(8.86), Inches(4.55), Inches(3.16), Inches(1.4), ["Every selected city benefits from lower freight.", "The rank order still does not move.", "That confirms the decision is about optimization, not about barely surviving freight."], font_size=13)


def slide_23(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 23, section="Recommendation")
    add_title(slide, "The same five cities stay top-ranked in every modeled scenario")
    q7r = m["q7r"].head(5).copy()
    add_panel(slide, Inches(0.78), Inches(1.8), Inches(7.1), Inches(4.78), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.04), Inches(2.4), Inches(0.18), "RANK MATRIX", font_size=10, color=THEME.muted, bold=True)
    table = slide.shapes.add_table(6, 4, Inches(1.0), Inches(2.4), Inches(6.58), Inches(3.6)).table
    headers = ["Rank", "Base", "+50%", "-50%"]
    for idx, header in enumerate(headers):
        cell = table.cell(0, idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(THEME.primary)
    for row_idx, (_, row) in enumerate(q7r.iterrows(), start=1):
        values = [str(row_idx), row["City"], row["City"], row["City"]]
        for col_idx, value in enumerate(values):
            cell = table.cell(row_idx, col_idx)
            cell.text = value
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(THEME.paper if row_idx % 2 else THEME.bg)
    widths = [0.8, 1.9, 1.9, 1.9]
    for idx, width in enumerate(widths):
        table.columns[idx].width = Inches(width)
    for row in table.rows:
        row.height = Inches(0.56)
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(11)
                    run.font.bold = row == table.rows[0]
                    run.font.color.rgb = rgb(THEME.paper if row == table.rows[0] else THEME.ink)
    add_panel(slide, Inches(8.22), Inches(1.8), Inches(4.36), Inches(4.78), fill=THEME.paper)
    add_stat_chip(slide, Inches(8.5), Inches(2.12), Inches(1.65), Inches(0.96), label="Rank changes", value="0", value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(10.26), Inches(2.12), Inches(2.0), Inches(0.96), label="Selected set", value="Same 5 cities", value_color=THEME.accent, align=PP_ALIGN.CENTER)
    add_bullets(
        slide,
        Inches(8.5),
        Inches(3.5),
        Inches(3.4),
        Inches(1.8),
        [
            "Base, upside, and downside freight scenarios all return the same five cities in the same order.",
            "That is the cleanest evidence that the recommendation is structurally stable.",
            "The explanation comes next: price support matters more than sensitivity alone.",
        ],
        font_size=13,
    )


def slide_24(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 24, section="Recommendation")
    add_title(slide, "Shipping sensitivity is highest in distant markets, not in the recommended set")
    q7s = m["q7s"].sort_values("Profit_Impact_for_50pct_Shipping_Change", ascending=False).head(8).reset_index(drop=True)
    selected = set(m["q7r"].head(5)["City"].tolist())
    items = [
        (
            row["City"],
            float(row["Profit_Impact_for_50pct_Shipping_Change"]),
            THEME.primary if row["City"] in selected else THEME.stress,
        )
        for _, row in q7s.iterrows()
    ]
    add_panel(slide, Inches(0.78), Inches(1.8), Inches(7.4), Inches(4.78), fill=THEME.paper)
    add_ranked_bar_list(
        slide,
        items,
        left=Inches(1.02),
        top=Inches(2.22),
        width=Inches(6.7),
        row_h=Inches(0.43),
        max_value=float(q7s["Profit_Impact_for_50pct_Shipping_Change"].max()),
        value_fmt="${:,.0f}",
        subtitle="Largest +/-50% profit swings",
    )
    add_panel(slide, Inches(8.38), Inches(1.8), Inches(4.2), Inches(4.78), fill=THEME.paper)
    add_textbox(slide, Inches(8.64), Inches(2.06), Inches(2.6), Inches(0.18), "HOW TO READ IT", font_size=10, color=THEME.muted, bold=True)
    add_bullets(
        slide,
        Inches(8.64),
        Inches(2.42),
        Inches(3.4),
        Inches(1.45),
        [
            "Red bars are the most freight-sensitive markets overall.",
            "Green bars show recommended cities that still move less than the most exposed long-haul markets.",
            "Sensitivity affects margin, but it does not explain the final ranking by itself.",
        ],
        font_size=13,
    )
    add_stat_chip(slide, Inches(8.64), Inches(4.42), Inches(1.72), Inches(0.96), label="Recommended range", value="$813-$1,024", value_color=THEME.primary)
    add_stat_chip(slide, Inches(10.48), Inches(4.42), Inches(1.78), Inches(0.96), label="What matters", value="Price still wins", value_color=THEME.accent)


def slide_25(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 25, section="Recommendation")
    add_title(slide, "Local retail price is the main lever behind rank stability")
    q5_price = m["q5"].sort_values("forecast_retail_price_jun2026", ascending=False).head(8).reset_index(drop=True)
    q7s = m["q7s"].sort_values("Profit_Impact_for_50pct_Shipping_Change", ascending=False).head(8).reset_index(drop=True)
    selected = set(m["q7r"].head(5)["City"].tolist())
    left_items = [(row["City"], float(row["forecast_retail_price_jun2026"]), THEME.primary if row["City"] in selected else THEME.primary_soft) for _, row in q5_price.iterrows()]
    right_items = [(row["City"], float(row["Profit_Impact_for_50pct_Shipping_Change"]), THEME.stress if row["City"] not in selected else THEME.compare) for _, row in q7s.iterrows()]
    add_panel(slide, Inches(0.78), Inches(1.82), Inches(5.75), Inches(4.7), fill=THEME.paper)
    add_ranked_bar_list(slide, left_items, left=Inches(1.02), top=Inches(2.22), width=Inches(5.15), row_h=Inches(0.43), max_value=float(q5_price["forecast_retail_price_jun2026"].max()), value_fmt="${:.2f}", subtitle="Top June price support")
    add_panel(slide, Inches(6.78), Inches(1.82), Inches(5.75), Inches(4.7), fill=THEME.paper)
    add_ranked_bar_list(slide, right_items, left=Inches(7.02), top=Inches(2.22), width=Inches(5.15), row_h=Inches(0.43), max_value=float(q7s["Profit_Impact_for_50pct_Shipping_Change"].max()), value_fmt="${:,.0f}", subtitle="Top freight sensitivity")
    add_panel(slide, Inches(1.02), Inches(6.02), Inches(11.5), Inches(0.7), fill=THEME.paper)
    add_textbox(slide, Inches(1.26), Inches(6.22), Inches(11.0), Inches(0.18), "The selected cities dominate the price ranking, not the sensitivity ranking. That is why local price support, not freight volatility alone, explains why the recommendation stays stable.", font_size=12, color=THEME.ink, font_name=FONT_BODY, bold=True)


def slide_26(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 26, section="Seasonality")
    add_title(slide, "Prices reach their high point in July")
    season = m["season_raw"]
    conv = season[season["Type"] == "conventional"].sort_values("month")
    org = season[season["Type"] == "organic"].sort_values("month")
    months = [month_name(int(v)) for v in conv["month"].tolist()]
    add_panel(slide, Inches(0.82), Inches(1.9), Inches(7.4), Inches(4.5), fill=THEME.paper)
    add_textbox(slide, Inches(1.08), Inches(2.16), Inches(2.0), Inches(0.18), "MONTHLY PRICE PROFILE", font_size=10, color=THEME.muted, bold=True)
    add_two_series_profile(
        slide,
        left=Inches(1.12),
        top=Inches(2.62),
        width=Inches(6.7),
        height=Inches(3.1),
        months=months,
        series_a=conv["mean_price"].tolist(),
        series_b=org["mean_price"].tolist(),
        label_a="Conventional",
        label_b="Organic",
        y_label="Price",
    )
    add_panel(slide, Inches(8.52), Inches(1.9), Inches(4.06), Inches(4.5), fill=THEME.paper)
    add_stat_chip(slide, Inches(8.8), Inches(2.18), Inches(1.76), Inches(0.96), label="Conventional peak", value=m["seasonality"]["conventional"]["price_peak"], value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(10.66), Inches(2.18), Inches(1.64), Inches(0.96), label="Organic peak", value=m["seasonality"]["organic"]["price_peak"], value_color=THEME.accent, align=PP_ALIGN.CENTER)
    add_bullets(
        slide,
        Inches(8.8),
        Inches(3.46),
        Inches(3.2),
        Inches(1.65),
        [
            "Both product types peak in July, not during the highest-volume months.",
            "That means the operating plan should switch from service protection to margin protection in summer.",
            "Summer is the cleanest season for monetizing premium markets.",
        ],
        font_size=13,
    )


def slide_27(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 27, section="Seasonality")
    add_title(slide, "Volumes peak earlier and trough in November")
    season = m["season_raw"]
    conv = season[season["Type"] == "conventional"].sort_values("month")
    org = season[season["Type"] == "organic"].sort_values("month")
    months = [month_name(int(v)) for v in conv["month"].tolist()]
    add_panel(slide, Inches(0.82), Inches(1.9), Inches(7.4), Inches(4.5), fill=THEME.paper)
    add_textbox(slide, Inches(1.08), Inches(2.16), Inches(2.2), Inches(0.18), "MONTHLY VOLUME PROFILE", font_size=10, color=THEME.muted, bold=True)
    add_two_series_profile(
        slide,
        left=Inches(1.12),
        top=Inches(2.62),
        width=Inches(6.7),
        height=Inches(3.1),
        months=months,
        series_a=conv["mean_monthly_volume"].tolist(),
        series_b=org["mean_monthly_volume"].tolist(),
        label_a="Conventional",
        label_b="Organic",
        y_label="Volume",
    )
    add_panel(slide, Inches(8.52), Inches(1.9), Inches(4.06), Inches(4.5), fill=THEME.paper)
    add_stat_chip(slide, Inches(8.8), Inches(2.18), Inches(1.76), Inches(0.96), label="Conventional peak", value=m["seasonality"]["conventional"]["volume_peak"], value_color=THEME.primary, align=PP_ALIGN.CENTER)
    add_stat_chip(slide, Inches(10.66), Inches(2.18), Inches(1.64), Inches(0.96), label="Organic peak", value=m["seasonality"]["organic"]["volume_peak"], value_color=THEME.compare, align=PP_ALIGN.CENTER)
    add_bullets(
        slide,
        Inches(8.8),
        Inches(3.46),
        Inches(3.2),
        Inches(1.65),
        [
            "Organic volume peaks in January while conventional peaks in May.",
            "Both soften into November, which is why off-peak demand support matters.",
            "Volume timing and price timing do not line up, creating the duck-curve operating problem.",
        ],
        font_size=13,
    )


def slide_28(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 28, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "Seasonality should change when West Valley pushes volume and when it protects margin")
    add_subtitle(
        slide,
        f"Organic volume peaks in {m['seasonality']['organic']['volume_peak']} while price peaks in {m['seasonality']['organic']['price_peak']}; that gap is the operating lever.",
        top=1.2,
        width=11.6,
    )
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_left = Inches(0.75)
    month_top = Inches(1.9)
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
    add_panel(slide, Inches(0.78), Inches(2.78), Inches(11.82), Inches(3.1), fill=THEME.paper)
    headers = [("Operating stance", 1.65), ("Window", 1.45), ("What West Valley should do", 5.0), ("Why it matters", 3.1)]
    x = Inches(1.0)
    for label, width in headers:
        add_textbox(slide, x, Inches(3.02), Inches(width), Inches(0.16), label.upper(), font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
        x += Inches(width + 0.16)
    rows = [
        ("Push volume", "Jan to May", "Prioritize service, retailer availability, and clean flow while the market is naturally absorbing more units.", "This is the best window to prove service quality before summer pricing peaks.", THEME.primary),
        ("Protect margin", "Jul to Sep", "Hold pricing discipline and allocate the strongest fruit to the highest-paying pilot markets.", "Price support is strongest here, so margin capture matters more than raw throughput.", THEME.accent),
        ("Stimulate demand", "Nov to Feb", "Use promotions, alternate channels, and tighter inventory planning when both types soften.", "Low-demand months require commercial support so the pilot does not confuse seasonality with weak economics.", THEME.compare),
    ]
    for idx, row in enumerate(rows):
        top = Inches(3.38 + idx * 0.8)
        band = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(1.0), top, Inches(1.42), Inches(0.58))
        band.fill.solid()
        band.fill.fore_color.rgb = rgb(row[4])
        band.line.color.rgb = rgb(row[4])
        add_textbox(slide, Inches(1.08), top + Inches(0.13), Inches(1.24), Inches(0.18), row[0], font_size=12, color=THEME.paper, font_name=FONT_HEAD, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, Inches(2.68), top + Inches(0.08), Inches(1.25), Inches(0.4), row[1], font_size=14, color=row[4], font_name=FONT_HEAD, bold=True)
        add_textbox(slide, Inches(4.12), top + Inches(0.05), Inches(4.72), Inches(0.46), row[2], font_size=12, color=THEME.ink)
        add_textbox(slide, Inches(9.2), top + Inches(0.05), Inches(2.95), Inches(0.46), row[3], font_size=12, color=THEME.ink)
    add_textbox(slide, Inches(0.82), Inches(6.18), Inches(11.1), Inches(0.22), "Management implication: the pilot should be judged against the right seasonal job each month, not against a flat annual operating assumption.", font_size=12, color=THEME.muted, font_name=FONT_BODY)


def slide_29(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 29, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "A monthly operating calendar can convert seasonality from risk into advantage")
    add_textbox(slide, Inches(0.82), Inches(1.25), Inches(1.55), Inches(0.16), "READING GUIDE", font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
    legend_items = [("Service", THEME.primary), ("Protect margin", THEME.accent), ("Stimulate demand", THEME.compare), ("Rebalance / reset", THEME.stress)]
    for idx, (label, color) in enumerate(legend_items):
        x = Inches(2.12 + idx * 2.45)
        dot = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, x, Inches(1.22), Inches(0.18), Inches(0.18))
        dot.fill.solid()
        dot.fill.fore_color.rgb = rgb(color)
        dot.line.color.rgb = rgb(color)
        add_textbox(slide, x + Inches(0.26), Inches(1.18), Inches(1.9), Inches(0.18), label, font_size=10, color=THEME.ink, font_name=FONT_BODY)
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
    add_panel(slide, Inches(0.68), Inches(1.58), Inches(12.06), Inches(4.16), fill=THEME.paper)
    table = slide.shapes.add_table(4, 13, Inches(0.82), Inches(1.86), Inches(11.72), Inches(3.45)).table
    table.columns[0].width = Inches(1.65)
    for col in range(1, 13):
        table.columns[col].width = Inches(0.79)
    for row in range(4):
        table.rows[row].height = Inches(0.84)
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
                    run.font.size = Pt(10.5)
                    run.font.bold = True
                    run.font.color.rgb = rgb(THEME.paper if cell.fill.fore_color.rgb in dark_fills else THEME.ink)
    add_stat_band(
        slide,
        Inches(0.82),
        Inches(5.98),
        Inches(11.72),
        Inches(0.78),
        [
            ("Jan to May", "Service + flow", "Use the market's natural volume strength to prove availability and execution."),
            ("Jul to Sep", "Margin season", "Allocate tightly and protect price while summer support is strongest."),
            ("Nov to Feb", "Demand support", "Stimulate consumption and tighten inventory in the softest months."),
        ],
        highlight_idx=1,
    )


def slide_30(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 30, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "Growers need flexible contracts, better cold-chain readiness, and alternate lanes")
    add_subtitle(slide, "Supply-side seasonality discipline should be built into contracts and execution rules before the pilot scales.", top=1.2, width=11.2)
    add_panel(slide, Inches(0.82), Inches(1.72), Inches(11.8), Inches(4.75), fill=THEME.paper)
    headers = [("Lever", 1.85), ("How it should work", 3.0), ("Critical operating move", 4.0), ("Why it matters", 2.15)]
    x = Inches(1.04)
    for label, width in headers:
        add_textbox(slide, x, Inches(1.98), Inches(width), Inches(0.16), label.upper(), font_size=10, color=THEME.muted, font_name=FONT_BODY, bold=True)
        x += Inches(width + 0.14)
    rows = [
        ("Contract tiers", "Base + flex volume", "Lock a stable base commitment, then layer in seasonal flex volume so supply can expand without year-round overcommitment.", "Prevents the pilot from buying peak-season optionality with permanent fixed cost.", THEME.primary),
        ("Cold-chain readiness", "Protect service", "Tighten transit monitoring, storage discipline, and receiving checks during the months when flow is highest.", "Spoilage and service misses can erase good city economics faster than freight swings do.", THEME.compare),
        ("Alternate lanes", "Reduce disruption", "Pre-qualify backup carriers and routes before the peak season so lane shocks do not force reactive reallocations.", "The pilot should never have to choose between service and margin because a lane fails.", THEME.stress),
    ]
    for idx, row in enumerate(rows):
        top = Inches(2.32 + idx * 1.17)
        rail = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(1.02), top, Inches(1.55), Inches(0.82))
        rail.fill.solid()
        rail.fill.fore_color.rgb = rgb(row[4])
        rail.line.color.rgb = rgb(row[4])
        add_textbox(slide, Inches(1.12), top + Inches(0.2), Inches(1.34), Inches(0.22), row[0], font_size=14, color=THEME.paper, font_name=FONT_HEAD, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, Inches(2.86), top + Inches(0.12), Inches(2.6), Inches(0.48), row[1], font_size=15, color=row[4], font_name=FONT_HEAD, bold=True)
        add_textbox(slide, Inches(5.92), top + Inches(0.08), Inches(3.8), Inches(0.62), row[2], font_size=12, color=THEME.ink)
        add_textbox(slide, Inches(10.12), top + Inches(0.08), Inches(1.95), Inches(0.62), row[3], font_size=12, color=THEME.ink)


def slide_31(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 31, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "Trade associations should smooth demand in off-peak months")
    add_subtitle(slide, "Demand-side support should be strongest in the softest months, not wasted when the market is already doing the work.", top=1.2, width=11.3)
    add_panel(slide, Inches(0.82), Inches(1.8), Inches(7.3), Inches(4.72), fill=THEME.paper)
    add_textbox(slide, Inches(1.04), Inches(2.05), Inches(2.2), Inches(0.2), "OFF-PEAK PLAYBOOK", font_size=11, color=THEME.muted, font_name=FONT_BODY, bold=True)
    plays = [
        ("1", "Consumer messaging", "Push recipes, convenience, and health messaging when avocados are less visible in routine weekly shopping.", THEME.primary),
        ("2", "Channel mix", "Lean harder on food-service, prepared foods, and institutional channels when retail pull weakens.", THEME.compare),
        ("3", "Promo timing", "Use the strongest promo calendar in soft months rather than discounting away naturally strong summer demand.", THEME.accent),
        ("4", "Trade support", "Coordinate retailer calendars with association campaigns so promotions follow the seasonal operating plan.", THEME.stress),
    ]
    for idx, play in enumerate(plays):
        y = Inches(2.42 + idx * 0.92)
        chip = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, Inches(1.1), y, Inches(0.34), Inches(0.34))
        chip.fill.solid()
        chip.fill.fore_color.rgb = rgb(play[3])
        chip.line.color.rgb = rgb(play[3])
        add_textbox(slide, Inches(1.15), y + Inches(0.08), Inches(0.22), Inches(0.14), play[0], font_size=11, color=THEME.paper, font_name=FONT_BODY, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, Inches(1.56), y - Inches(0.02), Inches(2.0), Inches(0.18), play[1].upper(), font_size=10, color=THEME.muted, bold=True)
        add_textbox(slide, Inches(1.56), y + Inches(0.18), Inches(5.75), Inches(0.42), play[2], font_size=12, color=THEME.ink)
    add_panel(slide, Inches(8.42), Inches(1.8), Inches(4.2), Inches(4.72), fill=THEME.panel)
    add_textbox(slide, Inches(8.68), Inches(2.05), Inches(2.4), Inches(0.2), "WHERE TO PUSH HARDER", font_size=11, color=THEME.muted, bold=True)
    add_stat_chip(slide, Inches(8.68), Inches(2.42), Inches(1.8), Inches(0.9), label="Softest months", value="Nov to Feb", value_color=THEME.compare)
    add_stat_chip(slide, Inches(10.55), Inches(2.42), Inches(1.75), Inches(0.9), label="Goal", value="Protect demand", value_color=THEME.accent)
    add_bullets(
        slide,
        Inches(8.7),
        Inches(3.55),
        Inches(3.45),
        Inches(1.7),
        [
            "Do not confuse seasonal softness with weak pilot economics.",
            "Use the same monthly calendar across retailers, channels, and trade campaigns.",
            "Measure promotional lift separately from baseline reorder demand.",
        ],
        font_size=13,
        color=THEME.ink,
    )


def slide_32(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 32, section="Seasonality")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.accent)
    add_title(slide, "A shared monthly S&OP cadence can align growers, West Valley, and retail partners")
    add_subtitle(slide, "The operating model is stronger when the same monthly forum translates market signals into volume, routing, and promotion decisions.", top=1.2, width=11.5)
    stakeholder_cards = [
        ("Growers", "Supply commitment", "Provide base volume, flex capacity, and harvest timing updates.", THEME.primary),
        ("West Valley", "Control tower", "Convert price, freight, and demand signals into city allocation decisions.", THEME.compare),
        ("Retailers", "Demand signal", "Feed promo calendars, replenishment risk, and reorder visibility into the review.", THEME.accent),
    ]
    for idx, card in enumerate(stakeholder_cards):
        add_card(slide, Inches(0.85 + idx * 4.08), Inches(1.86), Inches(3.3), Inches(1.62), header=card[0], metric=card[1], body=card[2], metric_color=card[3])
    add_panel(slide, Inches(2.05), Inches(3.82), Inches(9.25), Inches(1.16), fill=THEME.paper)
    steps = [("1", "Forecast demand"), ("2", "Lock commitments"), ("3", "Allocate by city"), ("4", "Review margin + service")]
    for idx, step in enumerate(steps):
        x = Inches(2.38 + idx * 2.23)
        bubble = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, x, Inches(4.1), Inches(0.32), Inches(0.32))
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = rgb(THEME.primary if idx in {0, 3} else THEME.compare if idx == 1 else THEME.accent)
        bubble.line.color.rgb = rgb(THEME.primary if idx in {0, 3} else THEME.compare if idx == 1 else THEME.accent)
        add_textbox(slide, x + Inches(0.03), Inches(4.18), Inches(0.24), Inches(0.12), step[0], font_size=10, color=THEME.paper, font_name=FONT_BODY, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, x + Inches(0.42), Inches(4.1), Inches(1.6), Inches(0.18), step[1], font_size=12, color=THEME.primary, font_name=FONT_HEAD, bold=True)
        if idx < len(steps) - 1:
            line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x + Inches(1.85), Inches(4.26), x + Inches(2.17), Inches(4.26))
            line.line.color.rgb = rgb(THEME.line)
            line.line.width = Pt(1.8)
    add_stat_band(
        slide,
        Inches(0.84),
        Inches(5.32),
        Inches(11.75),
        Inches(0.98),
        [
            ("Cadence", "Monthly", "Run the review monthly, not quarterly, because the volume-price gap changes within the season."),
            ("Decision output", "Commit + allocate", "Use the same forum to update grower commitments, routing, and retailer timing."),
            ("Success signal", "Margin + service", "The forum should improve realized margin without breaking fill rate or freshness."),
        ],
        highlight_idx=0,
    )


def slide_33(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 33, section="Implementation")
    add_title(slide, "Launch the 2026 pilot first, then scale what the market confirms")
    add_subtitle(slide, "Treat the first year as a live test of economics, service, and demand quality rather than a commitment to broad expansion.", top=1.2, width=11.6)

    add_panel(slide, Inches(0.82), Inches(1.75), Inches(8.4), Inches(4.85), fill=THEME.paper)
    add_textbox(slide, Inches(1.0), Inches(1.98), Inches(2.0), Inches(0.2), "ROLLOUT ROADMAP", font_size=11, color=THEME.muted, bold=True)
    phases = [
        ("2026", "Pilot", "Launch the five-city test and prove realized margin, fill rate, and spoilage control.", "What must be true: city economics hold in live execution.", THEME.primary),
        ("2027", "Expand selectively", "Add retailer doors only in markets where reorder behavior and service levels remain strong.", "What must be true: economics survive broader coverage.", THEME.compare),
        ("2028", "Optimize system", "Tighten grower contracts, allocation logic, and seasonal playbooks around what the pilot confirms.", "What must be true: process gains are repeatable.", THEME.accent),
    ]
    for idx, phase in enumerate(phases):
        top = Inches(2.35 + idx * 1.4)
        rail = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(1.0), top, Inches(1.05), Inches(0.74))
        rail.fill.solid()
        rail.fill.fore_color.rgb = rgb(phase[4])
        rail.line.color.rgb = rgb(phase[4])
        add_textbox(slide, Inches(1.02), top + Inches(0.14), Inches(1.0), Inches(0.2), phase[0], font_size=18, color=THEME.paper, font_name=FONT_HEAD, bold=True, align=PP_ALIGN.CENTER)

        lane = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(2.28), top, Inches(4.55), Inches(0.74))
        lane.fill.solid()
        lane.fill.fore_color.rgb = rgb(THEME.bg)
        lane.line.color.rgb = rgb(THEME.line)
        add_textbox(slide, Inches(2.48), top + Inches(0.1), Inches(4.1), Inches(0.18), phase[1].upper(), font_size=10, color=THEME.muted, bold=True)
        add_textbox(slide, Inches(2.48), top + Inches(0.3), Inches(4.1), Inches(0.28), phase[2], font_size=13, color=THEME.ink)

        check = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(6.98), top, Inches(1.9), Inches(0.74))
        check.fill.solid()
        check.fill.fore_color.rgb = rgb(THEME.panel)
        check.line.color.rgb = rgb(phase[4])
        check.line.width = Pt(1.2)
        add_textbox(slide, Inches(7.13), top + Inches(0.1), Inches(1.62), Inches(0.44), phase[3], font_size=11, color=THEME.ink)

    add_panel(slide, Inches(9.52), Inches(1.75), Inches(3.05), Inches(4.85), fill=THEME.panel)
    add_textbox(slide, Inches(9.78), Inches(1.98), Inches(2.2), Inches(0.2), "SCALE ONLY IF", font_size=11, color=THEME.muted, bold=True)
    gates = [
        ("Margin", "Realized margin clears the base-case plan after freight and spoilage."),
        ("Service", "Fill rate stays credible through seasonal peaks and lane pressure."),
        ("Demand", "Retailers reorder because pilot demand is repeatable, not promotional noise."),
    ]
    for idx, gate in enumerate(gates):
        y = Inches(2.45 + idx * 1.2)
        dot = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, Inches(9.82), y, Inches(0.28), Inches(0.28))
        dot.fill.solid()
        dot.fill.fore_color.rgb = rgb(THEME.accent if idx == 2 else THEME.primary if idx == 0 else THEME.compare)
        dot.line.color.rgb = rgb(THEME.accent if idx == 2 else THEME.primary if idx == 0 else THEME.compare)
        add_textbox(slide, Inches(10.18), y - Inches(0.02), Inches(1.9), Inches(0.18), gate[0].upper(), font_size=10, color=THEME.muted, bold=True)
        add_textbox(slide, Inches(10.18), y + Inches(0.18), Inches(2.0), Inches(0.52), gate[1], font_size=12, color=THEME.ink)


def slide_34(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 34, section="Implementation")
    add_title(slide, "Pilot KPIs should focus on margin, service, spoilage, and repeat orders")
    add_panel(slide, Inches(0.82), Inches(1.78), Inches(4.0), Inches(4.75), fill=THEME.paper)
    add_textbox(slide, Inches(1.04), Inches(2.02), Inches(1.8), Inches(0.2), "HEALTH CHECK", font_size=11, color=THEME.muted, bold=True)
    hero_kpis = [
        ("Gross margin", "Primary proof that price support and cost discipline hold.", THEME.primary),
        ("Fill rate", "Primary proof that service can scale in live operation.", THEME.compare),
        ("Reorder rate", "Primary proof that demand is recurring, not one-off.", THEME.accent),
    ]
    for idx, item in enumerate(hero_kpis):
        y = Inches(2.45 + idx * 1.25)
        bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(1.05), y, Inches(0.22), Inches(0.7))
        bar.fill.solid()
        bar.fill.fore_color.rgb = rgb(item[2])
        bar.line.color.rgb = rgb(item[2])
        add_textbox(slide, Inches(1.42), y + Inches(0.02), Inches(1.9), Inches(0.18), item[0].upper(), font_size=10, color=THEME.muted, bold=True)
        add_textbox(slide, Inches(1.42), y + Inches(0.22), Inches(3.0), Inches(0.42), item[1], font_size=13, color=THEME.ink)

    add_panel(slide, Inches(5.08), Inches(1.78), Inches(7.45), Inches(4.75), fill=THEME.paper)
    add_textbox(slide, Inches(5.32), Inches(2.02), Inches(2.5), Inches(0.2), "PILOT SCORECARD", font_size=11, color=THEME.muted, bold=True)
    table = slide.shapes.add_table(7, 3, Inches(5.32), Inches(2.35), Inches(6.95), Inches(3.78)).table
    headers = ["KPI", "Why it matters", "Cadence / owner"]
    rows = [
        ("Realized gross margin", "Confirms whether forecast economics survive live execution.", "Weekly / finance"),
        ("Freight per unit", "Shows whether routing and carrier discipline are improving.", "Weekly / logistics"),
        ("Fill rate", "Measures retailer execution quality during seasonal peaks.", "Weekly / operations"),
        ("Spoilage rate", "Captures cold-chain and freshness failures directly.", "Weekly / operations"),
        ("Reorder rate", "Tests whether demand is repeatable beyond launch.", "Monthly / commercial"),
        ("Forecast accuracy", "Shows whether monthly S&OP is improving allocation decisions.", "Monthly / planning"),
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
    widths = [2.0, 3.55, 1.4]
    for idx, width in enumerate(widths):
        table.columns[idx].width = Inches(width)
    for row_idx, row in enumerate(table.rows):
        row.height = Inches(0.54)
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(11)
                    run.font.bold = row_idx == 0
                    run.font.color.rgb = rgb(THEME.paper if row_idx == 0 else THEME.ink)


def slide_35(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 35, section="Implementation")
    add_title(slide, "Expansion should follow stage gates, not automatic geography growth")
    add_subtitle(slide, "The model is strong enough to choose where to test, but scale should still depend on pilot evidence rather than assumed allocation precision.", top=1.2, width=11.7)
    stages = [
        ("1", "Pilot live", "Launch and collect clean economics by city.", THEME.primary),
        ("2", "Economics verified", "Confirm realized margin and freight per unit.", THEME.compare),
        ("3", "Service verified", "Confirm fill rate, spoilage control, and reorder behavior.", THEME.primary_soft),
        ("4", "Scale selectively", "Expand only where pilot evidence remains strong.", THEME.accent),
    ]
    for idx, stage in enumerate(stages):
        x = Inches(0.75 + idx * 3.08)
        top = Inches(2.25)
        band = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, top, Inches(2.45), Inches(0.42))
        band.fill.solid()
        band.fill.fore_color.rgb = rgb(stage[3])
        band.line.color.rgb = rgb(stage[3])
        add_textbox(slide, x + Inches(0.06), top + Inches(0.08), Inches(2.3), Inches(0.18), f"STEP {stage[0]}".upper(), font_size=11, color=THEME.paper, bold=True, align=PP_ALIGN.CENTER)

        box = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, Inches(2.78), Inches(2.45), Inches(1.85))
        box.fill.solid()
        box.fill.fore_color.rgb = rgb(THEME.paper)
        box.line.color.rgb = rgb(THEME.line)
        add_textbox(slide, x + Inches(0.16), Inches(3.0), Inches(2.1), Inches(0.28), stage[1], font_size=17, color=stage[3], font_name=FONT_HEAD, bold=True)
        add_textbox(slide, x + Inches(0.16), Inches(3.4), Inches(2.1), Inches(0.65), stage[2], font_size=12, color=THEME.ink)
        if idx < len(stages) - 1:
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x + Inches(2.48), Inches(3.68), x + Inches(3.0), Inches(3.68))
            connector.line.color.rgb = rgb(THEME.line)
            connector.line.width = Pt(2.0)

    add_panel(slide, Inches(1.08), Inches(5.05), Inches(10.95), Inches(0.95), fill=THEME.paper)
    add_textbox(slide, Inches(1.28), Inches(5.28), Inches(2.2), Inches(0.16), "WHY THE STAGE GATES MATTER", font_size=10, color=THEME.muted, bold=True)
    add_textbox(slide, Inches(3.25), Inches(5.22), Inches(8.35), Inches(0.3), "They keep West Valley from pretending it can allocate the full 20,000-unit order with exact retailer-level precision before the live pilot proves what actually works.", font_size=14, color=THEME.ink)


def slide_36(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 36, section="Risks")
    add_badge(slide, "Inference", Inches(11.2), Inches(0.28), Inches(1.4), fill=THEME.stress)
    add_title(slide, "The highest-risk threats are freight spikes, import disruptions, and forecast error")
    add_panel(slide, Inches(0.82), Inches(1.75), Inches(7.5), Inches(4.5), fill=THEME.paper)
    v_line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(4.58), Inches(1.98), Inches(4.58), Inches(5.98))
    h_line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(1.1), Inches(4.0), Inches(7.98), Inches(4.0))
    for line in [v_line, h_line]:
        line.line.color.rgb = rgb(THEME.line)
        line.line.width = Pt(1.6)
    add_textbox(slide, Inches(3.5), Inches(1.83), Inches(2.2), Inches(0.2), "High impact", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(3.5), Inches(6.02), Inches(2.2), Inches(0.2), "Low impact", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(0.72), Inches(3.7), Inches(0.9), Inches(0.4), "Low\nprob.", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(8.0), Inches(3.7), Inches(0.9), Inches(0.4), "High\nprob.", font_size=11, color=THEME.muted, bold=True, align=PP_ALIGN.CENTER)

    risks = [
        ("Freight spikes", 6.65, 2.5, THEME.stress),
        ("Import disruption", 5.0, 2.2, THEME.stress),
        ("Forecast error", 6.0, 3.15, THEME.accent),
        ("Retailer uptake", 5.85, 4.35, THEME.compare),
        ("Spoilage", 4.45, 4.15, THEME.compare),
        ("Labor pressure", 3.25, 3.05, THEME.primary_soft),
    ]
    for label, x, y, color in risks:
        bubble = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, Inches(x), Inches(y), Inches(0.82), Inches(0.82))
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = rgb(color)
        bubble.line.color.rgb = rgb(color)
        add_textbox(slide, Inches(x - 0.3), Inches(y + 0.84), Inches(1.45), Inches(0.4), label, font_size=11, color=THEME.ink, align=PP_ALIGN.CENTER)

    add_panel(slide, Inches(8.66), Inches(1.75), Inches(3.86), Inches(4.5), fill=THEME.panel)
    add_textbox(slide, Inches(8.92), Inches(1.98), Inches(2.4), Inches(0.2), "WATCHLIST", font_size=11, color=THEME.muted, bold=True)
    responses = [
        ("Freight spikes", "Pre-book core lanes and keep alternates warm before the peak season hits."),
        ("Import disruption", "Use flexible grower commitments and staggered sourcing windows."),
        ("Forecast error", "Re-run allocation decisions monthly using realized pilot demand."),
    ]
    for idx, response in enumerate(responses):
        y = Inches(2.42 + idx * 1.22)
        add_textbox(slide, Inches(8.95), y, Inches(2.8), Inches(0.18), response[0].upper(), font_size=10, color=THEME.stress if idx == 0 else THEME.primary if idx == 1 else THEME.compare, bold=True)
        add_textbox(slide, Inches(8.95), y + Inches(0.2), Inches(3.0), Inches(0.48), response[1], font_size=12, color=THEME.ink)


def slide_37(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 37, section="Risks")
    add_title(slide, "Each major risk has a specific operational countermeasure")
    add_subtitle(slide, "The deck is stronger when every major threat already has an operational response and clear owner.", top=1.2, width=11.4)
    table = slide.shapes.add_table(6, 4, Inches(0.72), Inches(1.85), Inches(11.85), Inches(4.15)).table
    headers = ["Risk", "Trigger", "Countermeasure", "Owner"]
    rows = [
        ("Freight spikes", "Peak-season lane tightness", "Lock core carrier capacity and maintain alternate lanes.", "Logistics lead"),
        ("Import or supply disruption", "Supply interruption or customs delay", "Use flexible grower contracts and staggered commitments.", "Sourcing lead"),
        ("Spoilage / service failures", "Shrink or weak fill-rate trend", "Tighten cold-chain controls and receiving discipline.", "Operations lead"),
        ("Forecast error", "Demand misses by city", "Run monthly S&OP and reallocate by city using realized demand.", "Commercial lead"),
        ("Retailer uptake risk", "Weak reorder behavior", "Require stage gates before expanding beyond the pilot.", "General manager"),
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
    widths = [2.1, 2.45, 5.05, 2.25]
    for idx, width in enumerate(widths):
        table.columns[idx].width = Inches(width)
    for row in table.rows:
        row.height = Inches(0.69)
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(11)
                    run.font.bold = row == table.rows[0]
                    run.font.color.rgb = rgb(THEME.paper if row == table.rows[0] else THEME.ink)
    add_panel(slide, Inches(0.95), Inches(6.18), Inches(10.9), Inches(0.62), fill=THEME.paper)
    add_textbox(slide, Inches(1.15), Inches(6.38), Inches(10.5), Inches(0.16), "Operating principle: the pilot should never carry an unmanaged risk; every major threat must already have a trigger, action, and owner before scale decisions are made.", font_size=12, color=THEME.ink)


def slide_38(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 38, section="Limitations")
    add_badge(slide, "Caveat", Inches(11.28), Inches(0.28), Inches(1.28), fill=THEME.stress)
    add_title(slide, "The current model is strong enough for city selection but not yet for exact allocation")
    left_items = [
        "The cleaned dataset resolves to 40 city markets even though the case text references 41 metro regions.",
        "The model is useful for choosing where to test because it compares cities on a consistent 20,000-unit scorecard.",
        "The ranking is resilient: all 40 cities remain profitable even at +50% shipping, so this is an optimization problem.",
    ]
    right_items = [
        "2025 is partial-year data only and June 2025 retail price is used as the simple proxy for June 2026 retail price.",
        "The model does not include spoilage shrink, retailer-level demand curves, or a fully expanded operating cost stack.",
        "That means the deck can defend city selection today, but not an exact retailer-by-retailer allocation plan yet.",
    ]
    add_panel(slide, Inches(0.8), Inches(1.9), Inches(5.7), Inches(3.7), fill=THEME.paper)
    add_panel(slide, Inches(6.85), Inches(1.9), Inches(5.7), Inches(3.7), fill=THEME.paper)
    add_textbox(slide, Inches(1.0), Inches(2.12), Inches(2.3), Inches(0.25), "What we can defend now", font_size=15, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(slide, Inches(1.0), Inches(2.45), Inches(5.1), Inches(2.85), left_items, font_size=14)
    add_textbox(slide, Inches(7.05), Inches(2.12), Inches(2.5), Inches(0.25), "What still needs more data", font_size=15, color=THEME.stress, font_name=FONT_HEAD, bold=True)
    add_bullets(slide, Inches(7.05), Inches(2.45), Inches(5.1), Inches(2.85), right_items, font_size=14)
    add_panel(slide, Inches(1.1), Inches(5.95), Inches(10.95), Inches(0.72), fill=THEME.panel)
    add_textbox(slide, Inches(1.3), Inches(6.18), Inches(2.2), Inches(0.16), "NEXT DATA TO COLLECT", font_size=10, color=THEME.muted, bold=True)
    add_textbox(slide, Inches(3.2), Inches(6.12), Inches(8.45), Inches(0.22), "Pilot reorder behavior, spoilage by lane, and retailer-level demand response would let West Valley move from city selection to exact allocation logic.", font_size=13, color=THEME.ink)


def slide_39(prs: Presentation, m: dict[str, object]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 39, section="Conclusion")
    add_title(slide, "Launch the 5-city pilot, then scale only where the pilot confirms the model")
    add_panel(slide, Inches(0.78), Inches(1.78), Inches(7.0), Inches(4.85), fill=THEME.paper)
    add_textbox(slide, Inches(1.02), Inches(2.04), Inches(2.6), Inches(0.2), "FINAL RECOMMENDATION", font_size=11, color=THEME.muted, font_name=FONT_BODY, bold=True)
    add_textbox(slide, Inches(1.02), Inches(2.36), Inches(5.7), Inches(0.72), "Launch Seattle, Boise, Portland, Spokane, and San Diego first.", font_size=26, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_textbox(slide, Inches(1.02), Inches(3.1), Inches(5.95), Inches(0.48), "The recommendation is robust because premium city pricing stays stronger than modeled freight swings and seasonality can be managed operationally.", font_size=15, color=THEME.ink)
    for city, x, width in [("Seattle", 1.02, 1.16), ("Boise", 2.28, 1.04), ("Portland", 3.42, 1.22), ("Spokane", 4.74, 1.17), ("San Diego", 6.01, 1.39)]:
        add_badge(slide, city, Inches(x), Inches(3.88), Inches(width), fill=THEME.primary, text_color=THEME.paper)
    for idx, (label, value, color) in enumerate(
        [
            ("Avg profit", fmt_money(m["top5_profit_avg"]), THEME.primary),
            ("Top-5 margin", fmt_pct(m["top5_margin_avg"]), THEME.compare),
            ("Freight result", "Same 5 cities", THEME.accent),
        ]
    ):
        add_stat_chip(slide, Inches(1.0 + idx * 2.06), Inches(4.72), Inches(1.84), Inches(1.06), label=label, value=value, value_color=color)

    proof_cards = [
        ("Economics", fmt_money(m["top5_profit_avg"]) + " avg profit", "The top five produce a materially stronger average profit than the next tier.", THEME.primary),
        ("Resilience", "Same 5 cities", "The ranking is unchanged in the base, +50%, and -50% freight cases.", THEME.compare),
        ("Operating discipline", "Pilot before scale", "Run the pilot first, then expand only where realized margin and service hold.", THEME.accent),
    ]
    for idx, card in enumerate(proof_cards):
        add_card(slide, Inches(8.15), Inches(1.94 + idx * 1.48), Inches(4.45), Inches(1.26), header=card[0], metric=card[1], body=card[2], metric_color=card[3])
    add_panel(slide, Inches(8.15), Inches(6.04), Inches(4.45), Inches(0.62), fill=THEME.bg, line=THEME.line)
    add_textbox(slide, Inches(8.34), Inches(6.2), Inches(4.0), Inches(0.18), "Next step: launch, measure realized economics, and scale selectively rather than assuming the full model is already proven.", font_size=11, color=THEME.ink)


def slide_40(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, 40, section="Appendix", footer="Sources and backup")
    add_title(slide, "Backup map: sources, assumptions, and appendix exhibits")
    add_panel(slide, Inches(0.78), Inches(1.82), Inches(4.0), Inches(4.6))
    add_panel(slide, Inches(4.96), Inches(1.82), Inches(3.38), Inches(4.6))
    add_panel(slide, Inches(8.52), Inches(1.82), Inches(4.0), Inches(4.6))
    add_textbox(slide, Inches(1.0), Inches(2.08), Inches(2.6), Inches(0.24), "Primary sources", font_size=15, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(
        slide,
        Inches(1.0),
        Inches(2.45),
        Inches(3.5),
        Inches(3.45),
        [
            "case_full.md and case_context.md",
            "case_comp_data.csv",
            "outputs/question_1.md through outputs/question_9.md",
            "q5 to q7 profitability scenario CSVs",
            "q8 seasonality CSVs and charts",
        ],
        font_size=13,
    )

    add_textbox(slide, Inches(5.18), Inches(2.08), Inches(2.4), Inches(0.24), "Core assumptions", font_size=15, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(
        slide,
        Inches(5.18),
        Inches(2.45),
        Inches(2.92),
        Inches(3.45),
        [
            "20,000-unit comparable city scorecards",
            "June 2025 retail price used as June 2026 proxy",
            "Wholesale price modeled at 40% of retail",
            "$0.20 acquisition cost per avocado",
            "Shipping = $1,500 fixed + $50 per 100 miles",
        ],
        font_size=13,
    )
    add_textbox(slide, Inches(8.75), Inches(2.08), Inches(2.8), Inches(0.24), "Backup exhibits available", font_size=15, color=THEME.primary, font_name=FONT_HEAD, bold=True)
    add_bullets(
        slide,
        Inches(8.75),
        Inches(2.45),
        Inches(3.45),
        Inches(3.45),
        [
            "Winner matrix and city trend lines",
            "Growth/share bridge and elasticity visuals",
            "Selection matrix, frontier zoom, and freight sensitivity",
            "Seasonality price and volume charts",
            "Model caveats and implementation stage gates",
        ],
        font_size=13,
    )
    add_textbox(slide, Inches(0.98), Inches(6.64), Inches(11.0), Inches(0.24), "Use this appendix to answer questions on data scope, scenario assumptions, seasonality, or why the five-city recommendation stays stable under freight stress.", font_size=12, color=THEME.muted, font_name=FONT_BODY)


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
    slide_6(prs, metrics)
    slide_7(prs, metrics)
    slide_8(prs, metrics)
    slide_9(prs, metrics)
    slide_10(prs, metrics)
    slide_11(prs, metrics)
    slide_12(prs, metrics)
    slide_13(prs)
    slide_14(prs, metrics)
    slide_15(prs, metrics)
    slide_16(prs, metrics)
    slide_17(prs, metrics)
    slide_18(prs, metrics)
    slide_19(prs, metrics)
    slide_20(prs, metrics)
    slide_21(prs, metrics)
    slide_22(prs, metrics)
    slide_23(prs, metrics)
    slide_24(prs, metrics)
    slide_25(prs, metrics)
    slide_26(prs, metrics)
    slide_27(prs, metrics)
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
