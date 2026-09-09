from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@dataclass
class Settings:
    pg_host: str = os.getenv("PG_HOST", "localhost")
    pg_port: int = int(os.getenv("PG_PORT", "5432"))
    pg_database: str = os.getenv("PG_DATABASE", "postgres")
    pg_user: str = os.getenv("PG_USER", "postgres")
    pg_password: str = os.getenv("PG_PASSWORD", "postgres")

    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))

    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

    igot_api_base_url: str = os.getenv("IGOT_API_BASE_URL", "")

    similarity_top_k: int = int(os.getenv("SIMILARITY_TOP_K", "5"))
    max_quiz_questions: int = int(os.getenv("MAX_QUIZ_QUESTIONS", "5"))


settings = Settings()
