"""CLI entrypoint.

Run via: `python -m babelextreme <subcommand> [options]`
"""

from __future__ import annotations

import json
from pathlib import Path

import click

from .ingestion.cache import cache_dir_for, write_page
from .ingestion.pdf_reader import iter_pages, page_count
from .pipeline import process


def parse_page_range(spec: str, total: int) -> list[int]:
    """Parse "1-5", "3", "1,3,5", "1-3,5-7" into a sorted unique page list."""
    pages: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            lo_s, hi_s = chunk.split("-", 1)
            lo, hi = int(lo_s), int(hi_s)
            if lo > hi:
                raise click.BadParameter(f"range {chunk!r} is reversed")
            pages.update(range(lo, hi + 1))
        else:
            pages.add(int(chunk))
    out = sorted(pages)
    bad = [n for n in out if n < 1 or n > total]
    if bad:
        raise click.BadParameter(f"page(s) {bad} out of range (PDF has {total} pages)")
    return out


def _write_output_json(doc, out_root: Path, stem: str) -> Path:
    out_dir = Path(out_root) / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "output.json"
    out_path.write_text(
        json.dumps(doc.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return out_path


@click.group()
def main() -> None:
    """Babel-Extreme apprentice pipeline."""


@main.command()
@click.argument("pdf_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--pages", "pages_spec", default="1", show_default=True,
              help='Page range, e.g. "1-5" or "1,3,7" or "1-3,5".')
@click.option("--dpi", type=int, default=200, show_default=True)
@click.option("--out", "out_root", type=click.Path(file_okay=False, path_type=Path),
              default=Path("outputs"), show_default=True)
def ingest(pdf_path: Path, pages_spec: str, dpi: int, out_root: Path) -> None:
    """Stage 1: render PDF pages to PNG and cache them on disk."""
    total = page_count(pdf_path)
    page_numbers = parse_page_range(pages_spec, total)
    cache_dir = cache_dir_for(pdf_path, out_root)

    click.echo(f"PDF: {pdf_path}  (total pages: {total})")
    click.echo(f"Rendering pages {page_numbers} at {dpi} DPI -> {cache_dir}")

    for rendered in iter_pages(pdf_path, page_numbers, dpi):
        out_path = write_page(rendered, cache_dir)
        click.echo(
            f"  page {rendered.page_number:>4}  "
            f"{rendered.width_px}x{rendered.height_px}px  -> {out_path}"
        )


@main.command()
@click.argument("pdf_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--pages", "pages_spec", default="1", show_default=True)
@click.option("--dpi", type=int, default=200, show_default=True)
@click.option("--out", "out_root", type=click.Path(file_okay=False, path_type=Path),
              default=Path("outputs"), show_default=True)
@click.option("--no-ocr", is_flag=True, help="Skip OCR; content stays empty.")
@click.option("--no-figures", is_flag=True, help="Skip figure extraction.")
@click.option("--no-html", is_flag=True, help="Skip HTML reconstruction.")
def extract(pdf_path: Path, pages_spec: str, dpi: int, out_root: Path,
            no_ocr: bool, no_figures: bool, no_html: bool) -> None:
    """Stage 2 + 4: layout, OCR, figures, then HTML reconstruction."""
    total = page_count(pdf_path)
    page_numbers = parse_page_range(pages_spec, total)
    click.echo(f"PDF: {pdf_path}  (total pages: {total})")
    click.echo(
        f"Processing pages {page_numbers} at {dpi} DPI  "
        f"(ocr={'off' if no_ocr else 'on'}, figures={'off' if no_figures else 'on'}, "
        f"html={'off' if no_html else 'on'})"
    )

    doc = process(
        pdf_path=pdf_path,
        page_numbers=page_numbers,
        dpi=dpi,
        out_root=out_root,
        do_ocr=not no_ocr,
        do_figures=not no_figures,
        do_html=not no_html,
    )

    out_path = _write_output_json(doc, out_root, pdf_path.stem)
    for page in doc.pages:
        figures = sum(1 for e in page.elements if e.type == "figure")
        text_pop = sum(1 for e in page.elements if e.type == "text_block" and e.content)
        text_total = sum(1 for e in page.elements if e.type == "text_block")
        click.echo(
            f"  page {page.page_number:>4}  elements: {len(page.elements):>3}  "
            f"text: {text_pop}/{text_total}  figures: {figures}"
        )
    click.echo(f"Wrote {out_path}")


@main.command()
@click.argument("pdf_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--pages", "pages_spec", default="1", show_default=True)
@click.option("--dpi", type=int, default=200, show_default=True)
@click.option("--out", "out_root", type=click.Path(file_okay=False, path_type=Path),
              default=Path("outputs"), show_default=True)
def run(pdf_path: Path, pages_spec: str, dpi: int, out_root: Path) -> None:
    """End-to-end: ingestion + layout + OCR + figures + HTML."""
    total = page_count(pdf_path)
    page_numbers = parse_page_range(pages_spec, total)
    click.echo(f"PDF: {pdf_path}  (total pages: {total})")
    click.echo(f"Running full pipeline on pages {page_numbers} at {dpi} DPI")

    doc = process(
        pdf_path=pdf_path,
        page_numbers=page_numbers,
        dpi=dpi,
        out_root=out_root,
        do_ocr=True,
        do_figures=True,
        do_html=True,
    )

    out_path = _write_output_json(doc, out_root, pdf_path.stem)
    click.echo(f"Wrote {out_path}")
    click.echo(f"HTML pages at {out_root / pdf_path.stem}/page_*.html")


if __name__ == "__main__":
    main()
