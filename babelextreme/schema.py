"""Typed Python dataclasses mirroring contracts/schema.json.

The JSON file at contracts/schema.json remains the source of truth; these
dataclasses exist so the pipeline can build typed objects in Python and
emit schema-valid JSON without dict-typo bugs.

See docs/output-schema.md for prose.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ElementType = Literal[
    "text_block",
    "heading",
    "caption",
    "table",
    "formula",
    "figure",
    "header",
    "footer",
    "list_item",
]


@dataclass(frozen=True)
class Bbox:
    x1: float
    y1: float
    x2: float
    y2: float

    def to_dict(self) -> dict:
        return {"x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2}


@dataclass(frozen=True)
class Cell:
    row: int
    col: int
    row_span: int
    col_span: int
    content: str
    is_header: bool

    def to_dict(self) -> dict:
        return {
            "row": self.row,
            "col": self.col,
            "row_span": self.row_span,
            "col_span": self.col_span,
            "content": self.content,
            "is_header": self.is_header,
        }


@dataclass(frozen=True)
class Table:
    rows: int
    cols: int
    cells: list[Cell]

    def to_dict(self) -> dict:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "cells": [c.to_dict() for c in self.cells],
        }


@dataclass
class Element:
    id: str
    type: ElementType
    bbox: Bbox
    content: str
    confidence: float
    needs_review: bool
    translation: str | None = None
    table: Table | None = None
    figure_path: str | None = None

    def to_dict(self) -> dict:
        out: dict = {
            "id": self.id,
            "type": self.type,
            "bbox": self.bbox.to_dict(),
            "content": self.content,
            "confidence": self.confidence,
            "needs_review": self.needs_review,
        }
        if self.translation is not None:
            out["translation"] = self.translation
        if self.type == "table":
            if self.table is None:
                raise ValueError(f"Element {self.id} type=table requires table data")
            out["table"] = self.table.to_dict()
        if self.type == "figure":
            if not self.figure_path:
                raise ValueError(f"Element {self.id} type=figure requires figure_path")
            out["figure_path"] = self.figure_path
        return out


@dataclass
class Page:
    page_number: int
    width: int
    height: int
    elements: list[Element]
    reading_order: list[str]
    dpi_estimated: int | None = None

    def to_dict(self) -> dict:
        out: dict = {
            "page_number": self.page_number,
            "width": self.width,
            "height": self.height,
            "elements": [e.to_dict() for e in self.elements],
            "reading_order": list(self.reading_order),
        }
        if self.dpi_estimated is not None:
            out["dpi_estimated"] = self.dpi_estimated
        return out


@dataclass
class Document:
    source_file: str
    pages: list[Page]
    source_lang_detected: str | None = None
    target_lang: str | None = None
    extraction_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        out: dict = {
            "source_file": self.source_file,
            "pages": [p.to_dict() for p in self.pages],
        }
        if self.source_lang_detected is not None:
            out["source_lang_detected"] = self.source_lang_detected
        if self.target_lang is not None:
            out["target_lang"] = self.target_lang
        if self.extraction_notes:
            out["extraction_notes"] = list(self.extraction_notes)
        return out
