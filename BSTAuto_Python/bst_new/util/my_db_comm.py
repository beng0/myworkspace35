import psycopg2


def get_db_connect(myconp):
    conn = psycopg2.connect(database=myconp[0], user=myconp[1], password=myconp[2], host=myconp[3], port=myconp[4])
    cur = conn.cursor()
    return conn,cur

def close_all_resources(conn,cur):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

