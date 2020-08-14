from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
# from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from time import sleep
from util.my_to_excel import *
from util.my_read_excel import *
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




# 指定企业名和项目经理
def get_jst_xmjlyj_zhiding_qyandxmjl(driver,sheet1data,datahref):
    # 选择项目经理
    driver.find_element_by_xpath('//*[@id="ul_search_list_menu"]/li[4]/a').click()
    sleep(3)

    for row in sheet1data:
        zhongbiaoren = row[0].strip()
        xmjl = row[1].strip()

        # 输入项目经理名字
        xmjl_loc = (By.XPATH, '//*[@id="txt_builder_name"]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(xmjl_loc)).clear()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(xmjl_loc)).send_keys(str(xmjl))

        # 输入企业名字
        company_name_loc = (By.XPATH, '//*[@id="txt_company_name"]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).clear()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).send_keys(str(zhongbiaoren))

        # 点击搜索按钮
        driver.find_element_by_xpath('//*[@id="btn_search"]').click()
        sleep(3)

        href = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/ul/li/div[2]/div[1]/h2/strong/a').get_attribute('href').strip()
        tmp = [zhongbiaoren, xmjl, href]
        datahref.append(tmp)
        print(datahref)

# 指定企业名
def get_jst_xmjlyj_zhiding_qy(driver,sheet1data,datahref):
    # 选择项目经理
    driver.find_element_by_xpath('//*[@id="ul_search_list_menu"]/li[4]/a').click()
    sleep(3)

    for row in sheet1data:
        zhongbiaoren = row[0].strip()

        # 输入企业名字
        company_name_loc = (By.XPATH, '//*[@id="txt_company_name"]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).clear()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).send_keys(str(zhongbiaoren))

        # 点击搜索按钮
        driver.find_element_by_xpath('//*[@id="btn_search"]').click()
        sleep(3)

        # 该企业总共有多少个xmjl
        total_xmjl_count = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[1]/div/em').text.strip()
        xmjl_count = int(total_xmjl_count)
        if xmjl_count > 5 : xmjl_count = 5

        content_list = driver.find_elements_by_xpath('/html/body/div[8]/div[2]/div[2]/ul/li')
        for content in content_list:
            xmjl = content.find_element_by_xpath('./div[2]/div[1]/h2/strong/a').text.strip()
            href = content.find_element_by_xpath('./div[2]/div[1]/h2/strong/a').get_attribute('href')
            tmp = [zhongbiaoren, xmjl, href]
            datahref.append(tmp)
            print(datahref)
            xmjl_count -= 1
            if  xmjl_count == 0 : break

def get_xmjl_detail(driver,datahref,datalist):
    for zhongbiaoren,xmjl,href in datahref:
        driver.get(href)
        sleep(3)

        zbsl_loc = (By.XPATH, '//*[@id="newriskWrap"]/div[2]/ul/li[1]/div[2]/i')
        zbsl2 = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(zbsl_loc)).text.strip()
        print(href)

        # 计算该项目经理中标有几页数据
        zbsl_count = int(zbsl2)
        if zbsl_count > 15:
            if zbsl_count % 15 == 0:
                total_ye = zbsl_count // 15
            else:
                total_ye = zbsl_count // 15 + 1
        else: total_ye = 1


        for gotoyema in range(1, total_ye + 1):
            if total_ye > 1:
                # 获得当前页码
                cur_yema = driver.find_element_by_xpath('//*[@id="newriskWrap"]/div[2]/div/div/div/label').text.strip()
                # 翻页
                if int(cur_yema) != int(gotoyema):
                    try:
                        driver.find_element_by_xpath('//*[@id="newriskWrap"]/div[2]/div/div/div/input[1]').clear()
                        driver.find_element_by_xpath('//*[@id="newriskWrap"]/div[2]/div/div/div/input[1]').send_keys(str(gotoyema))
                        driver.find_element_by_xpath('//*[@id="newriskWrap"]/div[2]/div/div/div/input[2]').clear()
                    except BaseException as msg:
                        print(msg)
                    sleep(3)

            zbdq = " "
            zbtime = " "
            zbly =  " "
            zbly_href = " "
            content_list = driver.find_elements_by_xpath('//*[@id="newriskWrap"]/div[2]/ul/li')[1:]
            for content in content_list:
                ggname = content.find_element_by_xpath('./div[2]/h2/a').text.strip()

                if content.find_element_by_xpath('./div[4]'):
                    zbdq = content.find_element_by_xpath('./div[4]').text.strip()

                if content.find_element_by_xpath('./div[5]'):
                    zbtime = content.find_element_by_xpath('./div[5]').text.strip()

                if content.find_element_by_xpath('./div[6]/a'):
                    zbly = content.find_element_by_xpath('./div[6]/a').text.strip()

                if content.find_element_by_xpath('./div[6]/a'):
                    zbly_href = content.find_element_by_xpath('./div[6]/a').get_attribute('href').strip()

                tmp = [href, zhongbiaoren,xmjl, ggname, zbdq,zbtime, zbsl_count, zbly, zbly_href]
                datalist.append(tmp)
                print(datalist)


if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.'))
    infilename = root_dir + r"\data\xmjl_list\广东_云南_山西_jst_xmjlyj_贺家斌_20200807.xlsx"
    outfilename = root_dir +r"\data\xmjl_list\广东_云南_山西_jst_xmjlyj_获取结果_贺家斌_"
    url = "https://passport.cbi360.net/login?url=https%3A%2F%2Fwww.cbi360.net%2Fhyjd%2F20200528%2F203181.html"
    driver = open(url)

    datahref=[]
    datalist = []

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    s = input("input  your  unm: ")
    if int(s) == 1:
        # 得到指定企业和项目经理的href
        get_jst_xmjlyj_zhiding_qyandxmjl(driver, sheet1data, datahref)

        # 得到指定企业
        # get_jst_xmjlyj_zhiding_qy(driver, sheet1data, datahref)

        tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        columnRows1 = ["zhongbiaoren", "xmjl", "href"]
        wirteDataToExcel(outfilename+"href_" + tablenamehouzui + "xmjlhref.xlsx", "Sheet1", columnRows1,datahref)
        print("to excel scussce")


        #得到每个项目经理的业绩
        get_xmjl_detail(driver,datahref,datalist)
        tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        columnRows = ["href", "zhongbiaoren", "xmjl", "ggname", "zbdq","zbtime", "zbsl_count", "zbly", "zbly_href"]
        wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "Sheet1", columnRows,datalist)
        print("to excel scussce")