"""Table detection + cell extraction (scaffold).

v1 minimum (plan.md Phase 4.2): Hough/Canny line detection; emit table.cells[]
with row_span/col_span. Skip entirely if no clean table is in the page subset.
"""

# TODO(phase-4.2): detect grid via OpenCV line ops; populate Cell records.
