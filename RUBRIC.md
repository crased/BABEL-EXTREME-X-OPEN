# Evaluation Rubric

We score on six dimensions, weighted. Total: 100 points. Stretch goals add up
to 20 more.

| # | Dimension | Weight | What we look for |
|---|---|---|---|
| 1 | **Schema validity** | 15 | Output validates against [`schema.json`](schema.json) on every bundled sample. Edge cases handled (empty pages, no tables, etc.). Run [`eval_runner.py`](eval_runner.py) — if it fails, you start at 0 here. |
| 2 | **Extraction recall on bundled samples** | 25 | Of the text regions a human can see on the page, how many did you extract with non-empty `content`? Measured on your declared "showcase page" plus the private eval set. |
| 3 | **Layout fidelity** | 20 | Bboxes are within page bounds and don't overlap implausibly. Reading order is plausible on multi-column pages. Tables retain row/col structure. |
| 4 | **Code quality** | 15 | Module boundaries, type hints where they help, no dead code, no hardcoded paths, no committed secrets. Single command runs on a fresh checkout. README sufficient to reproduce. |
| 5 | **Architectural reasoning in write-up** | 15 | Did you make defensible choices for OCR engine, intermediate representation, and reconstruction strategy? Did you say *why* you chose what you chose? "I picked X because Y, considered Z and rejected it because W" earns this. "I used X" earns nothing. |
| 6 | **Honest limitation discussion** | 10 | What doesn't work? Where does your pipeline fall over? "It fails on page N because my table detector loses merged cells" earns most of this. Silent failures cost more than disclosed ones. |

## Floor conditions

If any of these are true, the submission scores 0 regardless of the above:

- The bundled command does not run on a fresh checkout (we test this).
- `eval_runner.py` reports schema validation failure on your output.
- The repo is public on GitHub or any other public host. See
  [`CONFIDENTIALITY.md`](CONFIDENTIALITY.md).
- Submission is more than 7 days late without prior notice.

## Stretch dimensions

Up to 20 additional points, capped:

- Translation, end-to-end on at least your showcase page, with a documented
  language pair: up to **+10**
- PDF rendering of the reconstruction with selectable text: up to **+5**
- Document-level glossary with measurable consistency improvement: up to **+5**
- Confidence-driven escalation between extractors with measurable accuracy
  delta: up to **+5**

(Stretch points cap at +20 even if your sum exceeds it.)

Stretch points cannot make up for missing required deliverables.

## What we don't score

- Performance and latency. We won't time you.
- Accuracy on the private eval set. We use it to differentiate top
  candidates, but published scores are based on the bundled samples only.
- UI, deployment, auth.
- Whether you used "the right" tools. We score whether you can defend the
  ones you picked.

## How we grade write-ups

We read the write-up first. If your reasoning is sharp, ambiguous code reads
charitably. If your reasoning is thin, even working code looks lucky.
