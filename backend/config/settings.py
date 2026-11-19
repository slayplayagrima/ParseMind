from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

DEFAULT_ALLOWED_ORIGINS = (
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "http://localhost:3000,"
    "http://127.0.0.1:3000,"
    "https://parsemind.vercel.app"
)


class Settings(BaseSettings):
    """
    Application configuration, loaded from environment variables
    and the .env file. Invalid or missing required values fail
    at startup instead of on the first request.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "ParseMind"

    VERSION: str = "1.0.0"

    DEBUG: bool = False

    HOST: str = "127.0.0.1"

    PORT: int = Field(default=8000, gt=0, lt=65536)

    GROQ_API_KEY: str = Field(min_length=1)

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    LLM_TIMEOUT_SECONDS: float = Field(default=30, gt=0)

    LLM_MAX_RETRIES: int = Field(default=2, ge=0)

    # Vercel Functions reject request bodies over 4.5 MB, so uploads are
    # capped at 4 MB to leave room for multipart overhead.
    MAX_UPLOAD_MB: int = Field(default=4, gt=0)

    MAX_PDF_PAGES: int = Field(default=50, gt=0)

    UPSTASH_REDIS_REST_URL: str = ""

    UPSTASH_REDIS_REST_TOKEN: str = ""

    RATE_LIMIT_REQUESTS: int = Field(default=10, gt=0)

    RATE_LIMIT_WINDOW_SECONDS: int = Field(default=3600, gt=0)

    ALLOWED_ORIGINS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: _split_origins(DEFAULT_ALLOWED_ORIGINS),
    )

    @field_validator("UPSTASH_REDIS_REST_URL")
    @classmethod
    def _strip_trailing_slash(cls, value: str) -> str:
        return value.strip().rstrip("/")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def _parse_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return _split_origins(value)
        return value


def _split_origins(raw: str) -> list[str]:
    """
    Split a comma-separated origin list, tolerating stray quotes,
    spaces and trailing slashes copied from hosting dashboards.
    """

    return [
        origin.strip().strip('"').strip("'").rstrip("/")
        for origin in raw.split(",")
        if origin.strip()
    ]


settings = Settings()
