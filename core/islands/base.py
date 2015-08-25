from collections import namedtuple
import re
from urllib import parse
from bs4 import BeautifulSoup
from core import sanitize
from core.structurers import ResultInfo
__author__ = 'zz'


island_netloc_table = {}
island_class_table = {}


DivInfo = namedtuple('DivInfo', ['content', 'link', 'response_num', 'image'])


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
    _island_scheme = 'http'
    _count_pattern = re.compile(r'\s(\d+)\s')
    _static_root = ''
    json_data = False
    show_image = True

    def __init__(self, current_url, res):
        if not self.json_data:
            self.pd = BeautifulSoup(res.content)
        else:
            self.pd = res.json()

        self.current_url = current_url

    @property
    def current_page_url(self):
        url = getattr(self, '_current_page_url', self.current_url)
        return url

    @current_page_url.setter
    def current_page_url(self, value):
        self._current_page_url = value


    @property
    def root_url(self):
        return parse.urlunsplit((self._island_scheme, self._island_netloc, '', '', ''))

    @property
    def static_root(self):
        return self._static_root or self.root_url

    def get_div_response_num(self, tip):
        """
        return response count
        """
        text = tip.text
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

    def get_div_content_text(self, tip):
        """
        return content
        """
        raise NotImplementedError

    def get_div_image(self, tip):
        raise NotImplementedError

    def get_next_page(self):
        """
        return (url, page_num)
        """
        raise NotImplementedError

    def next_page_valid(self, next_page_url, page_num):
        raise NotImplementedError

    def next_page(self, max_page, current_page_url=None):
        """
        return next page url
        """
        if current_page_url:
            self.current_page_url = current_page_url

        url, page_num = self.get_next_page()
        if url and page_num <= max_page and self.next_page_valid(url, page_num):
            return url
        else:
            return None

    def island_split_page(self):
        """
        must return list of ResultInfo instance
        """
        results = []

        pd = self.pd
        tips = self.get_tips(pd)
        for tip in tips:
            response_num = int(self.get_div_response_num(tip))
            link = self.complete_link(self.get_div_link(tip))
            text = self.get_div_content_text(tip)
            text = sanitize.clean(text)
            image_url = self.get_div_image(tip) if self.show_image else ''
            # image_url = self.complete_link(image_url)

            result = ResultInfo(text=text, link=link, response_num=response_num, image_url=image_url)
            results.append(result)

        return results


    def complete_link(self, url, root_url=None):
        if not url:
            return ''

        if root_url is None:
            root_url = self.root_url

        return parse.urljoin(root_url, url)


    def complete_image_link(self, url):
        if url.startswith('/'):
            url = url[1:]
        return self.complete_link(url, root_url=self.static_root)


    @staticmethod
    def init_start_url(start_url):
        """
        :param start_url:
        :return:返回初始化的url， 对特别的首页加上是加上分页后缀
        """
        return start_url


