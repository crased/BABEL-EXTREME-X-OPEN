"""Figure crop and reference.

A region is reclassified as a figure when OCR returns no text or
confidence falls below the figure threshold — those regions are likely
diagrams / images / pictures rather than prose.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from ..schema import Bbox


def save_figure(
    image: Image.Image,
    bbox: Bbox,
    *,
    figures_dir: Path,
    element_id: str,
) -> str:
    """Crop bbox from image, save PNG, return relative path for figure_path."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    x1, y1, x2, y2 = int(bbox.x1), int(bbox.y1), int(bbox.x2), int(bbox.y2)
    cropped = image.crop((x1, y1, x2, y2))
    filename = f"{element_id}.png"
    cropped.save(figures_dir / filename, format="PNG")
    return f"figures/{filename}"
