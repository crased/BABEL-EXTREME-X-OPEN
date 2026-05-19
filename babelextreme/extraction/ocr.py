"""OCR adapter built on PaddleOCR (CPU, lang=ru).

The model object is expensive to construct (loads ONNX/Paddle weights), so
the adapter caches one instance per process. mkldnn is disabled because
PaddleOCR's onednn path crashes on some Linux x86_64 CPUs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from PIL import Image

os.environ.setdefault("FLAGS_use_mkldnn", "0")

from paddleocr import PaddleOCR  # noqa: E402

from ..schema import Bbox


@dataclass(frozen=True)
class OcrResult:
    text: str
    confidence: float


@lru_cache(maxsize=1)
def _get_engine(lang: str = "ru") -> PaddleOCR:
    return PaddleOCR(
        lang=lang,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        enable_mkldnn=False,
    )


def ocr_region(image: Image.Image, bbox: Bbox, *, lang: str = "ru") -> OcrResult:
    """Crop the bbox from image, run OCR, return joined text + mean confidence."""
    x1, y1, x2, y2 = int(bbox.x1), int(bbox.y1), int(bbox.x2), int(bbox.y2)
    if x2 <= x1 or y2 <= y1:
        return OcrResult(text="", confidence=0.0)

    crop = np.asarray(image.convert("RGB"))[y1:y2, x1:x2]
    if crop.size == 0:
        return OcrResult(text="", confidence=0.0)

    engine = _get_engine(lang)
    results = engine.predict(crop)
    if not results:
        return OcrResult(text="", confidence=0.0)

    texts: list[str] = []
    scores: list[float] = []
    for r in results:
        for t, s in zip(r.get("rec_texts", []), r.get("rec_scores", [])):
            t = t.strip()
            if t:
                texts.append(t)
                scores.append(float(s))

    if not texts:
        return OcrResult(text="", confidence=0.0)

    return OcrResult(text=" ".join(texts), confidence=float(np.mean(scores)))
