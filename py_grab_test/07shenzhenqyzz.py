#coding=utf-8
__Author__  = "hejb"

from py_grab_test.selenium_base import *

se = Base_()
bs = Bsoup()
de = Doexcel()
qyzzs = []
se.open_("http://data.gdcic.net/Dop/Open/EnterpriseInfo.aspx?OrgCode=672981403")

soup = bs.get_soup("#ent-qua>table>tbody")

trs = soup.select("tr")

for i in range(1,len(trs)):
    tr = trs[i]
    qyzzms = tr.select("tr>td:nth-child(3)")[0].get_text().split("；")
    print(qyzzms)
    for qyzz in qyzzms:
        qyzzs.append(qyzz)

print(qyzzs)
