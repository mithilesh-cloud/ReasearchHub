import numpy as np


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    vec_a = np.array(a, dtype=np.float32)
    vec_b = np.array(b, dtype=np.float32)
    denom = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)) + 1e-12
    return float(np.dot(vec_a, vec_b) / denom)


def top_k_similar(query_vector: list[float], items: list[tuple[int, list[float]]], k: int = 4) -> list[int]:
    scored = [(idx, cosine_similarity(query_vector, vector)) for idx, vector in items if vector]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [item_id for item_id, _score in scored[:k]]
