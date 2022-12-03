import re
import unicodedata
from enum import Enum


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class Model(str, Enum):
    TINY_EN = 'tiny.en',
    TINY = 'tiny',
    BASE_EN = 'base.en',
    BASE = 'base',
    SMALL_EN = 'small.en',
    SMALL = 'small',
    MEDIUM_EN = 'medium.en',
    MEDIUM = 'medium',
    LARGE = 'large'
