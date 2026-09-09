from __future__ import annotations

import hashlib
import math

from .config import settings


class EmbeddingProvider:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self.embeddings = None
        self._fallback_error = None
        self._fallback_dimension = 384

    def _ensure_embeddings(self):
        if self.embeddings is not None:
            return

        try:
            from langchain_huggingface import HuggingFaceEmbeddings

            self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
        except Exception as exc:
            self.embeddings = None
            self._fallback_error = str(exc)

    def embed_query(self, text: str):
        self._ensure_embeddings()

        if self.embeddings is not None:
            return self.embeddings.embed_query(text)

        return self._fallback_embed(text)

    def embed_documents(self, documents: list[str]):
        self._ensure_embeddings()

        if self.embeddings is not None:
            return self.embeddings.embed_documents(documents)

        return [self._fallback_embed(doc) for doc in documents]

    def _fallback_embed(self, text: str):
        tokens = [token for token in text.lower().split() if token]
        if not tokens:
            return [0.0] * self._fallback_dimension

        vector = [0.0] * self._fallback_dimension

        for token in tokens:
            index = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % self._fallback_dimension
            vector[index] += 1.0

        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector

        return [value / magnitude for value in vector]

    @property
    def is_fallback(self) -> bool:
        return self.embeddings is None

    @property
    def fallback_error(self) -> str | None:
        return self._fallback_error
