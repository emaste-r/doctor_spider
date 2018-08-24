# coding=utf-8

from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class ProxyTestSpider(CrawlSpider):
    # spider的唯一名称
    name = 'proxy_test'

    # 开始爬取的url
    start_urls = ["http://ip111.cn/"]

    # 从页面需要提取的url 链接(link)
    links = LinkExtractor(allow=[])

    # 设置解析link的规则，callback是指解析link返回的响应数据的的方法
    rules = [Rule(link_extractor=links, callback="parse_content", follow=True)]

    def parse_content(self, response):
        """
        解析响应的数据，获取需要的数据字段
        :param response: 响应的数据
        :return:
        """
        print response.url
        print response.body
