from __future__ import annotations
from src.adapters.embeddings import EmbeddingClient, cosine

def test_hash_embedding_deterministic():
    cfg = {"models":{"embedding":{"provider":"auto"}}}
    emb = EmbeddingClient(cfg)
    v1 = emb.embed_texts(["hello world"])[0]
    v2 = emb.embed_texts(["hello world"])[0]
    assert v1 == v2
    # similarity sanity
    a = emb.embed_texts(["machine learning engineer"])[0]
    b = emb.embed_texts(["ml engineer"])[0]
    c = emb.embed_texts(["classical pianist"])[0]
    assert cosine(a,b) > cosine(a,c)
