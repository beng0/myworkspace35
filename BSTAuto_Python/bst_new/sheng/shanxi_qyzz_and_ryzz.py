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

# 返回主页面
def  back_main_document(driver):
    # 回到主文档
    driver.switch_to.default_content()
    sleep(3)
    driver.find_element_by_xpath('//*[starts-with(@id,"ymPrompt_btn_")]').click()
    sleep(3)

# 进入查询企业frame
def to_query_qy_frame(driver):
    # 进入查询企业frame
    queryqy_frame = driver.find_element_by_xpath('//*[@id="main"]')
    driver.switch_to.frame(queryqy_frame)
    qy_loc = (By.XPATH, '//*[@id="txtEnt_name"]')
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(qy_loc))

def to_tankuang_frame(driver):
    # 回到最外层页面
    driver.switch_to.default_content()
    zz_frame = driver.find_element_by_xpath('//*[@id="ym-ml"]/div/div/div/iframe')
    # 进入弹出div frame
    driver.switch_to.frame(zz_frame)
    qyzz_loc = (By.XPATH, '//*[@id="main8"]/ul[1]/li/table/tbody/tr[7]/td[2]')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(qyzz_loc))



def get_ryzz_detail(driver,gotoye,total_ye_count,sheng,shi,qyname,ryzz_data):
    print("ryzz第 "+str(gotoye)+" 页 "+qyname)
    jbxx_loc = (By.XPATH, '//*[@id="main8"]/ul[4]/li/table/tbody/tr')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(jbxx_loc))
    ry_list = driver.find_elements_by_xpath('//*[@id="main8"]/ul[4]/li/table/tbody/tr')[:-1]
    for content in ry_list:
        name = content.find_element_by_xpath('./td[2]').text.strip()
        ryzz = content.find_element_by_xpath('./td[3]').text.strip()
        zsbh = content.find_element_by_xpath('./td[4]').text.strip()
        zszt = content.find_element_by_xpath('./td[5]').text.strip()
        tmp=[sheng,shi,qyname,name,ryzz,zsbh,zszt]
        ryzz_data.append(tmp)
        print(ryzz_data)

    if (total_ye_count != 1) and (gotoye != total_ye_count):
        # 翻页
        driver.find_element_by_xpath('//*[@id="main8"]/ul[4]/li/table/tbody/tr[15]/td/div/div/a[contains(text(),"下一页")]').click()
        jbxx_loc=(By.XPATH,'//*[@id="main8"]/ul[1]/li/table/tbody/tr[1]/td')
        WebDriverWait(driver,30).until(EC.visibility_of_element_located(jbxx_loc))
        # 点击执业人员
        driver.find_element_by_xpath('//*[@id="menu8"]/li[4]').click()
        sleep(10)



