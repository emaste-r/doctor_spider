# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import logging

from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class HospitalDetailDao(BaseDao):
    db_name = "doctor"
    table_name = "hospital_detail"

    @classmethod
    def get_by_index(cls, index):
        sql = "select `index` from {db}.{tbl} where `index`={index}".format(db=cls.db_name,
                                                                            tbl=cls.table_name,
                                                                            index=index)
        item = doctor_conn.fetchone(sql)
        return item

    @classmethod
    def get_by_name(cls, name):
        sql = "select * from {db}.{tbl} where `name`={name}".format(db=cls.db_name,
                                                                    tbl=cls.table_name,
                                                                    index=name)
        item = doctor_conn.fetchone(sql)
        return item

    @classmethod
    def get_all_indexs(cls):
        sql = "select `index` from {db}.{tbl}".format(db=cls.db_name,
                                                      tbl=cls.table_name)
        print sql
        items = doctor_conn.fetchall(sql)
        return items

    @classmethod
    def get_all_indexs_which_need_to_deal_section(cls):
        sql = "select `index` from {db}.{tbl} where deal_section_flag=0".format(db=cls.db_name,
                                                                                tbl=cls.table_name)
        print sql
        items = doctor_conn.fetchall(sql)
        return items

    @classmethod
    def update_deal_section_flag(cls, index, status=-1):
        sql = "update {db}.{tbl}  set deal_section_flag={status} where `index`={index}".format(db=cls.db_name,
                                                                                               tbl=cls.table_name,
                                                                                               status=status,
                                                                                               index=index)
        doctor_conn.execute_sql(sql)

    @classmethod
    def insert(cls, hospital_item):
        try:
            sql = "insert into {db}.{tbl}(`name`, `index`, img_url, section_cnt, doctor_cnt, comment_cnt, province, city) " \
                  "values  ('{name}', {index}, '{img_url}', {section_cnt}, {doctor_cnt}, {comment_cnt}, {province}, " \
                  "{city}) ".format(
                    db=cls.db_name,
                    tbl=cls.table_name, name=hospital_item["name"].encode("utf-8"),
                    index=hospital_item["index"] if "index" in hospital_item else 0,
                    section_cnt=hospital_item["section_cnt"] if "section_cnt" in hospital_item else 0,
                    doctor_cnt=hospital_item["doctor_cnt"] if "doctor_cnt" in hospital_item else 0,
                    comment_cnt=hospital_item["comment_cnt"] if "comment_cnt" in hospital_item else 0,
                    province=hospital_item["province"] if "province" in hospital_item else 0,
                    city=hospital_item["city"] if "city" in hospital_item else 0,
                    img_url=hospital_item["img_url"].encode("utf-8")
            )
            doctor_conn.execute_sql(sql)
        except Exception, ex:
            logging.error(ex, exc_info=1)
            return None

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
