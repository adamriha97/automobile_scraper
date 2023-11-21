import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re

from automobile_scraper.items import AaaautoItem


class AaaautoSpiderSpider(scrapy.Spider):
    name = "aaaauto_spider"
    allowed_domains = ["www.aaaauto.cz"]
    start_urls = ["https://www.aaaauto.cz/ojete-vozy/"] # https://www.aaaauto.cz

    custom_settings = {
        'FEEDS': {'aaaauto_data.json': {'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_ARGUMENTS': ['--headless'], # '--headless'
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800
        },
        'ITEM_PIPELINES': {
            'automobile_scraper.pipelines.AaaautoPipeline': 310
        }
        }
    
    ### with_images != 1 -> data scraped without images, with_images == 1 -> data scraped with images (longer process)
    with_images = 0

    def parse(self, response):
        number_of_pages = int(max(response.css('nav.pagenav ul li a ::attr(data-page)').getall(), key=lambda x: int(x)))
        for i in range(number_of_pages):
            page_url = 'https://www.aaaauto.cz/ojete-vozy/?page=' + str(i + 1)
            if i == 0: yield response.follow(page_url, callback=self.parse_page) # if i == 0: 
    
    def parse_page(self, response):
        car_urls = response.css('div.carsGrid div.card a.fullSizeLink ::attr(href)').getall()
        #car_urls = ["https://www.aaaauto.cz/cz/skoda-praktik/car.html?id=622530220#"]
        for car_url in car_urls: #if car_url == "https://www.aaaauto.cz/cz/vw-e-golf/car.html?id=613072851#":
            if self.with_images != 1:
                yield response.follow(car_url, callback=self.parse_car_page)
            else:
                yield SeleniumRequest(url=car_url, callback=self.parse_car_page, wait_time=15, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'slick-track'))) #slick-track electro-stats

    def parse_car_page(self, response):
        item = AaaautoItem()
        item['url'] = response.url
        item['id'] = response.url.split('?id=')[1]
        item['manufacturer'] = response.css('h1 ::text').getall()[0].replace('\n', '').replace('\t', '')
        item['model'] = '-'.join(response.url.split('/')[4].split('-')[1:])
        item['model_long'] = response.css('h1 ::text').getall()[1].replace('\n', '').replace('\t', '').split(', ')[0]
        item['year'] = response.css('h1 ::text').getall()[1].replace('\n', '').replace('\t', '').split(', ')[-1]
        item['year_int'] = int(response.css('h1 ::text').getall()[1].replace('\n', '').replace('\t', '').split(', ')[-1])
        item['tech_params'] = {}
        tech_params = response.css('div.techParamsRow.general tr')
        for tech_param in tech_params:
            item['tech_params'][tech_param.css('th ::text').get().replace('\n', '').replace('\t', '')] = tech_param.css('td ::text').get().replace('\n', '').replace('\t', '')
        try:
            item['tachometr_int'] = int(re.sub(r'[^0-9]', '', item['tech_params']['Tachometr']))
        except:
            item['tachometr_int'] = -1
        item['tech_params_other'] = {}
        tech_param_rows = response.css('div.techParamsRow')
        if len(tech_param_rows) > 1:
            tech_params_other_names = tech_param_rows[1].css('h3 ::text').getall()
            tech_params_other_tables = tech_param_rows[1].css('table.transparentTable')
            for name, table in zip(tech_params_other_names, tech_params_other_tables):
                item['tech_params_other'][name] = {}
                table_params = table.css('tr')
                for table_param in table_params:
                    item['tech_params_other'][name][table_param.css('th ::text').get()] = table_param.css('td ::text').get()
        consumptions = response.css('div.countbarItem ::text').getall()
        if len(response.css('div.countbarItem ::text').getall()) > 0:
            item['consumption'] = consumptions[-3] + " " + consumptions[-2]
            item['consumption_int'] = float(consumptions[-3])
        else:
            item['consumption'] = "N/A"
            item['consumption_int'] = -1
        info_box = response.css('ul.infoBoxNav')
        price = "0"
        if info_box.css('li.infoBoxNavTitle ::text').getall()[1].replace('\n', '').replace('\t', '').replace(' ', '') == 'Cena': #if info_box.css('li.infoBoxNavTitle span ::text').get().replace('\n', '').replace('\t', '').replace(' ', '') == 'Cena':
            price = info_box.css('li.infoBoxNavTitle strong ::text').get()
            item['price'] = price
        elif info_box.css('li')[2].css('span ::text').get().replace('\n', '').replace('\t', '').replace(' ', '') == 'Cena':
            price = info_box.css('li')[2].css('span.notranslate ::text').getall()[-1].replace('\n', '').replace('\t', '').strip()
            item['price'] = price
        item['price_int'] = int(price.replace(' ', '').split('Kč')[0])
        item['equipment'] = {}
        package_names = response.css('ul.multipleTab')[0].css('li span ::text').getall()
        packages = response.css('ul.multipleTab')[0].css('li div')
        for i in range(len(packages)):
            item['equipment'][package_names[i]] = packages[i].css('li ::text').getall()
        #item['electro_stats'] = {}
        #electro_stats = response.css('ul.electro-stats__list li.electro-stats__list-item')
        #for electro_stat in electro_stats:
        #    item['electro_stats'][electro_stat.css('::text').get()] = electro_stat.css('strong.electro-stats__list-value ::text').get()
        item['images'] = list(filter(lambda x: x.split('/')[2] == "aaaautoeuimg.vshcdn.net", response.css('div#gallery li.galleryLi div.slick-track img ::attr(src)').getall()))
        yield item
