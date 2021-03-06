 # -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request,Spider
from urllib.parse import urlencode
from image360.items import ImageItem

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('imageid')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            # item['thumb'] = image.get('ghimg_thumb_url')
            yield item

    def start_requests(self):
        data = {'ch':'beauty','listtype':'new'} # 定义开始爬取的request请求
        base_url = 'http://image.so.com/zj?'
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            data['sn'] = page*30
            params = urlencode(data)
            url = base_url+params
            yield Request(url,self.parse) # 递归