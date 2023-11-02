import scrapy


class AaaautoSpiderSpider(scrapy.Spider):
    name = "aaaauto_spider"
    allowed_domains = ["www.aaaauto.cz"]
    start_urls = ["https://www.aaaauto.cz/ojete-vozy/"] # https://www.aaaauto.cz

    custom_settings = {
        'FEEDS': {'aaaauto_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8',
        }

    def parse(self, response):
        number_of_pages = int(max(response.css('nav.pagenav ul li a ::attr(data-page)').getall(), key=lambda x: int(x)))
        for i in range(number_of_pages):
            page_url = 'https://www.aaaauto.cz/ojete-vozy/?page=' + str(i + 1)
            if i == 0: yield response.follow(page_url, callback=self.parse_page) # if i == 0: 
    
    def parse_page(self, response):
        car_urls = response.css('div.carsGrid div.card a.fullSizeLink ::attr(href)').getall()
        for car_url in car_urls:
            yield response.follow(car_url, callback=self.parse_car_page)

    def parse_car_page(self, response):
        id = response.url.split('?id=')[1]
        yield {
            'url': response.url,
            'id': id
        }
