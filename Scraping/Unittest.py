# Unittest.py
import unittest
from scrapy.http import HtmlResponse, Request
from twisted.internet import defer
from twisted.trial import unittest as twisted_unittest
from scrapy.crawler import CrawlerRunner
from .Spider import MySpider



class MySpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = MySpider(init_data=[{'region': 'euw1', 'summonerName': 'leaguify'}])

    def _mock_response(self, url='http://www.example.com', meta=None):
        if meta is None:
            meta = {}
        return HtmlResponse(url=str(url), body='', encoding='utf-8', request=Request(url=url, meta=meta))

    def test_parse(self):
        response = self._mock_response(url='https://u.gg/lol/profile/euw1/leaguify/champion-stats')
        results = self.spider.parse(response)
        print(results)
        # You can now check whether the 'parse' function behaves as expected,
        # e.g. whether it yields the expected items or requests.
