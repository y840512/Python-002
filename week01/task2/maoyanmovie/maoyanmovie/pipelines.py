# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
from maoyanmovie.items import MaoyanmovieItem

class MaoyanmoviePipeline:
    # def process_item(self, item, spider):
    #     return item
    def process_item(self, item, spider):
        my_name = item['my_name']
        my_type = item['my_type']
        my_time = item['my_time']
        my_list = [{'电影名称':my_name, '电影类型':my_type, '上映时间':my_time}]
        movie2 = pd.DataFrame(data = my_list)
        movie2.to_csv('movie2.csv',mode = 'a', encoding='utf-8', index=False, header=False)
        return item
