from .base import BaseIsland
from core.islands.mixins import NextPageJsonParameterMixin
from urllib import parse
__author__ = 'zz'


class NiMingBanIsland(NextPageJsonParameterMixin, BaseIsland):
    _island_name = 'nimingban'
    _island_netloc = 'h.nimingban.com'
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
        return tip['image']

    @staticmethod
    def init_start_url(start_url):
        if '.json' not in start_url:
            parts = parse.urlsplit(start_url)
            path = parts.path + '.json'
            return parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
