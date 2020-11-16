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
    myconp = ["biaost", "zl_reader", "zl_reader", "192.168.60.61", "5433", "public", "zl_test"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\企业抽取_20200826.xlsx"
    outfilename = root_dir + r"\get_bst_qyyj\标事通企业业绩_数据准备_贺家斌_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    data=[]
    for row in sheet1data:
        zhongbiaoren = row[1].strip()

        qy_yj_sql="""SELECT href,zhongbiaoren,gg_name,diqu,xmjl,fabu_time,quyu 
        FROM "{schema}"."gg_meta" where zhongbiaoren='{zhongbiaoren}' 
        ORDER BY fabu_time desc;""".format(schema=myconp[5],zhongbiaoren=zhongbiaoren)
        print(qy_yj_sql)
        cur.execute(qy_yj_sql)
        result = cur.fetchall()
        for content in result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href",  "entname", "gg_name", "diqu", "xmjl", "fabu_time", "quyu"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, data)

    if cur:cur.close()
    if conn:conn.close()



