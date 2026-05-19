"""End-to-end pipeline orchestrator.

Order: ingestion -> extraction (layout + OCR + figures) -> reconstruction (HTML).
Translation (Stage 3) is intentionally not wired in v1 — see docs/03-stage-translation.md.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from .extraction.figures import save_figure
from .extraction.ids import make_id
from .extraction.layout import detect_regions
from .extraction.ocr import ocr_region
from .extraction.reading_order import band_sort
from .ingestion.cache import cache_dir_for, write_page
from .ingestion.pdf_reader import iter_pages, page_count
from .reconstruction.html_renderer import write_document
from .schema import Document, Element, Page


CONFIDENCE_REVIEW_THRESHOLD = 0.75
FIGURE_CONFIDENCE_THRESHOLD = 0.30
FIGURE_MIN_AREA_FRAC = 0.02


def process(
    pdf_path: Path,
    page_numbers: list[int],
    *,
    dpi: int,
    out_root: Path,
    lang: str = "ru",
    do_ocr: bool = True,
    do_figures: bool = True,
    do_html: bool = True,
) -> Document:
    stem = pdf_path.stem
    out_dir = Path(out_root) / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = cache_dir_for(pdf_path, out_root)
    figures_dir = out_dir / "figures"

    total = page_count(pdf_path)
    notes: list[str] = []
    pages: list[Page] = []

    for rendered in iter_pages(pdf_path, page_numbers, dpi):
        write_page(rendered, cache_dir)
        page_area = float(rendered.width_px * rendered.height_px)

        regions = detect_regions(rendered.image)
        ordered = band_sort(regions)

        elements: list[Element] = []
        seq = 0
        for region in ordered:
            candidate_id = make_id(rendered.page_number, seq + 1)
            element = _build_element(
                element_id=candidate_id,
                region_bbox=region.bbox,
                image=rendered.image,
                page_area=page_area,
                figures_dir=figures_dir,
                lang=lang,
                do_ocr=do_ocr,
                do_figures=do_figures,
            )
            if element is None:
                notes.append(
                    f"page {rendered.page_number}: dropped noise region "
                    f"bbox=({region.bbox.x1:.0f},{region.bbox.y1:.0f},"
                    f"{region.bbox.x2:.0f},{region.bbox.y2:.0f})"
                )
                continue
            seq += 1
            if element.needs_review:
                notes.append(
                    f"page {rendered.page_number} {element.id}: low-confidence "
                    f"({element.confidence:.2f}, type={element.type})"
                )
            elements.append(element)

        pages.append(
            Page(
                page_number=rendered.page_number,
                width=rendered.width_px,
                height=rendered.height_px,
                elements=elements,
                reading_order=[e.id for e in elements],
                dpi_estimated=rendered.dpi,
            )
        )

    doc = Document(
        source_file=pdf_path.name,
        source_lang_detected=lang if do_ocr else None,
        pages=pages,
        extraction_notes=_summarize_notes(notes, total, page_numbers, do_ocr),
    )

    if do_html and pages:
        write_document(doc, out_dir)

    return doc


def _build_element(
    *,
    element_id: str,
    region_bbox,
    image: Image.Image,
    page_area: float,
    figures_dir: Path,
    lang: str,
    do_ocr: bool,
    do_figures: bool,
) -> Element | None:
    text = ""
    confidence = 0.0

    if do_ocr:
        result = ocr_region(image, region_bbox, lang=lang)
        text = result.text
        confidence = result.confidence

    bbox_area = (region_bbox.x2 - region_bbox.x1) * (region_bbox.y2 - region_bbox.y1)
    treat_as_figure = (
        do_figures
        and (
            (not text and bbox_area >= page_area * FIGURE_MIN_AREA_FRAC)
            or (do_ocr and confidence < FIGURE_CONFIDENCE_THRESHOLD and bbox_area >= page_area * FIGURE_MIN_AREA_FRAC)
        )
    )

    if not text and not treat_as_figure and do_ocr:
        return None

    if treat_as_figure:
        figure_path = save_figure(
            image, region_bbox, figures_dir=figures_dir, element_id=element_id
        )
        return Element(
            id=element_id,
            type="figure",
            bbox=region_bbox,
            content="",
            confidence=max(confidence, 0.5),
            needs_review=False,
            figure_path=figure_path,
        )

    return Element(
        id=element_id,
        type="text_block",
        bbox=region_bbox,
        content=text,
        confidence=confidence,
        needs_review=confidence < CONFIDENCE_REVIEW_THRESHOLD,
    )


def _summarize_notes(
    notes: list[str], total_pages: int, page_numbers: list[int], do_ocr: bool
) -> list[str]:
    summary: list[str] = []
    summary.append(
        f"processed pages {page_numbers} of {total_pages} total; ocr={'on' if do_ocr else 'off'}"
    )
    if not do_ocr:
        summary.append("OCR disabled; content fields are empty by design")
    if notes:
        summary.append(f"{len(notes)} low-confidence elements flagged")
        summary.extend(notes[:20])
    return summary
