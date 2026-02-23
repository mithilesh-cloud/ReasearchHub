from __future__ import annotations

import hashlib
from functools import lru_cache

import numpy as np

from app.core.config import get_settings


@lru_cache
def _load_model():
    from sentence_transformers import SentenceTransformer

    settings = get_settings()
    return SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_text(text: str) -> list[float]:
    if not text:
        return [0.0] * 32
    try:
        model = _load_model()
        vector = model.encode(text, normalize_embeddings=True)
        return vector.tolist()
    except Exception:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        vals = np.frombuffer(digest, dtype=np.uint8).astype(np.float32)
        normalized = vals / (np.linalg.norm(vals) + 1e-12)
        return normalized.tolist()
