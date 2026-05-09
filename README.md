# Babel-Extreme Apprentice Assignment

A take-home for apprentice-tier AI engineering candidates. The task: turn an
image-only scanned PDF into a structured JSON document with bounding boxes,
plus a reconstructed HTML view. Translation is a stretch goal.

## Read in this order

1. [`BRIEF.md`](BRIEF.md) — what we want, what we test, what's out of scope.
2. [`OUTPUT_CONTRACT.md`](OUTPUT_CONTRACT.md) — the JSON shape your pipeline must emit.
3. [`schema.json`](schema.json) — machine-validatable version of the contract.
4. [`RUBRIC.md`](RUBRIC.md) — how we score.
5. [`WRITE_UP_TEMPLATE.md`](WRITE_UP_TEMPLATE.md) — required sections in your submission.
6. [`CONFIDENTIALITY.md`](CONFIDENTIALITY.md) — handling rules.

## Inputs and references

- [`inputs/`](inputs/) — bundled samples.
- [`expected/`](expected/) — one worked output for shape reference (not an answer key).
- [`reading-list.md`](reading-list.md) — flat list of tools and papers. Not a recommendation.
- [`starter/`](starter/) — skeleton files and a non-prescriptive `requirements.txt.example`.

## Pre-flight before submission

Run `python eval_runner.py outputs/` to validate your output JSONs against the
schema and see your population stats. If this fails, your submission scores 0
on schema validity.

## Time budget

~25–30 hours over 5–7 calendar days. Required deliverables fit ~20h; stretch
goals soak the rest.

## Submission

Private fork only. See [`CONFIDENTIALITY.md`](CONFIDENTIALITY.md).
