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

            try:
                HospitalSectionDao.insert({
                    "hospital_index": hospital_index,
                    "section_p": section_p,
                    "section_c": section_c,
                    "doctor_cnt": doctor_cnt,
                    "like_cnt": like_cnt,
                    "link": link,
                })
            except Exception, ex:
                map_item = HospitalSectionDao.get_by_hospital_index_sectionP_sectionC(hospital_index, section_p,
                                                                                      section_c)
                if map_item:
                    # 说明是两种不同的链接： 假设有2个普外科，但它们的链接是不同的。
                    if map_item["link"] != link:
                        tmp_cnt = 1
                        while True:
                            try:
                                HospitalSectionDao.insert({
                                    "hospital_index": hospital_index,
                                    "section_p": section_p,
                                    "section_c": section_c + "_%s" % tmp_cnt,
                                    "doctor_cnt": doctor_cnt,
                                    "like_cnt": like_cnt,
                                    "link": link,
                                })
                                break
                            except Exception, ex:
                                print ex
                                tmp_cnt += 1
    return item


if __name__ == '__main__':
    start_urls = []

    # 找到未存在科室的医院
    for index_item in HospitalDetailDao.get_all_indexs_which_need_to_deal_section():
        print index_item
        start_urls.append("http://www.mingyihui.net/hospital_%s/departments.html" % index_item["index"])
    print "start_urls len=%s" % len(start_urls)

    start_urls.reverse()

    for url in start_urls:
        hospital_index = re.findall(r'\d+', url)[0]
        try:
            item = get_item(url)
            HospitalDetailDao.update_deal_section_flag(hospital_index, 2)
        except Exception, ex:
            print ex
            HospitalDetailDao.update_deal_section_flag(hospital_index, -2)

        time.sleep(1)
