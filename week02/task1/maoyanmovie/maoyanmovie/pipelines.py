# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
import pymysql

class MaoyanPipeline:
    
    def __init__(self, config):
        self.config = config

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MYSQL_CONFIG'))

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.config['password'],
            db=self.config['db']
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        with self.conn.cursor() as cur:
            sql = "INSERT INTO 'movie_info' ('movie_name`, 'actor', `time`) VALUES (%s, %s, %s)"
            cur.execute(sql, (item['name'], item['my_type'], item['my_time']))
        self.conn.commit()
        return item

