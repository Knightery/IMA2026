#!/usr/bin/env python3
"""
Visual QA for PowerPoint slide overlap and crowding.

This script is built for deck QA on Windows with PowerPoint installed.
It opens a PPTX through PowerPoint COM, inspects rendered shape geometry,
and flags likely layout problems such as:

- text overlapping other text
- text overlapping graphics or charts
- peer shapes colliding or crowding each other
- shapes extending off the slide
- possible chart-label crowding inside chart/image regions (heuristic)

It can also export slide PNGs and annotated review images.

Example:
    python slides/visual_qa_overlap.py slides/case-deck.pptx

Output:
    slides/visual_qa/<deck_name>/
        overlap_report.json
        overlap_report.md
        exported_slides/
        annotated/
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
from PIL import Image, ImageDraw
import win32com.client  # type: ignore[import-untyped]


PNG_SAVE_FORMAT = 18
MIN_INTERSECTION_AREA = 18.0
MIN_SHAPE_OVERLAP_RATIO = 0.18
MIN_TEXT_OVERLAP_RATIO = 0.12
NEAR_GAP_THRESHOLD = 1.0
EDGE_TOLERANCE = 5.0


@dataclass(frozen=True)
class Rect:
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    @property
    def area(self) -> float:
        return max(self.width, 0.0) * max(self.height, 0.0)

    def intersection(self, other: "Rect") -> "Rect | None":
        left = max(self.left, other.left)
        top = max(self.top, other.top)
        right = min(self.right, other.right)
        bottom = min(self.bottom, other.bottom)
        if right <= left or bottom <= top:
            return None
        return Rect(left, top, right - left, bottom - top)

    def intersection_area(self, other: "Rect") -> float:
        inter = self.intersection(other)
        return inter.area if inter else 0.0

    def contains(self, other: "Rect", margin: float = 0.0) -> bool:
        return (
            self.left - margin <= other.left
            and self.top - margin <= other.top
            and self.right + margin >= other.right
            and self.bottom + margin >= other.bottom
        )

    def expand(self, amount: float) -> "Rect":
        return Rect(
            self.left - amount,
            self.top - amount,
            self.width + amount * 2.0,
            self.height + amount * 2.0,
        )

    def to_list(self) -> list[float]:
        return [
            round(self.left, 2),
            round(self.top, 2),
            round(self.width, 2),
            round(self.height, 2),
        ]


@dataclass(frozen=True)
class ShapeInfo:
    slide_index: int
    shape_id: int
    name: str
    kind: str
    bounds: Rect
    text_bounds: Rect | None
    text: str
    z_order: int
    is_container: bool
    is_decorative: bool

    @property
    def effective_bounds(self) -> Rect:
        if self.text_bounds and self.text:
            return self.text_bounds
        return self.bounds


@dataclass(frozen=True)
class Issue:
    slide_index: int
    severity: str
    issue_type: str
    message: str
    box: Rect | None = None
    shape_ids: tuple[int, ...] = ()
    shape_names: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["box"] = None if self.box is None else self.box.to_list()
        return payload


def safe_text(text: str, limit: int = 80) -> str:
    clean = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."


def shape_kind(shape) -> str:
    try:
        if getattr(shape, "HasChart", False):
            return "chart"
    except Exception:
        pass
    try:
        if getattr(shape, "HasTable", False):
            return "table"
    except Exception:
        pass
    type_id = getattr(shape, "Type", None)
    if type_id == 13:
        return "picture"
    if type_id == 17:
        return "textbox"
    if type_id == 9:
        return "line"
    if type_id == 10:
        return "connector"
    if type_id == 6:
        return "group"
    if type_id == 1:
        return "autoshape"
    return f"type_{type_id}"


def collect_shape_text(shape) -> tuple[str, Rect | None]:
    try:
        if not shape.HasTextFrame:
            return "", None
        text_frame = shape.TextFrame2
        if not text_frame.HasText:
            return "", None
        text_range = text_frame.TextRange
        text = text_range.Text or ""
        box = Rect(
            float(text_range.BoundLeft),
            float(text_range.BoundTop),
            float(text_range.BoundWidth),
            float(text_range.BoundHeight),
        )
        return text, box
    except Exception:
        return "", None


def is_decorative(shape_kind_name: str, bounds: Rect, slide_width: float, slide_height: float, text: str) -> bool:
    if text.strip():
        return False
    if shape_kind_name in {"line", "connector"}:
        return True
    if bounds.width <= 2.0 or bounds.height <= 2.0:
        return True
    if bounds.width >= slide_width * 0.95 and bounds.height <= 10.0:
        return True
    if bounds.height >= slide_height * 0.95 and bounds.width <= 10.0:
        return True
    return False


def is_container(shape_kind_name: str, bounds: Rect, slide_width: float, slide_height: float, text: str) -> bool:
    if text.strip():
        return False
    area_ratio = bounds.area / (slide_width * slide_height)
    if area_ratio >= 0.55:
        return True
    if shape_kind_name in {"autoshape", "picture"} and area_ratio >= 0.18:
        return True
    return False


def collect_shapes_from_slide(slide, slide_index: int, slide_width: float, slide_height: float) -> list[ShapeInfo]:
    shapes: list[ShapeInfo] = []
    for idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(idx)
        bounds = Rect(float(shape.Left), float(shape.Top), float(shape.Width), float(shape.Height))
        text, text_bounds = collect_shape_text(shape)
        kind = shape_kind(shape)
        shapes.append(
            ShapeInfo(
                slide_index=slide_index,
                shape_id=idx,
                name=str(shape.Name),
                kind=kind,
                bounds=bounds,
                text_bounds=text_bounds,
                text=text,
                z_order=int(getattr(shape, "ZOrderPosition", idx)),
                is_container=is_container(kind, bounds, slide_width, slide_height, text),
                is_decorative=is_decorative(kind, bounds, slide_width, slide_height, text),
            )
        )
    return shapes


def axis_gap(a: Rect, b: Rect) -> tuple[float, float]:
    if a.right < b.left:
        dx = b.left - a.right
    elif b.right < a.left:
        dx = a.left - b.right
    else:
        dx = 0.0
    if a.bottom < b.top:
        dy = b.top - a.bottom
    elif b.bottom < a.top:
        dy = a.top - b.bottom
    else:
        dy = 0.0
    return dx, dy


def should_ignore_pair(a: ShapeInfo, b: ShapeInfo) -> bool:
    if a.is_decorative or b.is_decorative:
        return True
    if a.kind == "group" or b.kind == "group":
        return True
    if a.bounds.contains(b.bounds, margin=2.0) or b.bounds.contains(a.bounds, margin=2.0):
        return True
    if a.is_container and a.bounds.contains(b.effective_bounds, margin=1.0):
        return True
    if b.is_container and b.bounds.contains(a.effective_bounds, margin=1.0):
        return True
    if not a.text.strip() and a.kind in {"autoshape", "picture", "table"} and a.bounds.contains(b.effective_bounds, margin=2.0):
        return True
    if not b.text.strip() and b.kind in {"autoshape", "picture", "table"} and b.bounds.contains(a.effective_bounds, margin=2.0):
        return True
    return False


def overlap_issue(a: ShapeInfo, b: ShapeInfo) -> Issue | None:
    if should_ignore_pair(a, b):
        return None

    left_box = a.effective_bounds
    right_box = b.effective_bounds
    inter = left_box.intersection(right_box)
    if not inter:
        return None

    inter_area = inter.area
    if inter_area < MIN_INTERSECTION_AREA:
        return None

    denom = min(left_box.area, right_box.area)
    if denom <= 0:
        return None
    ratio = inter_area / denom

    is_text_pair = bool(a.text.strip()) or bool(b.text.strip())
    threshold = MIN_TEXT_OVERLAP_RATIO if is_text_pair else MIN_SHAPE_OVERLAP_RATIO
    if ratio < threshold:
        return None

    if bool(a.text.strip()) and bool(b.text.strip()):
        issue_type = "text_overlap"
        severity = "critical"
    elif bool(a.text.strip()) or bool(b.text.strip()):
        issue_type = "text_graphic_overlap"
        severity = "critical"
    else:
        issue_type = "graphic_overlap"
        severity = "warning"

    message = (
        f"{a.name} ({a.kind}) overlaps {b.name} ({b.kind}) "
        f"with {ratio:.0%} overlap of the smaller rendered box."
    )
    return Issue(
        slide_index=a.slide_index,
        severity=severity,
        issue_type=issue_type,
        message=message,
        box=inter,
        shape_ids=(a.shape_id, b.shape_id),
        shape_names=(a.name, b.name),
    )


def crowded_issue(a: ShapeInfo, b: ShapeInfo) -> Issue | None:
    if should_ignore_pair(a, b):
        return None
    if not (a.text.strip() or b.text.strip()):
        return None
    if a.kind == "autoshape" and not a.text.strip():
        return None
    if b.kind == "autoshape" and not b.text.strip():
        return None
    if a.text.strip() and len(" ".join(a.text.split())) < 8:
        return None
    if b.text.strip() and len(" ".join(b.text.split())) < 8:
        return None
    left_box = a.effective_bounds
    right_box = b.effective_bounds
    if left_box.intersection(right_box):
        return None

    dx, dy = axis_gap(left_box, right_box)
    if min(dx, dy) > NEAR_GAP_THRESHOLD:
        return None
    if dx > 6.0 or dy > 6.0:
        return None

    overlap_height = max(0.0, min(left_box.bottom, right_box.bottom) - max(left_box.top, right_box.top))
    overlap_width = max(0.0, min(left_box.right, right_box.right) - max(left_box.left, right_box.left))
    if overlap_height < min(left_box.height, right_box.height) * 0.75 and overlap_width < min(left_box.width, right_box.width) * 0.75:
        return None

    union = Rect(
        min(left_box.left, right_box.left),
        min(left_box.top, right_box.top),
        max(left_box.right, right_box.right) - min(left_box.left, right_box.left),
        max(left_box.bottom, right_box.bottom) - min(left_box.top, right_box.top),
    )
    return Issue(
        slide_index=a.slide_index,
        severity="warning",
        issue_type="crowded_gap",
        message=f"{a.name} and {b.name} are extremely close and may look crowded in export.",
        box=union,
        shape_ids=(a.shape_id, b.shape_id),
        shape_names=(a.name, b.name),
    )


def off_slide_issue(shape: ShapeInfo, slide_width: float, slide_height: float) -> Issue | None:
    if shape.is_container or shape.is_decorative:
        return None
    box = shape.bounds
    if (
        box.left >= -EDGE_TOLERANCE
        and box.top >= -EDGE_TOLERANCE
        and box.right <= slide_width + EDGE_TOLERANCE
        and box.bottom <= slide_height + EDGE_TOLERANCE
    ):
        return None
    return Issue(
        slide_index=shape.slide_index,
        severity="critical",
        issue_type="off_slide",
        message=f"{shape.name} extends beyond the slide bounds.",
        box=shape.bounds,
        shape_ids=(shape.shape_id,),
        shape_names=(shape.name,),
    )


def clipping_issue(shape: ShapeInfo) -> Issue | None:
    if not shape.text.strip() or not shape.text_bounds:
        return None
    try:
        available = shape.bounds
        text_box = shape.text_bounds
        normalized_text = " ".join(shape.text.split())
        if len(normalized_text) < 20:
            return None
        overflow_left = max(0.0, available.left - text_box.left)
        overflow_top = max(0.0, available.top - text_box.top)
        overflow_right = max(0.0, text_box.right - available.right)
        overflow_bottom = max(0.0, text_box.bottom - available.bottom)
        max_horizontal = max(overflow_left, overflow_right)
        max_vertical = max(overflow_top, overflow_bottom)
        clipped = (
            max_horizontal > max(8.0, available.width * 0.1)
            or max_vertical > max(8.0, available.height * 0.18)
        )
        if clipped:
            return Issue(
                slide_index=shape.slide_index,
                severity="critical",
                issue_type="text_clipping",
                message=f"{shape.name} text bounds extend outside its text box.",
                box=text_box,
                shape_ids=(shape.shape_id,),
                shape_names=(shape.name,),
            )

        vertical_fill = text_box.height / max(available.height, 1.0)
        horizontal_fill = text_box.width / max(available.width, 1.0)
        text_length = len(" ".join(shape.text.split()))
        if text_length >= 90 and (vertical_fill > 0.98 or horizontal_fill > 0.99):
            return Issue(
                slide_index=shape.slide_index,
                severity="warning",
                issue_type="text_near_clip",
                message=f"{shape.name} text nearly fills its box and may clip on export.",
                box=available,
                shape_ids=(shape.shape_id,),
                shape_names=(shape.name,),
            )
    except Exception:
        return None
    return None


def chart_crowding_issue(shape: ShapeInfo, image: Image.Image, slide_width: float, slide_height: float) -> Issue | None:
    if shape.kind not in {"chart", "picture"}:
        return None
    if shape.bounds.area < 4500.0:
        return None

    img_w, img_h = image.size
    sx = img_w / slide_width
    sy = img_h / slide_height
    pad = 4
    x0 = max(0, int(shape.bounds.left * sx) - pad)
    y0 = max(0, int(shape.bounds.top * sy) - pad)
    x1 = min(img_w, int(shape.bounds.right * sx) + pad)
    y1 = min(img_h, int(shape.bounds.bottom * sy) + pad)
    if x1 - x0 < 50 or y1 - y0 < 50:
        return None

    crop = np.array(image.crop((x0, y0, x1, y1)).convert("L"))
    _, binary = cv2.threshold(crop, 210, 255, cv2.THRESH_BINARY_INV)
    num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(binary, 8)

    candidates: list[tuple[int, int, int, int]] = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area < 6 or area > 1200:
            continue
        if w > crop.shape[1] * 0.45 or h > crop.shape[0] * 0.25:
            continue
        if h < 3 or w < 2:
            continue
        candidates.append((x, y, w, h))

    if len(candidates) < 18:
        return None

    overlap_pairs = 0
    cluster_points: list[tuple[float, float]] = []
    dilated_rects = [Rect(x - 3, y - 2, w + 6, h + 4) for x, y, w, h in candidates]
    for i in range(len(dilated_rects)):
        for j in range(i + 1, len(dilated_rects)):
            inter = dilated_rects[i].intersection(dilated_rects[j])
            if inter and inter.area >= 12:
                overlap_pairs += 1
                cx = (inter.left + inter.right) / 2.0
                cy = (inter.top + inter.bottom) / 2.0
                cluster_points.append((cx, cy))

    if overlap_pairs < max(8, len(candidates) // 3):
        return None

    if cluster_points:
        xs = [pt[0] for pt in cluster_points]
        ys = [pt[1] for pt in cluster_points]
        local_box = Rect(min(xs) - 30, min(ys) - 20, max(xs) - min(xs) + 60, max(ys) - min(ys) + 40)
    else:
        local_box = Rect(0, 0, crop.shape[1], crop.shape[0])

    slide_box = Rect(
        shape.bounds.left + max(local_box.left, 0) / sx,
        shape.bounds.top + max(local_box.top, 0) / sy,
        min(local_box.width, crop.shape[1]) / sx,
        min(local_box.height, crop.shape[0]) / sy,
    )
    return Issue(
        slide_index=shape.slide_index,
        severity="warning",
        issue_type="possible_internal_label_crowding",
        message=f"{shape.name} has a dense cluster of small components that may indicate overlapping chart labels.",
        box=slide_box,
        shape_ids=(shape.shape_id,),
        shape_names=(shape.name,),
    )


def detect_slide_issues(
    shapes: list[ShapeInfo],
    slide_width: float,
    slide_height: float,
    slide_image: Image.Image | None,
) -> list[Issue]:
    issues: list[Issue] = []

    for shape in shapes:
        off_slide = off_slide_issue(shape, slide_width, slide_height)
        if off_slide:
            issues.append(off_slide)
        clip = clipping_issue(shape)
        if clip:
            issues.append(clip)

    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            overlap = overlap_issue(shapes[i], shapes[j])
            if overlap:
                issues.append(overlap)
            else:
                crowded = crowded_issue(shapes[i], shapes[j])
                if crowded:
                    issues.append(crowded)

    if slide_image is not None:
        for shape in shapes:
            crowding = chart_crowding_issue(shape, slide_image, slide_width, slide_height)
            if crowding:
                issues.append(crowding)

    unique: dict[tuple, Issue] = {}
    for issue in issues:
        key = (
            issue.slide_index,
            issue.issue_type,
            tuple(sorted(issue.shape_ids)),
            None if issue.box is None else tuple(round(v, 1) for v in issue.box.to_list()),
        )
        unique[key] = issue
    return sorted(
        unique.values(),
        key=lambda x: (x.slide_index, 0 if x.severity == "critical" else 1, x.issue_type, x.shape_ids),
    )


def export_slides(presentation, export_dir: Path) -> list[Path]:
    if export_dir.exists():
        shutil.rmtree(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)
    presentation.SaveAs(str(export_dir.resolve()), PNG_SAVE_FORMAT)
    images = sorted(export_dir.glob("*.PNG")) + sorted(export_dir.glob("*.png"))
    return images


def draw_issue_box(draw: ImageDraw.ImageDraw, rect: Rect, scale_x: float, scale_y: float, color: str) -> None:
    x0 = rect.left * scale_x
    y0 = rect.top * scale_y
    x1 = rect.right * scale_x
    y1 = rect.bottom * scale_y
    draw.rectangle((x0, y0, x1, y1), outline=color, width=4)


def annotate_slides(
    issues: Iterable[Issue],
    slide_images: dict[int, Path],
    output_dir: Path,
    slide_width: float,
    slide_height: float,
) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    issues_by_slide: dict[int, list[Issue]] = {}
    for issue in issues:
        issues_by_slide.setdefault(issue.slide_index, []).append(issue)

    colors = {
        "critical": "#e53935",
        "warning": "#fb8c00",
        "info": "#1e88e5",
    }

    for slide_index, image_path in slide_images.items():
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        sx = image.width / slide_width
        sy = image.height / slide_height
        for issue in issues_by_slide.get(slide_index, []):
            if issue.box:
                draw_issue_box(draw, issue.box, sx, sy, colors.get(issue.severity, "#e53935"))
        if issues_by_slide.get(slide_index):
            image.save(output_dir / image_path.name)


def build_markdown_report(
    pptx_path: Path,
    issues: list[Issue],
    shapes_by_slide: dict[int, list[ShapeInfo]],
    report_path: Path,
) -> None:
    lines: list[str] = []
    lines.append(f"# Visual QA Report: {pptx_path.name}")
    lines.append("")
    lines.append(f"- Slides scanned: {len(shapes_by_slide)}")
    lines.append(f"- Issues found: {len(issues)}")
    lines.append(f"- Critical: {sum(1 for issue in issues if issue.severity == 'critical')}")
    lines.append(f"- Warning: {sum(1 for issue in issues if issue.severity == 'warning')}")
    lines.append("")

    issues_by_slide: dict[int, list[Issue]] = {}
    for issue in issues:
        issues_by_slide.setdefault(issue.slide_index, []).append(issue)

    for slide_index in sorted(shapes_by_slide):
        slide_issues = issues_by_slide.get(slide_index, [])
        if not slide_issues:
            continue
        lines.append(f"## Slide {slide_index}")
        lines.append("")
        for issue in slide_issues:
            lines.append(
                f"- [{issue.severity.upper()}] `{issue.issue_type}`: {issue.message}"
            )
        lines.append("")

    if not issues:
        lines.append("No likely overlap issues were detected by the automated checks.")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def open_presentation(pptx_path: Path):
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = 1
    presentation = app.Presentations.Open(str(pptx_path.resolve()), WithWindow=False, ReadOnly=True)
    return app, presentation


def map_exported_images(image_dir: Path) -> dict[int, Path]:
    slide_images: dict[int, Path] = {}
    for image_path in sorted(image_dir.glob("*.png")) + sorted(image_dir.glob("*.PNG")):
        stem = image_path.stem
        digits = "".join(ch for ch in stem if ch.isdigit())
        if not digits:
            continue
        slide_images[int(digits)] = image_path
    return slide_images


def run_visual_qa(pptx_path: Path, output_dir: Path, export_images: bool = True) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    app = None
    presentation = None
    try:
        app, presentation = open_presentation(pptx_path)
        slide_width = float(presentation.PageSetup.SlideWidth)
        slide_height = float(presentation.PageSetup.SlideHeight)

        exported_dir = output_dir / "exported_slides"
        slide_images: dict[int, Path] = {}
        if export_images:
            export_slides(presentation, exported_dir)
            slide_images = map_exported_images(exported_dir)

        shapes_by_slide: dict[int, list[ShapeInfo]] = {}
        issues: list[Issue] = []

        for slide_index in range(1, presentation.Slides.Count + 1):
            slide = presentation.Slides(slide_index)
            shapes = collect_shapes_from_slide(slide, slide_index, slide_width, slide_height)
            shapes_by_slide[slide_index] = shapes
            slide_image = None
            if slide_index in slide_images:
                slide_image = Image.open(slide_images[slide_index])
            issues.extend(detect_slide_issues(shapes, slide_width, slide_height, slide_image))
            if slide_image is not None:
                slide_image.close()

        issues = sorted(issues, key=lambda x: (x.slide_index, x.severity, x.issue_type))

        json_payload = {
            "pptx": str(pptx_path.resolve()),
            "slide_count": len(shapes_by_slide),
            "issues": [issue.to_dict() for issue in issues],
        }
        (output_dir / "overlap_report.json").write_text(
            json.dumps(json_payload, indent=2),
            encoding="utf-8",
        )
        build_markdown_report(pptx_path, issues, shapes_by_slide, output_dir / "overlap_report.md")

        if slide_images:
            annotate_slides(issues, slide_images, output_dir / "annotated", slide_width, slide_height)

        return json_payload
    finally:
        if presentation is not None:
            presentation.Close()
        if app is not None:
            app.Quit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run visual QA overlap checks on a PowerPoint deck.")
    parser.add_argument("pptx", type=Path, help="Path to the PPTX file to scan.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for reports and annotated images. Defaults to slides/visual_qa/<deck_name>/",
    )
    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Do not export slide PNGs or generate annotated images.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pptx_path = args.pptx.resolve()
    if not pptx_path.exists():
        print(f"PPTX not found: {pptx_path}", file=sys.stderr)
        return 2
    if pptx_path.suffix.lower() != ".pptx":
        print(f"Expected a .pptx file, got: {pptx_path.name}", file=sys.stderr)
        return 2

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = pptx_path.parent / "visual_qa" / pptx_path.stem

    payload = run_visual_qa(pptx_path, output_dir, export_images=not args.no_export)
    issues = payload["issues"]
    critical = sum(1 for issue in issues if issue["severity"] == "critical")
    warnings = sum(1 for issue in issues if issue["severity"] == "warning")

    print(f"Scanned: {pptx_path}")
    print(f"Slides:  {payload['slide_count']}")
    print(f"Issues:  {len(issues)}")
    print(f"Critical: {critical}")
    print(f"Warning:  {warnings}")
    print(f"Report: {output_dir / 'overlap_report.md'}")
    if not args.no_export:
        print(f"Annotated: {output_dir / 'annotated'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
