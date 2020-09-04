import sys
import os
sys.path.append(os.path.abspath('../util'))
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

if  __name__=='__main__':
    myconp = ["biaost", "zl_reader", "zl_reader", "10.30.16.52", "5432", "public", "app_ry_query"]
    root_dir = os.path.dirname(os.path.abspath('.'))
    infilename = root_dir + r"\data\xmjl_list\云南_项目经理列表_模板.xlsx"
    outfilename = root_dir + r"\data\get_bst_xmjlyj\云南_bst_xmjlyj_获取结果_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    data=[]
    for row in sheet1data:
        zhongbiaoren = row[0].strip()
        xmjl = row[1].strip()

        xmjl_yj_sql="""SELECT unnest(ry_zhongbiao_info)::jsonb->>'href',entname,name,
        unnest(ry_zhongbiao_info)::jsonb->>'gg_name',xzqh,unnest(ry_zhongbiao_info)::jsonb->>'fabu_time',person_key,
        unnest(ry_zhongbiao_info)::jsonb->>'quyu' FROM "{schema}"."app_ry_query" 
        where entname = '{zhongbiaoren}' and name = '{xmjl}' 
        ORDER BY unnest(ry_zhongbiao_info)::jsonb->>'fabu_time' 
        desc;""".format(schema=myconp[5],xmjl=xmjl,zhongbiaoren=zhongbiaoren)
        # print(xmjl_yj_sql)
        cur.execute(xmjl_yj_sql)
        result = cur.fetchall()
        for content in  result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href",  "entname", "name", "ggname", "xzqh", "fabu_time", "person_key","quyu"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, data)

    if cur:
        cur.close()
    if conn:
        conn.close()



