from .base import BaseIsland, parse
from .mixins import NextPageStaticHtmlMixin
__author__ = 'zz'


class KomicaIsland(NextPageStaticHtmlMixin, BaseIsland):
    _island_name = 'komica'
    _island_netloc = "homu.komica.org"


    def get_tips(self, pd):
        return pd.find_all('font', {'color': '#707070'})

    def get_div_content_text(self, tip):
        return tip.previous_sibling.text

    def get_div_link(self, tip):
        link = tip.find_previous('a').get('href')
        return parse.urljoin(self.current_url, link)

    def get_div_image(self, tip):
        # magic!
        return list(tip.previous_elements)[21].get('src', '')



