import re
import os
from io import BytesIO
from typing import Union
from urllib.parse import urlparse, urljoin
import datetime as dt

from django.conf import settings

import requests
import numpy as np
from PIL import Image
from requests.exceptions import ConnectionError


def _set_cipher_set(reqs):
    reqs.packages.urllib3.disable_warnings()
    reqs.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    try:
        reqs.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    except AttributeError:
        pass
    return reqs


def _filter_by_ext(l:list, ext:str) -> list:
    return list(filter(lambda x: not x.lower().endswith(ext), l))


def _get_image_proportion(img: Image, top_limit=1) -> int:
    r = img.size[0] / img.size[1]
    if r > top_limit:
        return top_limit
    return r


def get_imageurl_from_site(url:str) -> Union[str, None]:
    try:
        r = requests.get(url)
    except ConnectionError:
        return None
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
    imgs = [i[0] for i in imgs if not i[0].lower().endswith('.svg')]
    imgs = [i for i in imgs if len(i) < 2048]
    return imgs[0] if imgs else None


# def download_image_from_site(url: str) -> Union[str, None]:
#     img_url = get_imageurl_from_site(url)
#     if not img_url:
#         return None
#     filepath = urlparse(url).path
#     filename = dt.datetime.now().strftime('%d.%m.%Y %H%M%S%f') + filepath
#     try:
#         req = requests.get(img_url)
#     except (MissingSchema, RequestException, ConnectionError):
#         return None
#     else:
#         with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as fw:
#             fw.write(req.content)
#     return urljoin(settings.MEDIA_URL, filepath)


def download_file_to_media(url: str) -> str:
    filepath = urlparse(url).path
    filename = os.path.split(filepath)[1]
    reqs = _set_cipher_set(requests) 
    req = reqs.get(url, verify=False)
    filename = dt.datetime.now().strftime('%d.%m.%Y %H%M%S%f') + filename.replace('%', '')
    with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as fw:
        fw.write(req.content)
    return urljoin(settings.MEDIA_URL, filename)


def get_file_by_url(url:str) -> Union[BytesIO, None]:
    try:
        r = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.RequestException):
        return None
    if r.status_code == 200:
        return BytesIO(r.content)
    return None


def img_estim(img, thrshld):
    is_light = np.mean(img) > thrshld
    return 'light' if is_light else 'dark'


def get_theme_by_urlfile(url:str) -> Union[str, None]:
    fobj = get_file_by_url(url)
    if fobj and not url.lower().endswith('.svg'):
        f = Image.open(fobj)
        return img_estim(f, 127)
    else:
        return None


def is_dark_theme(url: str) -> bool:
    print(url)
    return get_theme_by_urlfile(url) == 'dark'
