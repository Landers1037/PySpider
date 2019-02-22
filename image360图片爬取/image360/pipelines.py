# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

class Image360Pipeline(object):
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
        # sql = 'create database image360 default character set utf8 collate utf8_general_ci'
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, port=self.port)
        self.cursor = self.db.cursor()

        # sql = 'create table images(id varchar(255) primary key,url varchar(255) null,title varchar (255) null,thumb varchar (255) null '
        # self.cursor.execute(sql)

    def process_item(self,item,spider):
        data = item
        # keys = ','.join(data.keys())
        # values = ','.join(['%s']*len(data))
        # sql = 'insert into %s (%s) values (%s)'%(item.table,keys,values)

        # sql = 'insert ignore into images (id,url,title) values (%s,%s,%s)'
        # self.cursor.execute(sql,(data['id'],data['url'],data['title']))
        # self.db.commit()
        return item

    def close_spider(self,spider):
        self.db.close()

class ImagePipeline(ImagesPipeline): # 保存图片的方法重写
    def file_path(self, request, response=None, info=None):
        # 保存的文件名
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        # 一旦一张图片下载完成就执行的操作
        image_paths = [x['path'] for ok ,x in results if ok]
        if not image_paths:
            raise DropItem('image download failed')
        return item

    def get_media_requests(self, item, info):
        #  用于返回要处理的request请求
        yield Request(item['url'])