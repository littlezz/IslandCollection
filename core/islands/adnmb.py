from core.islands.base import BaseIsland
from core.islands.mixins import NextPageStaticHtmlMixin

__author__ = 'zz'


class ADNMBIsland(NextPageStaticHtmlMixin, BaseIsland):
    """
    养老岛
    """
    _island_name = 'adnmb'
    _island_netloc = 'h.adnmb.com'


    def get_tips(self, pd):
        return pd.find_all('span', class_='warn_txt2')

    def get_div_link(self, tip):
        tag_a = tip.parent.find('a', class_='qlink')
        if tag_a:
            return tag_a.get('href')
        else:
            return ''

    def get_div_content_text(self, tip):
        content_tag = tip.parent.find('div', class_='quote')
        if content_tag:
            return content_tag.text
        else:
            return ''

    def get_div_image(self, tip):
        img_tag =  tip.parent.find('img', class_='img')
        if img_tag:
            return img_tag.get('src')
        else:
            return ''

    @staticmethod
    def init_start_url(start_url):
        """
        'http://h.adnmb.com/home/forum/showt/id/1.html' ->
        'http://h.adnmb.com/home/forum/showt/id/1/page/1.html'
        """
        if 'page' not in start_url:
            base, suffix = start_url.rsplit('.', 1)
            start_url = base + '/page/1' + '.' + suffix

        return start_url


