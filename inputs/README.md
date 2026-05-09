# Inputs

## What's bundled

- [`sample-engineering-book.pdf`](sample-engineering-book.pdf) — a real
  scanned engineering reference, image-only (no extractable text layer),
  Russian-language source. Multi-hundred pages. Contains body prose, tables,
  technical diagrams with labels, and equations — i.e. all the difficulty
  axes you should expect to handle. Treat it as your development corpus.

## What we'll evaluate against

- The bundled sample (you process and submit outputs for it).
- A **private evaluation set** of 5–10 documents in the same style and
  difficulty range as the bundled sample. We do not share these. Strong
  submissions generalize beyond the development corpus; weak ones overfit.

## A note on the sample's content

The bundled document is technical / military-historical in subject matter
because it happens to be a representative scanned engineering book in our
hands. You are not being assessed on the subject matter and you don't need
to read or understand the content to do the work. Treat it as scanned pages
that need extraction.

## Pages-to-process

You don't have to process all pages of the bundled PDF. In your write-up,
declare a **showcase page** (or a small range, e.g. pp. 12–15) that you
believe shows your pipeline at its best. We'll grade extraction recall on
that showcase.

If you implement multi-page processing as a stretch goal, run on at least
20 pages and note it in your write-up.

## Reading the file

The PDF is image-only — `pdf2image`, `PyMuPDF`, `pdfplumber.open(...).pages[i].images`,
or any other PDF library that can rasterize pages will give you images. A
text-extraction call (`page.get_text()`, `pdftotext`) will return empty
strings; that is the assignment, not a bug.
