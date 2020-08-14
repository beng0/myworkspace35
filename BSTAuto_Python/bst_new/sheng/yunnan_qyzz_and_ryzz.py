import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium  import webdriver
from time  import sleep,ctime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from lmf.dbv2 import db_write
import pandas as pd
from util.my_read_excel import *
from util.my_to_excel import *
from datetime import datetime
# from bst.bst_datatest.test_case.models.my_to_excel import  *

def  openUrl(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("{}".format(url))
    return driver

# 切换窗口
def switch_to_window(driver,first_handle):
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != first_handle:
            driver.switch_to.window(handle)
            sleep(3)

# 关闭当前窗口
def close_current_window(driver,first_handle):
    driver.close()
    sleep(3)
    # 回到之前窗口
    driver.switch_to.window(first_handle)
    sleep(3)



# 企业资质详情
def get_qyzz_detail(sheng,shi,zbr,qyzz_data):
    content_list = driver.find_elements_by_xpath('//*[@id="qyzz_table"]/tr')
    for content in content_list:
        qyzz = content.find_element_by_xpath('./td[4]/div').text.strip()
        fzjg = content.find_element_by_xpath('./td[5]/div').text.strip()
        fzrq = content.find_element_by_xpath('./td[6]/div').text.strip()
        yxq = content.find_element_by_xpath('./td[7]/div').text.strip()
        tmp = [sheng,shi,zbr, qyzz, fzjg, fzrq, yxq]
        qyzz_data.append(tmp)
        print(qyzz_data)


# 人员资质详情
def get_ryzz_detail(sheng,shi,zbr,ryzz_data):
    content_list = driver.find_elements_by_xpath('//*[@id="zcry_table"]/tr')
    for content in content_list:
        name = content.find_element_by_xpath('./td[2]/div').text.strip()
        sfz = content.find_element_by_xpath('./td[3]/div').text.strip()
        zclb_jb = content.find_element_by_xpath('./td[4]/div').text.strip()
        zczsh = content.find_element_by_xpath('./td[5]/div').text.strip()
        zczys = content.find_element_by_xpath('./td[6]/div').text.strip()
        if "," in zczys:
            zczylis = zczys.split(",")
            for zczy in zczylis:
                tmp = [sheng, shi, zbr, name, sfz, zclb_jb, zczsh, zczy]
                ryzz_data.append(tmp)
        else:
            zczy = zczys
            tmp = [sheng, shi, zbr, name, sfz, zclb_jb, zczsh, zczy]
            ryzz_data.append(tmp)

        print(ryzz_data)




# 得到该企业qyzz
def get_qyzz(driver,sheng,shi,zbr,qyzz_data):

    table_text = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]').text
    if "暂无相关数据" in table_text:
        return qyzz_data

    driver.maximize_window()
    sleep(2)
    target = driver.find_element_by_xpath('//*[@id="pagebox"]/div/p[1]')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    sleep(2)

    # 共几页
    total_ye = (driver.find_element_by_xpath('//*[@id="pagebox"]/div/p[1]').text)[1:-2]
    total_ye_count = int(total_ye.strip())
    print("该企业总共有 " + str(total_ye_count) + " 页企业资质")

    if total_ye_count == 1:
        get_qyzz_detail(sheng,shi,zbr,qyzz_data)
    elif total_ye_count > 1:
        for crrut_ye in range(1, total_ye_count + 1):
            # 翻页
            if crrut_ye != 1:
                driver.find_element_by_xpath('//*[@id="pagebox"]/div/input').clear()
                driver.find_element_by_xpath('//*[@id="pagebox"]/div/input').send_keys(str(crrut_ye))
                driver.find_element_by_xpath('//*[@id="pagebox"]/div/button[5]').click()
                sleep(5)

            loc = (By.XPATH, '//*[@id="qyzz_table"]/tr[1]/td[5]/div')
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(loc))
            get_qyzz_detail(sheng,shi,zbr,qyzz_data)


