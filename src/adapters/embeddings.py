from __future__ import annotations
from typing import List
import hashlib
import math
import random

def _hash_to_vec(text: str, dim: int = 64, seed: int = 42) -> list[float]:
    rnd = random.Random(seed)
    vec = [0.0]*dim
    tokens = text.lower().split()
    for tok in tokens:
        h = int(hashlib.sha1(tok.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        sign = -1.0 if (h // dim) % 2 else 1.0
        vec[idx] += sign * 1.0
    # l2 normalize
    norm = math.sqrt(sum(v*v for v in vec)) or 1.0
    return [v / norm for v in vec]

def cosine(a: list[float], b: list[float]) -> float:
    n = min(len(a), len(b))
    dot = sum(a[i]*b[i] for i in range(n))
    na = math.sqrt(sum(x*x for x in a)) or 1.0
    nb = math.sqrt(sum(x*x for x in b)) or 1.0
    return dot/(na*nb)

class EmbeddingClient:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.provider = (cfg.get("models",{}).get("embedding",{}).get("provider") or "auto").lower()

    def embed_texts(self, texts: List[str]) -> List[list[float]]:
        # offline deterministic embedding by default
        return [_hash_to_vec(t) for t in texts]
