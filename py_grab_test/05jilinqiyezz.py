#coding=utf-8
__Author__  = "hejb"
from py_grab_test.selenium_base import *
from bs4 import BeautifulSoup

se = Base_()
bs = Bsoup()
de = Doexcel()
se.open_("http://cx.jlsjsxxw.com/corpinfo/CorpInfo.aspx")

qynames = []
qydiqus = []
qyzzas = []
qyhrefs = []
# 获取所有可选择的市
diqus = se.get_positions("css selector","#ddlCity>option")
# 获取所有可选择的资质
qyzzns = se.get_positions("css selector","#ddlZzlx>option")
for d in range(1,len(diqus)):
    # 选择所在市
    se.select_by_index("css selector","select#ddlCity",d)
    print(len(qyzzas))
    for z in range(1,len(qyzzns)-1):
        # 选择资质
        se.select_by_index("css selector","select#ddlZzlx",z)
        # 获取资质名称
        qyzza = se.get_text("#ddlZzlx>option:nth-child(%d)"%(z+1))
        # 点击搜索按钮
        se.click_("xpath","//select[@id='ddlZzlx']/../../td[7]/input")

        time.sleep(2)
        # 获取列表的soup文档
        soup = bs.get_soup("tbody#tbody_CorpInfo")
        # 获取所有行
        trs = soup.select("tr")
        if len(trs) > 10:
            for i in range(10):
                tr = trs[i]
                # 获取企业名称和地区
                if len(tr.select("tr>td:nth-child(2)")) > 0:
                    qyname = tr.select("tr>td:nth-child(2)>a")[0].get_text()
                    qydiqu = tr.select("tr>td:nth-child(4)")[0].get_text()
                    qyhref = "http://cx.jlsjsxxw.com/" + tr.select("tr>td:nth-child(2)>a")[0]["href"]
                    print(qyhref)
                    # print(qyname)
                    # print(qydiqu)
                    qynames.append(qyname)
                    qydiqus.append(qydiqu)
                    qyzzas.append(qyzza)
                    qyhrefs.append(qyhref)
                else:
                    continue
        else:
            for i in range(len(trs)):
                tr = trs[i]
                # 获取企业名称和地区
                if len(tr.select("tr>td:nth-child(2)"))>0:
                    qyname = tr.select("tr>td:nth-child(2)>a")[0].get_text()
                    qydiqu = tr.select("tr>td:nth-child(4)")[0].get_text()
                    qyhref = "http://cx.jlsjsxxw.com/"+tr.select("tr>td:nth-child(2)>a")[0]["href"]
                    print(qyhref)
                    # print(qyname)
                    # print(qydiqu)
                    qynames.append(qyname)
                    qydiqus.append(qydiqu)
                    qyzzas.append(qyzza)
                    qyhrefs.append(qyhref)
                else:
                    continue

# 保存一个qylist文件
de.excel_w("E://mydata/jilinQyList.xls","sheet1",qynames,qydiqus,qyzzas,qyhrefs)

qyzzs = []
qynames1 = []
for href in qyhrefs:
    se.open_(href)
    qyname1 = se.get_text(".cpd_basic_table>tbody>tr:nth-child(1)>td:nth-child(2)")
    soup = bs.get_soup(".details_infor_container>.details_infor_content_01")
    tabs = soup.select("table")
    print(tabs)
    for tab in tabs:
        qyzzs_mm = tab.select("tbody>tr:nth-child(3)>td:nth-child(2)")[0].get_text().split(";")
        if qyzzs_mm[-1] == '':
            qyzzs_mm.pop()
        for qyzz in qyzzs_mm:
            qyzzs.append(qyzz)
            qynames1.append(qyname1)

de.excel_w("E://mydata/jilinQyzz.xls","sheet1",qynames1,qyzzs)








