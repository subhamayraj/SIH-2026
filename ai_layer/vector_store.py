from __future__ import annotations

import math

from langchain_core.documents import Document

from .config import settings
from .embeddings import EmbeddingProvider


class VectorStoreManager:
    def __init__(
        self,
        collection_name: str = "knowledge_base",
        embedding_provider: EmbeddingProvider | None = None,
    ):
        self.collection_name = collection_name
        self.embedding_provider = embedding_provider or EmbeddingProvider()
        self.docs: list[Document] = []
        self.store = None

        try:
            from langchain_postgres import PGVector

            self.store = PGVector(
                embeddings=self.embedding_provider,
                connection="postgresql+psycopg://{user}:{password}@{host}:{port}/{database}".format(
                    user=settings.pg_user,
                    password=settings.pg_password,
                    host=settings.pg_host,
                    port=settings.pg_port,
                    database=settings.pg_database,
                ),
                collection_name=self.collection_name,
                create_extension=True,
            )
        except Exception:
            self.store = None

    def add_documents(self, docs: list[Document]):
        if self.store is not None:
            self.store.add_documents(docs)
            return

        self.docs.extend(docs)

    def similarity_search(self, query: str, k: int | None = None):
        if self.store is not None:
            return self.store.similarity_search(query, k=k or settings.similarity_top_k)

        query_embedding = self.embedding_provider.embed_query(query)
        scored_docs = []

        for doc in self.docs:
            document_embedding = self.embedding_provider.embed_query(doc.page_content)
            score = self._cosine_similarity(query_embedding, document_embedding)
            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scored_docs[: (k or settings.similarity_top_k)]]

    @staticmethod
    def _cosine_similarity(vector_a, vector_b):
        if len(vector_a) != len(vector_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        magnitude_a = math.sqrt(sum(a * a for a in vector_a))
        magnitude_b = math.sqrt(sum(b * b for b in vector_b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)
