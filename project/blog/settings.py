# -*- coding: utf-8 -*-

BOT_NAME = 'blog'

SPIDER_MODULES = ['blog.spiders']
NEWSPIDER_MODULE = 'blog.spiders'

ITEM_PIPELINES = ['blog.pipelines.BlogPipeline']

# 反防爬设置
    # 禁止cookies,
COOKIES_ENABLES = False
    # 设置时间延迟，每1s爬取一次
DOWNLOAD_DELAY = 1
    # 使用user agent池
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'blog.rotate_useragent.RotateUserAgentMiddleware': 400
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'blog (+http://www.yourdomain.com)'
