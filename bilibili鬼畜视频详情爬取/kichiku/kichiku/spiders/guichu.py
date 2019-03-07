# -*- coding: utf-8 -*-
# 一个bilibili的鬼畜爬虫分析工具
# 使用selenium来分析动态的js界面
import scrapy
import json
from kichiku.items import KichikuItem
import selenium.webdriver
from selenium.webdriver.chrome.options import Options

class GuichuSpider(scrapy.Spider):
    name = 'guichu'
    allowed_domains = ['www.bilibili.com']
    base_url = 'https://www.bilibili.com/v/kichiku/guide/?spm_id_from=333.334.b_7072696d6172795f6d656e75.67#/all/default/0/'

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 指定使用无头的模式
        self.driver = selenium.webdriver.Chrome(chrome_options=chrome_options)


    # def closed(self,spider):
    #     self.driver.close()

    def parse(self, response):
        datas = response.css('.vd-list li')
        for data in datas:
            item = KichikuItem()

            item['title'] = data.css('a p::text').extract_first()
            item['play'] = data.css('.play::text').extract_first()

            item['danmu'] = data.css('.danmu::text').extract_first()

            item['up'] = data.css('.up-info a::text').extract_first()

            item['time'] = data.css('.pic span::text').extract_first()

            yield item

    def start_requests(self):
        for page in range(1,self.settings.get('PAGE')+1):
            url = self.base_url+str(page)
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

