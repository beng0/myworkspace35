from bst.bst_datatest.test_case.models.my_db_comm import get_db_connect,close_all_resources

def write_data_to_db(myconp,mySchema,tableName,all_sheet_data):
    conn,cur = get_db_connect(myconp)
    field_sql=creat_table(conn, cur, mySchema, tableName, all_sheet_data)
    insert_data(conn, cur, mySchema, tableName, all_sheet_data,field_sql)
    close_all_resources(conn, cur)


def creat_table(conn,cur,mySchema,tableName,all_sheet_data):

    sheetValue=[]
    field_count=0
    for content in all_sheet_data:
        sheetValue=content[1]
        field_count = len(sheetValue[0])

    count = 0
    field_sql = []
    for  field in sheetValue[0]:
        if  count == field_count-1:
            temp = field + '  varchar(500)  '
            field_sql.append(temp)
            break
        temp= field +'  varchar(500) ,'
        field_sql.append(temp)
        count +=1

    s = ' '.join(field_sql)
    creat_table_sql='drop table if exists "{mySchema}"."{tableName}"; create  table  "{mySchema}"."{tableName}"('.format(mySchema=mySchema,tableName=tableName)+ s + ');'
    cur.execute(creat_table_sql)
    conn.commit()
    print("表创建成功")
    return sheetValue[0]


def  insert_data(conn,cur,mySchema,tableName,all_sheet_data,field_sql):
    insert_sql1= ','.join(field_sql)
    s4="%s"
    insert_sql2=ping_string2(field_sql,s4)
    insert_sql_format ='insert   into  "{mySchema}"."{tableName}"('.format(mySchema=mySchema,tableName=tableName)+insert_sql1+')  VALUES('+insert_sql2+'); '

    for sheetConte in all_sheet_data:
        # 得到sheet名字
        # sheetName =sheetConte[0]
        # 得到每个sheet中的内容
        sheetValue = sheetConte[1]
        # 得到除了第一行(字段名字)的所有表数据
        all_insert_sql=[]
        col_count =0
        for row in sheetValue[1:]:
            # row_sql_temp = []
            # for col in row:
            #     temp="'"+str(col)+"'"
            #     row_sql_temp.append(temp)
            #     col_count += 1
            #     # print(row_sql_temp)
            # all_insert_sql.append(row_sql_temp)

            values=("'"+str(row[0])+"'","'"+str(row[1])+"'","'"+str(row[2])+"'","'"+str(row[3])+"'","'"+str(row[4])+"'","'"+str(row[5])+"'","'"+str(row[6])+"'","'"+str(row[7])+"'")
            insert_sql=insert_sql_format % values
            print(insert_sql)
            all_insert_sql.append(insert_sql)

        insert_sql2 = ' '.join(all_insert_sql)
        print(insert_sql2)
        try:
            cur.execute(insert_sql2)
            conn.commit()
        except  BaseException  as  msg:
            print(insert_sql2)
            continue

def ping_string2(field_sql,s1):
    field_sql_temp = []
    for  field in field_sql:
        temp= s1
        field_sql_temp.append(temp)
    s = ','.join(field_sql_temp)
    return s



def ping_string(field_sql,s1,s2,s3):
    field_sql_count=len(field_sql)
    count = 0
    field_sql_temp = []
    for  field in field_sql:
        if  count == field_sql_count-1:
            temp = s1+field +s3
            field_sql_temp.append(temp)
            break
        temp= s1+field +s2
        field_sql_temp.append(temp)
        count +=1

    s = ' '.join(field_sql_temp)
    return s