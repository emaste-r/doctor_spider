# coding=utf-8
import logging

from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class HospitalDao(BaseDao):
    db_name = "doctor"
    table_name = "hospital"

    @classmethod
    def insert(cls, hospital_list):
        """
        获取全部分类列表
        :return:
        """

        if len(hospital_list) == 0:
            logging.error("######## nothing to be inserted...")
            logging.error("######## nothing to be inserted...")
            logging.error("######## nothing to be inserted...")
            return

        sql = "insert into {db}.{tbl}(`name`, `number`, grade, category, is_public, is_appoint, address, " \
              "img_url, section_cnt, doctor_cnt, comment_cnt, like_cnt, good_at, csr) values ".format(db=cls.db_name,
                                                                                                      tbl=cls.table_name)

        item = {}
        try:
            for index, item in enumerate(hospital_list):
                sql += " ('{name}', {number}, {grade}, {category}, {is_public}, {is_appoint}, '{address}', " \
                       "'{img_url}', {section_cnt}, {doctor_cnt}, {comment_cnt}, {like_cnt}, '{good_at}', {csr}),". \
                    format(name=item["name"].encode("utf-8"),
                           number=item["number"] if "number" in item else 0,
                           grade=item["grade"] if "grade" in item else 0,
                           category=item["category"] if "category" in item else 0,
                           is_public=item["is_public"] if "is_public" in item else 0,
                           is_appoint=item["is_appoint"] if "is_appoint" in item else 0,
                           address=item["address"].encode("utf-8"),
                           img_url=item["img_url"].encode("utf-8"),
                           section_cnt=item["section_cnt"] if "section_cnt" in item else 0,
                           doctor_cnt=item["doctor_cnt"] if "doctor_cnt" in item else 0,
                           comment_cnt=item["comment_cnt"] if "comment_cnt" in item else 0,
                           like_cnt=item["like_cnt"] if "like_cnt" in item else 0,
                           good_at=(' '.join(item["good_at"])).encode("utf-8"),
                           csr=item["csr"] if "csr" in item else 0
                           )
        except Exception, ex:
            logging.error(ex, exc_info=1)
            # print item
            raise ex

        sql = sql[:-1]  # 去掉最后的,

        sql += " on duplicate key update del_flag=0"
        doctor_conn.execute_sql(sql)
