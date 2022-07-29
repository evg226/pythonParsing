# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def proccessPrice(value: str):
    value = value.replace(" ", "")
    try:
        value = int(value)
    except:
        pass
    return value

def proccessSpec(value: str):
    return value.strip()

class CastaparserItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(proccessPrice), output_processor=TakeFirst())
    _id = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    specLabel = scrapy.Field(input_processor=MapCompose(proccessSpec))
    specValue = scrapy.Field(input_processor=MapCompose(proccessSpec))
