# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutomobileScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AaaautoItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    manufacturer = scrapy.Field()
    model = scrapy.Field()
    model_long = scrapy.Field()
    year = scrapy.Field()
    tech_params = scrapy.Field()
    price = scrapy.Field()
    price_info = scrapy.Field()
    equipment = scrapy.Field()
    consumption = scrapy.Field()
    image = scrapy.Field()