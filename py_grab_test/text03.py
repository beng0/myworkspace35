from py_grab_test.selenium_base import  *
# from py_grab_test.base import *
import xlwt
import xlrd
from bs4 import BeautifulSoup
import re

se = Base_()
se.open_("http://hngcjs.hnjs.gov.cn/tBRegPerson/renDetaill?id=482685&specialtytypnum=81")
strjs_r = """var topwin = window.top.document.getElementById("newsiframe").contentWindow;
return topwin.document.querySelector("div.news_con").innerHTML"""
html = driver.execute_script(strjs_r)
soup = BeautifulSoup(html,"html.parser")
print(soup.get_text())
print("注册专业" in soup.get_text())

p = re.compile("注册专业")
m = p.match("注册专业啦啦啦")
print(m.group())
g = p.match(soup.get_text())
print(type(soup.get_text()))
k = 0
for string in soup.strings:
    if "注册专业" in string:
        k +=1

s = soup.select("tbody>tr:nth-child(2)>td:nth-child(2)")[0].get_text()
print(k)
print(s)

lis = []
a = None
lis.append(a)
