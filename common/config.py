# coding=utf-8
import json

from common.constant import *

run_venv = 1

if run_venv == RUN_EVEN_TEST:
    SQL_TRACE_ENABLE = False  # sql调试模式，测试机打开
else:
    SQL_TRACE_ENABLE = False

DOC_DIR = "docs/"
DOC_TEMPLATE_DIR = "doc_templates/"

city_json = json.load(open("support/docs/city.json"))
