import re

from django.http import request


def normalize_phrase(phrase: str) -> str:
    phrase = re.sub(r"\s{1,}", " ", phrase)
    phrase = phrase.strip()
    phrase = phrase.lower()
    return phrase


def get_alias(name: str) -> str:
    return normalize_phrase(name)


def extract_get_param(request: request) -> dict:
    result = {}
    for key in request.GET:
        val = request.GET.get(key)
        if val == 'None':
            val = None
        result[key] = val
    return result
