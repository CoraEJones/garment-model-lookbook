#!/usr/bin/env python3
"""Build a minimal 16:9 garment lookbook from verified images.

Only item IDs and five view labels are visible page text. Labels default to
Chinese / English; --language also accepts zh or en. Requires reportlab, Pillow,
and pypdf. Images are contained without distortion; optional source viewports
remain supported. This script never generates images or retouches garments.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
import sys
import tempfile
from typing import Any

try:
    from PIL import Image, ImageOps
    from pypdf import PdfReader
    from reportlab.lib.colors import HexColor
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
except ImportError as exc:
    raise SystemExit(
        "Missing PDF dependency. Use the bundled Python runtime or install "
        "reportlab Pillow pypdf in the chosen environment. " + str(exc)
    ) from exc


PAGE_W, PAGE_H = 960, 540
INK, MUTED, RULE = HexColor("#171717"), HexColor("#686868"), HexColor("#d5d5d5")
VIEW_LABELS = {
    "bilingual": (
        (("front", "正面 / Front"), ("back", "背面 / Back"), ("side", "侧面 / Side")),
        (("front", "实拍正面 / Original Front"), ("back", "实拍背面 / Original Back")),
    ),
    "zh": (
        (("front", "正面"), ("back", "背面"), ("side", "侧面")),
        (("front", "实拍正面"), ("back", "实拍背面")),
    ),
    "en": (
        (("front", "Front"), ("back", "Back"), ("side", "Side")),
        (("front", "Original Front"), ("back", "Original Back")),
    ),
}


@dataclass
class Asset:
    path: Path
    crop: tuple[float, float, float, float]
    width: int
    height: int


def require_text(value: Any, location: str, default: str | None = None) -> str:
    """Validate text without rewriting significant spaces in IDs or paths."""
    if default is not None and (value is None or isinstance(value, str) and not value.strip()):
        return default
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location}: expected non-empty text")
    return value


def require_item_id(value: Any, location: str) -> str:
    item_id = require_text(value, location)
    if item_id != item_id.strip():
        raise ValueError(f"{location}: leading or trailing whitespace is not permitted; preserve the intended identifier explicitly")
    if any(ord(char) < 32 or 127 <= ord(char) <= 159 or char in "\u2028\u2029" for char in item_id):
        raise ValueError(f"{location}: line breaks, tabs and control characters are not permitted")
    return item_id


def read_asset(spec: Any, base: Path, location: str) -> Asset:
    if isinstance(spec, str):
        spec = {"path": spec}
    if not isinstance(spec, dict):
        raise ValueError(f"{location}: expected an image path or {{path, crop}}")
    raw_path = require_text(spec.get("path"), location + ".path")
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = base / path
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"{location}: image does not exist: {path}")
    crop = spec.get("crop", [0, 0, 1, 1])
    if not isinstance(crop, (list, tuple)) or len(crop) != 4:
        raise ValueError(f"{location}.crop: use [x, y, width, height], normalized 0..1")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in crop):
        raise ValueError(f"{location}.crop: all values must be finite numbers")
    x, y, w, h = map(float, crop)
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > 1 + 1e-9 or y + h > 1 + 1e-9:
        raise ValueError(f"{location}.crop: rectangle must fit inside the image")
    try:
        with Image.open(path) as opened:
            opened.load()
            oriented = ImageOps.exif_transpose(opened)
            width, height = oriented.size
    except Exception as exc:
        raise ValueError(f"{location}: cannot decode image {path}: {exc}") from exc
    return Asset(path, (x, y, w, h), width, height)


def read_manifest(path: Path) -> tuple[dict, list[dict], list[Asset]]:
    try:
        document = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read manifest {path}: {exc}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("items"), list) or not document["items"]:
        raise ValueError("Manifest must be an object with a non-empty items list")
    # Collection/title/style notes may remain in the archival manifest, but are
    # neither required for production nor rendered on any PDF page.
    collection = require_text(document.get("collection"), "collection", "")
    assets: list[Asset] = []
    prepared = []
    ids = set()
    for index, raw in enumerate(document["items"]):
        loc = f"items[{index}]"
        if not isinstance(raw, dict):
            raise ValueError(f"{loc}: expected an object")
        item_id = require_item_id(raw.get("id"), loc + ".id")
        if item_id in ids:
            raise ValueError(f"{loc}: duplicate id {item_id!r}")
        ids.add(item_id)
        item = {
            "id": item_id,
            "side_inferred": raw.get("side_inferred", True),
        }
        if not isinstance(item["side_inferred"], bool):
            raise ValueError(f"{loc}.side_inferred: expected true or false")
        for group, views in (("model", ("front", "back", "side")), ("source", ("front", "back"))):
            if not isinstance(raw.get(group), dict):
                raise ValueError(f"{loc}.{group}: required image mapping is missing")
            item[group] = {}
            for view in views:
                if view not in raw[group]:
                    raise ValueError(f"{loc}.{group}.{view}: required view is missing; no placeholder is permitted")
                spec = raw[group][view]
                asset_loc = f"{loc}.{group}.{view}"
                if group == "source" and isinstance(spec, list):
                    if not spec:
                        raise ValueError(f"{asset_loc}: image list must not be empty")
                    source_assets = [
                        read_asset(entry, path.parent, f"{asset_loc}[{number}]")
                        for number, entry in enumerate(spec)
                    ]
                    item[group][view] = source_assets
                    assets.extend(source_assets)
                else:
                    asset = read_asset(spec, path.parent, asset_loc)
                    item[group][view] = asset
                    assets.append(asset)
        prepared.append(item)
    return {"collection": collection}, prepared, assets


def font_candidates(explicit: str | None) -> list[Path]:
    if explicit:
        return [Path(explicit).expanduser().resolve()]
    win = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    candidates = [
        win / "msyh.ttc", win / "Deng.ttf", win / "simhei.ttf", win / "simsun.ttc",
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    env_font = os.environ.get("LOOKBOOK_FONT")
    if env_font:
        candidates.insert(0, Path(env_font).expanduser())
    return candidates


def register_font(explicit: str | None, required: str) -> tuple[str, Path]:
    required_codes = {ord(c) for c in required if not c.isspace()}
    errors = []
    for candidate in font_candidates(explicit):
        if not candidate.is_file():
            if explicit:
                errors.append(f"font does not exist: {candidate}")
            continue
        try:
            font = TTFont("LookbookText", str(candidate), subfontIndex=0)
            missing = required_codes.difference(font.face.charToGlyph)
            if missing:
                sample = " ".join(f"U+{code:04X}" for code in sorted(missing)[:8])
                raise ValueError("missing required glyphs: " + sample)
            pdfmetrics.registerFont(font)
            return "LookbookText", candidate
        except Exception as exc:
            errors.append(f"{candidate}: {exc}")
    raise ValueError(
        "No embeddable font covers the Chinese labels and supplied text. "
        "Pass --font PATH_TO_CJK_TTF_OR_TTC (TrueType outlines; TTC face 0), "
        "or set LOOKBOOK_FONT. " + " | ".join(errors)
    )


def item_id_font_size(item_id: str, font: str) -> float:
    """Keep the full style identifier; never silently truncate a product ID."""
    width_at_12 = pdfmetrics.stringWidth(item_id, font, 12)
    size = min(12.0, 12 * 904 / width_at_12) if width_at_12 else 12.0
    if size < 9:
        raise ValueError(f"Item id is too long for the page header: {item_id!r}")
    return size


def text_line(pdf: canvas.Canvas, text: str, x: float, y: float, width: float,
              font: str, size: float, color=INK, align: str = "left") -> None:
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    if pdfmetrics.stringWidth(text, font, size) > width + 1e-6:
        raise ValueError(f"Text does not fit its page box: {text!r}")
    if align == "right":
        pdf.drawRightString(x + width, y, text)
    else:
        pdf.drawString(x, y, text)


def draw_asset(pdf: canvas.Canvas, asset: Asset, box: tuple[float, float, float, float]) -> None:
    """Contain a selected viewport; embed the full image and clip on the PDF.

    crop uses the EXIF-oriented image's top-left coordinate system. Source files
    are opened read-only. The crop affects only this PDF viewport.
    """
    bx, by, bw, bh = box
    cx, cy, cw, ch = asset.crop
    visible_w, visible_h = asset.width * cw, asset.height * ch
    scale = min(bw / visible_w, bh / visible_h)
    fitted_w, fitted_h = visible_w * scale, visible_h * scale
    dx, dy = bx + (bw - fitted_w) / 2, by + (bh - fitted_h) / 2
    with Image.open(asset.path) as original:
        oriented = ImageOps.exif_transpose(original)
        oriented.load()
        if oriented.mode not in ("RGB", "RGBA", "L"):
            oriented = oriented.convert("RGB")
        # Export at up to 300 ppi at the actual placed size; original assets
        # remain untouched. JPEG avoids very large lossless photo streams.
        export_size = (
            max(1, math.ceil(asset.width * scale / 72 * 300)),
            max(1, math.ceil(asset.height * scale / 72 * 300)),
        )
        oriented.thumbnail(export_size, Image.Resampling.LANCZOS)
        if oriented.mode == "RGBA":
            reader = ImageReader(oriented)
        else:
            encoded = io.BytesIO()
            oriented.convert("RGB").save(encoded, format="JPEG", quality=94, subsampling=0)
            encoded.seek(0)
            reader = ImageReader(encoded)
        pdf.saveState()
        clipping = pdf.beginPath()
        clipping.rect(dx, dy, fitted_w, fitted_h)
        pdf.clipPath(clipping, stroke=0, fill=0)
        pdf.drawImage(
            reader,
            dx - cx * asset.width * scale,
            dy - (1 - cy - ch) * asset.height * scale,
            width=asset.width * scale,
            height=asset.height * scale,
            mask="auto",
        )
        pdf.restoreState()


def visible_page_text(item: dict, language: str = "bilingual") -> list[str]:
    """The complete allowlist of visible vector text on a page."""
    model_views, source_views = VIEW_LABELS[language]
    return [item["id"]] + [label for _, label in model_views + source_views]


def draw_source_view(pdf: canvas.Canvas, assets: Asset | list[Asset],
                     box: tuple[float, float, float, float]) -> None:
    """Fit one reference or a set's top/bottom references side by side."""
    views = assets if isinstance(assets, list) else [assets]
    x, y, width, height = box
    gap = 6 if len(views) > 1 else 0
    cell_width = (width - gap * (len(views) - 1)) / len(views)
    if cell_width <= 0:
        raise ValueError("Too many source images for the available width")
    for index, asset in enumerate(views):
        draw_asset(pdf, asset, (x + index * (cell_width + gap), y, cell_width, height))


