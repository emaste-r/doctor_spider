# coding=utf-8
import logging
import time

import requests
from lxml import etree

from dao.doctor.doctor_dao import HospitalDoctorMapDao
from dao.hospital.hospital_detail_dao import HospitalDetailDao
from dao.section.hospital_section_dao import HospitalSectionDao


def get_item(hospital_index, section_p, section_c, url, province, city, area):
    print "###################################"
    print "deal: %s" % url
    r = requests.get(url)
    content = r.content

    content = content.replace('<div class="clr"> </div>', '<div class="clr"> </div></div>')
    selector = etree.HTML(content)
    item = {
        "hospital_index": hospital_index,
        "section_p": section_p,
        "section_c": section_c,
        "province": province,
        "city": city,
        "area": area,
    }
    doctor_list = selector.xpath('/html/body/div[8]/div[1]/div[2]/ul/li')
    for i in doctor_list:
        try:
            item["link"] = "http://www.mingyihui.net" + i.xpath('a/@href')[0]
            item["name"] = i.xpath('div[1]/a/h3/text()')[0]

            item["img_url"] = i.xpath('a/img/@src')[0]
            item["good_at"] = i.xpath('div[1]/p/text()')[0].replace(" 擅长： ", "")

            # 头衔
            title = i.xpath('div[1]/span/text()')
            if title:
                item["title"] = title[0].replace("(", "").replace(" )", "")
            else:
                item["title"] = ""

            HospitalDoctorMapDao.insert(item)
        except Exception, ex:
            if "Duplicate" in str(ex):
                print ex
                continue

            logging.error(ex, exc_info=1)
            return {}
    return item


if __name__ == '__main__':
    need_to_deal_section_item = []

    # 找到未存在医生的科室
    for section_item in HospitalSectionDao.get_all_sections_which_need_to_deal_doctor():
        need_to_deal_section_item.append(section_item)
    print "need_to_deal_section len=%s" % len(need_to_deal_section_item)

    hospital_dic = {}

    for section_item in need_to_deal_section_item:
        section_id = section_item["id"]
        hospital_index = section_item["hospital_index"]
        section_p = section_item["section_p"]
        section_c = section_item["section_c"]
        url = section_item["link"]
        doctor_cnt = section_item["doctor_cnt"]

        if hospital_index not in hospital_dic:
            hospital_detail = HospitalDetailDao.get_by_index(hospital_index)
            hospital_dic[hospital_index] = {
                "province": hospital_detail["province"],
                "city": hospital_detail["city"],
                "area": hospital_detail["area"],
            }
        try:
            item = get_item(hospital_index, section_p, section_c, url,
                            hospital_dic[hospital_index]["province"],
                            hospital_dic[hospital_index]["city"],
                            hospital_dic[hospital_index]["area"])
            if item:
                HospitalSectionDao.update_deal_doctor_flag(section_id, 1)
        except Exception, ex:
            print ex
            HospitalSectionDao.update_deal_doctor_flag(section_id, -1)

        time.sleep(1)
