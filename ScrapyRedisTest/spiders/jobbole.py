# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     jobbole
   Description :
   Author :       wsm
   date：          2019-01-13
-------------------------------------------------
   Change Activity:
                   2019-01-13:
-------------------------------------------------
"""
__author__ = 'wsm'

from scrapy_redis.spiders import RedisSpider
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
import re



class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']

    def parse(self, response):
        # do stuff
        post_nodes = response.css('#archive .post-thumb a')
        for post_node in post_nodes:
            # 如果提取到的 href 不带域名
            # response.url + post_url 或用如下方法
            # yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": ''}, callback=self.parse_detail, dont_filter=True)
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")

            # urljoin 如果传的 url 没域名 会自动从 response 中获取 url 进行拼接  如果获取的 url 有域名 则直接保存
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail, dont_filter=True)

        # 获取下一页 url 交给 scrapy 进行处理
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        pass