import scrapy
from automobile_scraper.items import AaaautoItem


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
        item = AaaautoItem()
        item['url'] = response.url
        item['id'] = response.url.split('?id=')[1]
        item['manufacturer'] = response.css('h1 ::text').getall()[0].replace('\n', '').replace('\t', '')
        item['model'] = '-'.join(response.url.split('/')[4].split('-')[1:])
        item['model_long'] = response.css('h1 ::text').getall()[1].replace('\n', '').replace('\t', '').split(', ')[0]
        item['year'] = response.css('h1 ::text').getall()[1].replace('\n', '').replace('\t', '').split(', ')[1]
        item['tech_params'] = {}
        tech_params = response.css('div.techParamsRow tr')
        for tech_param in tech_params:
            item['tech_params'][tech_param.css('th ::text').get().replace('\n', '').replace('\t', '')] = tech_param.css('td ::text').get().replace('\n', '').replace('\t', '')
        info_box = response.css('ul.infoBoxNav')
        if info_box.css('li.infoBoxNavTitle ::text').getall()[1].replace('\n', '').replace('\t', '').replace(' ', '') == 'Cena': #if info_box.css('li.infoBoxNavTitle span ::text').get().replace('\n', '').replace('\t', '').replace(' ', '') == 'Cena':
            item['price'] = info_box.css('li.infoBoxNavTitle strong ::text').get()
        elif info_box.css('li')[2].css('span ::text').get().replace('\n', '').replace('\t', '').replace(' ', '') == 'Cena':
            item['price'] = info_box.css('li')[2].css('span.notranslate ::text').getall()[-1].replace('\n', '').replace('\t', '').strip()
        item['equipment'] = {}
        package_names = response.css('ul.multipleTab')[0].css('li span ::text').getall()
        packages = response.css('ul.multipleTab')[0].css('li div')
        for i in range(len(packages)):
            item['equipment'][package_names[i]] = packages[i].css('li ::text').getall()
        yield item
