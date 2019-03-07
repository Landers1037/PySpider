# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class KichikuPipeline(object):
    def process_item(self, item, spider):
        return item

class pgPipeline():
    def __init__(self,host,database,user,password,port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        self.db = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        self.cursor = self.db.cursor()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('SQL_HOST'),
            database=crawler.settings.get('SQL_DATABASE'),
            user=crawler.settings.get('SQL_USER'),
            password=crawler.settings.get('SQL_PASSWORD'),
            port=crawler.settings.get('SQL_PORT'),
        )

    def open_spider(self,spider):
        self.db = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        data = item

        sql = 'insert into guichu(标题,播放量,弹幕数,时长,up) values (%s,%s,%s,%s,%s)'


        self.cursor.execute(sql,(data['title'],data['play'],data['danmu'],data['time'],data['up']))
        self.db.commit()

        self.db.rollback()

        return item

    def close_spider(self,spider):
        self.db.close()