def draw_page(pdf: canvas.Canvas, item: dict, font: str, language: str = "bilingual") -> None:
    # White ground, one thin outer rule, a header rule and a quiet separator.
    # There are intentionally no titles, descriptions, inference tags or pages.
    pdf.setFillColor(HexColor("#ffffff"))
    pdf.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.4)
    pdf.rect(14, 14, 932, 512, stroke=1, fill=0)
    pdf.line(28, 496, 932, 496)
    pdf.line(704, 28, 704, 486)

    model_views, source_views = VIEW_LABELS[language]
    text_line(pdf, item["id"], 28, 508, 904, font, item_id_font_size(item["id"], font))

    col_w, col_gap = 212, 10
    for index, (view, label) in enumerate(model_views):
        x = 28 + index * (col_w + col_gap)
        draw_asset(pdf, item["model"][view], (x, 49, col_w, 437))
        text_line(pdf, label, x, 30, col_w, font, 8, MUTED)

    draw_source_view(pdf, item["source"]["front"], (724, 282, 208, 204))
    text_line(pdf, source_views[0][1], 724, 266, 208, font, 8, MUTED)
    draw_source_view(pdf, item["source"]["back"], (724, 49, 208, 201))
    text_line(pdf, source_views[1][1], 724, 30, 208, font, 8, MUTED)
    pdf.showPage()


