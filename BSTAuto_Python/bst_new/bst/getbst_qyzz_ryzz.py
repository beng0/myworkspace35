import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

if __name__ == '__main__':
    myconp = ["biaost", "zl_reader", "zl_reader", "10.30.16.52", "5432", "public", "zl_test"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\企业抽取_模板.xlsx"
    outfilename = root_dir + r"\get_bst_qyyj\云南bst企业资质_贺家斌_"
    outfilename2 = root_dir + r"\get_bst_qyyj\云南bst人员资质_贺家斌_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    data = []
    for row in sheet1data:
        zhongbiaoren = row[2].strip()

        qyzz_sql = """SELECT gsd,jgdz,href,entname,zzlb,zzmc,zzcode FROM "{schema}"."qy_zz" 
        where entname = '{entname}';""".format(schema=myconp[5], entname=zhongbiaoren)
        print(qyzz_sql)
        cur.execute(qyzz_sql)
        result = cur.fetchall()
        for content in result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["gsd", "jgdz", "href", "entname", "zzlb", "zzmc", "zzcode"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "qyzz", columnRows, data)

    if cur: cur.close()
    if conn: conn.close()

    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()
    ryzz_data = []
    for row in sheet1data:
        zhongbiaoren = row[2].strip()
        ryzz_sql = """SELECT ent_key,tydm,xzqh,entname,name,zsbh,zclb,zhuanye,ryzz_code FROM "{schema}"."app_qy_zcry" 
        where entname='{entname}';""".format(schema=myconp[5], entname=zhongbiaoren)
        print(ryzz_sql)
        cur.execute(ryzz_sql)
        result1 = cur.fetchall()
        for content in result1:
            ryzz_data.append(content)

    columnRows = ["ent_key", "tydm", "xzqh", "entname", "name", "zsbh", "zclb", "zhuanye", "ryzz_code"]
    wirteDataToExcel(outfilename2 + tablenamehouzui + ".xlsx", "qyzz", columnRows, ryzz_data)

    if cur: cur.close()
    if conn: conn.close()