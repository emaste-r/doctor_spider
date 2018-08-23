# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from common import config
from dao.hospital.hospital_detail_dao import HospitalDetailDao


class HospitalDetailPipeline(object):
    def __init__(self):
        self.hospital_list = []

    def process_item(self, item, spider):
        for k, v in item.iteritems():
            print "%s=%s" % (k, v)

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

        self.hospital_list.append(item)
        return item

    def close_spider(self, spider):
        print "len(self.hospital_list)=%s" % len(self.hospital_list)

        # 尽可能按照index排序
        self.hospital_list.sort(key=lambda x: x["index"])

        print "call insert..."
        HospitalDetailDao.insert(self.hospital_list)
        print "call end..."
