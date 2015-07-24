from bs4 import BeautifulSoup
import urllib.parse
from collections import namedtuple
import re
from urllib import parse
__author__ = 'zz'



island_netloc_table = {}
island_class_table = {}
DivInfo = namedtuple('DivInfo', ['content', 'link', 'response_num'])


class IslandNotDetectError(Exception):
    pass






class IslandMeta(type):

    def __init__(cls, name, bases, ns):
        island_name = ns.get('_island_name')
        island_netloc = ns.get('_island_netloc')
        assert island_name, 'Not define _island_name in {} class'.format(name)
        assert island_netloc, 'Not define _island_netloc in {} class'.format(name)

         # register island and netloc
        island_netloc_table.update({island_netloc: island_name})

        # register island class
        island_class_table.update({island_name: cls})

        super().__init__(name, bases, ns)





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
        return a list of BeautifulSoup object that contain tips content
        """
        raise NotImplementedError

    def get_div_link(self, bs):
        """
        return the link href string, eg, 'http://xx.com', or /xx/xx.html """
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
        for tip in tips:
            response_num = int(self.get_div_response(tip.text))
            link = self.complete_link(self.get_div_link(tip))
            content = self.get_div_content(tip)
            div = DivInfo(content=content, link=link, response_num=response_num)
            result.append(div)

        return result


    def complete_link(self, url):
        base = 'http://' + self._island_netloc
        return parse.urljoin(base, url)




class ADNMBIsland(BaseIsland, metaclass=IslandMeta):
    """
    养老岛
    """
    _island_name = 'adnmb'
    _island_netloc = 'h.adnmb.com'


    def get_tips(self, bs):
        return bs.find_all('span', class_='warn_txt2')

    def get_div_link(self, bs):
        tag_a = bs.parent.find('a', class_='qlink')
        if tag_a:
            return tag_a.get('href')
        else:
            return None

    def get_div_content(self, bs):
        content_tag = bs.parent.find('div', class_='quote')
        if content_tag:
            return content_tag.text
        else:
            return None



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
        netloc = urllib.parse.urlparse(self.url).netloc
        for url, name in island_netloc_table.items():
            if url == netloc:
                return name
        else:
            raise IslandNotDetectError('netloc is {}'.format(netloc))



    def split_page(self):
        return self._island.island_split_page(self.bs)

    def filter_divs(self, response_gt, *args):
        return [div for div in self.divs if div.response_num>response_gt]

