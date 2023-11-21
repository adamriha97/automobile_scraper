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
    field_names = scrapy.Field()

    url = scrapy.Field()
    id = scrapy.Field()
    manufacturer = scrapy.Field()
    model = scrapy.Field()
    model_long = scrapy.Field()
    year = scrapy.Field()
    year_int = scrapy.Field()
    tech_params = scrapy.Field()
    tachometr_int = scrapy.Field()
    tech_params_other = scrapy.Field()
    consumption = scrapy.Field()
    consumption_int = scrapy.Field()
    price = scrapy.Field()
    price_int = scrapy.Field()
    equipment = scrapy.Field()
    #electro_stats = scrapy.Field()
    images = scrapy.Field()