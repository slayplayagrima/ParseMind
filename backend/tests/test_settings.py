import pytest
from pydantic import ValidationError

from config.settings import Settings


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """
    Start each test from a known environment, ignoring any local .env file.
    """

    for name in [
        "GROQ_API_KEY",
        "ALLOWED_ORIGINS",
        "MAX_UPLOAD_MB",
        "UPSTASH_REDIS_REST_URL",
        "DEBUG",
    ]:
        monkeypatch.delenv(name, raising=False)

    monkeypatch.setenv("GROQ_API_KEY", "test-key")


def load() -> Settings:
    return Settings(_env_file=None)


def test_defaults():
    settings = load()

    assert settings.GROQ_MODEL == "llama-3.3-70b-versatile"
    assert settings.MAX_UPLOAD_MB == 4
    assert settings.DEBUG is False
    assert "https://parsemind.vercel.app" in settings.ALLOWED_ORIGINS


def test_missing_groq_key_fails_at_startup(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY")

    with pytest.raises(ValidationError, match="GROQ_API_KEY"):
        load()


def test_empty_groq_key_fails_at_startup(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "")

    with pytest.raises(ValidationError, match="GROQ_API_KEY"):
        load()


def test_invalid_number_fails_at_startup(monkeypatch):
    monkeypatch.setenv("MAX_UPLOAD_MB", "ten")

    with pytest.raises(ValidationError, match="MAX_UPLOAD_MB"):
        load()


def test_non_positive_limit_fails_at_startup(monkeypatch):
    monkeypatch.setenv("MAX_UPLOAD_MB", "0")

    with pytest.raises(ValidationError, match="MAX_UPLOAD_MB"):
        load()


def test_boolean_parsing(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")

    assert load().DEBUG is True


def test_origins_are_normalized(monkeypatch):
    monkeypatch.setenv(
        "ALLOWED_ORIGINS",
        " \"https://a.example.com/\" , 'https://b.example.com',,",
    )

    assert load().ALLOWED_ORIGINS == [
        "https://a.example.com",
        "https://b.example.com",
    ]


def test_upstash_url_trailing_slash_is_removed(monkeypatch):
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://x.upstash.io/")

    assert load().UPSTASH_REDIS_REST_URL == "https://x.upstash.io"
