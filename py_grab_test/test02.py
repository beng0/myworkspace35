from py_grab_test.selenium_base import  *
# from py_grab_test.base import *
import xlwt
from bs4 import BeautifulSoup
se = Base_()
se.open_("http://hngcjs.hnjs.gov.cn/company/QiyeDetail?id=161172")
html1 = driver.page_source
print(html1)
print('\nend----------------------------------------------------------')
se.open_("http://hngcjs.hnjs.gov.cn/company/Qyzz?corpcode=91410200MA3XCTMX71&corpname=%E4%B8%87%E6%B1%87%E5%B7%A5%E7%A8%8B%E5%92%A8%E8%AF%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8")
html = driver.page_source
print(html)
print(html == html1)
soup = BeautifulSoup(html,"html.parser")
qyzzs_m = soup.select("tbody>tr:nth-child(4)>td:nth-child(2)>span")
print(qyzzs_m)
qyzzs = []
for qyzz in qyzzs_m:
    qyzz = qyzz.get_text().replace(",", "")
    qyzzs.append(qyzz)

print(qyzzs)