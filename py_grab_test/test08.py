from py_grab_test.selenium_base import *
from bs4 import BeautifulSoup

se = Base_()
bs = Bsoup()
de = Doexcel()
se.open_("http://cx.jlsjsxxw.com/corpinfo/CorpInfo.aspx")


qyzzs = []
qynames1 = []
qyhrefs = ["http://cx.jlsjsxxw.com/CorpInfo/CorpDetailInfo.aspx?rowGuid=6c4f9544-11f0-4fed-9bb3-e8bac3a7a27a&corpid=74843445-8&VType=1"]
for href in qyhrefs:
    se.open_(href)
    qyname1 = se.get_text(".cpd_basic_table>tbody>tr:nth-child(1)>td:nth-child(2)")
    soup = bs.get_soup(".details_infor_container>.details_infor_content_01")
    tabs = soup.select("table")
    print(tabs)
    for tab in tabs:
        qyzzs_mm = tab.select("tbody>tr:nth-child(3)>td:nth-child(2)")[0].get_text().split(";")
        print(qyzzs_mm)
        if qyzzs_mm[-1] == '':
            qyzzs_mm.pop()
        # print(qyzzs_m)
        for qyzz in qyzzs_mm:
            qyzzs.append(qyzz)
            print(qyzzs)
            qynames1.append(qyname1)

de.excel_w("E://mydata/jilinQyzz.xls","sheet1",qynames1,qyzzs)