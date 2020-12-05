#
# Created by maks5507 (me@maksimeremeev.com)
#


import requests
from bs4 import BeautifulSoup
import unicodedata


class URLParser:

    @staticmethod
    def parse(url):
        try:
            request = requests.get(url)
            content = request.content.decode()
            soup = BeautifulSoup(content, "lxml")
            text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
            text = unicodedata.normalize('NFKD', text)
            return text
        except Exception:
            return ''
