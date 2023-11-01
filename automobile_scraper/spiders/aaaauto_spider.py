import scrapy


class AaaautoSpiderSpider(scrapy.Spider):
    name = "aaaauto_spider"
    allowed_domains = ["www.aaaauto.cz"]
    start_urls = ["https://www.aaaauto.cz"]

    def parse(self, response):
        pass
