from bs4 import BeautifulSoup
import urllib.parse
from collections import namedtuple
__author__ = 'zz'



island_netloc_table = {}
island_class_table = {}
DivInfo = namedtuple('DivInfo', ['content', 'link', 'response_num'])

class IslandNotDetectError(Exception):
    pass


class IslandMeta(type):

    def __new__(cls, name, bases, ns):

        island_name = ns.get('_island_name')
        island_netloc = ns.get('_island_netloc')
        assert island_name, 'Not define _island_name in {} class'.format(name)
        assert island_netloc, 'Not define _island_netloc in {} class'.format(name)

        ns.pop('_island_name')
        ns.pop('_island_netloc')

        # rename subclass method
        for name in ns:
            if not name.startswith('_'):
                value = ns.pop(name)
                ns['_' + island_name + '_' + name] = value

        # register island and netloc
        island_netloc_table.update({island_netloc: island_name})

        # register island class
        island_class_table.update({island_name: cls})

        return super().__new__(cls, name, bases, ns)

class EmptyMeta(type):
    pass



class BaseIsland:
    _island_name = ''
    _island_netloc = ''

    @staticmethod
    def island_split_page(bs):
        """
        must return DivInfo object
        """
        raise NotImplementedError



class ADNMBIsland(BaseIsland, metaclass=IslandMeta):
    """
    养老岛
    """
    _island_name = 'adnmb'
    _island_netloc = 'h.adnmb.com'

    @staticmethod
    def island_split_page(bs):
        pass


class NMBIsland(BaseIsland, metaclass=IslandMeta):
    """
    主岛
    """
    _island_name = 'nimingban'
    _island_netloc = 'h.nimingban.com'


    @staticmethod
    def island_split_page(bs):
        pass



class Analyzer:

    def __init__(self, url, data:bytes):
        self.url = url
        self.bs = BeautifulSoup(data)
        self.island_name = self.determine_island_name()
        self._island = island_class_table[self.island_name]()
        self.divs = self.split_page()

    def determine_island_name(self):
        netloc = urllib.parse.urlparse(self.url)
        for url, name in island_netloc_table:
            if url == netloc:
                return name
        else:
            raise IslandNotDetectError


    def _call_method(self, suffix):
        """
        通过岛名调用相应的方法
        """
        method_name = '_' + self.island_name + '_' + suffix
        return getattr(self._island, method_name)()

    def split_page(self):
        return self._call_method('island_split_page')

    def filter_divs(self, response_num, *args):
        return [div for div in self.divs if div.response_num>response_num]

