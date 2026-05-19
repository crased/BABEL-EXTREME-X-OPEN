"""HTML reconstruction.

Renders one HTML file per page using absolute-positioned divs sized to each
element's pixel bbox. DOM order follows reading_order so copy-paste and
screen-reader traversal pick up the human reading order.
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..schema import Document, Page

_TEMPLATES_DIR = Path(__file__).parent / "templates"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_page(doc: Document, page: Page, page_numbers: list[int]) -> str:
    env = _env()
    template = env.get_template("page.html")
    elements_by_id = {e.id: e for e in page.elements}
    return template.render(
        source_file=doc.source_file,
        source_lang=doc.source_lang_detected,
        page=page,
        page_numbers=page_numbers,
        elements_by_id=elements_by_id,
    )


def write_document(doc: Document, out_dir: Path) -> list[Path]:
    """Write one page_<n>.html per page plus a copy of styles.css. Returns the file paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    page_numbers = [p.page_number for p in doc.pages]
    written: list[Path] = []
    for page in doc.pages:
        html = render_page(doc, page, page_numbers)
        out_path = out_dir / f"page_{page.page_number:04d}.html"
        out_path.write_text(html, encoding="utf-8")
        written.append(out_path)

    styles_src = _TEMPLATES_DIR / "styles.css"
    styles_dst = out_dir / "styles.css"
    styles_dst.write_text(styles_src.read_text(encoding="utf-8"), encoding="utf-8")
    written.append(styles_dst)

    # Convenience: reconstructed.html -> first page
    if doc.pages:
        first = out_dir / f"page_{doc.pages[0].page_number:04d}.html"
        index = out_dir / "reconstructed.html"
        index.write_text(first.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(index)

    return written
