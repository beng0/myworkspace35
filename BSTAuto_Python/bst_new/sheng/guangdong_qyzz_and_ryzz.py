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
from my_read_excel import *
from my_to_excel import *
from datetime import datetime
# from bst.bst_datatest.test_case.models.my_to_excel import  *

def  openUrl(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("{}".format(url))
    return driver


#得到企业和相应的href
def get_data_single(data,driver,num):
    locator = (By.XPATH, '//table[@class="data-list"]//tr[2]//a')
    val = WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator)).get_attribute('href')[-30:]
    # print(val)
    cnum = driver.find_element_by_xpath('//span[@class="current"]').text
    # 翻页
    if int(cnum) != int(num):
        driver.execute_script("javascript:__doPostBack('ctl00$ContentPlaceHolder1$AspNetPager1','%s')"%num)
        locator = (By.XPATH, '//table[@class="data-list"]//tr[2]//a[not(contains(@href,"%s"))] ' % val)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    table = soup.find('table', class_='data-list')
    trs = table.find_all('tr')[1:]
    qy_count = 1
    for tr in trs:
        entname=tr.find('a').text
        href = tr.find('a')['href']
        tmp = [href,entname]
        data.append(tmp)
        print(data)
        qy_count +=1
        if qy_count== 6: break  #只取5个企业


# 得到企业资质
def get_qyzz_detail_single(driver,sheng,shi, href,entname,qyzz_data):
    driver.get(href)
    locator = (By.XPATH, '//div[@class="ln-title"][string-length()>5]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, '//div[@class="ln-title"][string-length()>5]')

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    table = soup.find('table', class_='data-list')
    trs = table.find_all('tr')[1:]

    for td  in trs:
        entname= soup.find('div', class_='ln-title').text.strip()
        zslb=td.find_all('td')[1].get_text()
        zzdjs=td.find_all('td')[2].get_text()
        if "；" in zzdjs:
            zzdjlis = zzdjs.split("；")[0:-1]
            for zzdj in zzdjlis:
                tmp = [sheng, shi, href, entname, zslb, zzdj]
                qyzz_data.append(tmp)
        else:
            zzdj = zzdjs
            tmp = [sheng, shi, href, entname, zslb, zzdj]
            qyzz_data.append(tmp)
        print(qyzz_data)


# 得到人员资质
def get_ryzz_detail_single(driver,sheng,shi, href,entname,ryzz_data):
        driver.get(href)
        locator = (By.XPATH, '//div[@class="ln-title"][string-length()>5]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        print(href)


        ry_page=driver.find_element_by_xpath('//div[@id="ent-person"]').text
        # print(ry_page)
        if "暂无信息"  in  ry_page:
            return ryzz_data


        if  "更多→"  in  ry_page:
            locator = (By.XPATH, '//div[@id="ctl00_ContentPlaceHolder1_showmore_person"]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_showmore_person').click()")

            time.sleep(2)
            driver.switch_to.frame('nyroModalIframe')


        page = driver.page_source
        body = etree.HTML(page)
        content_list = body.xpath("//*[@id='ent-person']/a[@class='doubt']")

        for content in content_list:
            ryname = content.xpath("./div/div/span[1]/text()")[0].strip()
            zsbh= content.xpath("./div/div/span[2]/text()")[0].strip()
            ryzz = content.xpath("./div/div/h5[1]/text()")[0].strip()
            tmp = [sheng,shi,href,entname,ryname,zsbh,ryzz]
            ryzz_data.append(tmp)
            print(ryzz_data)

# 得到指定页数企业对应的qyzz ryzz
def get_zhiding_yeshu_zz(driver):
    data = []
    for i in range(1, 2):
        # 得到企业和相应的href
        get_data_single(data, driver, i)

    qyzz_data = []
    ryzz_data = []

    for href,entname in data:
        # 得到企业资质
        tmp=get_qyzz_detail_single(driver, href,entname,qyzz_data)
        # 得到人员资质
        tmp2=get_ryzz_detail_single(driver,href,entname,ryzz_data)

    print(qyzz_data)
    print(ryzz_data)

    # 保存企业资质
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng","shi","href", "entname","zslb", "zzdj"]
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, qyzz_data)
    print("to  excel  success")

    # 保存人员资质
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng","shi","href","entname","name","zsbh","zzdj"]
    wirteDataToExcel(outfilename_gd_ryzz + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, ryzz_data)
    print("to  excel  success")

# 得到指定页数企业对应的qyzz ryzz
def get_zhiding_qy_zz(driver,infilename,outfilename_gd_ryzz,outfilename_gd_qyzz):

    # 读取excel中的数据
    all_sheet_data1 = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    zhiding_qy_data = all_sheet_data1[0][1][1:6]
    print(zhiding_qy_data)

    qyzz_data = []
    ryzz_data = []

    for row in zhiding_qy_data:
        sheng = row[0].strip()
        shi = row[1].strip()
        href = row[3].strip()
        entname = row[2].strip()
        # 得到企业资质
        tmp=get_qyzz_detail_single(driver,sheng,shi, href,entname,qyzz_data)
        # 得到人员资质
        tmp2=get_ryzz_detail_single(driver,sheng,shi,href,entname,ryzz_data)

    print(qyzz_data)
    print(ryzz_data)

    # 保存企业资质
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng","shi","href", "entname","zslb", "zzdj"]
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyzz_data)
    print("qyzz_data to  excel  success")

    # 保存人员资质
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["sheng","shi","href","entname","name","zsbh","zzdj"]
    wirteDataToExcel(outfilename_gd_ryzz + tablenamehouzui + ".xlsx", "ryzz_data", columnRows, ryzz_data)
    print("ryzz_data to  excel  success")




if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\广东_云南_山西建设通企业业绩_贺家斌_href_20200805.xlsx"
    outfilename_gd_ryzz = root_dir + r"\get_sheng_ryzz_qyzz\广东_省平台ryzz_贺家斌_"
    outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\广东_省平台qyzz_贺家斌_"

    driver=openUrl("http://data.gdcic.net/Dop/Open/EnterpriseList.aspx")

    # 得到指定页数企业对应的qyzz ryzz
    # get_zhiding_yeshu_zz(driver)

    # 得到指定企业对应的qyzz ryzz
    get_zhiding_qy_zz(driver,infilename,outfilename_gd_ryzz,outfilename_gd_qyzz)

    driver.quit()

