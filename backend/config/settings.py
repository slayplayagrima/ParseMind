import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application configuration.
    """

    APP_NAME = "ContractMind AI"

    VERSION = "1.0.0"

    DEBUG = os.getenv(
        "DEBUG",
        "False",
    ).lower() == "true"

    HOST = os.getenv(
        "HOST",
        "127.0.0.1",
    )

    PORT = int(
        os.getenv(
            "PORT",
            "8000",
        )
    )

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
    )

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile",
    )

    origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,https://parsemind-production.up.railway.app,https://parsemind.vercel.app"
)

    ALLOWED_ORIGINS = [
    origin.strip()
    for origin in origins.split(",")
    if origin.strip()
]

settings = Settings()