from scrapy import Spider, Request, Item, Field


class MySpider(Spider):
    name = "my_spider"
    custom_settings = {
        "ITEM_PIPELINES": {"src.scraping.pipeline.DataPipeline": 300},
    }

    def __init__(self, init_data, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        for data in init_data:
            self.start_urls.append({
                'url': f"https://u.gg/lol/profile/{data['region']}/{data['summonerName']}/champion-stats",
                'alternative_url': f"https://u.gg/lol/profile/{data['region']}/{data['summonerName']}/champion-stats?queueType=normal_draft_5x5",
                'tried_alternative': False  # To track whether the alternative URL has been tried
            })

    def start_requests(self):
        for url_data in self.start_urls:
            yield Request(url=url_data['url'], callback=self.parse, meta={'url_data': url_data})

    def parse(self, response):
        columns = [
            "rank",
            "champion",
            "winRate",
            "winsLoses",
            "kda",
            "kills",
            "deaths",
            "assists",
            "lp",
            "maxKills",
            "maxKills",
            "cs",
            "damage",
            "gold",
        ]
        row_index = 1
        url_data = response.meta['url_data']
        while True:
            try:
                row = {}
                base_selector = (
                    f"div.rt-tr-group:nth-child({row_index}) > div:nth-child(1)"
                )
                selectors = [
                    f"{base_selector} > div:nth-child(1) > span:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)::text",
                    f"{base_selector} > div:nth-child(3) > div:nth-child(1) > strong:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(3) > div:nth-child(1) > span:nth-child(3)::text",
                    f"{base_selector} > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(4) > div:nth-child(1) > span:nth-child(2) > strong:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(4) > div:nth-child(1) > span:nth-child(2) > strong:nth-child(3)::text",
                    f"{base_selector} > div:nth-child(4) > div:nth-child(1) > span:nth-child(2) > strong:nth-child(5)::text",
                    f"{base_selector} > div:nth-child(5) > span:nth-child(1) > span:nth-child(2)::text",
                    f"{base_selector} > div:nth-child(6) > span:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(7) > span:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(8) > span:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(9) > span:nth-child(1)::text",
                    f"{base_selector} > div:nth-child(10) > span:nth-child(1)::text",
                ]
                is_row_empty = True
                for column, selector in zip(columns, selectors):
                    item = response.css(selector).get()
                    if item:
                        is_row_empty = False
                        item = item.strip()
                        if column == "winRate":
                            item = item.rstrip("%")
                        elif column in ["damage", "gold"]:
                            item = item.replace(",", "")
                        row[column] = item
                    else:
                        row[column] = "N/A"
                if is_row_empty:
                    if not url_data['tried_alternative']:
                        # If no data and haven't tried the alternative URL, then try it.
                        url_data['tried_alternative'] = True
                        yield Request(url=url_data['alternative_url'], callback=self.parse, meta={'url_data': url_data})
                    break

                item = SummonerItem()
                item['url'] = response.meta['url_data']['url']
                item['rank'] = row['rank']
                item['champion'] = row['champion']
                item['winRate'] = row['winRate']
                item['winsLoses'] = row['winsLoses']
                item['kda'] = row['kda']
                item['kills'] = row['kills']
                item['deaths'] = row['deaths']
                item['assists'] = row['assists']
                item['lp'] = row['lp']
                item['maxKills'] = row['maxKills']
                item['cs'] = row['cs']
                item['damage'] = row['damage']
                item['gold'] = row['gold']
                yield item
                row_index += 1
            except Exception as e:
                self.log(f"Error: {e}")
                break
class SummonerItem(Item):
    url = Field()
    rank = Field()
    champion = Field()
    winRate = Field()
    winsLoses = Field()
    kda = Field()
    kills = Field()
    deaths = Field()
    assists = Field()
    lp = Field()
    maxKills = Field()
    cs = Field()
    damage = Field()
    gold = Field()