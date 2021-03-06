from util.my_read_excel import *
from util.my_to_excel import *
import psycopg2
from datetime import datetime


if __name__=='__main__':
    myconp = ["biaost", "zl_reader", "zl_reader", "192.168.60.61", "5433", "public", "dm"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/bst_new/data'
    infilename = root_dir + r"\test_sheng_zz_result\山西_省平台qyzz_整理后_胡金花_20200728_153210.xlsx"
    outfilename = root_dir + r"\test_sheng_zz_result\山西_省平台qyzz_测试结果_胡金花_"

    # 读取excel的数据
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][1:]  # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    print(sheet1data)

    # 连接数据库
    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    result_data = []
    for row in sheet1data:
        sql_zzcode ="""	SELECT zzcode 
                        FROM    "{schema}"."dict_qy_zz"   
                        where  name='{zzlb}'  or  match_text='{zzlb}' 
                        or  name like  '%{zzlb}%'  or  match_text like '%{zzlb}%';""".format(schema=myconp[6],zzlb=row[3].strip())
        print(sql_zzcode)

        # 查询相应企业资质在bst的zzcode
        cur.execute(sql_zzcode)
        result_zzcode = cur.fetchall()

        tmp = []
        ishave_zzcode = "无"
        if result_zzcode:
            ent_key_sql = """select ent_key from "{schema}"."app_qy_query" WHERE entname = '{zbr}' ;""".format(schema=myconp[5], zbr=row[2].strip())

            cur.execute(ent_key_sql)
            ent_key_result = cur.fetchall()
            # 判断是否有相应的企业
            if ent_key_result:
                ent_key = ent_key_result[0][0]

                if result_zzcode:
                    sql_string = """SELECT  unnest(qy_zz_info)::jsonb->> 'zzmc'  zzmc ,
                                            unnest(qy_zz_info)::jsonb->> 'zzbh' zzbh,
                                            unnest(qy_zz_info)::jsonb->> 'zzcode'  zzcode, 
                                            unnest(qy_zz_info)::jsonb->> 'zzlb'  zzlb
                                            FROM   "{schema}".app_qy_query WHERE entname='{zbr}' ;""".format(schema=myconp[5],zbr=row[2].strip())
                    print(sql_string)

                    # 查询企业资质
                    cur.execute(sql_string)
                    result = cur.fetchall()

                    # 判断bst相应企业是否有相应的资质
                    for content in result:
                        if result_zzcode[0][0] == content[2]:
                            ishave_zzcode = "有"
                            break
                    tmp=[row[0],row[1],row[2],row[3],result_zzcode[0][0],ishave_zzcode,ent_key]
            else:tmp=[row[0],row[1],row[2],row[3],result_zzcode[0][0],ishave_zzcode,"bst没有该企业"]
        else:tmp=[row[0],row[1],row[2],row[3],"bst目录表无相应的资质",ishave_zzcode,""]

        result_data.append(tmp)
        print(result_data)

    # 数据保存到Excel  sheng	shi	qyname	qyzz
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng", "shi", "qyname", "qyzz","bst目录表是否有相应的资质","bst相应企业是否有相应的资质","ent_key"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, result_data)
    print("to excel scuess")

    # 关闭数据库资源
    if cur: cur.close()
    if conn:conn.close()
