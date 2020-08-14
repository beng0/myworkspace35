import psycopg2
from bst.bst_datatest.test_case.models.my_db_comm import get_db_connect,close_all_resources


def  getData(myconp,mySchema,tableName,qury_sql):
    """返回指定表列名和所有数据"""
    conn, cur = get_db_connect(myconp)

    # # 获得列名
    # columnNames_sql = "select COLUMN_NAME from information_schema.COLUMNS where  table_schema = '%s'  and   table_name='%s'" % (mySchema, tableName)
    # cur.execute(columnNames_sql)
    # columnRows = cur.fetchall()

    # 获得所有数据
    cur.execute(qury_sql)
    recordRows = cur.fetchall()

    conn.commit()
    close_all_resources(conn,cur)

    return recordRows