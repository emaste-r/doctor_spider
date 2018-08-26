# coding=utf-8
import re
import time

import requests
from lxml import etree

from common import config
from dao.hospital.hospital_detail_dao import HospitalDetailDao


def get_item(url):
    print "###################################"
    print "deal: %s" % url
    r = requests.get(url)
    content = r.content

    selector = etree.HTML(content)
    item = {}
    item['index'] = re.findall(r'\d+', url)[0]
    try:
        item['name'] = selector.xpath('/html/body/div[7]/div[1]/h1/text()')[0]
    except Exception, ex:
        print ex
        return {}

    item['province'] = selector.xpath('/html/body/div[6]/a[2]/text()')[0]
    item['city'] = selector.xpath('/html/body/div[6]/a[3]/text()')[0]
    item['img_url'] = selector.xpath('/html/body/div[7]/div[2]/div[1]/div[1]/img/@src')[0]

    # 医生数量、科室数量
    _cnt_str = selector.xpath('/html/body/div[7]/div[2]/div[1]/div[1]/p/text()')[0]
    if _cnt_str:
        item['section_cnt'] = re.findall(r'\d+', _cnt_str)[0]
        item['doctor_cnt'] = re.findall(r'\d+', _cnt_str)[1]

    # 评论数量
    try:
        _comment_str = selector.xpath('/html/body/div[7]/div[2]/div[3]/div[1]/div[2]/p/text()')[0]
        if _comment_str:
            item['comment_cnt'] = re.findall(r'\d+', _comment_str)[0]
    except Exception, ex:
        print ex
        item['comment_cnt'] = 0

    for k, v in item.items():
        print "%s=%s" % (k, v)
    return item


def process_item(item):
    item["index"] = int(item["index"])

    # 清洗省市区
    for i in config.city_json:
        if i["text"] == item['province']:
            item['province'] = int(i["value"])
            for j in i["children"]:
                if j["text"] == item["city"] or item["city"] in j["text"] or j["text"] in item["city"]:
                    item['city'] = int(j["value"])
                    break
    if not isinstance(item['province'], int):
        item['province'] = -1
    if not isinstance(item['city'], int):
        item['city'] = -1

    # 直接插入
    print "insert db...call..."
    HospitalDetailDao.insert(item)
    print "insert db...end..."

    return item


if __name__ == '__main__':
    not_allow_urls = []
    for index_item in HospitalDetailDao.get_all_indexs():
        not_allow_urls.append("http://www.mingyihui.net/hospital_%s.html" % index_item["index"])
    print "not_allow_urls len=%s" % len(not_allow_urls)

    # 开始爬取的url
    start_urls = []
    for i in range(1, 10300):
        url = "http://www.mingyihui.net/hospital_%s.html" % i
        if url not in not_allow_urls:
            start_urls.append(url)
    print "start_urls len=%s" % len(start_urls)

    for url in start_urls:
        item = get_item(url)
        if not item:
            pass
        else:
            item = process_item(item)
        time.sleep(2)
