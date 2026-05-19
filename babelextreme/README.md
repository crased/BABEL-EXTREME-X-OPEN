# babelextreme

CPU-only Python pipeline that turns an image-only scanned PDF into a
schema-valid `output.json` ([`contracts/schema.json`](../contracts/schema.json))
plus per-page HTML reconstructions.

## Architecture

```
PDF -> ingestion -> extraction (layout + OCR + figures) -> reconstruction (HTML)
```

Stages live in the matching subpackages:

| Module | Role |
|---|---|
| `babelextreme.ingestion.pdf_reader` | PyMuPDF page rasterizer |
| `babelextreme.ingestion.cache` | Persists rendered PNGs to `outputs/<stem>/_cache/` |
| `babelextreme.extraction.layout` | OpenCV morphology -> region bboxes |
| `babelextreme.extraction.reading_order` | Band-sort by (y, x) |
| `babelextreme.extraction.ids` | Deterministic `el_<page>_<seq>` IDs |
| `babelextreme.extraction.ocr` | PaddleOCR adapter (Russian, CPU, mkldnn off) |
| `babelextreme.extraction.figures` | Crops figure regions to `outputs/<stem>/figures/` |
| `babelextreme.reconstruction.html_renderer` | Jinja2 absolute-positioned HTML |
| `babelextreme.schema` | Typed dataclasses mirroring the JSON Schema |
| `babelextreme.pipeline` | Orchestrator |
| `babelextreme.cli` | `click` group: `ingest`, `extract`, `run` |

## Usage

```bash
# end-to-end, pages 3-7 at 200 DPI
python -m babelextreme run inputs/sample-engineering-book.pdf --pages 3-7 --dpi 200

# just stage 1 (cache page PNGs)
python -m babelextreme ingest inputs/sample-engineering-book.pdf --pages 1-5

# extract with toggles
python -m babelextreme extract inputs/sample-engineering-book.pdf --pages 3 --no-ocr --no-html
```

Outputs land at `outputs/<pdf-stem>/`:
- `output.json` — the schema-valid contract artifact
- `page_<n>.html` and `reconstructed.html` — per-page HTML
- `styles.css`
- `figures/<element-id>.png` — cropped figure assets
- `_cache/page_<n>.png` — rendered page images (regeneratable)

## Verification

```bash
python tools/eval_runner.py outputs/sample-engineering-book/
```

Expected on the bundled sample, pages 3-7:
```
schema:       OK
pages:        5
elements:     16
text-bearing: 15/15 populated (100%)
figures:      1/1 with path
bbox issues:  0
read-order misses: 0
ALL OK
```

## Known limitations (v1)

- **Layout heuristic, not a model.** Morphology-based region detection works
  on clean Russian engineering scans but will misgroup complex multi-column
  layouts. Tune `dilate_kernel` and `min_area_frac` in
  [`extraction/layout.py`](extraction/layout.py).
- **Reading order is band-sort.** No multi-column awareness. Documented in
  [`../plan.md`](../plan.md) Risk #5.
- **Tables not implemented.** Regions that look table-like fall through to
  `text_block` or get reclassified as figures by the confidence heuristic.
- **No formulas.** Formula recognition (LaTeX) requires a vision model out
  of scope for v1.
- **Translation not wired.** `target_lang` and `Element.translation` stay
  unset; see [`../docs/03-stage-translation.md`](../docs/03-stage-translation.md).
- **mkldnn disabled.** PaddleOCR's onednn path crashes on some x86_64 CPUs
  with the bundled PaddlePaddle build; CPU inference runs without it but is
  slower.

## Determinism

IDs are `el_<page>_<seq>` with seq from a stable band-sorted bbox order.
Re-running on the same input produces byte-identical `output.json`.
