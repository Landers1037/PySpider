# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

class JdPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline():
    def __init__(self,host,database,user,password,port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        self.db = pymysql.connect(self.host, self.user, self.password, self.database, port=self.port)
        self.cursor = self.db.cursor()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self,spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, port=self.port)
        self.cursor = self.db.cursor()


    def process_item(self,item,spider):
        data = item
        # keys = ','.join(data.keys())
        # values = ','.join(['%s']*len(data))
        # sql = 'insert into %s (%s) values (%s)'%(item.table,keys,values)

        sql = 'insert ignore into jd (标题,颜色,图片,价格) values (%s,%s,%s,%s)'
        self.cursor.execute(sql,(data['title'],data['colors'],data['img'],data['price']))
        self.db.commit()
        return item

    def close_spider(self,spider):
        self.db.close()


