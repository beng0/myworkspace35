import sys
import os
sys.path.append(os.path.abspath('../util'))
print(sys.path)
print(os.path.abspath('../util'))

from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

if  __name__=='__main__':
    myconp = ["base_db", "zl_reader", "zl_reader", "10.30.16.31", "5432", "app", "app_ry_query"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\xmjl_list\云南_项目经理列表_模板.xlsx"
    outfilename = root_dir + r"\get_bst_qyyj\标事通xmjlzz_数据准备_贺家斌_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    data=[]
    for row in sheet1data:
        entname = row[2].strip()
        name = row[1].strip()

        qy_yj_sql="""SELECT entname,name,unnest(ryzz_info)->>'zsbh',
        unnest(ryzz_info)->>'zclb',unnest(ryzz_info)->>'zhuanye',unnest(ryzz_info)->>'youxiao_date',
        unnest(ryzz_info)->>'ryzz_code' FROM "app_ry_query" where 
        entname = '{entname}' and name = '{name}';""".format(schema=myconp[5],entname=entname,name=name)
        print(qy_yj_sql)
        cur.execute(qy_yj_sql)
        result = cur.fetchall()
        for content in result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["entname","name",  "zsbh", "zclb", "zhuanye", "youxiao_date", "ryzz_code"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, data)

    if cur:cur.close()
    if conn:conn.close()



