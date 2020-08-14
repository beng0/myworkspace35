from bst.bst_datatest.test_case.models.get_db_excel import *
import psycopg2
import sqlalchemy

def jst_qyyj(conp,myconp,outfilename1,outfilename2,jst_qyyj_table,jst_qyyj_atbst_table):
    try:
        schema = myconp[5]
        mySchema=myconp[6]
        conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
        cur = conn.cursor()

        # 先创建一个建设通公告通过公告名称在gg_meta的结果
        sql_date="""drop table if exists "{mySchema}"."{tablename}";
            create  table  "{mySchema}"."{tablename}"(
                        href  varchar(500) ,
                        diqu  varchar(500) ,
                        quyu varchar(500) ,
                        fabu_time varchar(500) ,
                        ggtype varchar(500) ,
                        jytype varchar(500) ,
                        gg_name varchar(500) ,
                        html_key varchar(500) ,
                        person_key varchar(500) ,
                        zhongbiaoren varchar(500) ,
                        xmjl  varchar(500)
                        );""".format(tablename=jst_qyyj_atbst_table,mySchema=mySchema)
        cur.execute(sql_date)
        conn.commit()


        sql_name = """SELECT  TRIM(xmjl) ,TRIM(zhongbiaoren),trim(ggname)  FROM    "{mySchema}"."{jst_qyyj_table}"   where xmjl is not Null and zhongbiaoren is not Null and ggname is not null""".format(jst_qyyj_table=jst_qyyj_table,mySchema=mySchema)
        cur.execute(sql_name)
        results = cur.fetchall()
        for row in results:
            xmjl1 = row[0]
            zhongbiaoren1 = row[1]
            ggname1 = row[2]

            # 检查gg_meta表
            sql_gg_meta = """select  count(*) as count from  "{schema}".gg_meta  where   gg_name   like  '%{ggname}%';""".format(schema=schema, ggname=ggname1)
            cur.execute(sql_gg_meta)
            result_gg_meta = cur.fetchall()
            for count in result_gg_meta:
                if count[0] > 0:
                    # 建设通公告标事通是否有gg_meta
                    set_gg_meta = """update "{mySchema}"."{jst_qyyj_table}"   set  gg_meta='OK'   WHERE  xmjl='{xmjl}'  and   zhongbiaoren='{zhongbiaoren}'
                                and   ggname ='{ggname}' ; """.format(schema=schema, mySchema=mySchema,
                                                                      jst_qyyj_table=jst_qyyj_table, xmjl=xmjl1,
                                                                      zhongbiaoren=zhongbiaoren1, ggname=ggname1)
                    print(set_gg_meta)
                    cur.execute(set_gg_meta)
                    conn.commit()

                    get_gg_meta = """select  href,diqu,quyu,fabu_time,ggtype,jytype,gg_name,html_key,person_key,zhongbiaoren,xmjl
                               from  "{schema}".gg_meta  where   gg_name like  '%{ggname}%'""".format(schema=schema,
                                                                                                      ggname=ggname1)
                    cur.execute(get_gg_meta)
                    result_get_gg_meta = cur.fetchall()
                    # 把建设通企业业绩通过公告名称模糊查询得到在gg_meta中的值
                    for row in result_get_gg_meta:
                        href = row[0]
                        diqu = row[1]
                        quyu = row[2]
                        fabu_time = row[3]
                        ggtype = row[4]
                        jytype = row[5]
                        gg_name = row[6]
                        html_key = row[7]
                        person_key = row[8]
                        zhongbiaoren2 = row[9]
                        xmjl2 = row[10]

                        jst_qyyj_atbst_sql = """insert   into  "{mySchema}"."{jst_qyyj_atbst_table}"(href,diqu,quyu,fabu_time,ggtype,jytype,gg_name,html_key,person_key,zhongbiaoren,xmjl)
                                   VALUES('{href}','{diqu}','{quyu}','{fabu_time}','{ggtype}','{jytype}','{gg_name}','{html_key}',
                                     '{person_key}','{zhongbiaoren}','{xmjl}'); """.format(mySchema=mySchema,
                                                                                           jst_qyyj_atbst_table=jst_qyyj_atbst_table,
                                                                                           href=href,
                                                                                           diqu=diqu, quyu=quyu,
                                                                                           fabu_time=fabu_time, ggtype=ggtype,
                                                                                           jytype=jytype,
                                                                                           gg_name=gg_name, html_key=html_key,
                                                                                           person_key=person_key,
                                                                                           zhongbiaoren=zhongbiaoren2, xmjl=xmjl2)
                        # print(sql4)
                        try:
                            cur.execute(jst_qyyj_atbst_sql)
                            conn.commit()
                        except  BaseException  as  msg:
                            print(jst_qyyj_atbst_sql)
                            continue
                else:
                    set_gg_meta2 = """update "{mySchema}"."{jst_qyyj_table}"   set  gg_meta='NO'   WHERE  xmjl='{xmjl}'  and   zhongbiaoren='{zhongbiaoren}'
                                                    and   ggname ='{ggname}' ; """.format(schema=schema, mySchema=mySchema,
                                                                                          jst_qyyj_table=jst_qyyj_table,
                                                                                          xmjl=xmjl1,
                                                                                          zhongbiaoren=zhongbiaoren1,
                                                                                          ggname=ggname1)
                    print(set_gg_meta2)
                    cur.execute(set_gg_meta2)
                    conn.commit()
                    # db_command(sql5, dbtype=dbtype, conp=conp)

        sql_name2 = """SELECT  TRIM(xmjl) ,TRIM(zhongbiaoren),trim(ggname)  FROM    "{mySchema}"."{jst_qyyj_table}"   where xmjl is not Null and zhongbiaoren is not Null and ggname is not null""".format(
                jst_qyyj_table=jst_qyyj_table, mySchema=mySchema)
        cur.execute(sql_name2)
        results2 = cur.fetchall()
        for row in results2:
            xmjlname = row[0]
            zbr = row[1]
            ggname = row[2]

            # 检查gg表
            sql_gg = """select  count(*) as count from  "{schema}".gg  where   gg_name like '%{ggname}%';""".format(schema=schema, ggname=ggname)
            print("sql_gg  " + sql_gg)
            cur.execute(sql_gg)
            result_gg = cur.fetchall()
            for count in result_gg:
                print("gg count    "+  str(count[0]))
                if count[0] > 0:
                    # 建设通公告标事通是否有gg
                    set_gg = """update "{mySchema}"."{jst_qyyj_table}"   set  gg='OK'   WHERE  xmjl='{xmjl}'  and   zhongbiaoren='{zhongbiaoren}'
                            and   ggname ='{ggname}' ; """.format(schema=schema,mySchema=mySchema,jst_qyyj_table=jst_qyyj_table,xmjl=xmjlname,zhongbiaoren=zbr,ggname=ggname)
                    print("set_gg  " + set_gg)
                    cur.execute(set_gg)
                    conn.commit()
                else:
                    set_gg2 = """update "{mySchema}"."{jst_qyyj_table}"   set  gg='NO'   WHERE  xmjl='{xmjl}'  and   zhongbiaoren='{zhongbiaoren}'
                                and   ggname ='{ggname}' ; """.format(schema=schema,mySchema=mySchema,jst_qyyj_table=jst_qyyj_table,xmjl=xmjlname,zhongbiaoren=zbr,ggname=ggname)
                    print("set_gg2  " + set_gg2)
                    cur.execute(set_gg2)
                    conn.commit()


        sql_query_all = '''select * from    "{mySchema}"."{tablename}"   ORDER BY  id::int'''.format(tablename=jst_qyyj_table,mySchema=mySchema)
        # cur.execute(sql_query_all)
        # result = cur.fetchall()
        result1 = db_query(sql_query_all, dbtype='postgresql', conp=conp)
        read_db_2_excel(conp,outfilename1,result1)

        sql_query_all2 = '''select * from    "{mySchema}"."{tablename}"  '''.format(tablename=jst_qyyj_atbst_table, mySchema=mySchema)
        result = db_query(sql_query_all2, dbtype='postgresql', conp=conp)
        # cur.execute(sql_query_all2)
        # result = cur.fetchall()
        read_db_2_excel(conp, outfilename2, result)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


