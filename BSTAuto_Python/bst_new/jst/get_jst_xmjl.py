from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
# from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from time import sleep
from BSTAuto_Python.bst_new.util.my_to_excel import *
from BSTAuto_Python.bst_new.util.my_read_excel import *
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    driver.find_element_by_xpath('//div[@class="nav-box"]/div[4]/a').click()
    sleep(3)

    for row in sheet1data:
        zhongbiaoren = row[0].strip()
        xmjl = row[1].strip()

        # 输入项目经理名字
        driver.execute_script("""document.querySelector('input[placeholder="请输入项目经理完整姓名"]').value=''""")
        xmjl_loc = (By.XPATH, '//input[@placeholder="请输入项目经理完整姓名"]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(xmjl_loc)).send_keys(str(xmjl))

        # 输入企业名字
        driver.execute_script("""document.querySelector('input[placeholder="请输入企业名称关键词"]').value=''""")
        sleep(1)
        for i in range(20):
            driver.find_element_by_xpath('//input[@placeholder="请输入企业名称关键词"]').send_keys(Keys.BACK_SPACE)
        driver.find_element_by_xpath('//input[@placeholder="请输入企业名称关键词"]').send_keys(zhongbiaoren)

        # 点击搜索按钮
        driver.find_element_by_xpath('//span[text()="查询"]').click()

        sleep(3)
        hreflis = driver.find_elements_by_xpath('//strong[@class="personnel-name"]/a')
        for hrefli in hreflis:
            href = hrefli.get_attribute('href').strip()
            tmp = [zhongbiaoren, xmjl, href]
            datahref.append(tmp)
        print(datahref)

# 指定企业名
def get_jst_xmjlyj_zhiding_qy(driver,sheet1data,datahref):
    # 选择项目经理
    driver.find_element_by_xpath('//div[@class="nav-box"]/div[4]/a').click()
    sleep(3)

    for row in sheet1data:
        zhongbiaoren = row[1].strip()

        # 输入企业名字
        driver.execute_script("""document.querySelector('input[placeholder="请输入企业名称关键词"]').value=''""")
        sleep(1)
        for i in range(20):
            driver.find_element_by_xpath('//input[@placeholder="请输入企业名称关键词"]').send_keys(Keys.BACK_SPACE)
        driver.find_element_by_xpath('//input[@placeholder="请输入企业名称关键词"]').send_keys(zhongbiaoren)

        # 点击搜索按钮
        driver.find_element_by_xpath('//span[text()="查询"]').click()

        sleep(3)

        # 该企业总共有多少个xmjl
        total_xmjl_count = driver.find_element_by_xpath('//div[@class="table-top clear"]/div/em').text.strip()
        xmjl_count = int(total_xmjl_count)
        if xmjl_count > 20 : xmjl_count = 20

        content_list = driver.find_elements_by_xpath('//div[@id="res-table"]/div[2]/div')
        for content in content_list:
            xmjl = content.find_element_by_xpath('./ul/li[2]//strong/a').text.strip()
            href = content.find_element_by_xpath('./ul/li[2]//strong/a').get_attribute('href')
            tmp = [zhongbiaoren, xmjl, href]
            datahref.append(tmp)
            print(datahref)
            xmjl_count -= 1
            if  xmjl_count == 0 : break

def get_xmjl_detail(driver,datahref,datalist):
    for zhongbiaoren,xmjl,href in datahref:
        driver.get(href)
        sleep(3)

        zbsl_loc = (By.XPATH, '//div[@class="table"]/dl[1]/dd[2]/i')
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
                cur_yema = driver.find_element_by_xpath('//div[@class="pagination-wrap"]/ul/li[@class="active"]/a').text.strip()
                # 翻页
                if int(cur_yema) != int(gotoyema):
                    try:
                        driver.find_element_by_xpath('//input[@class="jumpnum"]').clear()
                        driver.find_element_by_xpath('//input[@class="jumpnum"]').send_keys(str(gotoyema))
                        driver.find_element_by_xpath('//li/a[text()="转到"]').click()
                    except BaseException as msg:
                        print(msg)
                    sleep(3)

            zbdq = " "
            zbtime = " "
            zbly =  " "
            zbly_href = " "
            content_list = driver.find_elements_by_xpath('//div[@class="table"]/dl')[1:]
            for content in content_list:
                ggname = content.find_element_by_xpath('./dd/h2/a').text.strip()

                if content.find_element_by_xpath('./dd[4]'):
                    zbdq = content.find_element_by_xpath('./dd[4]').text.strip()

                if content.find_element_by_xpath('./dd[5]'):
                    zbtime = content.find_element_by_xpath('./dd[5]').text.strip()

                if content.find_element_by_xpath('./dd[6]/a'):
                    zbly = content.find_element_by_xpath('./dd[6]/a').text.strip()

                if content.find_element_by_xpath('./dd[6]/a'):
                    zbly_href = content.find_element_by_xpath('./dd[6]/a').get_attribute('href').strip()

                tmp = [href, zhongbiaoren,xmjl, ggname, zbdq,zbtime, zbsl_count, zbly, zbly_href]
                datalist.append(tmp)
                print(datalist)


if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.'))
    infilename = root_dir + r"\data\qy_list\企业抽取_模板.xlsx"
    outfilename = root_dir +r"\data\get_jst_xmjlyj\云南__jst_xmjlyj_获取结果_贺家斌_"
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