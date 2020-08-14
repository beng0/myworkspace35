#coding=utf-8
__Author__ = "hejb"
from py_grab_test.selenium_base import  *
import xlwt
from bs4 import BeautifulSoup

se = Base_()

# 读取企业列表里的数据
tabname = "E://mydata/qyzznames.xls"
book = xlrd.open_workbook(tabname)
sheet = book.sheet_by_index(0)

book_w = xlwt.Workbook()
sheet_w = book_w.add_sheet("sheet1",cell_overwrite_ok=True)

print(sheet.nrows)
print(sheet.ncols)
qynames = []
qyzz_hrefs = []
qyzzs = []
for i in range(1,sheet.nrows):
    # print(sheet.cell(i,2).value)
    qyname = sheet.cell(i,1).value
    qyhref = sheet.cell(i,2).value
    driver.get(qyhref)
    url_h = driver.execute_script(" return document.querySelector('iframe#newsiframe').getAttribute('src')")
    # print(url_h)
    qyzz_href = "http://hngcjs.hnjs.gov.cn" + url_h
    # print(qyzz_href)
    driver.get(qyzz_href)
    time.sleep(1)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].outerHTML")
    soup = BeautifulSoup(html,"html.parser")

    qyzzs_m = soup.select("tbody>tr:nth-child(4)>td:nth-child(2)>span")
    print(qyzzs_m)
    for qyzz in qyzzs_m:
        qyzz = qyzz.get_text().replace(",", "")
        qyzzs.append(qyzz)
        qynames.append(qyname)
        qyzz_hrefs.append(qyzz_href)

print(qyzzs)
print(qynames)
print(qyzz_hrefs)

len_a = len(qyzzs)
for i in range(1,len_a):
    row = i
    qyname = qynames[i-1]
    qyzz_href = qyzz_hrefs[i-1]
    qyzz = qyzzs[i-1]
    sheet_w.write(row,1,qyname)
    sheet_w.write(row,2,qyzz_href)
    sheet_w.write(row,3,qyzz)

book_w.save("E://mydata//qyzz.xls")
print("success")





