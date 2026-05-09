# Starter

Two files, no obligations.

- [`requirements.txt.example`](requirements.txt.example) — the bare
  foundations (Pillow, OpenCV, PyMuPDF, jsonschema, Pydantic). Copy to
  `requirements.txt` at the repo root and add the OCR / VLM / LLM /
  reconstruction libraries you actually pick.
- [`run.py.template`](run.py.template) — a 60-line CLI skeleton with
  `process()` and `reconstruct()` stubs that already produce a schema-valid
  (but useless) JSON. Use it as a scaffold or delete it.

You are not required to keep this structure. Pick a Python package layout
you can defend, and document it in your write-up.
