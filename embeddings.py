from __future__ import annotations

from sentence_transformers import SentenceTransformer

from settings import settings

_model_cache: SentenceTransformer | None = None


def load_embedding_model(model_name: str | None = None) -> SentenceTransformer:
    global _model_cache
    if _model_cache is not None:
        return _model_cache
    model_name = model_name or settings.embedding_model
    _model_cache = SentenceTransformer(model_name)
    return _model_cache


def encode_texts(texts: list[str], model_name: str | None = None) -> list[list[float]]:
    model = load_embedding_model(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.tolist()
