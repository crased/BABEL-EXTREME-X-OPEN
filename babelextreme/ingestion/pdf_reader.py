"""PDF -> page-image rasterizer.

Library functions for Stage 1 (see plan.md Phase 1). Takes a path,
returns a pymupdf document or a rendered page as a PIL.Image. No
hard-coded paths, no script-style entrypoints — the CLI layer owns I/O.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pymupdf
from PIL import Image


@dataclass(frozen=True)
class RenderedPage:
    page_number: int
    image: Image.Image
    width_px: int
    height_px: int
    dpi: int


def open_pdf(path: str | Path) -> pymupdf.Document:
    return pymupdf.open(str(path))


def page_count(path: str | Path) -> int:
    with open_pdf(path) as doc:
        return doc.page_count


def render_page(doc: pymupdf.Document, page_index: int, dpi: int) -> RenderedPage:
    page = doc.load_page(page_index)
    zoom = dpi / 72.0
    matrix = pymupdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    mode = "RGB" if pix.n == 3 else "RGBA" if pix.n == 4 else "L"
    image = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
    return RenderedPage(
        page_number=page_index + 1,
        image=image,
        width_px=pix.width,
        height_px=pix.height,
        dpi=dpi,
    )


def iter_pages(
    path: str | Path, page_numbers: list[int], dpi: int
) -> Iterator[RenderedPage]:
    with open_pdf(path) as doc:
        total = doc.page_count
        for n in page_numbers:
            if n < 1 or n > total:
                raise ValueError(f"page {n} out of range (PDF has {total} pages)")
            yield render_page(doc, n - 1, dpi)
