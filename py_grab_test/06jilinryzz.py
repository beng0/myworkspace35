#coding=utf-8
__Author__  = "hejb"

from py_grab_test.selenium_base import *
from bs4 import BeautifulSoup
import re

se = Base_()
bs = Bsoup()
de = Doexcel()

se.open_("http://cx.jlsjsxxw.com/UserInfo/CertifiedEngineers.aspx?Page=1")
# 选取人员资质和点击查询
se.select_by_index("css selector","select#ddlSpecialty",4)
se.click_("id","btnSearch")
rynames = []
qynames = []
qynames1 = []
ryhrefs = []
ryzzas = []
ryzzs = []
zhuanyes = []
rynames1 = []
# 人员列表总条数
totalnum = int(se.get_text("span#lblRowsCount"))

# 翻页函数
# def goPage(pagenum):
#     strjs_f = """function __doPostBack(eventTarget, eventArgument,pagenum) {
#         document.querySelector("#newpage").value = pagenum
#         var theForm = document.forms['form1']
#         theForm.__EVENTTARGET.value = eventTarget;
#         theForm.__EVENTARGUMENT.value = eventArgument;
#         theForm.submit();
#     }
#     __doPostBack('Linkbutton5','',%d)"""%(pagenum)
#     driver.execute_script(strjs_f)
if totalnum >= 40:
    se.click_("css selector","#divPage ul>li:nth-child(3)>a")

# 获取人员列表当页所有人员
soup = bs.get_soup(".list_container>table>tbody")
trs = soup.select("tr")
for tr in trs:
    ryname = tr.select("tr>td:nth-child(2)>a")[0].get_text()
    ryhref = "http://cx.jlsjsxxw.com/UserInfo/"+tr.select("tr>td:nth-child(2)>a")[0]["href"]
    qyname = tr.select("tr>td:nth-child(5)")[0]["title"]
    ryzza = tr.select("tr>td:nth-child(4)")[0].get_text().strip()
    # print(ryname)
    # print(ryhref)
    # print(qyname)
    rynames.append(ryname)
    ryhrefs.append(ryhref)
    qynames.append(qyname)
    ryzzas.append(ryzza)

de.excel_w("E://mydata/jilinryList.xls","sheet1",rynames,ryhrefs,qynames,ryzzas)

for h  in range(len(ryhrefs)):
    ryhref = ryhrefs[h]
    qyname = qynames[h]
    ryname = rynames[h]
    se.open_(ryhref)
    soup = bs.get_soup(".details_infor_content_01")
    ryzzs_m = soup.select(".leibie>span")
    print(ryzzs_m)
    tabs = soup.select("table")
    for i in range(len(ryzzs_m)):
        ryzz_m = ryzzs_m[i].get_text()
        if "高级工程师" in ryzz_m:
            continue
        else:
            ryzz = ryzz_m
            tab = tabs[i].get_text()
            zhuanyems = re.findall(r"注册专业：(.*?)注册",tab)
            if len(zhuanyems) == 0:
                zhuanyes.append('')
                ryzzs.append(ryzz)
                qynames1.append(qyname)
                rynames1.append(ryname)
            else:
                for zhuanye in zhuanyems:
                    zhuanyes.append(zhuanye)
                    ryzzs.append(ryzz)
                    qynames1.append(qyname)
                    rynames1.append(ryname)
print(zhuanyes)
print(ryzzs)
print(qynames1)
print(rynames1)

de.excel_w("E://mydata/jilinryzz.xls","sheet1",qynames1,rynames1,ryzzs,zhuanyes)
print(ryzzs)


































