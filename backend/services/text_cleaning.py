import re


def clean_text(text: str) -> str:
    """
    Normalize extracted text: unify line endings, collapse runs of
    spaces and tabs, and keep at most one blank line between blocks.
    """

    text = re.sub(r"\r\n?", "\n", text)

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
