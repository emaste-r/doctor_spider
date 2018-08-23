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
    def insert(cls, hospital_list):
        """
        获取全部分类列表
        :return:
        """

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
