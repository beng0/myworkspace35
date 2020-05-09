#coding=utf-8

from py_grab_test.selenium_base import  *
import xlwt
from bs4 import BeautifulSoup

book = xlwt.Workbook()
sheet = book.add_sheet("sheet1",cell_overwrite_ok=True)

se = Base_()

se.open_("http://hngcjs.hnjs.gov.cn/company/list?corpname=")
# driver.switch_to_frame("newsiframe")
# ele = se.get_position("css selector","select#CretType")
#
# s = Select(ele)
# s.select_by_value("1")
# 选择建筑业
se.select_by_value("css selector","select#CretType","7")
# 点击唤出企业注册地下拉框
# se.click_("css selector",".filter_dropdown>span>span")
# 获取注册地的个数
len_di = len(se.get_positions("css selector",".dropdown-menu.staff_dropdown>li"))
print(len_di)
# 定义数据用来存储数据
qynames = []
qyhrefs = []
qydizis = []


for i in range(1,len_di+1):
    # 选择企业注册地
    se.click_("css selector", ".filter_dropdown>span>span")
    time.sleep(1)
    se.click_("css selector",".dropdown-menu.staff_dropdown>li:nth-child("+str(i)+")>a")
    # 点击搜索
    se.click_("name","ctl09")
    # 保存页面并转换为bs4文档
    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html,"html.parser")
    # 获取每一行
    qylis = soup.select("#tagContenth tbody>tr")
    # 获取第一页企业的数量
    len_q = len(qylis)
    print(len_q)
    for i in range(2,len_q+1):
        # 获取企业名称
        qyname = soup.select("#tagContenth tbody>tr:nth-child("+str(i)+")>td:nth-child(2)>a")[0].get_text()
        qynames.append(qyname)
        # 获取企业链接
        qyhref = "http://hngcjs.hnjs.gov.cn"+ soup.select("#tagContenth tbody>tr:nth-child("+str(i)+")>td:nth-child(2)>a")[0]["href"]
        qyhrefs.append(qyhref)
        # 获取企业注册地
        qydizi = soup.select("#tagContenth tbody>tr:nth-child("+str(i)+")>td:nth-child(5)>span")[0].get_text()
        qydizis.append(qydizi)

print(qynames)
print(qyhrefs)
print(qydizis)

len_a = len(qynames)
for i in range(1,len_a):
    row = i
    qyname = qynames[i-1]
    qyhref = qyhrefs[i-1]
    qydizi = qydizis[i-1]
    sheet.write(row,1,qyname)
    sheet.write(row,2,qyhref)
    sheet.write(row,3,qydizi)

book.save("E://mydata//qyzznames.xls")
print("success")


