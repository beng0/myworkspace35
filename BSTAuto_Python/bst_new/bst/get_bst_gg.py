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
    myconp = ["base_db", "zl_reader", "zl_reader", "10.0.64.25", "54325", "app", "gg_meta"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\kw_list\keywords20201103.xlsx"
    outfilename = root_dir + r"\get_bst_gg\标事通标讯_数据准备_贺家斌_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    data=[]
    for row in sheet1data:
        kw = row[0].strip()

        qy_yj_sql="""SELECT gg_name,fabu_time,html_key
        FROM app."gg_meta" where xzqh like '53%' and gg_name like '%{kw}%' 
        and fabu_time between '2020-12-01' and '2020-12-04' and ggtype = '招标公告'
        ORDER BY fabu_time desc;""".format(schema=myconp[5],kw=kw)
        print(qy_yj_sql)
        cur.execute(qy_yj_sql)
        result = cur.fetchall()
        for content in result:
            print(content)
            tmp = [kw,content[0],content[1],content[2]]
            data.append(tmp)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["kw","gg_name",  "fabu_time","html_key"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "bst_gg", columnRows, data)

    if cur:cur.close()
    if conn:conn.close()



