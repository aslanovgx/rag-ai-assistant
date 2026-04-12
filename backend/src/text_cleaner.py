import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text to improve readability and embedding quality.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()