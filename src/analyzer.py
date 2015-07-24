from bs4 import BeautifulSoup
import urllib.parse
from collections import namedtuple
import re

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



class BaseIsland:

    _island_name = ''
    _island_netloc = ''
    _count_pattern = re.compile(r'\s(\d+)\s')

    def get_div_response(self, text):
        """
        return response count from text
        """
        match = self._count_pattern.search(text)
        if match:
            return match.group(1)
        else:
            # may be the text is 'sega'
            return 0



    def get_tips(self, bs):
        """
        BeautifulSoup object that contain tips content
        """
        raise NotImplementedError

    def get_div_link(self, bs):
        """
        return the link href string, eg, 'http://xx.com'
        """
        raise NotImplementedError

    def get_div_content(self, bs):
        """
        return content
        """
        raise NotImplementedError

    def island_split_page(self, bs):
        """
        must return DivInfo object
        """
        result = []

        tips = self.get_tips(bs)
        for tip in tips
            response_num = self.get_div_response(tip.text)
            link = self.get_div_link(tip)
            content = self.get_div_content(tip)
            div = DivInfo(content=content, link=link, response_num=response_num)
            result.append(div)

        return result





class ADNMBIsland(BaseIsland, metaclass=IslandMeta):
    """
    养老岛
    """
    _island_name = 'adnmb'
    _island_netloc = 'h.adnmb.com'






class NMBIsland(BaseIsland, metaclass=IslandMeta):
    """
    主岛
    """
    _island_name = 'nimingban'
    _island_netloc = 'h.nimingban.com'





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

