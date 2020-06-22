import psycopg2
import xlrd
import xlwt


def excel_w(file_position, sheet_name,col, lis):
    book = xlwt.Workbook()
    sheet = book.add_sheet(sheet_name, cell_overwrite_ok=True)
    for r in range(len(lis)):
        sheet.write(r + 1, col, lis[r])
    book.save(file_position)
    print("write excel success")

list1 = []
book = xlrd.open_workbook("E://mytest/test01ry.xlsx")
sheet = book.sheet_by_index(0)
print(sheet.row_values(0))
print(sheet.nrows)
conn = psycopg2.connect(host="192.168.1.171",user="postgres",password="since2015",database="zljzsheng",port="5432")
cur = conn.cursor()
for i in range(1,sheet.nrows):
    strdb = """SELECT * FROM zljzsheng_hebei_renyuan.gg_html WHERE page ~ '%s' AND page ~ '%s';"""%(sheet.cell(i,2).value,sheet.cell(i,3).value)
    cur.execute(strdb)
    lis = cur.fetchall()
    print(lis)
    if len(lis) > 0:
        list1.append("ok")
    else:
        list1.append("")
excel_w("E://mytest/test01ry.xlsx","sheet1",11,list1)

conn.close()



