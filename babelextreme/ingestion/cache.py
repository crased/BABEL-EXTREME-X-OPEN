"""Page-image cache writer.

Writes rendered pages to outputs/<stem>/_cache/page_<n>.png with predictable
filenames so later stages can pick them up without re-rendering.
"""

from __future__ import annotations

from pathlib import Path

from .pdf_reader import RenderedPage


def cache_dir_for(pdf_path: str | Path, out_root: str | Path) -> Path:
    stem = Path(pdf_path).stem
    return Path(out_root) / stem / "_cache"


def write_page(rendered: RenderedPage, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_path = cache_dir / f"page_{rendered.page_number:04d}.png"
    rendered.image.save(out_path, format="PNG")
    return out_path
