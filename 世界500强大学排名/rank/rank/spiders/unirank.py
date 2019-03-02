# -*- coding: utf-8 -*-
import scrapy
from rank.items import RankItem

class UnirankSpider(scrapy.Spider):
    name = 'unirank'
    allowed_domains = ['http://www.shanghairanking.com']
    start_urls = ['http://www.shanghairanking.com/ARWU2018.html']

    def parse(self, response):
        # with open('1.html','w',encoding='utf-8')as f:
        #     f.write(response.text)
        campus = response.css('tr')
        # campus1 = response.css('.bgf5')

        for data in campus:
            item = RankItem()
            item['years'] = str(response.url).replace('http://www.shanghairanking.com/ARWU','').replace('.html','')
            item['ranks'] = data.css('td::text').extract_first()
            item['uni'] = data.css('.left a::text').extract_first()
            item['location'] = data.css('td a::attr(title)').extract_first()
            item['score']= data.css('td:nth-child(9) div::text').extract_first()
            yield item

    def start_requests(self):
        base_url = 'http://www.shanghairanking.com/ARWU'
        for i in range(1,self.settings.get('YEAR')+1):
            parse = 2019-i
            url = base_url+str(parse)+'.html'
            yield scrapy.Request(url,self.parse)