#coding= utf-8

from py_grab_test.selenium_base import *

se = Base_()
bs = Bsoup()
de = Doexcel()

qynames = []
qyzzs = []
lis = de.read_excel("E://mydata/浙江/浙江建设通企业资质_数据准备_胡金花_20200601_142300.xlsx","Sheet1")
for j in range(1,250):
    qyname1 = lis[j-1][0]
    qyname = lis[j][0]
    if qyname1 == qyname:
        continue
    else:
        se.open_("http://223.4.65.131:8080/enterprise.php")
        time.sleep(2)
        se.get_position("css selector", "input#CorpName").send_keys(qyname)
        time.sleep(1)
        se.click_("css selector", "input[value='搜索']")
        time.sleep(1)
        totalnum = se.get_text("span.vcountPage")
        print(totalnum)
        if int(totalnum) > 0:
            se.click_s("tr.auto_h>td:nth-child(2) a")
            print(1)
            time.sleep(1)
            soup = bs.get_soup("div.t1")
            tbodys = soup.select("div.zizhi_list>table>tbody")
            for tbody in tbodys:
                trs = tbody.select("tr")
                if len(trs) < 4:
                    qynames.append(qyname)
                    qyzzs.append("")
                else:
                    trs1 = tbody.select("div.zizhi_list>table>tbody table>tbody>tr")
                    for i in range(1,len(trs1)):
                        qyzz = trs1[i].select("td")[0].get_text()
                        print(qyzz)
                        qyzzs.append(qyzz)
                        qynames.append(qyname)
        else:
            print(2)
            qynames.append(qyname)
            qyzzs.append(qyzz)

de.excel_w("E://mydata/浙江/zhejiangqyzz.xls","sheet1",qynames,qyzzs)
