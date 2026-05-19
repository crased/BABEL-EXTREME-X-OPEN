"""Layout / region detection via OpenCV morphology.

Pipeline (plan.md Phase 2.2):
    PIL.Image
      -> grayscale
      -> Otsu inverse threshold      (text=white, background=black)
      -> horizontal dilation         (merge chars into lines, lines into blocks)
      -> find contours
      -> bounding rects, filtered by min area and page-edge guard
      -> Region records
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image

from ..schema import Bbox


@dataclass(frozen=True)
class Region:
    bbox: Bbox
    type_hint: str = "text_block"


def detect_regions(
    image: Image.Image,
    *,
    dilate_kernel: tuple[int, int] = (60, 12),
    min_area_frac: float = 0.0015,
    max_area_frac: float = 0.95,
) -> list[Region]:
    """Return candidate regions for a single page image.

    Tuning knobs:
      dilate_kernel:  (width, height) of horizontal dilation kernel in px.
                      Larger width = more horizontal merging.
      min_area_frac:  reject regions smaller than this fraction of the page.
      max_area_frac:  reject regions larger than this fraction of the page
                      (filters the full-page background contour).
    """
    arr = np.asarray(image.convert("L"))
    height, width = arr.shape
    page_area = float(height * width)

    _, binary = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, dilate_kernel)
    dilated = cv2.dilate(binary, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions: list[Region] = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = float(w * h)
        if area < page_area * min_area_frac:
            continue
        if area > page_area * max_area_frac:
            continue
        x2 = min(x + w, width)
        y2 = min(y + h, height)
        regions.append(
            Region(
                bbox=Bbox(x1=float(x), y1=float(y), x2=float(x2), y2=float(y2)),
                type_hint="text_block",
            )
        )

    return regions
