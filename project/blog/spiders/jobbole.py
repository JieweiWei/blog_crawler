# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from blog.items import BlogItem
import re

class JobboleSpider(CrawlSpider):
    # 定义爬虫名称
    name = "jobbole"
    # 定义爬虫允许访问的域址，防止其爬到博客外
    allowed_domains = ["blog.jobbole.com"]
    # 爬虫起始url
    start_urls = [
        'http://blog.jobbole.com/',
    ]
    # 定义爬取规则
    rules = [
        # 若为起始url，则跟进
        Rule(LinkExtractor(allow=(start_urls[0]+'$')), follow=True),
        # 若为索引页，则跟进
        Rule(LinkExtractor(allow=('.+/all-posts/(page/\d+/)?$')), follow=True),
        # 若为文章页停止跟进，使用分析函数都页面进行分析
        Rule(LinkExtractor(allow=('/\d+/$')), callback='parse_blog', follow=False)
    ]

    # 博客页面分析函数
    def parse_blog(self, response):
        item = BlogItem()
        # 使用xpath提取博客文章的标题，链接和标签
        item['title'] = response.xpath('//h1/text()').extract()[0].encode('utf-8')
        item['link'] = response.url.encode('utf-8')
        entry_meta_str = self.from_html_to_str(response.xpath('//div[@class="entry-meta"]').extract()[0]).encode('utf-8')
        index = entry_meta_str.rfind('：')
        item['tag'] = ''.join((''.join(entry_meta_str[index+len('：'):].split('\n'))).split(', '))
        item['content'] = ''
        # 由于博客的页面的html结果比较混乱，所以不采用xpath进行提取，
        # 而是使用html标签过滤函数对标签进行过滤，过滤出文章内容
        for sel in response.xpath("//div[@class='entry']"):
            item['content'] = self.from_html_to_str(''.join(sel.xpath('p').extract())).encode('utf-8')
        return item

    # Tool function: filte html tag.
    def from_html_to_str(self, html_content):
        # Filte <br> or <br />.
        html_content = re.sub(r'<br\s*?/?>', '\n', html_content)
        # Filte other tag.
        html_content = re.sub(r'</?\w+[^>]*>', ' ', html_content)
        # Filte comment tag.
        html_content = re.sub(r'<!--[\s\S]*-->', '', html_content)
        # Compress the blank line.
        html_content = re.sub(r'\n+', '\n', html_content)
        # Replace the char entity.
        html_content = self.replace_char_entity(html_content)
        return html_content

    # Tool function: replace char entity.
    def replace_char_entity(self, htmlstr):
        CHAR_ENTITIES = {
            'nbsp': '',
            '160': '',
            'lt': '<',
            '60': '<',
            'gt': '>',
            '62': '>',
            'amp': '&',
            '38': '&',
            'quot': '"',
            '34':'"'
        }
        #命名组,把 匹配字段中\w+的部分命名为name,可以用group函数获取
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            key = sz.group('name') #命名组的获取
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1) #1表示替换第一个匹配
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                htmlstr = re_charEntity.sub('',htmlstr,1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

