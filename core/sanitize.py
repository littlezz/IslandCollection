import re
from urllib import parse
__author__ = 'zz'

# match <br> \n \r
_clean_pattern = re.compile(r'<br\s?/?>|\n|\r')

_replace_pattern = re.compile(r'nbsp;?')


def clean(text):
    text = _clean_pattern.sub('', text)
    text = _replace_pattern.sub(' ', text)
    return text


def url_clean(url):
    url, _ = parse.urldefrag(url)
    return url