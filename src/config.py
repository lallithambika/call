from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Call Center Compliance AI"
    app_env: str = "development"
    api_key: str = Field(default="change-me", alias="X_API_KEY")

    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    whisper_model: str = "small"
    llm_provider: str = "huggingface"  # huggingface | openai
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    hf_summarizer_model: str = "facebook/bart-large-cnn"
    hf_zero_shot_model: str = "MoritzLaurer/ModernBERT-large-zeroshot-v2.0"
    hf_sentiment_model: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    chroma_persist_directory: str = "./data/chroma"
    task_timeout_seconds: int = 180

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache

def get_settings() -> Settings:
    return Settings()
