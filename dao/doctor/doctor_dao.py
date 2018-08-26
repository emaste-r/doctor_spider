# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class HospitalDoctorMapDao(BaseDao):
    db_name = "doctor"
    table_name = "hospital_doctor_map"

    @classmethod
    def insert(cls, map_item):
        sql = "insert into {db}.{tbl}(`hospital_index`, `section_p`, section_c, `name`, link, img_url, title, good_at, province, city, area) " \
              "values  ({hospital_index}, '{section_p}', '{section_c}', '{name}', '{link}', '{img_url}', '{title}', '{good_at}', {province}, {city}, {area}) ".format(
                db=cls.db_name,
                tbl=cls.table_name,
                hospital_index=map_item["hospital_index"] if "hospital_index" in map_item else 0,
                section_p=map_item["section_p"] if "section_p" in map_item else 0,
                section_c=map_item["section_c"] if "section_c" in map_item else 0,
                link=map_item["link"] if "link" in map_item else 0,
                name=map_item["name"] if "name" in map_item else 0,
                img_url=map_item["img_url"] if "img_url" in map_item else 0,
                title=map_item["title"] if "title" in map_item else 0,
                good_at=map_item["good_at"] if "good_at" in map_item else 0,
                province=map_item["province"] if "province" in map_item else 0,
                city=map_item["city"] if "city" in map_item else 0,
                area=map_item["area"] if "area" in map_item else 0,
        )
        doctor_conn.execute_sql(sql)
