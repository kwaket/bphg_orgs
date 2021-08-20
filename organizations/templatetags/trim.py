import os

from django import template


register = template.Library()


def _trim(text, symbol):
    if isinstance(text, (str, os.PathLike)):
        if text.startswith(symbol):
            text = text[1:]
        if text.endswith(symbol):
            text = text[:-1]
        return text
    return False


@register.filter('trim')
def trim(text, symbol):
    return _trim(text, symbol)


@register.filter('trimdash')
def trimdash(text):
    return _trim(text, '-')
