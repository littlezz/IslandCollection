from src.islands.base import BaseIsland

__author__ = 'zz'


class ADNMBIsland(BaseIsland):
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
            return None

    def get_div_content(self, tip):
        content_tag = tip.parent.find('div', class_='quote')
        if content_tag:
            return content_tag.text
        else:
            return None

