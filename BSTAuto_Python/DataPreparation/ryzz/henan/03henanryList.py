#coding=utf-8
__Author__ = "hejb"
from py_grab_test.selenium_base import  *
import xlwt
from bs4 import BeautifulSoup

book = xlwt.Workbook()
sheet = book.add_sheet("sheet1",cell_overwrite_ok=True)


se = Base_()
se.open_("http://hngcjs.hnjs.gov.cn/tBRegPerson/renListMaster")

driver.switch_to_frame("newsiframe")

# 点击出人员类别下拉框
se.click_("css selector",".filter_dropdown")
# 获取大的人员类别长度
len_r1 = len(se.get_positions("css selector","ul.staff_dropdown>li"))
print(len_r1)
names = []
ryhrefs = []
qys = []
ryzzs = []
for i in range(7,len_r1+1):
    # 先判断是否有细分类
    if se.exist_or_not("ul.staff_dropdown>li:nth-child("+str(i)+")>ul") == 1:
        # 如果存在，获取细分类的人员类别长度
        len_r2 = len(se.get_positions("css selector","ul.staff_dropdown>li:nth-child("+str(i)+")>ul>li"))
        for j in range(1,len_r2+1):
            # 依次点击每个分类
            se.click_s("ul.staff_dropdown>li:nth-child("+str(i)+")>ul>li:nth-child("+str(j)+")>a")
            # 点击搜索按钮
            se.click_("css selector", "input[value='搜索']")
            # 翻页
            for n in range(2): #设置总共翻两页
                strjs_f = """var topwin = window.top.document.getElementById("newsiframe").contentWindow;
                topwin.document.querySelector("#page").value = "%d";
                topwin.document.forms[0].submit();"""%(n+1)
                driver.execute_script(strjs_f)
                time.sleep(1)
                # 获取该页面人员列表的长度
                len_trs = driver.execute_script("return document.querySelectorAll('#tagContenth0>table>tbody>tr').length")
                for k in range(1,len_trs):
                    # 等待被执行的js字符串,将每一个tr转换为bs4文档
                    strjs_t = "return document.querySelectorAll('#tagContenth0>table>tbody>tr')["+str(k)+"].outerHTML"
                    tr = driver.execute_script(strjs_t)
                    trbs4 = BeautifulSoup(tr,"html.parser")
                    # print(trbs4)
                    name = trbs4.select("td")[1].get_text()
                    names.append(name)
                    ryhref = "http://hngcjs.hnjs.gov.cn"+trbs4.select("td>a")[0]["href"]
                    ryhrefs.append(ryhref)
                    qy = trbs4.select("td")[2].get_text()
                    qys.append(qy)
                    ryzz = trbs4.select("td")[3].get_text()
                    ryzzs.append(ryzz)
                    # print(ryhref)
                    # print(name)

    else:
        # 如果不存在，直接点击大分类
        se.click_s("ul.staff_dropdown>li:nth-child("+str(i)+")>a")
        # 点击搜索按钮
        se.click_("css selector", "input[value='搜索']")
        # 翻页
        for n in range(2):  # 设置总共翻两页
            strjs_f = """var topwin = window.top.document.getElementById("newsiframe").contentWindow;
            topwin.document.querySelector("#page").value = "%d";
            topwin.document.forms[0].submit();"""%(n+1)
            driver.execute_script(strjs_f)
            # 获取页面人员数据长度
            len_trs = driver.execute_script("return document.querySelectorAll('#tagContenth0>table>tbody>tr').length")
            for k in range(1, len_trs):
                # 等待被执行的js字符串,将每一个tr转换为bs4文档
                strjs_t = "return document.querySelectorAll('#tagContenth0>table>tbody>tr')[" + str(k) + "].outerHTML"
                tr = driver.execute_script(strjs_t)
                trbs4 = BeautifulSoup(tr, "html.parser")
                # print(trbs4)
                name = trbs4.select("td")[1].get_text()
                names.append(name)
                ryhref = "http://hngcjs.hnjs.gov.cn" + trbs4.select("td>a")[0]["href"]
                ryhrefs.append(ryhref)
                qy = trbs4.select("td")[2].get_text()
                qys.append(qy)
                ryzz = trbs4.select("td")[3].get_text()
                ryzzs.append(ryzz)
                # print(ryhref)
                # print(name)

print(names)
print(ryhrefs)

len_a = len(names)
for i in range(1,len_a):
    row = i
    name = names[i-1]
    ryhref = ryhrefs[i-1]
    qy = qys[i-1]
    ryzz = ryzzs[i-1]
    sheet.write(row,1,name)
    sheet.write(row,2,ryhref)
    sheet.write(row,3,qy)
    sheet.write(row,4,ryzz)

book.save("E://mydata//rylist.xls")
print("success")



