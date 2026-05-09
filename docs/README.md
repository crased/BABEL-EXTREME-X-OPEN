# Documentation

Design notes and reference material for the Babel-Extreme pipeline.

## Overview and stages

| Document | Description |
|---|---|
| [Overview](./00-overview.md) | Design principles and pipeline diagram. |
| [Stage 1: Ingestion](./01-stage-ingestion.md) | PDF → image extraction, deskew, denoise. |
| [Stage 2: Extraction](./02-stage-extraction.md) | OCR and layout analysis. |
| [Stage 3: Translation](./03-stage-translation.md) | Forward-looking — translation extension. |
| [Stage 4: Reconstruction](./04-stage-reconstruction.md) | HTML / PDF reconstruction. |
| [Cross-Cutting](./05-cross-cutting.md) | Error handling, confidence, parallelism. |
| [Deployment](./06-deployment.md) | Forward-looking — Docker and CLI sketches. |
| [Verification](./verification.md) | Notes on scanned-document support across components. |

## Schema

| Document | Description |
|---|---|
| [Output schema (prose)](./output-schema.md) | Prose explanation of the JSON output format. |
| [`../contracts/schema.json`](../contracts/schema.json) | Machine-readable JSON Schema (source of truth). |

## Reference

| Document | Description |
|---|---|
| [Reading list](./reading-list.md) | Tools, papers, and resources. Not all are recommendations — context-dependent. |
| [Project description](./task-description.md) | Detailed project description and preservation philosophy. |
| [References](./07-references.md) | External tool links. |
