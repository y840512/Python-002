# -*- coding: utf-8 -*-
import scrapy
import lxml.etree
from maoyanmovie.items import MaoyanmovieItem
from scrapy.selector import Selector



class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass
    def start_requests(self):
        url = f'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url = url, callback=self.parse, dont_filter=False)


    def parse(self, response):
        # print(response.url)
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]') #//dl[@class="movie-list"]
        for movie in movies[0:10]:
            item = MaoyanmovieItem()
            my_name = movie.xpath('./div[1]/span[1]/text()')
            my_type = movie.xpath('./div[2]/text()')
            my_time = movie.xpath('./div[4]/text()')

            item['my_name'] = my_name.extract_first().strip()
            item['my_type'] = my_type.extract()[1].replace('\n', '').replace(' ', '').strip()
            item['my_time'] = my_time.extract()[1].replace('\n', '').replace(' ', '').strip()
            yield item
