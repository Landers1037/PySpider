# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class KaoyanItem(scrapy.Item):
    years = Field()
    school = Field()
    cate = Field()
    profession = Field()
    score = Field()