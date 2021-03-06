from .base import BaseIsland
from core.islands.mixins import NextPageJsonParameterMixin
from urllib import parse
__author__ = 'zz'


class KoukokuIsland(NextPageJsonParameterMixin, BaseIsland):
    """
    光驱岛
    """
    _island_name = 'kukuku'
    _island_netloc = 'kukuku.cc'
    _static_root = 'http://static.koukuko.com/h/'
    json_data = True

    def get_tips(self, pd):

        return [thread for thread in pd['data']['threads']]

    def get_div_link(self, tip):
        thread_id = tip['id']
        suffix = 't' + '/' + str(thread_id)
        return parse.urljoin(self.root_url, suffix)

    def get_div_content_text(self, tip):
        return tip['content']

    def get_div_response_num(self, tip):
        return tip['replyCount']

    def get_div_image(self, tip):
        thumb = tip['thumb']
        return self.complete_image_link(thumb)

    @staticmethod
    def init_start_url(start_url):
        if '.json' not in start_url:
            parts = parse.urlsplit(start_url)
            path = parts.path + '.json'
            return parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


class OldKoukukoIsland(KoukokuIsland):
    """
    旧光驱岛域名
    """
    _island_netloc = 'h.koukuko.com'
    _island_name = 'old_koukuko'
