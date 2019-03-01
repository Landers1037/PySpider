# -*- coding: utf-8 -*-
'''
对京东的商品爬取尝试对一个关键字列表进行遍历，获取其对应的全部商品信息
'''
import scrapy
from jd.items import shopItem
from scrapy import Request

class JdspiderSpider(scrapy.Spider):
    name = 'jdspider'
    allowed_domains = ['jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=iphone&enc=utf-8&wq=iphone&page=']

    def parse(self, response):
        with open('1.html','w',encoding='utf-8')as f:
            f.write(response.text)
        goods = response.css('.gl-item')
        for shop in goods:
            item = shopItem()
            item['title'] = shop.css('.p-name-type-2 a em::text').extract_first()
            item['img'] = shop.css('.p-img img::attr(source-data-lazy-img)').extract_first()
            item['colors'] = shop.css('.ps-item a::attr(title)').extract_first()
            item['price'] = shop.css('.p-price i::text').extract_first()
            yield item

    def start_requests(self):
        # data = {'ch':'beauty','listtype':'new'} # 定义开始爬取的request请求
        base_url = 'https://search.jd.com/Search?keyword=iphone&enc=utf-8&wq=iphone&page='
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            url = base_url+str(page)
            yield Request(url,self.parse) # 递归
