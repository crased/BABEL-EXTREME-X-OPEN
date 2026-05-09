# Sample Input

[`sample-engineering-book.pdf`](sample-engineering-book.pdf) is a real scanned engineering reference — image-only (no extractable text layer), Russian-language source, several hundred pages. It contains body prose, tables, technical diagrams with labels, and equations: a representative cross-section of difficulty for a real engineering book.

The file's subject matter is technical/military-historical because that is what was on hand as a representative scanned engineering volume. The pipeline is not specialized to subject matter — treat it as scanned pages that need extraction.

## Reading the file

The PDF is image-only. Any PDF library that can rasterize pages (`pdf2image`, `PyMuPDF`, `pypdfium2`, `pdfplumber`, etc.) will produce page images. Calls like `page.get_text()` or `pdftotext` return empty strings — that is the input shape, not a bug.
