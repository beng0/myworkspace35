from bst_new.util.my_read_excel import *
from bst_new.util.my_to_excel import *
import psycopg2
from datetime import datetime

if  __name__=='__main__':
    myconp = ["biaost", "zl_reader", "zl_reader", "192.168.60.61", "5433", "public", "zl_test"]
    root_dir = os.path.dirname(os.path.abspath('.'))
    infilename = root_dir + r"\data\xmjl_list\广东_云南_山西_jst_xmjlyj_抽取的企业_每个企业6条_胡金花_2020-07-27_134842.xlsx"
    outfilename = root_dir + r"\data\get_bst_xmjlyj\广东_云南_山西_bst_xmjlyj_获取结果_胡金花_"

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

        xmjl_yj_sql="""select   unnest(ry_zhongbiao_info)::jsonb ->> 'href' href,
                        xzqh,entname,name,
                        unnest(ry_zhongbiao_info)::jsonb ->> 'gg_name'  gg_name,
                        unnest(ry_zhongbiao_info)::jsonb ->> 'quyu'  quyu,
                        SUBSTRING(unnest(ry_zhongbiao_info)::jsonb ->> 'fabu_time',0,11)    fabu_time,
                        unnest(ry_zhongbiao_info)::jsonb ->> 'html_key' html_key 
                        FROM  "{schema}".app_ry_query WHERE name='{xmjl}' and entname='{zhongbiaoren}'     
                        ORDER BY   to_date(SUBSTRING(unnest(ry_zhongbiao_info)::jsonb ->> 'fabu_time',0,11),'yyyy-MM-dd')   desc ;""".format(schema=myconp[5],xmjl=xmjl,zhongbiaoren=zhongbiaoren)
        # print(xmjl_yj_sql)
        cur.execute(xmjl_yj_sql)
        result = cur.fetchall()
        for content in  result:
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href",  "xzqh", "zhongbiaoren", "xmjl", "ggname", "quyu", "zbtime","html_key"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, data)

    if cur:
        cur.close()
    if conn:
        conn.close()



