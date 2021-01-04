from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
# from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from time import sleep
from BSTAuto_Python.bst_new.util.my_to_excel import *
from BSTAuto_Python.bst_new.util.my_read_excel import *
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

def  open(url):
    # 代理IP
    # driver = get_driver_moni_ip()
    # driver.get("http://httpbin.org/ip")
    # print(driver.page_source)
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


# 得到导入企业的链接
def get_xmjlzz_href(driver,sheet1data):
    href_data = []
    for row in sheet1data:
        entname = row[2].strip()
        name = row[1].strip()
        driver.find_element_by_id('perName').clear()
        driver.find_element_by_id('entName').clear()
        driver.find_element_by_id('perName').send_keys(name)
        driver.find_element_by_id('entName').send_keys(entname)
        driver.find_element_by_id('search_Btn').click()
        sleep(3)
        signtext = driver.find_element_by_id('table').text
        if '暂无相关数据...' in signtext:
            continue
        else:
            trs = driver.find_elements_by_xpath('//tbody[@id="table"]/tr')
            for tr in trs:
                href_m = tr.get_attribute('onclick').split("'")[1]
                print(href_m)
                href = "https://www.ynjzjgcx.com/" + href_m
                tmp = [entname,name,href]
                href_data.append(tmp)
    print(href_data)
    return href_data


# 得到相应企业的全部企业资质信息
def get_qyzz_detail(driver,href_data):
    ryzz_data = []
    for tmp in href_data:
        name = tmp[1]
        entname = tmp[0]
        href = tmp[2]
        driver.get(href)
        sleep(1)
        zjhm = driver.find_element_by_id('idcardNum').text.strip()
        trs = driver.find_elements_by_xpath('//tbody[@id="cyzg_table"]/tr')
        for tr in trs:
            zclb = tr.find_element_by_xpath('./td[1]/div').text.strip()
            zsbh = tr.find_element_by_xpath('./td[2]/div').text.strip()
            zhuanye = tr.find_element_by_xpath('./td[3]/div').text.strip()
            youxiao_date = tr.find_element_by_xpath('./td[5]/div').text.strip()
            tmp1 = [entname, name, zjhm, zsbh, zclb, zhuanye, youxiao_date]
            ryzz_data.append(tmp1)
    return ryzz_data



if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\xmjl_list\云南_项目经理列表_模板.xlsx"
    outfilename = root_dir + r"\get_sheng_ryzz_qyzz\云南省xmjlzz_数据准备_贺家斌_"
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["entname", "name", "zjhm", "zsbh", "zclb", "zhuanye", "youxiao_date"]
    url = "https://www.ynjzjgcx.com/webHtml/per/index.html"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    driver=open(url)
    ryzz_data = []
    s = input("input  your  unm: ")
    if int(s) == 1:
        # 得到导入xmjl的链接
        href_data = get_xmjlzz_href(driver,sheet1data)
        ryzz_data = get_qyzz_detail(driver,href_data)
        wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, ryzz_data)