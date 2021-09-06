from io import BytesIO
from typing import Union
import random

import requests
# from requests.models import requote_uri
import numpy as np
from PIL import Image



def get_file_by_url(url:str) -> Union[BytesIO, None]:
    r = requests.get(url)
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
    return get_theme_by_urlfile(url) == 'dark'