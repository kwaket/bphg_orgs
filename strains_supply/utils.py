import re

def normalize_phrase(phrase: str) -> str:
    phrase = re.sub(r"\s{1,}", " ", phrase)
    phrase = phrase.strip()
    phrase = phrase.lower()
    return phrase


def get_alias(name: str) -> str:
    return normalize_phrase(name)

