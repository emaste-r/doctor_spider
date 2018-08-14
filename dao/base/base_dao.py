# coding=utf-8
import logging

from support.db.mysql_db import doctor_conn, doctor_user_conn


class BaseDao(object):
    db_name = ""
    table_name = ""

    @classmethod
    def get_by_id(cls, _id):
        """
        根据id获取
        :param _id:
        :return:
        """
        sql = "select * from {db}.{tbl} where id = {_id}". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   _id=_id,
                   )
        if cls.db_name == "doctor":
            item = doctor_conn.fetchone(sql)
        elif cls.db_name == "doctor_user":
            item = doctor_user_conn.fetchone(sql)
        else:
            logging.error("get_by_id() find no db to exec.")
            item = None
        return item
