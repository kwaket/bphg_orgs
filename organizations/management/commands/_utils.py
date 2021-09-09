import re
from urllib.parse import urljoin
from io import BytesIO
from typing import Union
import random

import requests
# from requests.models import requote_uri
import numpy as np
from PIL import Image
from requests import exceptions


def _filter_by_ext(l:list, ext:str) -> list:
    return list(filter(lambda x: not x.lower().endswith(ext), l))


def _get_image_proportion(img: Image, top_limit=1) -> int:
    r = img.size[0] / img.size[1]
    if r > top_limit:
        return top_limit
    return r


def get_imageurl_from_site(url:str) -> str:
    r = requests.get(url)
    imgs = re.findall(r'<img.*?>', str(r.content.decode('utf-8')))
    imgs = [re.findall(r'src\s?=\s?["\']{1}(.*?)["\']{1}\s', i) for i in imgs]
    imgs = [item for sublist in imgs for item in sublist]
    imgs2 = re.findall(r'background\-image:\s?url\((.*)\)', str(r.content.decode('utf-8')))
    imgs2 = [i for i in imgs2 if i]
    imgs.extend(imgs2)
    imgs = [i.strip('"') for i in imgs]
    imgs = [i.strip("'") for i in imgs]
    imgs = _filter_by_ext(imgs, '.svg')
    imgs = _filter_by_ext(imgs, '.png')
    imgs = _filter_by_ext(imgs, '.gif')
    imgs = [i for i in imgs if i]
    imgs = [urljoin(url, i) for i in imgs if not i.startswith('http://')]
    imgs = [i for i in imgs if not i.lower().endswith('.svg')]
    imgs = [i for i in imgs if not i.lower().endswith('.gif')]
    imgs = [(url, get_file_by_url(url)) for url in imgs]
    imgs = [(u, l) for (u, l) in imgs if u is not None and l is not None]
    imgs_ = [(u, i) for u, i in imgs if Image.open(i).size[0] > 500 and _get_image_proportion(Image.open(i)) > .5]
    imgs = imgs_ if imgs_ else imgs
    imgs = [(url, _get_image_proportion(Image.open(b)) , Image.open(b).size[0] * Image.open(b).size[1]) for (url, b) in imgs]

    imgs.sort(key=lambda x: -x[1])
    imgs = [i[0] for i in imgs]
    return imgs[0] if imgs else None


def get_file_by_url(url:str) -> Union[BytesIO, None]:
    print(url)
    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        return None
    except requests.exceptions.RequestException:
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
