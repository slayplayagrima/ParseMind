import json
import logging
from typing import Any
from config.settings import settings

from groq import Groq

logger = logging.getLogger(__name__)
print("Loaded key:", settings.GROQ_API_KEY)
DEFAULT_MODEL = settings.GROQ_MODEL

API_KEY = settings.GROQ_API_KEY

DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 4096

JSONDict = dict[str, Any]

_client: Groq | None = None


def get_client() -> Groq:
    """
    Returns a singleton Groq client.
    """

    global _client

    if _client is None:

        if not API_KEY:
            logger.error("GROQ_API_KEY not found.")
            raise RuntimeError(
                "GROQ_API_KEY is missing. Check your environment."
            )

        logger.info("Initializing Groq client...")

        _client = Groq(api_key=API_KEY)

    return _client


def _chat_completion(
    prompt: str,
    temperature: float = DEFAULT_TEMPERATURE,
) -> str:
    """
    Send a prompt to Groq and return the generated response.
    """

    client = get_client()

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature,
            max_tokens=DEFAULT_MAX_TOKENS,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("Groq returned an empty response.")

        return content.strip()

    except Exception as exc:

        logger.exception(
            "Error communicating with Groq."
    )

        message = str(exc)

        if "rate_limit" in message.lower():
            raise RuntimeError(
            "RATE_LIMIT_EXCEEDED"
            ) from exc

        raise RuntimeError(
            f"LLM request failed: {message}"
        ) from exc


def generate_text_response(prompt: str) -> str:
    """
    Generate a plain text response from the language model.
    """

    logger.info(
        "Generating text response using %s",
        DEFAULT_MODEL,
    )

    return _chat_completion(prompt)


def generate_json_response(prompt: str) -> JSONDict:
    """
    Generate and parse a JSON response from the language model.
    """

    logger.info(
        "Generating JSON response using %s",
        DEFAULT_MODEL,
    )

    json_prompt = f"""
You must respond ONLY with valid JSON.

Do not include markdown.

Do not include explanations.

{prompt}
"""

    response = _chat_completion(json_prompt)

    # Remove accidental Markdown fences if present
    response = response.strip()

    if response.startswith("```"):
        response = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        return json.loads(response)

    except json.JSONDecodeError as exc:
        logger.exception("Model returned invalid JSON.")
        raise ValueError(
            f"Invalid JSON returned by model:\n{response}"
        ) from exc


__all__ = [
    "DEFAULT_MODEL",
    "generate_text_response",
    "generate_json_response",
]