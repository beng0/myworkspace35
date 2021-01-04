import sys

sys.path.append('D:/bst_hjb/bst_new/util')
print(sys.path)
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

if __name__ == '__main__':
    myconp = ["base_db", "zl_reader", "zl_reader", "10.0.64.25", "54325", "app", "qy_zz"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\企业抽取_模板.xlsx"
    outfilename = root_dir + r"\get_bst_ryzz_qyzz\云南bst企业资质_贺家斌_"
    outfilename2 = root_dir + r"\get_bst_ryzz_qyzz\云南bst人员资质_贺家斌_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    data = []
    for row in sheet1data:
        zhongbiaoren = row[1].strip()

        qyzz_sql = """SELECT entname,zzmc,eddate,zzcode FROM "{schema}"."qy_zz" 
        where entname = '{entname}';""".format(schema=myconp[5], entname=zhongbiaoren)
        print(qyzz_sql)
        cur.execute(qyzz_sql)
        result = cur.fetchall()
        for content in result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["entname", "zzmc", "youxiao_date", "zzcode"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "qyzz", columnRows, data)

    if cur: cur.close()
    if conn: conn.close()

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()
    ryzz_data = []
    for row in sheet1data:
        zhongbiaoren = row[1].strip()
        ryzz_sql = """SELECT entname,name,zjhm,zsbh,zclb,zhuanye,ryzz_code FROM "{schema}"."app_qy_zcry" 
        where entname='{entname}';""".format(schema=myconp[5], entname=zhongbiaoren)
        print(ryzz_sql)
        cur.execute(ryzz_sql)
        result1 = cur.fetchall()
        for content in result1:
            ryzz_data.append(content)

    columnRows = ["entname", "name", "zjhm", "zsbh", "zclb", "zhuanye", "ryzz_code"]
    wirteDataToExcel(outfilename2 + tablenamehouzui + ".xlsx", "qyzz", columnRows, ryzz_data)

    if cur: cur.close()
    if conn: conn.close()
import sys

sys.path.append('D:/bst_hjb/bst_new/util')
print(sys.path)
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

if __name__ == '__main__':
    myconp = ["base_db", "zl_reader", "zl_reader", "10.0.64.25", "54325", "app", "qy_zz"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\企业抽取_模板.xlsx"
    outfilename = root_dir + r"\get_bst_ryzz_qyzz\云南bst企业资质_贺家斌_"
    outfilename2 = root_dir + r"\get_bst_ryzz_qyzz\云南bst人员资质_贺家斌_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    data = []
    for row in sheet1data:
        zhongbiaoren = row[1].strip()

        qyzz_sql = """SELECT entname,zzmc,eddate,zzcode FROM "{schema}"."qy_zz" 
        where entname = '{entname}';""".format(schema=myconp[5], entname=zhongbiaoren)
        print(qyzz_sql)
        cur.execute(qyzz_sql)
        result = cur.fetchall()
        for content in result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["entname", "zzmc", "youxiao_date", "zzcode"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "qyzz", columnRows, data)

    if cur: cur.close()
    if conn: conn.close()

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()
    ryzz_data = []
    for row in sheet1data:
        zhongbiaoren = row[1].strip()
        ryzz_sql = """SELECT entname,name,zjhm,zsbh,zclb,zhuanye,ryzz_code FROM "{schema}"."app_qy_zcry" 
        where entname='{entname}';""".format(schema=myconp[5], entname=zhongbiaoren)
        print(ryzz_sql)
        cur.execute(ryzz_sql)
        result1 = cur.fetchall()
        for content in result1:
            ryzz_data.append(content)

    columnRows = ["entname", "name", "zjhm", "zsbh", "zclb", "zhuanye", "ryzz_code"]
    wirteDataToExcel(outfilename2 + tablenamehouzui + ".xlsx", "qyzz", columnRows, ryzz_data)

    if cur: cur.close()
    if conn: conn.close()
