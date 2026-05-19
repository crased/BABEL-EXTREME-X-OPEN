"""Reading-order heuristic: band-sort.

Sort regions by (band(y_center), x_center). The band granularity smooths
out small vertical jitter between regions that should be read on the same
line. Multi-column awareness is a stretch goal (plan.md Phase 2 limit).
"""

from __future__ import annotations

from .layout import Region


def band_sort(regions: list[Region], *, band_height: int = 80) -> list[Region]:
    def key(r: Region) -> tuple[int, float]:
        cy = (r.bbox.y1 + r.bbox.y2) / 2.0
        cx = (r.bbox.x1 + r.bbox.x2) / 2.0
        return (int(cy) // band_height, cx)

    return sorted(regions, key=key)
