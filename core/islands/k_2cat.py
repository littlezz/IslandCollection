from .base import BaseIsland, parse
from .mixins import NextPageStaticHtmlMixin
from itertools import islice
import re
__author__ = 'zz'


class KomicaIsland(NextPageStaticHtmlMixin, BaseIsland):
    _island_name = 'komica'
    _island_netloc = "homu.komica.org"

    _count_pattern = re.compile(r'(\d+)')

    def get_tips(self, pd):
        return pd.find_all('font', {'color': '#707070'})

    def get_div_content_text(self, tip):
        return tip.previous_sibling.text

    def get_div_link(self, tip):
        link = tip.find_previous('a').get('href')
        return parse.urljoin(self.current_url, link)

    def get_div_image(self, tip):
        position_font = tip.find_previous('font', {'color':'#cc1105'})
        for elm in islice(position_font.previous_elements, 0, 2):
            if elm.name == 'img':
                return elm.get('src')

        return ''


