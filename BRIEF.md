# The Brief

## What we want you to build

A pipeline that takes a scanned PDF (image-only — no extractable text layer)
and produces:

1. A **structured JSON document** describing every region on every page —
   text blocks, headings, tables, formulas, figures, captions — with bounding
   boxes, content, and confidence per region.
2. A **reconstructed HTML view** of each page that preserves the spatial
   intent of the original. Region-level fidelity, not pixel-perfect.

Translation is a stretch goal. We care more about whether your extraction
actually fires.

## What we are testing

- Can you turn a scanned image into a useful structured representation?
- Can you make and defend tool/library choices we did not pre-decide for you?
- Does your code actually do, on the bundled samples, what your write-up
  claims?
- Can you describe the limitations of what you shipped, honestly?

## Five principles

These are non-negotiable. Implementation is yours.

1. **Preservation-first.** Non-text elements — images, diagrams, table
   grids — survive the round-trip unchanged. You only rewrite or translate
   text.
2. **Provenance.** Every text region carries its source bounding box from
   extraction to final output. If you lose the bbox, you lose the ability to
   reconstruct.
3. **Modularity.** Stages should be swappable. We want to see seams.
4. **Honest confidence.** Every output region carries a confidence score.
   Low-confidence regions are flagged, not silently dropped.
5. **Reproducibility.** A fresh checkout plus one command should produce the
   bundled outputs.

## Element rules

| Element | Translate? | Preserve as-is? |
|---|---|---|
| Body text, headings, captions, footnotes | Yes (if attempting translation) | Position, role |
| Table cell content | Yes | Grid structure, row/col count, merged cells |
| Chart and graph axis labels and legend text | Yes | Bars, lines, axes, scale values |
| Formulas — variables (`x`, `y`, `α`, `Σ`) and operators (`+`, `=`, `∫`) | No | LaTeX form, position |
| Formulas — descriptive prose ("where", "such that") | Yes | — |
| Photographs, diagrams, schematics | No | Pixel-exact |
| Page numbers, equation numbers | No | Position |

## Required deliverables

- A single command (e.g. `python -m yourpackage inputs/sample-engineering-book.pdf -o outputs/`)
  that produces a JSON output conforming to [`OUTPUT_CONTRACT.md`](OUTPUT_CONTRACT.md)
  for any PDF or image in `inputs/`.
- A single command that produces an HTML reconstruction for the same input.
- The bundled sample successfully processed end-to-end. Run
  `python eval_runner.py outputs/` to pre-check before submission.
- A 1–2 page write-up using [`WRITE_UP_TEMPLATE.md`](WRITE_UP_TEMPLATE.md).
- A `requirements.txt` or `pyproject.toml` that installs cleanly on Python 3.11+.

## Stretch goals

In rough order of value:

- Translate text content into a target language of your choice. Document the
  language pair and why you picked it.
- Render the HTML reconstruction as a PDF.
- Confidence-driven escalation — fall back to a secondary extractor on
  low-confidence regions.
- Document-level glossary so the same term translates consistently across
  regions.
- Process more than the first N pages of the sample (scale beyond a single page).

Stretch points cannot make up for missing required deliverables. See
[`RUBRIC.md`](RUBRIC.md).

## Out of scope

We are not testing UI, deployment, authentication, or scaling. Don't build
them.

## Time budget

Target ~25–30 hours over 5–7 calendar days. Below that you'll cut corners;
above that you'll spiral. Required deliverables fit ~20h; stretch goals soak
the rest.

## What we are not going to tell you

We will not tell you which OCR engine, which VLM, which LLM, which
intermediate format, or which PDF renderer to use. Picking these is the test.
[`reading-list.md`](reading-list.md) is a starting point, not a
recommendation. Any "best practice" you hear from us second-hand is not part
of this brief.

## Submission

Private fork only. Share via private invitation. See
[`CONFIDENTIALITY.md`](CONFIDENTIALITY.md).
