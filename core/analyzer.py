from urllib import parse
from .islands import island_netloc_table, island_class_table, IslandNotDetectError
__author__ = 'zz'


def determine_island_name(url):
    netloc = parse.urlparse(url).netloc
    for url, name in island_netloc_table.items():
        if url == netloc:
            return name
    else:
        raise IslandNotDetectError('netloc is {}'.format(netloc))


def init_start_url(url):
    island_name = determine_island_name(url)
    island_class = island_class_table[island_name]
    return island_class.init_start_url(url)


def validate_url(url):
    """
    :param url:
    :return:status code

    status code   --->  info
    ---------------------------
        0               success
        1               no scheme
        2               island not support


    """
    p = parse.urlparse(url)
    if not p.scheme:
        return 1

    try:
        determine_island_name(url)
    except IslandNotDetectError:
        return 2
    else:
        return 0


class Analyzer:

    def __init__(self, res, max_page):
        self.url = res.url
        self.res = res
        self.max_page = max_page
        self.island_name = determine_island_name(self.url)
        self._island = self._create_island_obj()
        self.divs = self.split_page()

    def _create_island_obj(self):
        island_class = island_class_table[self.island_name]
        return island_class(self.url, self.res)

    def split_page(self):
        return self._island.island_split_page()

    def filter_divs(self, response_gt, *args):
        return [div for div in self.divs if div.response_num > response_gt]

    def next_page(self, current_page_url=None):
        return self._island.next_page(self.max_page, current_page_url)


def get_thread_info(url, res):
    island_class = island_class_table[determine_island_name(url)]
    info_result = island_class.get_thread_info(url, res)
    return info_result
