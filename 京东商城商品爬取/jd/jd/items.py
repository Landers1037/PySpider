# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class shopItem(Item):
    title = Field()
    img = Field()
    colors = Field()
    price = Field()