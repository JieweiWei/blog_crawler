# -*- coding: utf-8 -*-

import scrapy

# 定义爬取的数据结构
class BlogItem(scrapy.Item):
    # 博客文章标题
    title = scrapy.Field()
    # 博客文章链接
    link = scrapy.Field()
    # 博客文章标签
    tag = scrapy.Field()
    # 博客文章内容
    content = scrapy.Field()
