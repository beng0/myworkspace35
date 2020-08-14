from collections import OrderedDict
import time
import os
import sys
from lmf.dbv2 import db_query, db_command
from pandas import DataFrame
from datetime import datetime
import pandas
from pprint import pprint


dirname = os.path.dirname(__file__)

def read_db_2_excel(conp,filename,result):
    now_datetime = datetime.now()
    now_datetime_str = now_datetime.strftime('%Y%m%d_%H%M%S')
    wenjian = filename + "_" + now_datetime_str
    #file_name = os.path.join(dirname, 'check_%s.xlsx' % wenjian)
    file_name = os.path.join(dirname, '%s.xlsx' % wenjian)
    ##文件已存在会报错,需手动确认删除
    if os.path.exists(file_name):
        raise FileExistsError("file exist")
    result.to_excel(file_name, index=False) # 写入excel文件
    print("导出成功")


if __name__ == '__main__':

    conp = ["postgres", "since2015", "192.168.1.171", "zljianzhu", "yunnan_renyuan_zljianzhu"]
    read_db_2_excel(conp)
