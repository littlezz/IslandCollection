import socks
import socket
import requests
from urllib import parse
from functools import partial
__author__ = 'zz'


stand_socket = socket.socket
_requests_get = requests.get


def set_proxy(addr=None, port=None):
    if not addr:
        socket.socket = stand_socket
        requests.get = _requests_get

    else:
        proxy = parse.urlsplit(addr)
        if proxy.scheme.lower() in ('http', 'https'):
            proxies = {
                'http': ':'.join((addr, port))
            }
            requests.get = partial(requests.get, proxies=proxies)
        elif proxy.scheme.lower() == 'socks5':
            socks.set_default_proxy(socks.SOCKS5, addr, port)
            socket.socket = socks.socksocket
        else:
            print('Unknown scheme')