def get_zhiding_qy_qyzz_and_ryzz(driver,sheet1data,ryzz_data,qyzz_data):
    ishas_qyzz_flag = 0
    for row in sheet1data:
        # 进入查询企业frame
        if ishas_qyzz_flag != 1:
            to_query_qy_frame(driver)

        # 输入企业名
        sheng = row[0].strip()
        shi = row[1].strip()
        qyname = row[2].strip()
        driver.find_element_by_xpath('//*[@id="txtEnt_name"]').clear()
        driver.find_element_by_xpath('//*[@id="txtEnt_name"]').send_keys(qyname)

        # 点击查询
        driver.find_element_by_xpath('//*[@id="formSeach"]/table/tbody/tr/td[5]/input').click()
        sleep(5)
        ishas_qyzz = driver.find_element_by_xpath('//*[@id="formList"]/table/tbody/tr[2]/td').text

        if "暂无相关内容！" in ishas_qyzz:
            ishas_qyzz_flag = 1
            continue

        # //*[@id="formList"]/table/tbody/tr[2]/td[1]/a
        # //*[@id="formList"]/table/tbody/tr[2]/td
        zhiding_qy_loc = (By.XPATH, '//*[@id="formList"]/table/tbody/tr[2]/td[1]/a')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhiding_qy_loc))

        qy_list = driver.find_elements_by_xpath('//*[@id="formList"]/table/tbody/tr')
        ishave_get_rydata = 0
        # 该企业有几行
        for qy_count in range(2,len(qy_list)):
            if qy_count !=2:to_query_qy_frame(driver)
            print("qy第 "+str(qy_count-1)+" 行 "+qyname)

            # 点击企业名进入弹出div
            driver.find_element_by_xpath('//*[@id="formList"]/table/tbody/tr['+str(qy_count)+']/td[1]/a').click()

            # 进入弹出div frame
            to_tankuang_frame(driver)

            # 获取企业资质
            qyzzs=driver.find_element_by_xpath('//*[@id="main8"]/ul[1]/li/table/tbody/tr[7]/td[2]').text
            qyzzlis = qyzzs.split("\n")
            for qyzz in qyzzlis:
                qyzz_tmp = [sheng, shi, qyname, qyzz]
                qyzz_data.append(qyzz_tmp)

            print(qyzz_data)

            # 企业有多行，人员只取一次
            if ishave_get_rydata == 0:
                ishave_get_rydata=1
                #点击执业人员
                driver.find_element_by_xpath('//*[@id="menu8"]/li[4]').click()

                # 人员是否有数据
                ishas_ry = driver.find_element_by_xpath('//*[@id="main8"]/ul[4]/li/table/tbody/tr[1]/td').text
                if "暂无相关内容！" in ishas_ry:
                    back_main_document(driver)
                    continue

                ry_list_loc = (By.XPATH, '//*[@id="main8"]/ul[4]/li/table/tbody/tr')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ry_list_loc))


                len_count = len(driver.find_elements_by_xpath('//*[@id="main8"]/ul[4]/li/table/tbody/tr'))
                # 元素聚焦到页码
                target = driver.find_element_by_xpath('//*[@id="main8"]/ul[4]/li/table/tbody/tr['+str(len_count)+']/td/div/div')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                sleep(3)


                total_ye = ((driver.find_element_by_xpath('//*[@id="main8"]/ul[4]/li/table/tbody/tr['+str(len_count)+']/td/div/div').text.strip())[-9:-6]).strip()
                total_ye_count = int(total_ye)
                print("人员总页数"+str(total_ye_count))

                if total_ye_count == 1:get_ryzz_detail(driver,1,total_ye_count,qyname,ryzz_data)
                else:
                    for gotoye in range(1,total_ye_count+1):
                        get_ryzz_detail(driver,gotoye,total_ye_count,sheng,shi,qyname,ryzz_data)
            # 返回主页面
            back_main_document(driver)
            ishas_qyzz_flag = 0




if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\广东_云南_山西建设通企业业绩_贺家斌_href_20200805.xlsx"
    outfilename_ryzz = root_dir + r"\get_sheng_ryzz_qyzz\山西_省平台ryzz_贺家斌_"
    outfilename_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\山西_省平台qyzz_贺家斌_"


    driver=openUrl("http://zjt.shanxi.gov.cn/jzscNew/Browse/JgJzscSearchInfo.aspx?type=1&cID=2")

    # 读取excel中的数据
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][11:16]
    print(sheet1data)

    ryzz_data = []
    qyzz_data = []
    # 得到指定企业对应的qyzz ryzz
    get_zhiding_qy_qyzz_and_ryzz(driver,sheet1data,ryzz_data,qyzz_data)
    driver.quit()

    # 保存qyzz
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng","shi","qyname", "qyzz"]
    wirteDataToExcel(outfilename_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, qyzz_data)
    print("qyzz  to  excel  success")

    # 保存ryzz
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows1 = ["sheng","shi","qyname", "name", "ryzz", "zsbh", "zszt"]
    wirteDataToExcel(outfilename_ryzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows1, ryzz_data)
    print("ryzz to  excel  success")

    driver.quit()