#在gg_meta获取云南待测试的数据
def get_gg_meta_to_zbrxmjl(dbtype,conp,filename,sql,mySchema,tablename,total,count):
    results = db_query(sql, dbtype="postgresql", conp=conp).values.tolist()
    # print(' '.join(results))
    # print(results)
    for href,diqu,quyu,fabu_time,ggtype,jytype,gg_name,html_key,person_key,zhongbiaoren,xmjl in results:
        sql = """insert   into  "{mySchema}"."{tablename}"(href,diqu,quyu,fabu_time,ggtype,jytype,gg_name,html_key,person_key,zhongbiaoren,xmjl)     
           VALUES('{href}','{diqu}','{quyu}','{fabu_time}','{ggtype}','{jytype}','{gg_name}','{html_key}',
             '{person_key}','{zhongbiaoren}','{xmjl}'); """.format(mySchema=mySchema,tablename=tablename,href=href,diqu=diqu,quyu=quyu,
                                                                                            fabu_time=fabu_time,ggtype=ggtype,jytype=jytype,
                                                                                            gg_name=gg_name,html_key=html_key,person_key=person_key,
                                                                                            zhongbiaoren=zhongbiaoren,xmjl=xmjl)
        # print("update  sql: "+sql)
        db_command(sql, dbtype=dbtype, conp=conp)
    # out_all_data(dbtype, conp, filename, sql, mySchema, tablename)
    print("共",total,"个网站，已完成",count,"个网站")

# 导出所有的数据
def out_all_data(dbtype,conp,filename,sql,mySchema,tablename):
     sql_date = """update  "{mySchema}"."{tablename}"   set    person_key=REPLACE(person_key,'.0','');""".format(mySchema=mySchema,tablename=tablename)
     db_command(sql_date, dbtype=dbtype, conp=conp)

     sql_query_all = '''select * from "{mySchema}"."{tablename}" '''.format(mySchema=mySchema,tablename=tablename)
     result = db_query(sql_query_all, dbtype=dbtype, conp=conp)
     read_db_2_excel(conp, filename, result)