# 得到该企业ryzz
def get_ryzz(driver,sheng,shi,zbr, ryzz_data,is_havedata):
    # 点击注册人员标签
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/ul/li[2]/span').click()
    sleep(5)

    table_text = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]').text
    if "暂无相关数据" in table_text:
        is_havedata = 1
        return is_havedata

    # 元素聚焦
    target = driver.find_element_by_xpath('//*[@id="pagebox"]/div/p[1]')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    sleep(2)

    # 共几页
    total_ye = (driver.find_element_by_xpath('//*[@id="pagebox"]/div/p[1]').text)[1:-2]
    print(total_ye)
    total_ye_count = int(total_ye.strip())
    print("该企业总共有 " + str(total_ye_count) + " 页人员资质")
    if total_ye_count > 2: total_ye_count=2 #只取2页


    if total_ye_count == 1:
        get_ryzz_detail(sheng,shi,zbr, ryzz_data)
    elif total_ye_count > 1:
        for crrut_ye in range(1, total_ye_count + 1):
            # 翻页
            if crrut_ye != 1:
                driver.find_element_by_xpath('//*[@id="pagebox"]/div/input').clear()
                driver.find_element_by_xpath('//*[@id="pagebox"]/div/input').send_keys(str(crrut_ye))
                driver.find_element_by_xpath('//*[@id="pagebox"]/div/button[5]').click()
                sleep(5)

            loc = (By.XPATH, '//*[@id="zcry_table"]/tr[1]/td[2]/div')
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(loc))
            get_ryzz_detail(sheng,shi,zbr, ryzz_data)






# 得到指定企业qyzz和 ryzz
def get_zhiding_qy_qyzz_and_ryzz(driver,zhiding_qy_data,qyzz_data,outfilename_qyzz,ryzz_data,outfilename_ryzz):
    zbr_loc = (By.XPATH,'//*[@id="entName"]')
    WebDriverWait(driver,30).until(EC.visibility_of_element_located(zbr_loc))

    for row in zhiding_qy_data:
        sheng = row[0].strip()
        shi = row[1].strip()
        zbr = row[2].strip()

        # 输入就企业名
        driver.find_element_by_xpath('//*[@id="entName"]').clear()
        driver.find_element_by_xpath('//*[@id="entName"]').send_keys(zbr)

        # 点击查询
        driver.find_element_by_xpath('//*[@id="search_Btn"]').click()
        sleep(3)

        # 跳到qyzz详情页面
        onclick_str=driver.find_element_by_xpath('//*[@id="table"]/tr').get_attribute('onclick')
        driver.execute_script(onclick_str)
        sleep(3)

        #切换窗口
        first_handle = driver.current_window_handle
        switch_to_window(driver, first_handle)

        table_loc = (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]')
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located(table_loc))

        # 得到该企业qyzz
        get_qyzz(driver,sheng,shi, zbr, qyzz_data)

        # 得到该企业ryzz
        is_havedata= 0
        get_ryzz(driver,sheng,shi, zbr, ryzz_data,is_havedata)
        if is_havedata :
            close_current_window(driver,first_handle)
            continue

        close_current_window(driver,first_handle)

    # 保存qyzz
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng","shi","zbr", "qyzz", "fzjg", "fzrq","yxq"]
    wirteDataToExcel(outfilename_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, qyzz_data)
    print("qyzz  to  excel  success")

    # 保存ryzz
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows1 = ["sheng","shi","zbr", "name", "sfz", "zclb_jb","zczsh", "zczy"]
    wirteDataToExcel(outfilename_ryzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows1, ryzz_data)
    print("ryzz to  excel  success")





if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\广东_云南_山西建设通企业业绩_贺家斌_href_20200805.xlsx"
    outfilename_ryzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台ryzz_贺家斌_"
    outfilename_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzz_贺家斌_"

    # 读取excel中的数据
    all_sheet_data1 = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    zhiding_qy_data = all_sheet_data1[0][1][6:11]
    print(zhiding_qy_data)

    # 得到指定页数企业对应的qyzz ryzz
    qyzz_data=[]
    ryzz_data = []
    driver = openUrl("https://www.ynjzjgcx.com/webHtml/ent/index.html?n=ent&t=1594779746310")
    get_zhiding_qy_qyzz_and_ryzz(driver,zhiding_qy_data,qyzz_data,outfilename_qyzz,ryzz_data,outfilename_ryzz)

    driver.quit()


