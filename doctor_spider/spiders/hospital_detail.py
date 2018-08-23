# coding=utf-8
import re

from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule

from doctor_spider.items.hospital_detail_item import HospitalDetailItem


class HospitalSpider(CrawlSpider):
    # spider的唯一名称
    name = 'hospital_detail'

    # 开始爬取的url
    for i in range(1, 2):
        start_urls = ["http://www.mingyihui.net/hospital_%s.html" % i]

    # 从页面需要提取的url 链接(link)
    links = LinkExtractor(allow=["http://www.mingyihui.net/hospital_\d+.html"])

    # 设置解析link的规则，callback是指解析link返回的响应数据的的方法
    rules = [Rule(link_extractor=links, callback="parse_content", follow=False)]

    # 配置管道文件
    custom_settings = {
        "ITEM_PIPELINES": {
            'doctor_spider.pipelines.hospital_detail_pipelines.HospitalDetailPipeline': 300,
        }
    }

    def parse_content(self, response):
        """
        解析响应的数据，获取需要的数据字段
        :param response: 响应的数据
        :return:
        """
        print response.url
        item = HospitalDetailItem()
        item['index'] = re.findall(r'\d+', response.url)[0]
        item['name'] = response.xpath('/html/body/div[7]/div[1]/h1/text()').extract()[0]
        item['province'] = response.xpath('/html/body/div[6]/a[2]/text()').extract()[0]
        item['city'] = response.xpath('/html/body/div[6]/a[3]/text()').extract()[0]
        item['img_url'] = response.xpath('/html/body/div[7]/div[2]/div[1]/div[1]/img/@src').extract()[0]

        # 医生数量、科室数量
        _cnt_str = response.xpath('/html/body/div[7]/div[2]/div[1]/div[1]/p/text()').extract()[0]
        if _cnt_str:
            item['section_cnt'] = re.findall(r'\d+', _cnt_str)[0]
            item['doctor_cnt'] = re.findall(r'\d+', _cnt_str)[1]

        # 评论数量
        try:
            _comment_str = response.xpath('/html/body/div[7]/div[2]/div[3]/div[1]/div[2]/p/text()').extract()[0]
            if _comment_str:
                item['comment_cnt'] = re.findall(r'\d+', _comment_str)[0]
        except Exception, ex:
            print ex
            item['comment_cnt'] = 0

        yield item
