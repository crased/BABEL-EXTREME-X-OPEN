# Worked Example Output

[`sample-engineering-book/output.example.json`](sample-engineering-book/output.example.json) is a **structure illustration** showing the schema's shape in motion. It is not ground truth and not a complete extraction of any real page.

## What to take from it

- The shape of the JSON the pipeline produces.
- How `bbox`, `reading_order`, `table.cells` (including merged cells via `row_span`/`col_span`), and `figure_path` interact.
- An example of an honest `needs_review=true` element with a corresponding note in `extraction_notes`.

## What not to take from it

- **The values.** Page numbers, IDs, content strings, confidences, and bbox coordinates are illustrative.
- **The element count.** A real page has dozens of elements; the example uses a handful for readability.
- **The page choice.** The example is a synthetic illustration, not a real page from the bundled PDF.

## Validating an output

```bash
python tools/eval_runner.py outputs/
```

Validates each `*.json` against [`../contracts/schema.json`](../contracts/schema.json) and prints population statistics.
