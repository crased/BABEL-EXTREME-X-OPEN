# BabelExtreme: System Overview

> **Status:** initial design / scope-of-vision document. The shipped scope (see [`../README.md`](../README.md)) is narrower than what's described here.

---

## Executive Summary

BabelExtreme is a **production-grade document translation pipeline** designed specifically for **image-only scanned PDFs** containing complex engineering content. Unlike consumer-grade tools, this system treats **visual fidelity as sacrosanct**—preserving every image, table structure, diagram, and formula while translating only the text content.

---

## Design Principles

1. **Preservation-First**: Non-text elements (images, diagrams, tables) transfer unchanged
2. **Semantic Awareness**: Understanding document structure, not just OCR text
3. **Modularity**: Swappable components at each pipeline stage
4. **Fault Tolerance**: Graceful degradation with confidence scoring
5. **Reproducibility**: Deterministic outputs for the same inputs

---

## System Architecture

### High-Level Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              BABELEXTREME PIPELINE                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │   STAGE 1    │    │   STAGE 2    │    │   STAGE 3    │    │   STAGE 4    │           │
│  │  INGESTION   │───▶│  EXTRACTION  │───▶│ TRANSLATION  │───▶│RECONSTRUCTION│           │
│  │              │    │              │    │              │    │              │           │
│  │ PDF → Images │    │ Layout + OCR │    │ LLM + VLM    │    │ Typst + PDF  │           │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘           │
│         │                   │                   │                   │                    │
│         ▼                   ▼                   ▼                   ▼                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │  Page Images │    │ Structured   │    │ Translated   │    │ Final PDF    │           │
│  │  (PNG/TIFF)  │    │ Markdown +   │    │ Content +    │    │ (Selectable  │           │
│  │              │    │ Coordinates  │    │ Label JSON   │    │  Text Layer) │           │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘           │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Comparative Analysis

### Why This Stack Beats Alternatives

| Feature | BabelDOC | **BabelExtreme** |
|---------|----------|------------------|
| **Formula Handling** | OCR (often garbled) | LaTeX extraction (mathematical integrity) |
| **Table Structure** | Best-effort visual | Semantic reconstruction (cell logic preserved) |
| **Diagram Labels** | Ignored | VLM extraction + overlay (original preserved) |
| **Image Quality** | Recompression | Pass-through (original bytes) |
| **Terminology Consistency** | None | Document-wide glossary |
| **Transparency** | Open source | Open source + auditable |
| **Offline Capability** | Yes | Yes (with local models) |

### Resource Requirements

| Configuration | VRAM | RAM | CPU | Use Case |
|---------------|------|-----|-----|----------|
| **API-Only** | 0 | 16GB | 4 cores | Low volume, cloud APIs |
| **Hybrid** | 8GB | 32GB | 8 cores | Medium volume, local extraction + API translation |
| **Full Local** | 48GB+ | 64GB | 16 cores | High volume, fully offline |

---

## Next Steps

See the individual stage documentation for detailed implementation:

1. [Stage 1: Ingestion](./01-stage-ingestion.md)
2. [Stage 2: Extraction](./02-stage-extraction.md)
3. [Stage 3: Translation](./03-stage-translation.md)
4. [Stage 4: Reconstruction](./04-stage-reconstruction.md)
