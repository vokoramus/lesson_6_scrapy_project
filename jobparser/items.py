# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # создаем свойства под каждый параметр
    name = scrapy.Field()
    salary = scrapy.Field()
    period = scrapy.Field()
    url = scrapy.Field()

    min = scrapy.Field()
    max = scrapy.Field()
    cur = scrapy.Field()

    _id = scrapy.Field()  # для mongo
