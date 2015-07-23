from bs4 import BeautifulSoup
import urllib.parse
__author__ = 'zz'



island_table = {
    'h.adnmb.com': 'adnmb',
    'h.nimingban.com': 'nimingban'
}


class IslandNotDetectError(Exception):
    pass


class Analyzer:

    def __init__(self, url, data:bytes):
        self.url = url
        self.bs = BeautifulSoup(data)
        self.island_name = self.determine_island_name()

    def determine_island_name(self):
        netloc = urllib.parse.urlparse(self.url)
        for url, name in island_table:
            if url == netloc:
                return name
        else:
            raise IslandNotDetectError


    def get_response_num(self):
        method_name = '_' + self.island_name + 'response_num'
        getattr(self, method_name)()

    def _adnmb_response_num(self):
        pass

    def _nimingban_response_num(self):
        pass