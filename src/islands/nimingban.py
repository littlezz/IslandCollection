from .base import BaseIsland, NextPageJsonParameterMixin
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

    def get_div_content(self, tip):
        return tip['content']

    def get_div_response_num(self, tip):
        return tip['replyCount']

    def get_div_image(self, tip):
        return tip['image']