def validate_pdf(data: bytes, items: list[dict], language: str = "bilingual") -> None:
    reader = PdfReader(io.BytesIO(data))
    expected_pages = len(items)
    if len(reader.pages) != expected_pages:
        raise ValueError(f"PDF page count mismatch: {len(reader.pages)} != {expected_pages}")
    for index, page in enumerate(reader.pages, 1):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        if abs(width - PAGE_W) > 0.01 or abs(height - PAGE_H) > 0.01 or abs(width / height - 16 / 9) > 1e-6:
            raise ValueError(f"Page {index} has unexpected dimensions {width} x {height}")
        resources = page.get("/Resources").get_object()
        fonts = resources.get("/Font").get_object()
        embedded = False
        for reference in fonts.values():
            descriptor = reference.get_object().get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                embedded |= any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
        if not embedded:
            raise ValueError(f"Page {index} lacks an embedded font")
        actual_text = [line.strip() for line in (page.extract_text() or "").splitlines() if line.strip()]
        expected_text = visible_page_text(items[index - 1], language)
        if actual_text != expected_text:
            raise ValueError(f"Page {index} has unexpected visible text: {actual_text!r}")


def main(argv: list[str] | None = None) -> int:
    # Stable JSON output even when the Windows console has a legacy code page.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="UTF-8 JSON manifest")
    parser.add_argument("output", type=Path, help="Destination .pdf; refused if it exists")
    parser.add_argument("--font", help="Embeddable CJK TrueType font (.ttf or .ttc face 0)")
    parser.add_argument("--language", choices=tuple(VIEW_LABELS), default="bilingual",
                        help="Page view labels: bilingual (default), zh, or en")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace the destination PDF")
    parser.add_argument("--check-only", action="store_true", help="Validate inputs and fonts without writing a PDF")
    args = parser.parse_args(argv)
    manifest = args.manifest.expanduser().resolve()
    output = args.output.expanduser().resolve()
    try:
        if output.suffix.lower() != ".pdf":
            raise ValueError("Output filename must end in .pdf")
        if output == manifest:
            raise ValueError("Output must not replace the manifest")
        if output.exists() and not args.overwrite and not args.check_only:
            raise ValueError(f"Refusing to overwrite existing PDF: {output}. Pass --overwrite deliberately.")
        metadata, items, assets = read_manifest(manifest)
        if any(asset.path == output for asset in assets):
            raise ValueError("Output must not replace an input image")
        required = "".join(text for item in items for text in visible_page_text(item, args.language))
        font, font_path = register_font(args.font, required)
        for item in items:
            item_id_font_size(item["id"], font)
        summary = {
            "status": "inputs_valid" if args.check_only else "created",
            "pages": len(items), "page_size_pt": [PAGE_W, PAGE_H], "aspect_ratio": "16:9",
            "font": str(font_path), "image_references": len(assets),
            "language": args.language,
            "visible_text": [visible_page_text(item, args.language) for item in items],
            "input_images": sorted({str(asset.path) for asset in assets}),
        }
        if args.check_only:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=(PAGE_W, PAGE_H), pageCompression=1)
        pdf.setTitle(metadata["collection"] or output.stem)
        pdf.setAuthor("")
        for item in items:
            draw_page(pdf, item, font, args.language)
        pdf.save()
        data = buffer.getvalue()
        validate_pdf(data, items, args.language)
        output.parent.mkdir(parents=True, exist_ok=True)
        if args.overwrite:
            # Atomic replacement only after an in-memory build and validation.
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".lookbook-", suffix=".tmp", delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(data)
                os.replace(temporary, output)
            finally:
                if temporary and temporary.exists():
                    temporary.unlink()
        else:
            # Exclusive creation also protects against a race after the check.
            with output.open("xb") as stream:
                stream.write(data)
        summary["output"] = str(output)
        summary["bytes"] = len(data)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(f"Lookbook error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
