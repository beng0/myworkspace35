#coding= utf-8

from py_grab_test.selenium_base import *
import re

se = Base_()
bs = Bsoup()
de = Doexcel()

se.open_("http://zjt.shanxi.gov.cn/jzscNew/Browse/JgJzscSearchInfo.aspx?type=1&cID=1")
rynames = []
zzdjs = []
qynames = []
zzbhs = []
zczys = []
def get_ryzz_by_qyname(qyname):

    driver.switch_to_frame("main")
    se.get_position("id","txtent_name").clear()
    se.get_position("id","txtent_name").send_keys(qyname)
    #点击查询按钮
    se.get_position("id","btnQuery").click()

    len_tr = driver.execute_script("return document.querySelectorAll('.statTab>tbody>tr').length")
    print(len_tr)
    if len_tr <=3:
        print(qyname+"：企业搜索不到")
        driver.switch_to_default_content()
        return


    pagestr = driver.execute_script("return document.querySelector('td.pagebg>div>div.page').innerText")
    print(pagestr)
    # "首页 | 上一页 | 下一页 | 尾页 　 当前显示 71 - 75 条　共 75 条 | 第页 / 共 6 页　 条/页   "
    pattern_p = re.compile(r'.*?共 (\d) 页')
    pagenum = int(pattern_p.match(pagestr).group(1))
    print(pagenum)

    for p in range(pagenum):
        len_tr = driver.execute_script("return document.querySelectorAll('.statTab>tbody>tr').length")
        for i in range(2,len_tr):
            sel_tr = ".statTab>tbody>tr:nth-child("+str(i)+")>td:nth-child(2)>a"
            print(sel_tr)
            se.get_position("css selector",sel_tr).click()
            ryname = driver.execute_script("return document.querySelector('.statTab>tbody>tr:nth-child("+str(i)+")>td:nth-child(2)>a').innerText")

            time.sleep(1)
            driver.switch_to_default_content()
            iframe2 = driver.find_element("css selector","div.ym-body>iframe")
            driver.switch_to_frame(iframe2)
            zzdj = driver.execute_script("return document.querySelector('#main3 tbody>tr:nth-child(5)>td:nth-child(4)').innerText")
            zzbh = driver.execute_script("return document.querySelector('#main3 tbody>tr:nth-child(6)>td:nth-child(2)').innerText")
            zczy = driver.execute_script("return document.querySelector('#main3 tbody>tr:nth-child(5)>td:nth-child(2)').innerText")
            if zzdj:
                zzdj = zzdj.strip()
            if zzbh:
                zzbh = zzbh.strip()
            if zczy:
                zczy_m = zczy.strip()
                zczy_lis = zczy_m.split(",")
                print(zczy_lis)
                for zczy in zczy_lis:
                    print(zczy)
                    rynames.append(ryname)
                    zzdjs.append(zzdj)
                    zzbhs.append(zzbh)
                    qynames.append(qyname)
                    zczys.append(zczy)
            else:
                rynames.append(ryname)
                zzdjs.append(zzdj)
                zzbhs.append(zzbh)
                qynames.append(qyname)
                zczys.append(zczy)
            driver.switch_to_default_content()
            se.get_position("xpath","//input[@value='关闭']").click()
            driver.switch_to_frame("main")
            print(zzdj)
        if p < pagenum-1:
            se.get_position("xpath","//td[@class='pagebg']/div/div/a[contains(text(),'下一页')]").click()

    print(rynames,zzdjs)
    driver.switch_to_default_content()



qy_lis = de.read_excel("D:\mydocument\svn - 副本\数据对比\对比结果\广东、深圳每周数据对比结果\山西企业列表_贺家斌_20200715.xlsx","Sheet1")

for q in range(1,len(qy_lis)):
    qyname = qy_lis[q][1]
    print(qyname)
    get_ryzz_by_qyname(qyname)

de.excel_w("D:\mydocument\svn - 副本\数据对比\对比结果\广东、深圳每周数据对比结果\山西人员zz列表20200715.xlsx", "sheet1", qynames,rynames,zzbhs,zzdjs,zczys)







