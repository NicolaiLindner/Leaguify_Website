import re

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem




class DataPipeline:
    def process_item(self, item, spider):
        """
        checks if champion-summoner combintion is needed and if so, adds it to the database
        :param item:
        :param spider:
        :return:
        """
        adapter = ItemAdapter(item)
        url = adapter.get("url")
        match = re.match(r"https:\/\/u\.gg\/lol\/profile\/(.+)\/(.+)\/champion-stats", url)
        region = match.group(1)
        summonerName = match.group(2)
        champion = adapter.get("champion")
