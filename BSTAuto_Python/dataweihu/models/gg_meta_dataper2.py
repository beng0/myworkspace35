from bst.bst_datatest.test_case.models.get_db_excel import *
import psycopg2
import sqlalchemy

def jst_qyyj(dbtype,conp,mySchema,outfilename1,outfilename2,jst_qyyj_table,jst_qyyj_atbst_table):
    schema = conp[5]

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
    # print(sql_date)
    db_command(sql_date, dbtype=dbtype, conp=conp)

    # sql_name = """SELECT  TRIM(xmjl) ,TRIM(zhongbiaoren),trim(ggname),REPLACE(REPLACE(REPLACE(REPLACE(trim(ggname),'（','\（'),'(','\('),'）','\）'),')','\)') ggname1  FROM    "{mySchema}"."{jst_qyyj_table}"   where xmjl is not Null and zhongbiaoren is not Null and ggname is not null""".format(jst_qyyj_table=jst_qyyj_table,mySchema=mySchema)
    sql_name = """SELECT  TRIM(xmjl) ,TRIM(zhongbiaoren),trim(ggname)  FROM    "{mySchema}"."{jst_qyyj_table}"   where xmjl is not Null and zhongbiaoren is not Null and ggname is not null""".format(jst_qyyj_table=jst_qyyj_table,mySchema=mySchema)
    # print(sql_name)
    results = db_query(sql_name, dbtype=dbtype, conp=conp).values.tolist()
    # print(results)
    for xmjl,zhongbiaoren,ggname in results:
            ggname2=ggname
        # try:
            sql8=f"""select  count(*) as count from  "{schema}".gg  where   gg_name like '%%{ggname}%%';"""
            # sql88 = str(sqlalchemy.text(sql8))
            # print("888  "+sql88)
            result8 = db_query(sql8, dbtype=dbtype, conp=conp).values.tolist()
            # result8 = db_query(sql8, dbtype=dbtype, conp=conp)
            for count in result8:
                if count[0] > 0:
                    # 建设通公告标事通是否有gg
                    sql8 = """update "{mySchema}"."{jst_qyyj_table}"   set  gg='OK'   WHERE  xmjl='{xmjl}'  and   zhongbiaoren='{zhongbiaoren}'
                                                and   ggname ='{ggname}' ; """.format(schema=schema, mySchema=mySchema,
                                                                                      jst_qyyj_table=jst_qyyj_table,
                                                                                      xmjl=xmjl,
                                                                                      zhongbiaoren=zhongbiaoren,
                                                                                      ggname=ggname)
                    print(sql8)
                    db_command(sql8, dbtype=dbtype, conp=conp)



            # sql1 = """select  count(*) count from  "{schema}".gg_meta   where   gg_name ~'{ggname}'""".format(schema=schema,ggname=ggname2)
            sql1= """select  count(*) as count from  "{schema}".gg_meta  where   gg_name   like  '%%{ggname}%%';""".format(schema=schema,ggname=ggname)
            result2 = db_query(sql1, dbtype=dbtype, conp=conp).values.tolist()
            # print(result2)
            for count in result2:
                if count[0] > 0:
                    # 建设通公告标事通是否有gg_meta
                    sql2 = """update "{mySchema}"."{jst_qyyj_table}"   set  gg_meta='OK'   WHERE  xmjl='{xmjl}'  and   zhongbiaoren='{zhongbiaoren}'
                            and   ggname ='{ggname}' ; """.format(schema=schema,mySchema=mySchema, jst_qyyj_table=jst_qyyj_table, xmjl=xmjl,zhongbiaoren=zhongbiaoren,ggname=ggname)
                    print(sql2)
                    db_command(sql2, dbtype=dbtype, conp=conp)

                    sql3="""select  href,diqu,quyu,fabu_time,ggtype,jytype,gg_name,html_key,person_key,zhongbiaoren,xmjl  
                           from  "{schema}".gg_meta  where   gg_name like  '%%{ggname}%%'""".format(schema=schema,ggname=ggname)
                    results3 = db_query(sql3, dbtype="postgresql", conp=conp).values.tolist()
                    # print(results3)
                    # 把建设通企业业绩通过公告名称模糊查询得到在gg_meta中的值
                    for href, diqu, quyu, fabu_time, ggtype, jytype, gg_name, html_key, person_key, zhongbiaoren, xmjl in results3:
                        sql4 = """insert   into  "{mySchema}"."{jst_qyyj_atbst_table}"(href,diqu,quyu,fabu_time,ggtype,jytype,gg_name,html_key,person_key,zhongbiaoren,xmjl)     
                               VALUES('{href}','{diqu}','{quyu}','{fabu_time}','{ggtype}','{jytype}','{gg_name}','{html_key}',
                                 '{person_key}','{zhongbiaoren}','{xmjl}'); """.format(mySchema=mySchema,
                                                                                       jst_qyyj_atbst_table=jst_qyyj_atbst_table, href=href,
                                                                                       diqu=diqu, quyu=quyu,
                                                                                       fabu_time=fabu_time, ggtype=ggtype,
                                                                                       jytype=jytype,
                                                                                       gg_name=gg_name, html_key=html_key,
                                                                                       person_key=person_key,
                                                                                       zhongbiaoren=zhongbiaoren, xmjl=xmjl)
                        # print(sql4)
                        db_command(sql4, dbtype=dbtype, conp=conp)
                else:
                    sql5 = """update "{mySchema}"."{jst_qyyj_table}"   set  gg_meta='NO'   WHERE  xmjl='{xmjl}'  and   zhongbiaoren='{zhongbiaoren}'
                                                and   ggname ='{ggname}' ; """.format(schema=schema, mySchema=mySchema,
                                                                                      jst_qyyj_table=jst_qyyj_table,
                                                                                      xmjl=xmjl,
                                                                                      zhongbiaoren=zhongbiaoren,
                                                                                      ggname=ggname)
                    print(sql5)
                    db_command(sql5, dbtype=dbtype, conp=conp)


    sql_query_all = '''select * from    "{mySchema}"."{tablename}"   ORDER BY  id::int'''.format(tablename=jst_qyyj_table,mySchema=mySchema)
    result = db_query(sql_query_all, dbtype=dbtype, conp=conp)
    read_db_2_excel(conp,outfilename1,result)

    sql_query_all2 = '''select * from    "{mySchema}"."{tablename}"  '''.format(tablename=jst_qyyj_atbst_table, mySchema=mySchema)
    result = db_query(sql_query_all2, dbtype=dbtype, conp=conp)
    read_db_2_excel(conp, outfilename2, result)



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