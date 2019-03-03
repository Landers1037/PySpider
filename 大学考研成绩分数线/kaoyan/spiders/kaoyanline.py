# -*- coding: utf-8 -*-
import scrapy
from kaoyan.items import KaoyanItem

class KaoyanlineSpider(scrapy.Spider):
    name = 'kaoyanline'
    allowed_domains = ['www.kaoshidian.com']
    start_urls = ['http://www.kaoshidian.com/kaoyan/fs-13-0-0-0-0.html']

    def parse(self, response):
        html = response.css('tr')
        for data in html:
            item = KaoyanItem()
            item['years'] = data.css('td[class="tc"]::text').extract_first()
            item['school'] = data.css('td[class="tc"]:nth-child(2) a::text').extract_first()
            item['cate'] = data.css('td[class="tc"]:nth-child(3)::text').extract_first()
            item['profession'] =data.css('td[class="tc"]:nth-child(5) a::text').extract_first()
            item['score'] = data.css('td[class="tc"]:nth-child(6)::text').extract_first()
            yield item

    def start_requests(self):
        base_url = 'http://www.kaoshidian.com/kaoyan/fs-13-0-0-0-'
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            url = base_url + str(page) + '.html'
            yield scrapy.Request(url,self.parse)