# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    ## add by yangbin 20200726
    my_name = scrapy.Field()
    my_type = scrapy.Field()
    my_time = scrapy.Field()
