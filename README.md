# Babel-Extreme

Pipeline for converting image-only scanned engineering documents into structured JSON plus an HTML reconstruction that preserves the page's spatial intent. Translation to a target language is a planned extension; see [`docs/`](docs/) for design notes.

## Status

Scaffold and design phase. The output schema, validation tooling, and a sample input are defined; the extraction and reconstruction code is not yet implemented.

## What it does (target behaviour)

Given a scanned PDF with no extractable text layer, Babel-Extreme aims to:

1. Detect and classify each region on each page as `text_block`, `heading`, `caption`, `table`, `formula`, `figure`, `header`, `footer`, or `list_item`.
2. Extract content — raw text for text-bearing regions, LaTeX for formulas, cropped image assets for figures.
3. Recover row and column structure for tables, including merged cells.
4. Emit a plausible reading order for multi-column pages.
5. Produce a structured JSON document conforming to [`contracts/schema.json`](contracts/schema.json), plus an HTML reconstruction of each processed page.

## Repository layout

| Path | What's there |
|---|---|
| [`contracts/schema.json`](contracts/schema.json) | JSON Schema for the output format — source of truth. |
| [`docs/output-schema.md`](docs/output-schema.md) | Prose explanation of the schema with examples. |
| [`docs/`](docs/) | System design notes — overview, per-stage notes, references, reading list. |
| [`inputs/sample-engineering-book.pdf`](inputs/sample-engineering-book.pdf) | Bundled scanned engineering reference (Russian, multi-hundred pages, image-only). |
| [`expected/sample-engineering-book/output.example.json`](expected/sample-engineering-book/output.example.json) | Worked example illustrating the schema's shape (not ground truth). |
| [`tools/eval_runner.py`](tools/eval_runner.py) | Schema validator and population-statistics utility. |

## Validating an output

```bash
pip install jsonschema
python tools/eval_runner.py path/to/outputs/
```

The runner walks the given directory, validates each `*.json` against `contracts/schema.json`, and prints population statistics — pages, elements, percentage of text-bearing elements with non-empty content, table-cell counts, figure-with-path counts, bbox issues, and reading-order misses.

## Sample input

[`inputs/sample-engineering-book.pdf`](inputs/sample-engineering-book.pdf) is image-only — no extractable text layer. It is several hundred pages of Russian-language engineering content with prose, tables, technical diagrams, and equations. The pipeline is not specialized to subject matter; treat it as scanned pages that need extraction.
