# -*- coding: utf-8 -*-
import scrapy
import json
from bilibili.items import fanItem

class BilibotSpider(scrapy.Spider):
    name = 'bilibot'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20']
    # custom_settings = {
    #     "DEFAULT_REQUEST_HEADERS":{
    #     'Accept': 'application/json, text/plain, */*',
    #     'DNT': '1',
    #     'Access-Control-Allow-Headers': 'Origin,No-Cache,X-Requested-With, If-Modified-Since, Pragma, Last-Modified, Cache-Control, Expires, Content-Type, Access-Control-Allow-Credentials',
    #     'Origin': 'https://www.bilibili.com',
    #     'Content-Encoding': 'gzip',
    #     'Transfer-Encoding': 'chunked',
    #     'Referer': 'https://www.bilibili.com/anime/index/?spm_id_from = 666.4.b_7072696d6172795f6d656e75.13',
    #     'User-Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.119\
    #     Safari / 537.36'
    #     },
    # }

    # def parse(self, response):
    #     data = response.text
    #     print(data)



    def parse(self,response):
        jsonBody = json.loads(response.body)
        result = jsonBody['result']
        data = result['data']
        for dict in data:
            modelItem = fanItem()
            modelItem['title'] = dict['title']
            modelItem['follow'] = dict['order']['follow']
            modelItem['play'] = dict['order']['play']
            try:
                modelItem['score'] = dict['order']['score']
            except Exception :
                modelItem['score'] = '没有数据'
            modelItem['cover'] = dict['cover']
            yield modelItem
        #     modelItems.append(modelItem)
        # return modelItems

    def start_requests(self):
        base_url = '''https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page='''
        for i in range(1,self.settings.get('MAX_PAGE')+1):
            url = base_url + str(i) + '&season_type=1&pagesize=20'
            yield scrapy.Request(url,callback=self.parse)

