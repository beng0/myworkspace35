from bst.bst_datatest.test_case.models.my_read_excel import  *
import psycopg2
from datetime import datetime
from bst.bst_datatest.test_case.models.my_to_excel import  *

if  __name__=='__main__':
    myconp = ["biaost", "zl_reader", "zl_reader", "192.168.60.61", "5433", "public", "zl_test"]
    infilename = r"D:\SVN\数据对比\对比结果\每周云南广东对比\广东项目经理抽取.xlsx"
    outfilename = r"D:\SVN\数据对比\对比结果\每周云南广东对比\广东标事通项目经理业绩_"

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
        # print(zhongbiaoren)
        xmjl = row[1].strip()
        # print(xmjl)

        xmjl_yj_sql="""select   unnest(ry_zhongbiao_info)::jsonb ->> 'href' href,xzqh,entname,name,
                        unnest(ry_zhongbiao_info)::jsonb ->> 'gg_name'  gg_name,
                        unnest(ry_zhongbiao_info)::jsonb ->> 'quyu'  quyu,
                        SUBSTRING(unnest(ry_zhongbiao_info)::jsonb ->> 'fabu_time',0,11)    fabu_time 
                        FROM  "{schema}".app_ry_query WHERE name='{xmjl}' and entname='{zhongbiaoren}'     
                        ORDER BY   to_date(SUBSTRING(unnest(ry_zhongbiao_info)::jsonb ->> 'fabu_time',0,11),'yyyy-MM-dd')   desc ;""".format(schema=myconp[5],xmjl=xmjl,zhongbiaoren=zhongbiaoren)
        print(xmjl_yj_sql)
        cur.execute(xmjl_yj_sql)
        result = cur.fetchall()
        print(result)
        for content in  result:
            print(content)
            data.append(content)
            print(data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href", "shi", "zhongbiaoren", "ggname", "diqu", "xmjl", "zbtime", "zbly"]
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, data)

    if cur:
        cur.close()
    if conn:
        conn.close()



