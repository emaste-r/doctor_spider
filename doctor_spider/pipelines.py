# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from dao.hospital.hospital_dao import HospitalDao


class HospitalSpiderPipeline(object):
    def __init__(self):
        self.hospital_list = []

    def process_item(self, item, spider):
        # print item["is_appoint"]
        # print item["tag_list"]

        try:
            # 处理排行榜的次序
            item["number"] = int(item["number"].replace('NO.', ''))

            # 是否可预约
            item["is_appoint"] = 1 if item["is_appoint"] == u'可预约' else 0

            # 客户满意度
            item["csr"] = int(item["csr"].replace('%', ''))

            # 用户评论数
            item["comment_cnt"] = int(item["comment_cnt"])

            # 用户点赞数
            item["like_cnt"] = int(item["like_cnt"])

            # 医生数
            item["doctor_cnt"] = int(item["doctor_cnt"])

            # 科室数
            item["section_cnt"] = int(item["section_cnt"])

            # 是否为公立
            if len(item["tag_list"]) > 0:
                # 三甲12 三级11 三乙10 三丙9 二甲8 二级7 二乙6 二丙5 一甲4 一级3 一乙2 一丙1 其他0
                for tag in item["tag_list"]:
                    if tag in [u'公立', u'公立医院']:
                        item["is_public"] = 1

                    # 1综合，2专科，3中医，4中西医结合
                    if tag in [u'综合', u'综合医院']:
                        item["category"] = 1
                    if tag in [u'专科', u'专科医院']:
                        item["category"] = 2
                    if tag in [u'中医']:
                        item["category"] = 3
                    if tag in [u'中西医结合']:
                        item["category"] = 4

                    if tag in [u'三甲', u'三级甲等']:
                        item["grade"] = 12
                    if tag in [u'三级', u'三级医院']:
                        item["grade"] = 11
                    if tag in [u'三乙', u'三级乙等']:
                        item["grade"] = 10
                    if tag in [u'三丙', u'三级丙等']:
                        item["grade"] = 9
                    if tag in [u'二甲', u'二级甲等']:
                        item["grade"] = 8
                    if tag in [u'二级', u'二级医院']:
                        item["grade"] = 7
                    if tag in [u'二乙', u'二级乙等']:
                        item["grade"] = 6
                    if tag in [u'二丙', u'二级丙等']:
                        item["grade"] = 5
                    if tag in [u'一甲', u'一级甲等']:
                        item["grade"] = 4
                    if tag in [u'一级', u'一级医院']:
                        item["grade"] = 3
                    if tag in [u'一乙', u'一级乙等']:
                        item["grade"] = 2
                    if tag in [u'一丙', u'一级丙等']:
                        item["grade"] = 1
        except Exception, ex:
            logging.error(ex, exc_info=1)
            return item

        self.hospital_list.append(item)
        return item

    def close_spider(self, spider):
        print "len(self.hospital_list)=%s" % len(self.hospital_list)

        print "call insert..."
        HospitalDao.insert(self.hospital_list)
        print "call end..."
