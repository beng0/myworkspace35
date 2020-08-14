#coding=utf-8
__Author__ = "hejb"
from py_grab_test.selenium_base import  *
import xlwt
import xlrd
from bs4 import BeautifulSoup

se = Base_()

book = xlrd.open_workbook("E://mydata/rylist.xls")
sheet = book.sheet_by_index(0)

book_w = xlwt.Workbook()
sheet_w = book_w.add_sheet("sheet1",cell_overwrite_ok=True)

print(sheet.nrows)

names = []
qys = []
ryzzs = []
zhuanyes = []
ryhrefs = []

for i in range(1,sheet.nrows):
    name = sheet.cell(i,1).value
    qy = sheet.cell(i,3).value
    ryzz = sheet.cell(i,4).value
    ryhref = sheet.cell(i,2).value
    se.open_(ryhref)
    # 获取人员详情页面的html并转换为bs4文档
    strjs_r = """var topwin = window.top.document.getElementById("newsiframe").contentWindow;
    return topwin.document.querySelector("div.news_con").innerHTML"""
    html = driver.execute_script(strjs_r)
    soup = BeautifulSoup(html,"html.parser")
    # 检查是否有注册专业，k为注册专业个数
    k = 0
    for string in soup.strings:
        if "注册专业" in string:
            k+=1
    # 如果有专业，遍历专业
    zhuanyes_m = []
    if k > 0 and "注册建造师" in ryzz:
        for j in range(k):
            zhuanyes_m.append(soup.select("tbody>tr:nth-child(%d)>td:nth-child(2)"%(j+2))[0])
        print(zhuanyes_m)
    elif k>0 and ("注册监理工程师" in ryzz or "注册造价工程师" in ryzz):
        for j in range(k):
            zhuanyes_m = (soup.select("tbody>tr:nth-child(%d)>td:nth-child(2)>span"%(j+2)))
        print(zhuanyes_m)
    else:
        zhuanyes_m = BeautifulSoup("<td></td>","html.parser").select("td")
    for n in zhuanyes_m:
        zhuanye = n.get_text()
        zhuanyes.append(zhuanye)
        names.append(name)
        qys.append(qy)
        ryzzs.append(ryzz)
        ryhrefs.append(ryhref)

print(zhuanyes)

len_a = len(zhuanyes)
for i in range(1,len_a):
    row = i
    name = names[i-1]
    ryhref = ryhrefs[i-1]
    qy = qys[i-1]
    ryzz = ryzzs[i-1]
    zhuanye = zhuanyes[i-1]
    sheet_w.write(row,3,name)
    sheet_w.write(row,2,ryhref)
    sheet_w.write(row,1,qy)
    sheet_w.write(row,4,ryzz)
    sheet_w.write(row,5,zhuanye)

book_w.save("E://mydata//henanryzz.xls")
print("success")








