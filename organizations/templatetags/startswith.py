import os

from django import template


register = template.Library()

@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, (str, os.PathLike)):
        return text.startswith(starts)
    return False
