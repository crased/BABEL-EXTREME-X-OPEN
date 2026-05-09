# Output Schema (Prose)

This document explains the JSON output format produced by the Babel-Extreme pipeline. The machine-readable source of truth is [`../contracts/schema.json`](../contracts/schema.json); this file gives the same definition with prose, examples, and convention notes.

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

`target_lang` is `null` if no translation was attempted. Otherwise set to the ISO-639-1 code of the target language (e.g. `"en"`).

## Element shape

Every element on a page has at minimum:

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | Page-unique, stable across reruns. Recommend `el_<page>_<seq>`. |
| `type` | enum | yes | One of: `text_block`, `heading`, `caption`, `table`, `formula`, `figure`, `header`, `footer`, `list_item`. |
| `bbox` | object | yes | Pixel coordinates: `{"x1": ..., "y1": ..., "x2": ..., "y2": ...}` in original page-image space. `x2 > x1` and `y2 > y1`. |
| `content` | string | yes for text-bearing types | Raw extracted text. For `formula`, LaTeX. For `figure`, may be empty. |
| `confidence` | float [0, 1] | yes | Aggregate confidence for this element. Honest, not aspirational. |
| `needs_review` | bool | yes | `true` if confidence is below the chosen review threshold. |
| `translation` | string \| null | optional | Translated content when translation is attempted. |
| `table` | object | required when `type=table` | See *Table shape*. |
| `figure_path` | string \| null | required when `type=figure` | Relative path to a cropped figure asset written alongside the JSON. |

Text-bearing types: `text_block`, `heading`, `caption`, `formula`, `header`, `footer`, `list_item`.

## Confidence

Every element carries a `confidence` in `[0, 1]`. There is no single right way to compute it; pick something defensible and document the approach in the implementation notes.

Reasonable approaches:

- **Text-bearing types** (`text_block`, `heading`, `caption`, `formula`, `header`, `footer`, `list_item`): the average per-character confidence reported by the OCR engine, or the engine's region-level score if it exposes one. For LaTeX from a formula recognizer, use whatever the model exposes; if nothing, score from a sanity check (renders cleanly → 1.0, renders with errors → low).
- **`table`**: aggregate from cell-level scores — e.g. mean of cell OCR confidences, or weighted by cell area. Penalize for missing cells.
- **`figure`**: the layout detector's region score, or a fixed value like 0.95 if the detector is opinion-free.

Set `needs_review = true` for any element below the chosen threshold. A calibrated 0.4 with `needs_review=true` is more useful than an aspirational 0.95.

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

Merged cells use `row_span` / `col_span` > 1. Cells covered by a span are omitted from the list. Empty cells have `content: ""` (not omitted).

## Reading order

`reading_order` is a list of element IDs in the order a human would read them. For multi-column pages, that means the column-aware sequence — not raster scan order.

Conventions for non-prose elements:

- A **figure** appears in reading order at the position where a reader would first encounter it — typically just before its caption.
- A **caption** immediately follows its figure or table.
- A **table** appears at the position where the surrounding text refers to it; if it floats in a sidebar with no clear referent, place it where it visually appears.
- **Headers** and **footers** (page numbers, running titles) go at the start and end respectively, regardless of visual position on the page.
- **Formulas** appear inline in the text flow at the position they visually occupy.

These are conventions, not hard rules.

## Coordinates

Use **pixels**, not normalized 0–1 floats. `bbox.x1`, `bbox.y1` are top-left; `bbox.x2`, `bbox.y2` are bottom-right. Top of the page is `y=0`. Coordinates must be within page dimensions (`0 <= x <= page.width`, same for `y`).

## Validation

[`../tools/eval_runner.py`](../tools/eval_runner.py) provides automated checks:

```bash
python tools/eval_runner.py outputs/
```

The runner walks the given directory, validates each `*.json` against `contracts/schema.json`, and prints population statistics.

**Hard checks** (non-zero exit on failure):

1. Output is valid JSON.
2. JSON validates against `contracts/schema.json`.

**Soft checks** (reported as counts and warnings):

3. For every text-bearing element, `content` is non-empty. Regions that genuinely cannot be read should be flagged `needs_review=true` with a one-line entry in `extraction_notes`.
4. Every `bbox` has `x2 > x1`, `y2 > y1`, and lies within page dimensions.
5. Every ID in `reading_order` exists in `elements`.
6. Across all pages in the output, at least 60% of detected text-bearing elements have non-empty `content`. Computed as a global average across whatever pages are present.

## Output file convention

For an input `inputs/X.pdf` (or `.png`), produce `outputs/X/output.json` and `outputs/X/reconstructed.html`. Cropped figure assets go under `outputs/X/figures/` and are referenced by relative path in `figure_path`.

## Worked example

See [`../expected/sample-engineering-book/output.example.json`](../expected/sample-engineering-book/output.example.json). That file illustrates **structure**, not ground truth — values, IDs, content strings, and bbox coordinates are illustrative.
