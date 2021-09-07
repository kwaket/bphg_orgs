import re
from urllib.parse import urljoin
from io import BytesIO
from typing import Union
import random

import requests
# from requests.models import requote_uri
import numpy as np
from PIL import Image


def _filter_by_ext(l:list, ext:str) -> list:
    return list(filter(lambda x: not x.lower().endswith(ext), l))


def get_imageurl_from_site(url:str) -> str:
    r = requests.get(url)
    imgs = re.findall(r'<img.*?>', str(r.content))
    imgs = [re.findall(r'src\s?=\s?["\']{1}(.*?)["\']{1}\s', i) for i in imgs]
    imgs = [_filter_by_ext(i, '.svg') for i in imgs]
    imgs = [urljoin(url, i[0]) for i in imgs if i]
    imgs = [i for i in imgs if not i[0].lower().endswith('.svg')]
    return imgs[0]


def get_file_by_url(url:str) -> Union[BytesIO, None]:
    print(url)
    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        return None

    if r.status_code == 200:
        return BytesIO(r.content)
    return None


def img_estim(img, thrshld):
    is_light = np.mean(img) > thrshld
    return 'light' if is_light else 'dark'


def get_theme_by_urlfile(url:str) -> str:
    fobj = get_file_by_url(url)
    if fobj:
        f = Image.open(fobj)
        return img_estim(f, 127)
    else:
        return None


def is_dark_theme(url: str) -> bool:
    print(url)
    return get_theme_by_urlfile(url) == 'dark'
