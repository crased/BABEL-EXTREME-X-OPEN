# Write-Up Template

Use this template for your submission write-up. 1–2 pages total. Markdown.
Save as `WRITE_UP.md` at the root of your fork.

---

## Approach

(3 paragraphs max. What does your pipeline do, end to end, for a single
input? Skip the "why this matters" framing — go straight to the mechanics.)

## Tool and library choices

| Choice | What I picked | Alternatives I considered | Why I picked this |
|---|---|---|---|
| OCR / layout extraction | | | |
| Intermediate representation | | | |
| Translation (if attempted) | | | |
| Reconstruction / rendering | | | |
| PDF / image preprocessing | | | |

(Brief — one or two sentences per "Why" cell. We're looking for evidence
that you considered the alternatives, not that you exhaustively benchmarked
them.)

## Trade-offs I made

(3–5 bullets. Each: the decision, what you gave up, why the trade was worth
it. Examples — "Skipped formula handling because LaTeX recognition would have
eaten 6h for one sample"; "Picked HTML over PDF because round-trip layout
fidelity wasn't graded.")

## Honest limitations

(What doesn't work. Where does your pipeline fall over? Be specific —
"sample page 5 has a multi-row merged-cell table; my detector treats each
row as a separate table." Silent failures lose more points than disclosed
ones; see RUBRIC.md.)

## Showcase page

Declare the page in the bundled sample that you used for development and
believe shows your pipeline at its best. We will use this for the per-element
extraction recall scoring.

- Page number: ___
- Why this page: (one sentence)

## What I'd do with more time

(2–4 bullets. The next things you'd build, ordered by priority.)

## How to reproduce

```bash
# from a fresh checkout
python -m venv .venv
. .venv/bin/activate     # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python -m yourpackage inputs/sample-engineering-book.pdf -o outputs/
python eval_runner.py outputs/
```

(Adjust to your actual commands. Must work on Python 3.11+ on a clean
machine.)
