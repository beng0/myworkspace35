from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
from datetime import datetime
from time import sleep
from bst.bst_datatest.test_case.models.my_to_excel import wirteDataToExcel

def get_bj_jl_ryzz(driver,jl_data,goto_yema):
    locator = (By.XPATH,'//*[@id="CommonSearchResult"]/table/tbody/tr/td/table[3]/tbody/tr[2]')
    WebDriverWait(driver,20).until(EC.visibility_of_element_located(locator))
    if goto_yema != 1:
        goto_ye_loc=(By.XPATH,'//*[@id="jumpPageBox"]')
        # print(str(goto_yema))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(goto_ye_loc)).clear()
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(goto_ye_loc)).send_keys(str(goto_yema))
        tz_button_loc=(By.XPATH,'//*[@id="pagingDiv"]/table/tbody/tr/td[2]/input[2]')
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(tz_button_loc)).click()

    page = driver.page_source
    body = etree.HTML(page)
    content_list = body.xpath('//*[@id="CommonSearchResult"]/table/tbody/tr/td/table[3]/tbody/tr')[1:]
    for content in content_list:
        name= content.find('.//td[1]').text
        qyname=content.find('.//td[2]').text
        zczy1=content.find('.//td[3]').text
        zczy2=content.find('.//td[4]').text
        zch=content.find('.//td[5]').text
        zsbh=content.find('.//td[6]').text
        temp=[qyname,name,zczy1,zczy2,zch,zsbh]
        jl_data.append(temp)


def get_bj_jz_ryzz(driver,jz_data,goto_yema):
    locator = (By.XPATH,'//*[@id="CommonSearchResult"]/table/tbody/tr/td/table[3]/tbody/tr[2]')
    WebDriverWait(driver,20).until(EC.visibility_of_element_located(locator))
    if goto_yema != 1:
        goto_ye_loc=(By.XPATH,'//*[@id="jumpPageBox"]')
        # print(str(goto_yema))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(goto_ye_loc)).clear()
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(goto_ye_loc)).send_keys(str(goto_yema))
        tz_button_loc=(By.XPATH,'//*[@id="pagingDiv"]/table/tbody/tr/td[2]/input[2]')
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(tz_button_loc)).click()

    page = driver.page_source
    body = etree.HTML(page)
    content_list = body.xpath('//*[@id="CommonSearchResult"]/table/tbody/tr/td/table[3]/tbody/tr')[1:]
    for content in content_list:
        name= content.find('.//td[1]').text
        zsbh=content.find('.//td[2]').text
        zch=content.find('.//td[3]').text
        zczy=content.find('.//td[4]').text
        qyname=content.find('.//td[5]').text
        jb=content.find('.//td[6]').text
        temp=[name,zsbh,zch,zczy,qyname,jb]
        jz_data.append(temp)

def get_bj_zj_ryzz(driver,zj_data,goto_yema):
    locator = (By.XPATH,'//*[@id="CommonSearchResult"]/table/tbody/tr/td/table[3]/tbody/tr[2]')
    WebDriverWait(driver,20).until(EC.visibility_of_element_located(locator))
    if goto_yema != 1:
        goto_ye_loc=(By.XPATH,'//*[@id="jumpPageBox"]')
        # print(str(goto_yema))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(goto_ye_loc)).clear()
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(goto_ye_loc)).send_keys(str(goto_yema))
        tz_button_loc=(By.XPATH,'//*[@id="pagingDiv"]/table/tbody/tr/td[2]/input[2]')
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(tz_button_loc)).click()

    page = driver.page_source
    body = etree.HTML(page)
    content_list = body.xpath('//*[@id="CommonSearchResult"]/table/tbody/tr/td/table[3]/tbody/tr')[1:]
    for content in content_list:
        name= content.find('.//td[1]').text
        zch=content.find('.//td[2]').text
        qyname=content.find('.//td[3]').text
        temp=[name,'造价工程师',zch,qyname]
        zj_data.append(temp)



if __name__=='__main__':
    now_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    driver = webdriver.Chrome()

    # # 获取监理工程师
    # driver.get('http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=314439')
    # jl_total_ye = 20
    # jl_data =[]
    # for goto_yema in range(5,jl_total_ye):
    #     get_bj_jl_ryzz(driver,jl_data,goto_yema)
    #
    # print(jl_data)
    #
    # # 把数据导出到xlsx
    # outfilename = r'D:\筑龙项目\人员资质测试\beijing\数据准备\省平台北京人员资质监理工程师_胡金花' + str(now_time) + '.xlsx'
    # columnRows = ['聘用单位','姓名','注册专业1','注册专业2','注册号','注册证书编号']
    # wirteDataToExcel(outfilename, "sheetName", columnRows, jl_data)

    # 获取建造师
    driver.get('http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=314443')
    jz_total_ye = 20
    jz_data = []
    for goto_yema in range(5, jz_total_ye):
        get_bj_jz_ryzz(driver, jz_data, goto_yema)

    print(jz_data)

    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\人员资质测试\beijing\数据准备\省平台北京人员资质建造工程师_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['姓名', '注册证书编号', '注册号', '注册专业', '聘用企业', '级别']
    wirteDataToExcel(outfilename, "sheetName", columnRows, jz_data)

    # # 获取造价师
    # driver.get('http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=314447')
    # zj_total_ye = 20
    # zj_data = []
    # for goto_yema in range(5, zj_total_ye):
    #     get_bj_zj_ryzz(driver, zj_data, goto_yema)
    #
    # print(zj_data)
    #
    # # 把数据导出到xlsx
    # outfilename = r'D:\筑龙项目\人员资质测试\beijing\数据准备\省平台北京人员资质造价工程师_胡金花' + str(now_time) + '.xlsx'
    # columnRows = ['姓名','类别','注册号', '单位名称']
    # wirteDataToExcel(outfilename, "sheetName", columnRows, zj_data)





    driver.quit()