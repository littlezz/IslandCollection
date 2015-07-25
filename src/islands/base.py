from collections import namedtuple
import re
from urllib import parse
from bs4 import BeautifulSoup

__author__ = 'zz'


island_netloc_table = {}
island_class_table = {}


DivInfo = namedtuple('DivInfo', ['content', 'link', 'response_num'])


class IslandNotDetectError(Exception):
    pass





class IslandMeta(type):

    def __init__(cls, name, bases, ns):
        if name != 'BaseIsland':
            island_name = ns.get('_island_name')
            island_netloc = ns.get('_island_netloc')
            assert island_name , 'Not define _island_name in {} class'.format(name)
            assert island_netloc , 'Not define _island_netloc in {} class'.format(name)

             # register island and netloc
            island_netloc_table.update({island_netloc: island_name})

            # register island class
            island_class_table.update({island_name: cls})

        super().__init__(name, bases, ns)


class BaseIsland(metaclass=IslandMeta):

    _island_name = ''
    _island_netloc = ''
    _count_pattern = re.compile(r'\s(\d+)\s')
    json_data = False

    def __init__(self, current_url, res):
        if not self.json_data:
            self.pd = BeautifulSoup(res.content)
        else:
            self.pd = res.json()

        self.current_url = current_url


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



    def get_tips(self, pd):
        """
        :param pd: a BeautifulSoup object or json object, determine by json_data
        return a list of  object that contain tips content
        """
        raise NotImplementedError

    def get_div_link(self, tip):
        """
        tip is a BeautifulSoup object contain response tip
        return the link href string, eg, 'http://xx.com', or /xx/xx.html """
        raise NotImplementedError

    def get_div_content(self, tip):
        """
        return content
        """
        raise NotImplementedError

    def get_next_page_url(self):
        raise NotImplementedError

    def next_page_valid(self, next_page_url):
        raise NotImplementedError

    def next_page(self):
        """
        return next page url
        """
        next_page_url = self.get_next_page_url()
        if self.next_page_valid(next_page_url):
            return next_page_url
        else:
            return None

    def island_split_page(self):
        """
        must return DivInfo object
        """
        result = []

        pd = self.pd
        tips = self.get_tips(pd)
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

