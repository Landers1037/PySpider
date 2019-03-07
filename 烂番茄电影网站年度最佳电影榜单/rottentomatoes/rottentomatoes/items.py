# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Field
import scrapy


class RottentomatoesItem(scrapy.Item):
    rank = Field()
    movie = Field()
    tomatometer = Field()
    movieyear = Field()
