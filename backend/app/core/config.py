from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> repository root
ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    # One .env at the repo root, found regardless of the working directory.
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    allowed_origins: str = "http://localhost:3000"
    max_upload_mb: int = 10

    supabase_jwt_secret: str = ""

    model_registry_dir: str = "./models"

    llm_provider: str = "groq"
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_api_key: str = ""
    llm_model: str = "openai/gpt-oss-120b"
    llm_max_tokens: int = 1024
    llm_temperature: float = 0.2

    @property
    def models_dir(self) -> Path:
        p = Path(self.model_registry_dir)
        return p if p.is_absolute() else ROOT / p

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def is_dev(self) -> bool:
        return self.app_env == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
