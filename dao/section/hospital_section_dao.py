# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import logging

from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class HospitalSectionDao(BaseDao):
    db_name = "doctor"
    table_name = "hospital_section_map"

    @classmethod
    def update_deal_doctor_flag(cls, section_id, status=-1):
        sql = "update {db}.{tbl}  set deal_doctor_flag={status} where `id`={section_id}".format(db=cls.db_name,
                                                                                                tbl=cls.table_name,
                                                                                                status=status,
                                                                                                section_id=section_id)
        doctor_conn.execute_sql(sql)

    @classmethod
    def get_all_sections_which_need_to_deal_doctor(cls):
        sql = "select * from {db}.{tbl} where deal_doctor_flag=0 limit 60000, 30000".format(db=cls.db_name,
                                                                         tbl=cls.table_name)
        print sql
        items = doctor_conn.fetchall(sql)
        return items

    @classmethod
    def get_by_hospital_index(cls, hospital_index):
        sql = "select * from {db}.{tbl} where `hospital_index`={hospital_index}". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   hospital_index=hospital_index)
        item = doctor_conn.fetchone(sql)
        return item

    @classmethod
    def get_by_hospital_index_sectionP_sectionC(cls, hospital_index, section_p, section_c):
        sql = "select * from {db}.{tbl} where `hospital_index`={hospital_index} " \
              "and section_p='{section_p}' and section_c='{section_c}'". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   hospital_index=hospital_index,
                   section_p=section_p,
                   section_c=section_c)
        item = doctor_conn.fetchone(sql)
        return item

    @classmethod
    def get_all_indexs(cls):
        sql = "select `index` from {db}.{tbl} ".format(db=cls.db_name, tbl=cls.table_name)
        items = doctor_conn.fetchall(sql)
        return items

    @classmethod
    def insert(cls, map_item):
        sql = "insert into {db}.{tbl}(`hospital_index`, `section_p`, section_c, doctor_cnt, link, like_cnt) " \
              "values  ({hospital_index}, '{section_p}', '{section_c}', {doctor_cnt}, '{link}', {like_cnt}) ".format(
                db=cls.db_name,
                tbl=cls.table_name,
                hospital_index=map_item["hospital_index"] if "hospital_index" in map_item else 0,
                section_p=map_item["section_p"] if "section_p" in map_item else 0,
                section_c=map_item["section_c"] if "section_c" in map_item else 0,
                link=map_item["link"] if "link" in map_item else 0,
                like_cnt=map_item["like_cnt"] if "like_cnt" in map_item else 0,
                doctor_cnt=map_item["doctor_cnt"] if "doctor_cnt" in map_item else 0,
        )
        doctor_conn.execute_sql(sql)

    @classmethod
    def insert_list(cls, hospital_list):
        if len(hospital_list) == 0:
            logging.error("######## nothing to be inserted...")
            return

        sql = "insert into {db}.{tbl}(`name`, `index`, img_url, section_cnt, doctor_cnt, comment_cnt, province, city) " \
              "values ".format(db=cls.db_name,
                               tbl=cls.table_name)

        try:
            for index, item in enumerate(hospital_list):
                sql += " ('{name}', {index}, '{img_url}', {section_cnt}, {doctor_cnt}, {comment_cnt}, '{province}', " \
                       "'{city}'),". \
                    format(name=item["name"].encode("utf-8"),
                           index=item["index"] if "index" in item else 0,
                           section_cnt=item["section_cnt"] if "section_cnt" in item else 0,
                           doctor_cnt=item["doctor_cnt"] if "doctor_cnt" in item else 0,
                           comment_cnt=item["comment_cnt"] if "comment_cnt" in item else 0,
                           province=item["province"] if "province" in item else 0,
                           city=item["city"] if "city" in item else 0,
                           img_url=item["img_url"].encode("utf-8")
                           )
        except Exception, ex:
            logging.error(ex, exc_info=1)
            raise ex

        sql = sql[:-1]  # 去掉最后的,
        doctor_conn.execute_sql(sql)
