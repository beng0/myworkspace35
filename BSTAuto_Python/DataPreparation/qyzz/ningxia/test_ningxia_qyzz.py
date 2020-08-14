__Author__ = 'hjh'
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
from datetime import datetime
from time import sleep
from bst.bst_datatest.test_case.models.my_to_excel import wirteDataToExcel



def get_nx_qyzz(driver,data):
    locator = (By.XPATH,'/html/body/div[4]/div[2]/ol[1]/li[1]')
    WebDriverWait(driver,20).until(EC.visibility_of_element_located(locator))


    page = driver.page_source
    body = etree.HTML(page)
    # 区内企业
    content_list = body.xpath('//html/body/div[4]/div[2]/ol[1]/li')
    for content in content_list:
        lb= content.find('.//a').text
        href= content.find('.//a').get('data')
        temp=[href,'区内企业',lb]
        data.append(temp)

    #进宁企业
    driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[2]/em').click()
    sleep(3)
    content_list = body.xpath('//html/body/div[4]/div[2]/ol[2]/li')
    for content in content_list:
        lb = content.find('.//a').text
        href = content.find('.//a').get('data')
        temp = [href,'进宁企业', lb]
        data.append(temp)


def  get_detail(driver,qyzz_data,goto_yema,href,qyfl,lb):

        locator =(By.XPATH,'//*[@id="layerTest"]/div[2]/table')
        WebDriverWait(driver,30).until(EC.visibility_of_element_located(locator))
        cur_qyname = driver.find_element(By.XPATH,'//*[@id="zy_web_company_info"]/tr[1]/td[3]/a').text

        wz_total_ye = driver.find_elements(By.XPATH,'//*[@id="pagenation"]/li')

        wz_total_ye_count = len(wz_total_ye)-1
        if wz_total_ye_count==0: return
        print(wz_total_ye_count)

        # 翻页
        if int(goto_yema) != 1:
            if int(goto_yema) == 2:
                driver.find_element(By.XPATH,'//*[@id="pagenation"]/li[2]/a').click()
            elif  goto_yema < wz_total_ye_count:
                driver.find_element(By.XPATH, '//*[@id="pagenation"]/li['+str(goto_yema+1)+']/a').click()
            else:
                return

            sleep(30)
            locator = (By.XPATH, '//*[@id="zy_web_company_info"]/tr[1]/td[3]/a[not(contains(text(),"%s"))]' % cur_qyname)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))



        page = driver.page_source
        body = etree.HTML(page)

        content_list = body.xpath('//*[@id="zy_web_company_info"]/tr')
        for content in content_list:
            xh = content.find('.//td[1]').text
            shxym = content.find('.//td[2]').text
            qyname = content.find('.//td[3]/a').text
            zcdz = content.find('.//td[4]').text
            qyzzlx = content.find('.//td[6]').text
            fddb = content.find('.//td[8]').text
            zt = content.find('.//td[9]').text
            temp=[href,qyfl,lb,xh,shxym,qyname,zcdz,qyzzlx,fddb,zt]
            qyzz_data.append(temp)
            print(qyzz_data)


if __name__=='__main__':
    now_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    driver = webdriver.Chrome()

    driver.get('http://www.nxjscx.com.cn/qysj.htm#')
    data=[]

    # # 拿到对应类别企业链接
    # get_nx_qyzz(driver, data)
    print(data)

    total_ye = 5
    qyzz_data=[]

    for href,qyfl,lb  in  data:
        print(href)
        driver.get(href)
        sleep(30)

        for goto_yema in range(1,total_ye):
            try:
                get_detail(driver,qyzz_data,goto_yema,href,qyfl,lb)
                print("共获取" + str(total_ye - 1) + "页，已完成" + str(goto_yema) + "页")
            except:
                continue

    print(qyzz_data)

    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\企业资质测试\nixia\数据准备\省平台宁夏企业资质_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['href','企业类别','资质分类','序号','社会信用代码','企业名称','注册地址','企业资质类型','法定代表人','状态']
    wirteDataToExcel(outfilename, "sheetName", columnRows, qyzz_data)

    driver.quit()