# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class RankPipeline(object):
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
        # 先新建一个表格存放大学排名
        self.cursor = self.db.cursor()
        # sql = 'create table if not exists unirank(years varchar(255) not null,rank varchar(255) not null,uni \
        # varchar(255) not null,location varchar(255) not null,score varchar(255) not null,primary key(years))'
        # self.cursor.execute(sql)

    def process_item(self,item,spider):
        data = item

        sql = 'insert into unirank (years,ranks,uni,location,score) values (%s,%s,%s,%s,%s)'

        self.cursor.execute(sql,(data['years'],data['ranks'],data['uni'],data['location'],data['score']))
        self.db.commit()

        return item

    def close_spider(self,spider):
        self.db.close()
