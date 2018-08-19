# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoctorItem(scrapy.Item):
    name = scrapy.Field()  # 医生名字
    img_url = scrapy.Field()  # 医院图片
    number = scrapy.Field()  # 排行
    section_cnt = scrapy.Field()  # 科室数量
    doctor_cnt = scrapy.Field()  # 医生数量
    comment_cnt = scrapy.Field()  # 就诊病人分享经验数量
    address = scrapy.Field()  # 地址
    like_cnt = scrapy.Field()  # 好评数
    csr = scrapy.Field()  # 用户满意度
    good_at = scrapy.Field()  # 医院擅长科目
    is_public = scrapy.Field()  # 是否公立
    grade = scrapy.Field()  # 分级
    category = scrapy.Field()  # 类别：综合、专科、中医、妇幼等
    is_appoint = scrapy.Field()  # 能否预约
    tag_list = scrapy.Field()  # 标签列表：公立、三甲、综合
