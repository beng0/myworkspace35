from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
from datetime import datetime
from time import sleep
from bst.bst_datatest.test_case.models.my_to_excel import wirteDataToExcel

def get_bj_qyzz(driver,data,goto_yema):
    locator = (By.XPATH,'//*[@id="tab_view"]')
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

    content_list = body.xpath('//*[@id="tab_view"]/tbody/tr')[1:]
    for content in content_list:
        qyname= content.find('.//td[1]').text
        zsbh=content.find('.//td[2]').text
        href=content.find('.//td[3]/a').get('href')
        href ='http://bjjs.zjw.beijing.gov.cn'+href
        temp=[href,qyname,zsbh]
        data.append(temp)


def get_detail(driver,data):
    qyzz_data=[]
    for href,qyname,zsbh in data:
        print(href)
        driver.get(href)
        qyname_loc = (By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[1]/td[2]')
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(qyname_loc))
        try:
            qyname=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[1]/td[2]').text.strip()
            xxdz=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[2]/td[2]').text.strip()
            zczb=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[3]/td[2]').text.strip()
            tyshxydm=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[4]/td[2]').text.strip()
            jjxz=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[5]/td[2]').text.strip()
            fddb=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[6]/td[2]').text.strip()
            zsbh=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[7]/td[2]').text.strip()
            zz=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[8]/td[2]').text.strip()
            xkjg=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[9]/td[2]').text.strip()
            yxq1=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[10]/td[2]/span[1]').text.strip()
            yxq2=driver.find_element(By.XPATH,'//*[@id="f769407bfe4f4f569aea330d15d7b927"]/div[3]/table/tbody/tr[10]/td[2]/span[2]').text.strip()
            yxq=yxq1+'~'+yxq2
            temp=[href,qyname,xxdz,zczb,tyshxydm,jjxz,fddb,zsbh,zz,xkjg,yxq]
            qyzz_data.append(temp)
        except:
            continue
    return qyzz_data





if __name__=='__main__':
    now_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    driver = webdriver.Chrome()
    driver.get('http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=307900')
    total_ye = 20
    data =[]
    for goto_yema in range(11,total_ye):
        get_bj_qyzz(driver,data,goto_yema)

    print(data)
    qyzz_data=get_detail(driver,data)
    print(qyzz_data)

    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\企业资质测试\beijing\数据准备\省平台北京企业资质_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['href','qyname','xxdz','zczb','tyshxydm','jjxz','fddb','zsbh','zz','xkjg','yxq']
    wirteDataToExcel(outfilename, "sheetName", columnRows, qyzz_data)
    driver.quit()