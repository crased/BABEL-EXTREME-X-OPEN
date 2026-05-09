# Output Contract

Your pipeline must emit JSON that validates against [`schema.json`](schema.json).
This file explains the schema; the JSON Schema is the source of truth.

## Top-level shape

```json
{
  "source_file": "sample-engineering-book.pdf",
  "source_lang_detected": "ru",
  "target_lang": null,
  "pages": [
    {
      "page_number": 1,
      "width": 2480,
      "height": 3508,
      "dpi_estimated": 300,
      "elements": [],
      "reading_order": ["el_1_001", "el_1_002"]
    }
  ],
  "extraction_notes": [
    "Stage-1 deskew applied (0.8°)",
    "1 region flagged for review (low OCR confidence)"
  ]
}
```

`target_lang` is `null` if you did not attempt translation. Set it to the
ISO-639-1 code of the target language otherwise (e.g. `"en"`).

## Element shape

Every element on a page has at minimum:

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | Page-unique, stable across reruns. Recommend `el_<page>_<seq>`. |
| `type` | enum | yes | One of: `text_block`, `heading`, `caption`, `table`, `formula`, `figure`, `header`, `footer`, `list_item`. |
| `bbox` | object | yes | Pixel coordinates: `{"x1": ..., "y1": ..., "x2": ..., "y2": ...}` in original page-image space. `x2 > x1` and `y2 > y1`. |
| `content` | string | yes for text-bearing types | Raw extracted text. For `formula`, LaTeX. For `figure`, may be empty. |
| `confidence` | float [0, 1] | yes | Your aggregate confidence for this element. Honest, not aspirational. |
| `needs_review` | bool | yes | `true` if confidence is below your chosen review threshold. |
| `translation` | string \| null | optional | Translated content if you attempted Stage 5. |
| `table` | object | required when `type=table` | See *Table shape*. |
| `figure_path` | string \| null | required when `type=figure` | Relative path to a cropped figure asset you write alongside the JSON. |

Text-bearing types: `text_block`, `heading`, `caption`, `formula`, `header`,
`footer`, `list_item`.

## Table shape

```json
{
  "rows": 5,
  "cols": 3,
  "cells": [
    {"row": 0, "col": 0, "row_span": 1, "col_span": 1, "content": "Test", "is_header": true},
    {"row": 0, "col": 1, "row_span": 1, "col_span": 1, "content": "Result", "is_header": true},
    {"row": 1, "col": 0, "row_span": 2, "col_span": 1, "content": "Sample A", "is_header": false}
  ]
}
```

Merged cells use `row_span` / `col_span` > 1. Cells covered by a span are
omitted from the list. Empty cells have `content: ""` (not omitted).

## Reading order

`reading_order` is a list of element IDs in the order a human would read them.
For multi-column pages, that means the column-aware sequence — not raster
scan order.

## Coordinates

Use **pixels**, not normalized 0–1 floats. `bbox.x1`, `bbox.y1` are top-left;
`bbox.x2`, `bbox.y2` are bottom-right. Top of the page is `y=0`. Coordinates
must be within page dimensions (`0 <= x <= page.width`, same for y).

## What we will validate automatically

[`eval_runner.py`](eval_runner.py) runs these checks. Run it before you
submit.

1. Output is valid JSON.
2. JSON validates against `schema.json`.
3. For every text-bearing element, `content` is non-empty **or**
   `needs_review=true` with an explanation surfaced in `extraction_notes`.
4. Every `bbox` has `x2 > x1`, `y2 > y1`, and lies within page dimensions.
5. Every ID in `reading_order` exists in `elements`.
6. On the bundled sample, on whichever page you choose to be your "showcase
   page" (declare it in your write-up), at least 60% of detected text-bearing
   elements have non-empty `content`. This is the floor. We set higher bars
   in the private rubric.

## Output file convention

For an input `inputs/X.pdf` (or `.png`), produce
`outputs/X/output.json` and `outputs/X/reconstructed.html`. If you cropped
figures, write them under `outputs/X/figures/` and reference them by
relative path in `figure_path`.

## Worked example

See [`expected/sample-engineering-book/output.example.json`](expected/sample-engineering-book/output.example.json).

That file illustrates **structure**, not ground truth. Your numbers, IDs, and
content will differ. Don't pattern-match against the values; use it to
understand the schema in motion.
