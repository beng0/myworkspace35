from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
# from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from time import sleep
from BSTAuto_Python.bst_new.util.my_to_excel import *
from BSTAuto_Python.bst_new.util.my_read_excel import *
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

def  open(url):
    # 代理IP
    # driver = get_driver_moni_ip()
    # driver.get("http://httpbin.org/ip")
    # print(driver.page_source)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    return driver

# 指定企业名和项目经理
ryzz_data = []
def get_jst_zhiding_xmjlzz(driver,sheet1data,outfilename):
    # driver.find_element_by_xpath('')
    for row in sheet1data:
        xmjl = row[1].strip()
        qyname = row[2].strip()

        # sleep(3)
        # driver.find_element_by_xpath('//div[text()="查询"]').click()
        #
        print(xmjl)
        driver.find_element_by_xpath('//input[@placeholder="请输入人员姓名"]').send_keys(xmjl)
        # sleep(1)
        #
        print(qyname)
        #
        # sleep(1)
        driver.find_element_by_xpath('//input[@placeholder="请输入企业名称关键词"]').send_keys(qyname)
        driver.find_element_by_xpath('//div[text()="查询"]').click()
        for i in range(20):
            driver.find_element_by_xpath('//input[@placeholder="请输入人员姓名"]').send_keys(Keys.BACK_SPACE)
            driver.find_element_by_xpath('//input[@placeholder="请输入企业名称关键词"]').send_keys(Keys.BACK_SPACE)
        # driver.execute_script("document.querySelector('input[placeholder=\"请输入人员姓名\"]').value = ''")
        # driver.execute_script("document.querySelector('input[placeholder=\"请输入企业名称关键词\"]').value = ''")
        sleep(4)
        counttext = driver.find_element_by_xpath("//div[@class='result']").text
        if '0' in counttext:
            continue
        content_list = driver.find_elements_by_xpath('//div[@id="res-table"]/div[2]/div')
        for content in content_list:
            xmjl_tmp = xmjl
            qyname_tmp = qyname
            ryzz = content.find_element_by_xpath('./dl/dd[1]').text.strip()
            zsbh = content.find_element_by_xpath('./dl/dd[2]/a').text.strip()
            youxiaoqi = content.find_element_by_xpath('./dl/dd[4]').text.split("：")[1].strip()
            tmp = [xmjl_tmp,qyname_tmp,ryzz,zsbh,youxiaoqi]
            ryzz_data.append(tmp)
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["xmjl", "qyname", "ryzz", "zsbh", "youxiaoqi"]
    wirteDataToExcel(outfilename + "qyyj_" + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, ryzz_data)
    print("ryzz  to   excel  sucess")
    print("企业业绩文件存放在" + outfilename + "qyyj_" + tablenamehouzui + ".xlsx")

if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\xmjl_list\云南_项目经理列表_模板.xlsx"
    outfilename = root_dir + r"\get_jst_ryzz_qyzz\建设通xmjlzz_数据准备_贺家斌_"
    url = "https://passport.cbi360.net/login?url=https%3A%2F%2Fwww.cbi360.net%2Fhyjd%2F20200528%2F203181.html"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    driver=open(url)
    s = input("input  your  unm: ")
    if int(s) == 1:
        # 得到导入企业的链接
        get_jst_zhiding_xmjlzz(driver,sheet1data,outfilename)

        # datalist=[['广州', '广州敏城建设工程有限公司', 'https://hhb.cbi360.net/sg_47307/', '726']]


        # 得到导入企业的全部中标业绩
        # max_ye指定最多查询建设通多少页的业绩
        # get_qyyj_detail(driver,outfilename,zhiding_qy_url,qyyj_data,max_ye=6)





























