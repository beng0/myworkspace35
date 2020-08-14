from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions  as  EC
from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from time import sleep
from lxml import etree


def open(url):
    driver = get_driver_moni_ip()
    # 查看本机ip，查看代理是否起作用
    driver.get("http://httpbin.org/ip")
    print(driver.page_source)
    return driver



def get_qyyj(driver,indata):
    qyyj_locator =(By.XPATH,'//*[@id="ul_search_list_menu"]/a[1]')
    WebDriverWait(driver,30).until(EC.visibility_of_element_located(qyyj_locator)).click()

    qyname_input_locator = (By.XPATH, '//*[@id="txt_company_name"]')
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located(qyyj_locator))

    for qyname in indata:
        driver.find_element(By.XPATH,'//*[@id="txt_company_name"]').clear()
        driver.find_element(By.XPATH, '//*[@id="txt_company_name"]').send_keys(qyname)
        driver.find_element(By.XPATH,'//*[@id="btn_search_company"]').click()
        sleep(10)
        #
        qyyj_name_locator='/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/h2/a/em'
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(qyyj_name_locator))
        href=driver.find_element(By.XPATH,'/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/h2/a/em').get_attribute('href')

        driver.get(href)







if __name__=='__main__':
    url = "https://hhb.cbi360.net/tenderbangsoso/"
    driver=open(url)

    indata=[]
    s = input("input  your  unm: ")
    if int(s) == 1:
        get_qyyj(driver,indata)

