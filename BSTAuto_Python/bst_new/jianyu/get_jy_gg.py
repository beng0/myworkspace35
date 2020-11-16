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


driver = webdriver.Chrome()
driver.get("https://www.jianyu360.com/jylab/supsearch/index.html")
driver.maximize_window()
driver.implicitly_wait(30)

s = input("input something")
driver.find_element("xpath","//input[@id='starttime']").click()
driver.switch_to.frame(driver.find_element("xpath","//iframe[@hidefocus='true']"))
# driver.find_element("xpath","//div[@class='navImg NavImgl']/a").click()
driver.find_element("xpath","//td[@onclick='day_Click(2020,11,4);']").click()
driver.switch_to.default_content()
driver.find_element("xpath","//input[@id='endtime']").click()
driver.switch_to.frame(driver.find_element("xpath","//iframe[@hidefocus='true']"))
driver.find_element("xpath","//td[@onclick='day_Click(2020,11,4);']").click()
driver.switch_to.default_content()
driver.find_element("xpath","//button[@id='timebut']").click()
driver.find_element("xpath","//font[text()='招标公告']").click()
driver.find_element("xpath","//font[text()='变更']").click()

sleep(2)

ggs = []
# ggname = driver.find_element("xpath","//div[@class='seaTender-inner w']/div[3]/"
#                                       "div[@class='lucene']/ul/li/div/div[@class='luce-left']/div/a").text
# print(ggname)

# 获取一页的gg
def get_page_ggs(kw):
    content_list = driver.find_elements("xpath","//div[@class='seaTender-inner w']/div[3]/div[@class='lucene']/ul/li")
    for content in content_list:
        kw = kw
        ggname = content.find_element("xpath","./div/div[@class='luce-left']/div/a").text.strip()
        fabu_time = content.find_element("xpath","./div/div[@class='luce-right']/span").text.strip()
        gg_temp = [kw,ggname,fabu_time]
        print(gg_temp)
        ggs.append(gg_temp)
        # print(ggnames)

# 检查是否有下一页
# a = driver.find_element("xpath","//a[@class='nbnext']").get_attribute("class")
# print(a)
# 获取一个关键词的近7天的公告
def get_kw_ggs(kw):
    driver.find_element("id","searchinput").clear()
    driver.find_element("id", "searchinput").send_keys(kw)
    driver.find_element("xpath", "//input[@value='搜索']").click()
    while True:
        get_page_ggs(kw)
        try:
            driver.find_element("xpath", "//a[@class='nbnext']")
        except:
            page_next = False
        else:
            page_next = True
        print(page_next)
        if page_next:
            driver.find_element("xpath",'//a[@class="nbnext"]').click()
            sleep(4)
        else:
            break

if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\jianyu\keywords20201103.xlsx"
    outfilename = root_dir + r"\jianyu\jianyuggnames_"
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["keyworld","ggnames","fabu_time"]
    keywords = read_excel(infilename)[0][1][1:]
    print(keywords)
    for row in keywords:
        kw = row[0].strip()
        get_kw_ggs(kw)
    print(ggs)
    wirteDataToExcel(outfilename+tablenamehouzui+".xlsx", "Sheet1", columnRows,ggs)
    print("ryxx  to   excel  sucess")








