from bs4 import BeautifulSoup
import urllib.parse
__author__ = 'zz'



island_table = {}


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
        island_table.update({island_netloc: island_name})

        return super().__new__(cls, name, bases, ns)







class ADNMBIslandMixin(metaclass=IslandMeta):
    """
    养老岛
    """
    _island_name = 'adnmb'
    _island_netloc = 'h.adnmb.com'

    def island_get_response_num(self):
        pass

    def island_split_page(self):
        pass


class NMBIslandMixin(metaclass=IslandMeta):
    """
    主岛
    """
    _island_name = 'nimingban'
    _island_netloc = 'h.nimingban.com'

    def island_get_response_num(self):
        pass

    def island_split_page(self):
        pass



class Analyzer(ADNMBIslandMixin, NMBIslandMixin):

    def __init__(self, url, data:bytes):
        self.url = url
        self.bs = BeautifulSoup(data)
        self.island_name = self.determine_island_name()
        self.divs = self.split_page()

    def determine_island_name(self):
        netloc = urllib.parse.urlparse(self.url)
        for url, name in island_table:
            if url == netloc:
                return name
        else:
            raise IslandNotDetectError


    def _call_method(self, suffix):
        """
        通过岛名调用相应的方法
        """
        method_name = '_' + self.island_name + '_' + suffix
        return getattr(self, method_name)()

    def split_page(self):
        return self._call_method('island_split_page')

    def get_response_num(self):
        return self._call_method('island_get_response_num')

