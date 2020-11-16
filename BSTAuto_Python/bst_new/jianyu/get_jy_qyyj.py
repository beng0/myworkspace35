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
driver.find_element("xpath","//a[@id='entsearch']").click()
sleep(2)
qyyjs = []

# 获取一页的gg
def get_page_qyyjs(qyname):
    try:
        driver.find_element("xpath","//div[@style='display:none']")
    except:
        qyyj_temp = [qyname, "1", "1"]
        qyyjs.append(qyyj_temp)
    else:
        content_list = driver.find_elements("xpath","//tbody/tr")
        for content in content_list:
            qyname = qyname
            qyyj = content.find_element("xpath","./td[3]").text.strip()
            fabu_time = content.find_element("xpath","./td[2]").text.strip()
            href = content.find_element("xpath","")
            qyyj_temp = [qyname,qyyj,fabu_time]
            print(qyyj_temp)
            qyyjs.append(qyyj_temp)
            # print(ggnames)



def get_qyyjs(qyname , page_num=1 , hasdata=True):
    driver.find_element("id","searchinput").clear()
    driver.find_element("id", "searchinput").send_keys(qyname)
    sleep(1)
    driver.find_element("xpath", "//input[@value='搜索']").click()
    sleep(5)
    try:
        driver.find_element("xpath", "//div[@style='display:none']")
    except:
        qyyjs.append([qyname,"无业绩","1"])
    else:
        while True:
            get_page_qyyjs(qyname)
            page_num = page_num+1
            try:
                driver.find_element("xpath", "//a[@class='nbnext']")
            except:
                page_next = False
            else:
                page_next = True
            print(page_next)
            if page_next and page_num <=2:
                driver.find_element("xpath",'//a[@class="nbnext"]').click()
                sleep(5)
            else:
                break

if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\jianyu\qynames20201105.xlsx"
    outfilename = root_dir + r"\jianyu\jianyuqyyjs_"
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["qyname","ggnames","fabu_time"]
    qynames = read_excel(infilename)[0][1][1:]
    print(qynames)
    for row in qynames:
        qyname = row[0].strip()
        get_qyyjs(qyname)
    print(qyyjs)
    wirteDataToExcel(outfilename+tablenamehouzui+".xlsx", "Sheet1", columnRows,qyyjs)
    print("qyyj  to   excel  sucess")