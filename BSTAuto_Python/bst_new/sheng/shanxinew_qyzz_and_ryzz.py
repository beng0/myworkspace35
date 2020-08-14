from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util.my_read_excel import *
from datetime import datetime
from util.my_to_excel import *

def  openUrl(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("{}".format(url))
    return driver


def get_ryzz_detail(driver,qyname,ryzz_data):
    driver.find_element_by_xpath('//*[@id="two-tab"]').click()
    # 出现姓名列头
    loc = (By.XPATH, '//*[@id="two"]/table/thead/tr/th[2]')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(loc))

    has_data = driver.find_element_by_xpath('//*[@id="two"]/table').text.strip()

    if "暂无数据" in has_data:
        driver.get('https://zjt.shanxi.gov.cn/SXJGPublic/HTML/Enterprise_List')
        sleep(3)
        return ryzz_data


    driver.find_element_by_xpath('//*[@id="pagination"]/li/a[contains(text(),"末页")]').click()
    sleep(3)


    total_ye = driver.find_element_by_xpath('//*[@id="pagination"]/li/a[contains(text(),"末页")]/../preceding-sibling::li[1]/a').text.strip()
    print(total_ye)
    total_ye_count = int(total_ye)

    driver.find_element_by_xpath('//*[@id="pagination"]/li/a[contains(text(),"首页")]').click()
    sleep(3)

    for gotoye in  range(2,total_ye_count+2):
        print("ryzz 第"+str(gotoye-1)+"页")
        print(total_ye_count-2)
        # 翻页
        if total_ye_count > 6:
            if (gotoye != 2) and (gotoye <= 7):
                driver.find_element_by_xpath('//*[@id="pagination"]/li['+str(gotoye)+']/a').click()
                sleep(3)
            elif (gotoye > 7) and (gotoye <= (total_ye_count-2)):
                driver.find_element_by_xpath('//*[@id="pagination"]/li[7]/a').click()
                sleep(3)
            elif gotoye == (total_ye_count-1):
                driver.find_element_by_xpath('//*[@id="pagination"]/li['+str(7+1)+']/a').click()
                sleep(3)
            elif gotoye == total_ye_count:
                driver.find_element_by_xpath('//*[@id="pagination"]/li['+str(7+2)+']/a').click()
                sleep(3)
            elif gotoye == (total_ye_count+1):
                driver.find_element_by_xpath('//*[@id="pagination"]/li['+str(7+3)+']/a').click()
                sleep(3)
        else:
            if (gotoye != 2):
                driver.find_element_by_xpath('//*[@id="pagination"]/li['+str(gotoye)+']/a').click()
                sleep(3)


        ryzz_list = driver.find_elements_by_xpath('//*[@id="Registrar"]/tr')
        for content in ryzz_list:
            name = content.find_element_by_xpath('./td[1]/a').text.strip()
            sfz = content.find_element_by_xpath('./td[2]').text.strip()
            zclb = content.find_element_by_xpath('./td[3]').text.strip()
            zyyzh = content.find_element_by_xpath('./td[4]').text.strip()
            fzrq = content.find_element_by_xpath('./td[5]').text.strip()
            yxq = content.find_element_by_xpath('./td[6]').text.strip()
            tmp=[qyname,name,sfz,zclb,zyyzh,fzrq,yxq]
            ryzz_data.append(tmp)
            print(ryzz_data)

    driver.get('https://zjt.shanxi.gov.cn/SXJGPublic/HTML/Enterprise_List')
    sleep(3)



def get_qyzz_detail(driver,qyname,qyzz_data):
    qyzz_list = driver.find_elements_by_xpath('//*[@id="Qualifications"]/tr')
    for content in qyzz_list:
        zzlb = content.find_element_by_xpath('./td[1]').text.strip()
        zsh = content.find_element_by_xpath('./td[2]').text.strip()
        zsyxq = content.find_element_by_xpath('./td[3]').text.strip()
        fzjg = content.find_element_by_xpath('./td[4]').text.strip()
        qyzz = content.find_element_by_xpath('./td[5]').text.strip()
        tmp=[qyname,zzlb,zsh,zsyxq,fzjg,qyzz]
        qyzz_data.append(tmp)
        print(qyzz_data)



def get_zhiding_qy_qyzz_and_ryzz(driver,sheet1data,ryzz_data,qyzz_data):
    driver.maximize_window()
    sleep(3)
    for row in sheet1data:

        qyname = row[0].strip()

        loc = (By.XPATH,'//*[@id="search_text"]')
        WebDriverWait(driver,30).until(EC.visibility_of_element_located(loc))

        #输入企业名
        driver.find_element_by_xpath('//*[@id="search_text"]').clear()
        driver.find_element_by_xpath('//*[@id="search_text"]').send_keys(qyname)

        #点击查询
        driver.find_element_by_xpath('//*[@id="Query_Data"]').click()
        sleep(3)

        href = driver.find_element_by_xpath('//*[@id="List_Enterprises"]/tr/td[1]/a').get_attribute('href')
        driver.get(href)
        sleep(3)

        get_qyzz_detail(driver,qyname,qyzz_data)

        get_ryzz_detail(driver,qyname, ryzz_data)



if __name__ == '__main__':
    conp = ["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
    infilename = r"D:\SVN\数据对比\对比结果\每周云南广东对比\山西\企业_胡金花_20200715.xlsx"
    outfilename_ryzz = r"D:\SVN\数据对比\对比结果\每周云南广东对比\山西\山西_省平台ryzz_胡金花_"
    outfilename_qyzz = r"D:\SVN\数据对比\对比结果\每周云南广东对比\山西\山西_省平台qyzz_胡金花_"

    driver = openUrl("https://zjt.shanxi.gov.cn/SXJGPublic/HTML/Enterprise_List")


    # 读取excel中的数据
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    ryzz_data = []
    qyzz_data = []
    # 得到指定企业对应的qyzz ryzz
    get_zhiding_qy_qyzz_and_ryzz(driver,sheet1data,ryzz_data,qyzz_data)
    driver.quit()

    # 保存qyzz
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["qyname", "zzlb","zsh","zsyxq","fzjg","qyzz"]
    wirteDataToExcel(outfilename_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, qyzz_data)
    print("qyzz  to  excel  success")

    # 保存ryzz
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows1 = ["qyname", "name", "sfz", "zclb", "zyyzh","fzrq","yxq"]
    wirteDataToExcel(outfilename_ryzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows1, ryzz_data)
    print("ryzz to  excel  success")


