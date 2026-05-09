# Expected

The single file in this folder, [`sample-engineering-book/output.example.json`](sample-engineering-book/output.example.json),
is a **structure illustration** — not an answer key.

## What you can take from it

- The **shape** of the JSON your pipeline must produce.
- How `bbox`, `reading_order`, `table.cells`, and `figure_path` interact.
- An example of an honest `needs_review=true` element with a corresponding
  note in `extraction_notes`.

## What you should not take from it

- **The values.** Page numbers, IDs, content strings, confidences, and
  bbox coordinates in the example are illustrative. Yours will be different
  because your pipeline is different.
- **The element count.** The example has a handful of elements per page so
  it's readable. A real page has dozens. We will compare your output against
  what is *actually* on each page, not against what's in the example.
- **The page choice.** The example is a synthetic illustration, not a real
  page from the bundled PDF.

## How to validate your own output

Once you have an `outputs/sample-engineering-book/output.json`, run:

```bash
python eval_runner.py outputs/
```

That will validate against `schema.json` and print population statistics.
This is the same script we run on submission; passing it locally is the
floor for getting your work read.
