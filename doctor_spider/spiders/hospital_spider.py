# coding=utf-8

from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule

from doctor_spider.items import DoctorSpiderItem


class HospitalSpider(CrawlSpider):
    # spider的唯一名称
    name = 'hospital'

    # 开始爬取的url
    start_urls = ["http://www.mingyihui.net/hospitallist.html"]

    # 从页面需要提取的url 链接(link)
    links = LinkExtractor(allow="http://www.mingyihui.net/hospitallist_\d+.html")

    # 设置解析link的规则，callback是指解析link返回的响应数据的的方法
    rules = [Rule(link_extractor=links, callback="parse_content", follow=True)]

    # 配置管道文件
    custom_settings = {
        "ITEM_PIPELINES": {
            'doctor_spider.pipelines.HospitalSpiderPipeline': 300,
        }
    }

    def parse_content(self, response):
        """
        解析响应的数据，获取需要的数据字段
        :param response: 响应的数据
        :return:
        """

        for element in response.xpath('//ul[@class="H_main"]/li[@class="H_list"]'):
            item = DoctorSpiderItem()

            item['name'] = element.xpath('div[1]/h3/a/text()').extract()[0]
            item['img_url'] = element.xpath('a/img/@src').extract()[0]
            item['number'] = element.xpath('a/div/text()').extract()[0]
            item['section_cnt'] = element.xpath('div[1]/dl[@class="H_list_center_add"]/dd[1]/span/text()').extract()[0]
            item['doctor_cnt'] = element.xpath('div[1]/dl[@class="H_list_center_add"]/dd[1]/span/text()').extract()[1]
            item['comment_cnt'] = \
                element.xpath('div[1]/dl[@class="H_list_center_add"]/dd[1]/span/text()').extract()[2]
            item['address'] = element.xpath('div[1]/dl[@class="H_list_center_add"]/dd[2]/@title').extract()[0]
            item['like_cnt'] = element.xpath('ul[1]/li[3]/text()').extract()[0]
            item['csr'] = element.xpath('ul[1]/li[4]/span[2]/text()').extract()[0]
            item['good_at'] = element.xpath(
                'div[1]/div[@class="H_list_center_add  more-dis-pt  more-dis-rela"]/div[@class="more-dis-chi more-dis-rela-chi"]/a/div/text()').extract()
            item['tag_list'] = element.xpath('div[1]/span/text()').extract()
            item['is_appoint'] = element.xpath('div[1]/a/text()').extract()[0]

            yield item
