from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default='development', alias='APP_ENV')
    chroma_base_dir: str = Field(default='./chroma_db', alias='CHROMA_BASE_DIR')
    chunking_strategy: str = Field(default='heading_aware', alias='CHUNKING_STRATEGY')
    embedding_model: str = Field(default='all-MiniLM-L6-v2', alias='EMBEDDING_MODEL')
    llm_mode: str = Field(default='mock', alias='LLM_MODE')
    llm_base_url: str | None = Field(default=None, alias='LLM_BASE_URL')
    llm_api_key: str | None = Field(default=None, alias='LLM_API_KEY')
    llm_model: str | None = Field(default=None, alias='LLM_MODEL')
    max_context_chars: int = Field(default=6000, alias='MAX_CONTEXT_CHARS')
    retrieval_k: int = Field(default=5, alias='RETRIEVAL_K')
    topk_min_score: float = Field(default=0.30, alias='TOPK_MIN_SCORE')
    threshold_min_score: float = Field(default=0.45, alias='THRESHOLD_MIN_SCORE')
    near_duplicate_threshold: float = Field(default=0.90, alias='NEAR_DUPLICATE_THRESHOLD')
    reference_date: str = Field(default='2026-10-10', alias='REFERENCE_DATE')

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @property
    def chroma_dir(self) -> Path:
        return Path(self.chroma_base_dir).resolve()

    def validate_llm_configuration(self) -> None:
        if self.llm_mode == 'mock':
            return
        if self.llm_mode != 'openai_compatible':
            raise ValueError(f'Unsupported LLM_MODE: {self.llm_mode}. Use mock or openai_compatible.')
        required = {
            'LLM_BASE_URL': self.llm_base_url,
            'LLM_API_KEY': self.llm_api_key,
            'LLM_MODEL': self.llm_model,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(
                'Real LLM mode selected but missing required configuration: ' + ', '.join(missing)
            )


settings = Settings()
settings.validate_llm_configuration()
