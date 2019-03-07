# -*- coding: utf-8 -*-
import scrapy
from rottentomatoes.items import RottentomatoesItem

class TomatoSpider(scrapy.Spider):
    name = 'tomato'
    allowed_domains = ['www.rottentomatoes.com']
    start_urls = ['https://www.rottentomatoes.com/']

    def parse(self, response):
        datas = response.css('.table tr')
        for data in datas:
            item = RottentomatoesItem()
            item['movieyear'] = response.url.replace('https://www.rottentomatoes.com/top/bestofrt/?year=','')
            item['rank'] = data.css('td:nth-child(1)::text').extract_first()
            item['movie'] = str(data.css('td a::text').extract_first()).strip()
            item['tomatometer'] = str(data.css('.tMeterScore::text').extract_first()).replace('\xa0','')
            yield item

    def start_requests(self):
        base_url = 'https://www.rottentomatoes.com/top/bestofrt/?year='
        for page in range(1950,2019):
            url = base_url + str(page)
            yield scrapy.Request(url,callback=self.parse)