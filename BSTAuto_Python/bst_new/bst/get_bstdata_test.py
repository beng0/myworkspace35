import sys
import os
import psycopg2
sys.path.append(os.path.abspath('../util'))
print(os.path.abspath('../util'))
print(sys.path)
from my_to_excel import *
from my_read_excel import *
from datetime import datetime

if __name__ == '__main__':
    myconp = ["base_db", "zl_reader", "zl_reader", "10.30.16.31", "5432", "dm_files", "zl_test"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    # infilename = root_dir + r"\qy_list\企业抽取_20200826.xlsx"
    outfilename = root_dir + r"\get_bst_qyyj\标事通数据抽取_数据准备_贺家斌_"

    # 读要查询的项目经理和相应企业进来
    # all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    # sheet1data = all_sheet_data[0][1][1:]
    # print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    quyu_data = []
    sql1 = """SELECT quyu FROM "dm_files"."t_s3_files_is_ok" group by quyu;"""
    cur.execute(sql1)
    quyu_result = cur.fetchall()
    for quyu in quyu_result:
        quyu_data.append(quyu[0])
    print(quyu_data)

    data = []
    for quyu in quyu_data:

        get_data_sql = """SELECT html_key::text,quyu  
            FROM "{schema}"."t_s3_files_is_ok" where quyu='{quyu}' 
            and not (content_tx_ocr is  null and content is  null) 
            order by random() 
            limit 2;""".format(schema=myconp[5], quyu=quyu)
        print(get_data_sql)
        cur.execute(get_data_sql)
        result = cur.fetchall()
        for content in result:
            data.append(content)

    print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["html_key", "href", "gg_name", "diqu", "xmjl", "fabu_time", "quyu"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "data", columnRows, data)

    if cur: cur.close()
    if conn: conn.close()

