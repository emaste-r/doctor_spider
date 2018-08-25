# coding=utf-8
import re
import time

import requests
from lxml import etree

from dao.hospital.hospital_detail_dao import HospitalDetailDao
from dao.section.hospital_section_dao import HospitalSectionDao


def get_item(url):
    print "###################################"
    print "deal: %s" % url
    r = requests.get(url)
    content = r.content

    selector = etree.HTML(content)
    item = {}
    hospital_index = re.findall(r'\d+', url)[0]
    item['hospital_index'] = hospital_index

    section_p_list = selector.xpath('/html/body/div[7]/div[2]/div[@class="classify_list clearfix"]')
    for i in section_p_list:
        section_p = i.xpath('h3/text()')[0]
        section_c_list = i.xpath('ul/li')
        for j in section_c_list:
            section_c = j.xpath('a/text()')[0]

            doctor_cnt_str = j.xpath('span/text()')[0]
            doctor_cnt = re.findall(r'\d+', doctor_cnt_str)[0]

            like_cnt_str = j.xpath('span/text()')[1]
            like_cnt = re.findall(r'\d+', like_cnt_str)[0]

            link = j.xpath('a/@href')[0]
            link = "http://www.mingyihui.net" + link

            HospitalSectionDao.insert({
                "hospital_index": hospital_index,
                "section_p": section_p,
                "section_c": section_c,
                "doctor_cnt": doctor_cnt,
                "like_cnt": like_cnt,
                "link": link,
            })
            # print section_c
            # print doctor_cnt
            # print like_cnt
            # print link

    return item


if __name__ == '__main__':
    start_urls = []

    # 找到未存在科室的医院
    for index_item in HospitalDetailDao.get_all_indexs_which_need_to_deal_section():
        print index_item
        start_urls.append("http://www.mingyihui.net/hospital_%s/departments.html" % index_item["index"])
    print "start_urls len=%s" % len(start_urls)

    for url in start_urls:
        hospital_index = re.findall(r'\d+', url)[0]
        try:
            item = get_item(url)
            HospitalDetailDao.update_deal_section_flag(hospital_index, 1)
        except Exception, ex:
            print ex
            HospitalDetailDao.update_deal_section_flag(hospital_index, -1)
        time.sleep(0.2)
