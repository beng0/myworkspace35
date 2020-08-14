from util.my_read_excel import *
from util.my_to_excel import *
import psycopg2
from datetime import datetime


if __name__=='__main__':
    myconp = ["biaost", "zl_reader", "zl_reader", "192.168.60.61", "5433", "public", "dm"]
    root_dir = os.path.dirname(os.path.abspath('.')) + '/bst_new/data'
    infilename = root_dir + r"\test_sheng_zz_result\云南_省平台ryzz_整理后_胡金花_20200728_145622.xlsx"
    outfilename = root_dir + r"\test_sheng_zz_result\云南_省平台ryzz_测试结果_胡金花_"

    # 读取excel的数据
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][1:]  # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    print(sheet1data)

    # 连接数据库
    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()

    result_data = []
    for row in sheet1data:
        if row[5]:
            sql_zzcode ="""SELECT rycode  FROM    "{schema}"."dict_ry_zz"  
                            where    zclb like   '%{zzlb}%'  
                            and   zhuanye  like  '%{zy}%';""".format(schema=myconp[6],zzlb=row[5].strip(),zy=row[7].strip())
        else:
            sql_zzcode = """SELECT rycode  FROM    "{schema}"."dict_ry_zz"  
                                        where    zclb like   '%{zzlb}%';""".format(schema=myconp[6], zzlb=row[5].strip())
        print(sql_zzcode)

        cur.execute(sql_zzcode)
        result_zzcode = cur.fetchall()
        tmp=[]
        ishave_zzcode = "无"
        # 是否有相应的人员资质
        if result_zzcode:
            ent_key_sql ="""select ent_key from "{schema}"."app_qy_query" WHERE entname = '{zbr}' ;""".format(schema=myconp[5],zbr=row[2].strip())

            cur.execute(ent_key_sql)
            ent_key_result = cur.fetchall()
            # 是否有相应的企业
            if ent_key_result:
                ent_key = ent_key_result[0][0]

                sql_string = """with a as ( select unnest(ry_zz_info) as r,ent_key from "{schema}"."app_qy_query" WHERE entname = '{zbr}' 
                                                AND EXISTS (SELECT  1  from  UNNEST (ry_zz_info) AS T (A)  WHERE   A ->> 'name'='{name}'))
                                select r::jsonb->>'ryzz_code' ryzz_code  ,r::jsonb->>'person_key' person_key 
                                from a where r::jsonb->>'name' = '{name}';""".format(schema=myconp[5],zbr=row[2].strip(),name=row[3].strip())
                print(sql_string)

                cur.execute(sql_string)
                result = cur.fetchall()

                # 判断bst相应企业是否有相应的资质
                person_key=''
                bst_rycode=''
                for content in result:
                    person_key=content[1]
                    bst_rycode =content[0]
                    print(content[0][0:len(result_zzcode[0][0])])
                    if result_zzcode[0][0] == content[0] or  result_zzcode[0][0] == content[0][0:len(result_zzcode[0][0])]:
                        ishave_zzcode = "有"
                        break
                tmp=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],result_zzcode[0][0],bst_rycode,ishave_zzcode,person_key,ent_key]
            else:tmp=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],result_zzcode[0][0],"",ishave_zzcode,"","bst没有该企业"]
        else:tmp=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],"","bst目录表无相应的资质","",ishave_zzcode,"",""]

        result_data.append(tmp)
        print(result_data)

    # 数据保存到Excel
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng","shi","zbr", "name", "sfz", "zclb_jb","zczsh","zczy","省平台code","bst_code","bst相应人是否有相应的资质","person_key","ent_key"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "Sheet1", columnRows, result_data)
    print("to excel scuess")

    # 关闭数据库资源
    if cur: cur.close()
    if conn:conn.close()
