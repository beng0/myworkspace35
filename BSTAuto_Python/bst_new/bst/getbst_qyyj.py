from util.my_read_excel import *
from util.my_to_excel import *
import psycopg2
from datetime import datetime

if  __name__=='__main__':
    myconp = ["biaost", "zl_reader", "zl_reader", "192.168.60.61", "5433", "public", "zl_test"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\get_jst_qyyj\广东_云南_山西建设通企业业绩_胡金花_href_20200727_115212.xlsx"
    outfilename = root_dir + r"\get_bst_qyyj\广东_云南_山西_bst_qyyj_get结果_胡金花_"

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

        qy_yj_sql="""SELECT href,diqu,gg_name,ent_key,entname,html_key,fabu_time  
                        FROM   "{schema}"."t_gg_ent_bridge"   where  entname='{zhongbiaoren}'  order  by   fabu_time   desc;""".format(schema=myconp[5],zhongbiaoren=zhongbiaoren)
        print(qy_yj_sql)
        cur.execute(qy_yj_sql)
        result = cur.fetchall()
        for content in result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href",  "diqu", "gg_name", "ent_key", "entname", "html_key", "fabu_time"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, data)

    if cur:cur.close()
    if conn:conn.close()




