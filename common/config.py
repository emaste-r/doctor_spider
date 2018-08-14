# coding=utf-8
from common.constant import *

run_venv = 1

if run_venv == RUN_EVEN_TEST:
    SQL_TRACE_ENABLE = True  # sql调试模式，测试机打开
else:
    SQL_TRACE_ENABLE = False

DOC_DIR = "docs/"
DOC_TEMPLATE_DIR = "doc_templates/"
