#coding=utf-8
from py_grab_test.selenium_base import *

rynames = []
ryzzs = []
zhuanyes = []
qynames = []
se = Base_()
bs = Bsoup()
de = Doexcel()
# 浙江建设通人员资质_胡金花_20200601_124542.xlsx
lis = de.read_excel("E://mydata/浙江/浙江建设通人员资质_胡金花_20200601_124542.xlsx","Sheet1")

for j in range(1,20):
    qyname1 = lis[j-1][0]
    qyname = lis[j][0]
    if qyname1 == qyname:
        continue
    else:
        se.open_("http://223.4.65.131:8080/enterprise.php")
        time.sleep(2)
        se.get_position("css selector","input#CorpName").send_keys(qyname)
        time.sleep(1)
        se.click_("css selector","input[value='搜索']")
        time.sleep(1)
        totalnum = se.get_text("span.vcountPage")
        print(totalnum)
        if int(totalnum) > 0:
            # se.click_("css selector","tr.auto_h>td:nth-child(2) a")
            se.click_s("tr.auto_h>td:nth-child(2) a")
            print(1)
            se.click_("id", "t2")
            time.sleep(1)
            tbody = bs.get_soup(".classContent.t2>.detail_list>tbody")
            trs = tbody.select("tr")
            for i in range(1, len(trs)):
                ryname = trs[i].select("td:nth-child(2)>a")[0].get_text().strip()
                ryzz = trs[i].select("td:nth-child(4)")[0].get_text().strip()
                zhuanyems = trs[i].select("td:nth-child(6)")[0].get_text().strip().split(",")
                for zhuanye in zhuanyems:
                    zhuanyes.append(zhuanye)
                    qynames.append(qyname)
                    rynames.append(ryname)
                    ryzzs.append(ryzz)


            # print(rynames)
            # print(ryzzs)
            # print(zhuanyes)
        else:
            print(2)
            qynames.append(qyname)
            rynames.append("")
            zhuanyes.append("")
            ryzzs.append("")





de.excel_w("E://mydata/浙江/zhejiangryzz.xls","sheet1",qynames,rynames,ryzzs,zhuanyes)