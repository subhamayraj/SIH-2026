from __future__ import annotations

from typing import Any

from langchain_core.documents import Document

from .embeddings import EmbeddingProvider
from .vector_store import VectorStoreManager


class AIService:
    def __init__(self):
        self.embedding_provider = EmbeddingProvider()
        self.vector_store = VectorStoreManager(embedding_provider=self.embedding_provider)

    def build_index(self, documents: list[dict[str, Any]]):
        docs = [
            Document(page_content=item["text"], metadata=item.get("metadata", {}))
            for item in documents
        ]
        self.vector_store.add_documents(docs)
        return {"status": "success", "count": len(docs)}

    def recommend_courses(self, user_profile: dict[str, Any], top_k: int = 5):
        query = self._profile_to_query(user_profile)
        results = self.vector_store.similarity_search(query, k=top_k)
        return [
            {
                "content": item.page_content,
                "metadata": item.metadata,
            }
            for item in results
        ]

    def generate_quiz(self, user_profile: dict[str, Any], questions_count: int = 5):
        query = self._profile_to_query(user_profile)
        results = self.vector_store.similarity_search(query, k=questions_count)
        return {
            "questions": [
                {
                    "question": item.page_content,
                    "source": item.metadata,
                }
                for item in results
            ]
        }

    def analyze_skill_gaps(self, user_profile: dict[str, Any]):
        query = self._profile_to_query(user_profile)
        results = self.vector_store.similarity_search(query, k=3)
        return {
            "gaps": [
                {
                    "content": item.page_content,
                    "metadata": item.metadata,
                }
                for item in results
            ]
        }

    def status(self):
        return {
            "using_fallback_embeddings": self.embedding_provider.is_fallback,
            "fallback_error": self.embedding_provider.fallback_error,
            "vector_store": "pgvector" if self.vector_store.store is not None else "in-memory",
        }

    @staticmethod
    def _profile_to_query(user_profile: dict[str, Any]) -> str:
        return " ".join(
            [
                str(user_profile.get("role", "")),
                str(user_profile.get("skills", "")),
                str(user_profile.get("interests", "")),
                str(user_profile.get("learning_goals", "")),
            ]
        )
