from urllib import parse
from .islands import island_netloc_table, island_class_table, IslandNotDetectError
__author__ = 'zz'





class Analyzer:

    def __init__(self, res, max_page):
        self.url = res.url
        self.res = res
        self.max_page = max_page
        self.island_name = self.determine_island_name()
        self._island = self._create_island_obj()
        self.divs = self.split_page()

    def determine_island_name(self):
        netloc = parse.urlparse(self.url).netloc
        for url, name in island_netloc_table.items():
            if url == netloc:
                return name
        else:
            raise IslandNotDetectError('netloc is {}'.format(netloc))


    def _create_island_obj(self):
        island_class = island_class_table[self.island_name]
        return island_class(self.url, self.res)

    def split_page(self):
        return self._island.island_split_page()

    def filter_divs(self, response_gt, *args):
        return [div for div in self.divs if div.response_num>response_gt]

    def next_page(self):
        return self._island.next_page(self.max_page)

