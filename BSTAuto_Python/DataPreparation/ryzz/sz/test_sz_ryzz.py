# coding=utf-8
import unittest
from datetime import datetime
from selenium import webdriver
from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from bst.bst_datatest.test_case.page_obj.sz.SzRyzzPage import *
from time import sleep
from lxml import etree
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support  import expected_conditions as EC
from chardet import detect
from lxml.html.clean import Cleaner
import re
from bst.bst_datatest.test_case.models.my_to_excel import wirteDataToExcel


def get_sz_zz(data, goto_yema, driver):
    locator = (By.XPATH, '//table[@class="data-list"]//a')
    val = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator)).get_attribute('href')[-30:]
    cur_yema = driver.find_element(By.XPATH, '//span[@class="current"]').text
    if int(cur_yema) != int(goto_yema):
        driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_AspNetPager1"]/div[2]/a[3]').click()
        locator = (By.XPATH, '//table[@class="data-list"]//a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator))

    page = driver.page_source
    body = etree.HTML(page)
    # print(etree.tostring(body))
    table = body.find('.//table[@class="data-list"]')
    qyname_list = table.xpath('//tr')[1:]
    for content in qyname_list:
        s = content.find('.//td[1]/a')
        qyname = s.text.strip()
        href = s.get('href').strip()
        temp = [qyname, href]
        data.append(temp)
    print(data)
    return data


def get_qyzz_detail(data,driver):
        qyzz_data=[]
        for qyname,href in data:
            driver.get(href)
            locator =(By.XPATH,'//*[@id="ent-qua"]/table/tbody/tr[1]/th[1]')
            WebDriverWait(driver,10).until(EC.visibility_of_element_located(locator))

            page =driver.page_source
            body=etree.HTML(page)

            qyzz_table=body.xpath('.//div[@id="ent-qua"]//table[@class="data-list"]//tr')[1:]
            for td  in  qyzz_table:
                try:
                    # print(etree.tostring(td))
                    zsbh=td[0].text
                    zslb=td[1].text
                    zzdj = td[2].text
                    fzjg = td[3].text
                    fzrq = td[4].text
                    zsyxq = td[5].text
                    zszt = td[6].text
                    temp=[href,qyname,zsbh,zslb,zzdj,fzjg,fzrq,zsyxq,zszt]
                    qyzz_data.append(temp)
                except:
                    continue
        print(qyzz_data)
        return qyzz_data

def get_ryzz_detail(data,driver):

    ryzz_data = []
    print(data)
    for qyname,href in data:
        print(href)
        driver.get(href)
        locator = (By.XPATH,'//*[@id="ent-person"]/div[1]')
        WebDriverWait(driver,20).until(EC.visibility_of_element_located(locator))

        ryzz_pate = driver.find_element(By.ID,'ent-person').text
        if "暂无信息" in ryzz_pate:
            continue
            # return  ryzz_data


        if "更多→" in ryzz_pate:
            locator =(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_showmore_person"]')
            WebDriverWait(driver,30).until(EC.visibility_of_element_located(locator))
            try:
                driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_showmore_person"]').click()
                sleep(10)
                ryzz_iframe = driver.find_element_by_css_selector('iframe[id="nyroModalIframe"]')
                driver.switch_to.frame('nyroModalIframe')

            except:
                continue




        page = driver.page_source
        body = etree.HTML(page)
        print(etree.tostring(body))

        content_list = body.xpath('.//*[@id="ent-person"]/a[not(contains(@class,"gotop")) and not(contains(@class,"spec-more nyroModal"))]')
        for content  in content_list:
            try:
                name = content.find('.//div/div/span[1]').text
                name = re.sub('\s+', '', name).strip()

                zsbh = content.find('.//div/div/span[2]').text
                zsbh=re.sub('\s+', '', zsbh).strip()

                zclb= content.find('.//div/div/h5[1]').text
                zclb=re.sub('\s+', '', zclb).strip()

                zxyzh = content.find('.//div/div/h5[2]').text
                zxyzh=re.sub('\s+', '', zxyzh).strip()

                temp=[href,qyname,name,zsbh,zclb,zxyzh]

                ryzz_data.append(temp)
            except:
                continue
            print(ryzz_data)
    return ryzz_data


if __name__=='__main__':
    driver = webdriver.Chrome()
    driver.get('http://data.gdcic.net/Dop/Open/EnterpriseList.aspx')
    total_ye = 9

    s = input("input your num： ")

    if int(s) == 1:
        now_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        data =[]
        for  goto_yema in range(3,total_ye):
            get_sz_zz(data,goto_yema,driver)
            print("共获取" + str(total_ye - 1) + "页，已完成" + str(goto_yema) + "页")

        # 把数据导出到xlsx
        outfilename = r'D:\筑龙项目\人员资质测试\guangdong\数据准备\深圳\省平台深圳企业列表' + str(now_time) + '.xlsx'
        columnRows = ['href', 'qyname']
        wirteDataToExcel(outfilename, "sheetName", columnRows, data)

        # # 获得企业资质详情
        # qyzz_data=get_qyzz_detail(data,driver)
        # # 把数据导出到xlsx
        # outfilename = r'D:\筑龙项目\企业资质测试\guangdong\数据准备\深圳\省平台深圳企业资质' + str(now_time) + '.xlsx'
        # columnRows = ['href', 'qyname', 'zsbh', 'zsbh', 'zslb', 'zzdj','fzjg','fzrq','zsyxq','zszt']
        # wirteDataToExcel(outfilename, "sheetName", columnRows, qyzz_data)


        # 获得人员资质详情
        ryzz_data=get_ryzz_detail(data,driver)

        # 把数据导出到xlsx
        outfilename = r'D:\筑龙项目\人员资质测试\guangdong\数据准备\深圳\省平台深圳人员资质' + str(now_time) + '.xlsx'
        columnRows = [ 'href', 'qyname', 'name', 'zsbh', 'zclb', 'zxyzh']
        wirteDataToExcel(outfilename,"sheetName",columnRows, ryzz_data)

        driver.quit()