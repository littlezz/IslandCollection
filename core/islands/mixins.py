import os.path
import re
from urllib import parse
import requests

__author__ = 'zz'


class NextPageStaticHtmlMixin:
    _static_count_pattern = re.compile(r'(\d+)')

    def get_next_page(self):
        path = parse.urlparse(self.current_url).path
        basename = os.path.basename(path)
        # static html basename must be d.htm(l)
        current_page_num, suffix  = basename.split('.')

        if current_page_num == 'index':
            current_page_num = 0

        next_page_num = int(current_page_num) + 1
        next_basename = '.'.join((str(next_page_num), suffix))


        # In [73]: parse.urljoin('gg/h.html','gg.html')
        # Out[73]: 'gg/gg.html'
        return parse.urljoin(self.current_url, next_basename), next_page_num

    def next_page_valid(self, next_page_url, page_num):
        return requests.head(next_page_url).ok


class NextPageJsonParameterMixin:
    _has_next_page = True


    def get_max_page(self):
        return int(self.pd['page']['size'])

    def get_next_page(self):
        max_page = self.get_max_page()


        base_url, query = parse.splitquery(self.current_url)
        if not query:
            query='page=0'

        _, count = parse.parse_qsl(query)[0]
        count = int(count) + 1
        if count > max_page:
            self._has_next_page = False

        next_query = parse.urlencode({'page': count})
        url = base_url+ '?' + next_query
        return url, count


    def next_page_valid(self, url, page_num):
        return self._has_next_page