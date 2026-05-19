"""Deterministic element-ID generator.

Format: el_<page>_<seq>, where seq is a zero-padded sequence number.
Re-running the pipeline on the same input must produce byte-identical IDs.
See plan.md Risk #4 (non-deterministic IDs).
"""

from __future__ import annotations


def make_id(page_number: int, seq: int) -> str:
    return f"el_{page_number}_{seq:03d}"
