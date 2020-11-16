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
from selenium.webdriver import ActionChains

def  open(url):
    # 代理IP
    # driver = get_driver_moni_ip()
    # driver.get("http://httpbin.org/ip")
    # print(driver.page_source)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    return driver




# 指定企业名和项目经理
def get_jst_xmjlyj_zhiding_qyandxmjl(driver,jst_xmjl_data,datahref):
    loc = (By.XPATH, '//*[@id="jst-nav"]/a')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(loc))
    element = driver.find_element_by_xpath('//*[@id="jst-nav"]/a')
    ActionChains(driver).move_to_element(element).perform()
    xmjl_loc2 = (By.XPATH, '//*[@id="jst-nav"]//label[text()="项目经理"]')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(xmjl_loc2))
    xmjl_element = driver.find_element_by_xpath('//*[@id="jst-nav"]//label[text()="项目经理"]')
    ActionChains(driver).move_to_element(xmjl_element).perform()
    xmjl_element.click()
    sleep(5)

    for row in jst_xmjl_data:
        driver.get('https://www.cbi360.net/hhb/buildersoso/')
        sleep(3)
        xmjl = row[1].strip()
        zhongbiaoren = row[2].strip()


        # 输入项目经理名字
        xmjl_loc = (By.XPATH, '//input[contains(@placeholder,"请输入项目经理完整姓名")]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(xmjl_loc)).clear()
        driver.find_element_by_xpath('//*[@id="nav-builder"]/div/div[1]/div[3]/input[1]').clear()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(xmjl_loc)).send_keys(str(xmjl))

        # 输入企业名字
        company_name_loc = (By.XPATH, '//input[contains(@placeholder,"请输入企业名称关键词")]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).clear()
        driver.find_element_by_xpath('//*[@id="nav-builder"]/div/div[1]/div[3]/input[2]').clear()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).send_keys(str(zhongbiaoren))


        # 点击搜索按钮
        driver.find_element_by_xpath('//*[@id="nav-builder"]//span[text()="查询"]').click()
        sleep(3)

        xmjl_count=driver.find_element_by_xpath('//*[@id="res-table"]/div[1]/div/em').text.strip()
        xmjl_count2 = int(xmjl_count)
        if xmjl_count2==0:continue

        data_list = driver.find_elements_by_xpath('//*[@id="res-table"]/div[2]/div')
        for  content  in  data_list:
            href = content.find_element_by_xpath('./ul/li[2]/h2/strong/a').get_attribute('href').strip()
            tmp = [zhongbiaoren, xmjl, href]
            datahref.append(tmp)
            print(datahref)

# 指定企业名
def get_jst_xmjlyj_zhiding_qy(driver,sheet1data,datahref):
    # 选择项目经理
    driver.find_element_by_xpath('//*[contains(text(),"查项目经理")]').click()
    sleep(3)

    for row in sheet1data:
        zhongbiaoren = row[2].strip()

        # 输入企业名字
        company_name_loc = (By.XPATH, '//input[contains(@placeholder,"请输入企业名称关键词")]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).clear()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).send_keys(str(zhongbiaoren))

        # 点击搜索按钮
        driver.find_element_by_xpath('//span[contains(text(),"查询")]').click()
        sleep(3)

        # 该企业总共有多少个xmjl
        total_xmjl_count = driver.find_element_by_xpath('//div[contains(text(),"共找到")]/em').text.strip()
        xmjl_count = int(total_xmjl_count)
        if xmjl_count > 5 : xmjl_count = 5

        content_list = driver.find_elements_by_xpath('//div[contains(text(),"共找到")]/../../div/following-sibling::div/div[@class="table-con"]')
        for content in content_list:
            xmjl = content.find_element_by_xpath('./ul/li[2]/h2/strong/a').text.strip()
            href = content.find_element_by_xpath('./ul/li[2]/h2/strong/a').get_attribute('href')
            tmp = [zhongbiaoren, xmjl, href]
            datahref.append(tmp)
            print(datahref)
            xmjl_count -= 1
            if  xmjl_count == 0 : break

def get_xmjl_detail(driver,datahref,datalist_zb):
    for zhongbiaoren,xmjl,href in datahref:
        print(href)
        driver.get(href)
        sleep(3)

        zbsl_loc = (By.XPATH, '//*[@id="__layout"]/div/div[4]/div[2]/div/div/div[2]/div[1]/span')
        zbsl = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(zbsl_loc)).text.strip()
        total_ye = total_yema(zbsl)
        datalist_zb = data_zb(total_ye, href, zhongbiaoren, xmjl, zbsl,datalist_zb)

        tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        columnRows = ["href", "zhongbiaoren", "xmjl", "ggname", "zbdq", "je", "zbtime", "zbsl_count", "zbly","zbly_href"]
        wirteDataToExcel(infilename_jst_xmjlyj + tablenamehouzui + ".xlsx", "Sheet1", columnRows, datalist_zb)
        print("to excel scussce")

def  total_yema(zbsl):
    # 计算该项目经理中标有几页数据
    zbsl_count = int(zbsl)
    if zbsl_count > 10:
        if zbsl_count % 10 == 0:
            total_ye = zbsl_count // 10
        else:
            total_ye = zbsl_count // 10 + 1
    else:
        total_ye = 1
    return total_ye

def  data_zb(total_ye,href, zhongbiaoren, xmjl,zbsl,datalist_zb):
    print(href)
    for gotoyema in range(1, total_ye + 1):
        if total_ye > 1:
            yema_input_xpath = '//span[text()="转到"]/../preceding-sibling::div[1]/input'
            driver.find_element_by_xpath(yema_input_xpath).clear()
            driver.find_element_by_xpath(yema_input_xpath).send_keys(str(gotoyema))

            driver.find_element_by_xpath('//span[text()="转到"]').click()
            sleep(3)

        ggname = " "
        zbdq = " "
        je = " "
        zbtime = " "
        zbly = " "
        zbly_href = " "
        je = " "
        content_list = driver.find_elements_by_xpath('//*[@id="__layout"]/div/div[4]/div[2]/div/div/div[2]/div[3]/div[1]/div[1]/div/div[3]/table/tbody/tr')
        for content in content_list:
            ggname = content.find_element_by_xpath('./td[2]/div/h2/a').text.strip()

            if content.find_element_by_xpath('./td[3]/div/span'):
                zbdq = content.find_element_by_xpath('./td[3]/div/span').text.strip()

            if content.find_element_by_xpath('./td[4]/div/span'):
                je = content.find_element_by_xpath('./td[4]/div/span').text.strip()

            if content.find_element_by_xpath('./td[5]/div/span'):
                zbtime = content.find_element_by_xpath('./td[5]/div/span').text.strip()

            if content.find_element_by_xpath('./td[6]/div/a'):
                zbly = content.find_element_by_xpath('./td[6]/div/a').text.strip()
                zbly_href = content.find_element_by_xpath('./td[6]/div/a').get_attribute('href').strip()

            tmp = [href, zhongbiaoren, xmjl, ggname, zbdq, je, zbtime, zbsl, zbly, zbly_href]
            datalist_zb.append(tmp)
            print(datalist_zb)
    return datalist_zb

def  get_guangdong_xmjl_href(driver,sheet1data,datahref,shenfen_xpath):
    # 选择项目经理
    driver.find_element_by_xpath('//*[contains(text(),"查项目经理")]').click()
    sleep(3)


    # driver.find_element_by_xpath('//*[@id="link-box"]/a[contains(text(),"广东")]').click()
    driver.find_element_by_xpath(shenfen_xpath).click()
    sleep(3)

    # 点击搜索按钮
    driver.find_element_by_xpath('//span[contains(text(),"查询")]').click()
    sleep(3)

    xmjl_count = driver.find_element_by_xpath('//*[@id="res-table"]/div[1]/div/em').text
    # 计算该企业中标有几页数据
    zbsl_count = int(xmjl_count)
    if zbsl_count > 15:
        if zbsl_count % 15 == 0:
            total_ye = zbsl_count // 15
        else:
            total_ye = zbsl_count // 15 + 1
    else:
        total_ye = 1
    print("总页数：" + str(total_ye))
    if total_ye > 5: total_ye = 5

    for gotoyema in range(1, total_ye + 1):
        print("第" + str(gotoyema) + "页")
        if gotoyema > 1:
            locator2 = (By.XPATH, '//*[@id="res-table"]/div[2]/div[16]/ul/li[12]/input')
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

            element = driver.find_element_by_xpath('//*[text()="转到"]')
            driver.execute_script("arguments[0].click();", element)
            sleep(3)


        content_list = driver.find_elements_by_xpath('//*[@id="res-table"]/div[2]/div[@class="table-con"]')
        for content in content_list:
            #                                     //*[@id="res-table"]/div[2]/div[2]/ul/li[2]/h2/strong/a
            #                                     //*[@id="res-table"]/div[2]/div[1]/ul/li[2]/h2/strong/a
            xmjl = content.find_element_by_xpath('./ul/li[2]/h2/strong/a').text.strip()
            print(xmjl)
            href = content.find_element_by_xpath('./ul/li[2]/h2/strong/a').get_attribute('href')
            print(href)
            zbr = content.find_element_by_xpath('./ul/li[2]/h2/a').text.strip()
            print(zbr)
            tmp = [zbr, xmjl, href]
            datahref.append(tmp)
            print(datahref)


def read_excel_data(infilename):
    jy_qyyj_data =[]
    # 读取标事通企业业绩
    all_sheet_data1 = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    jy_qyyj_data = all_sheet_data1[0][1][1:]
    # print(jy_qyyj_data)
    return jy_qyyj_data

if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    # infilename = root_dir + r"\data\get_jst_qyyj\广东_云南_山西建设通企业业绩_胡金花_href_20201009_171336.xlsx"
    # outfilename = root_dir +r"\data\get_jst_xmjlyj\广东_云南_山西_jst_xmjlyj_获取结果_胡金花_"
    infilename_xmjl = root_dir + r"\xmjl_list\云南_项目经理列表_模板.xlsx"
    infilename_xmjl_href = root_dir + r"\get_jst_xmjlyj\建设通企业业绩_数据准备_贺家斌_href_20201111_152217.xlsx"
    infilename_jst_xmjlyj_href = root_dir + r"\get_jst_xmjlyj\建设通项目经理业绩_href_贺家斌_"
    infilename_jst_xmjlyj = root_dir + r"\get_jst_xmjlyj\建设通企业业绩_中标公示_贺家斌_"


    url = "https://passport.cbi360.net/login?url=https%3A%2F%2Fwww.cbi360.net%2Fhyjd%2F20200528%2F203181.html"
    driver = open(url)

    datahref=[]
    datalist_zb = []
    datalist_sk = []

    jst_xmjl_data = (read_excel_data(infilename_xmjl))[:100]
    print(jst_xmjl_data)


    s = input("input  your  unm: ")
    if int(s) == 1:
        # 得到指定企业和项目经理的href
        get_jst_xmjlyj_zhiding_qyandxmjl(driver, jst_xmjl_data, datahref)

        # 得到指定企业
        # get_jst_xmjlyj_zhiding_qy(driver, sheet1data, datahref)

        # 广东企业
        # for sheng, shenfen_xpath in shenfen_list:
        #     get_guangdong_xmjl_href(driver, sheet1data, datahref,shenfen_xpath)
        #
        # tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        # columnRows1 = ["zhongbiaoren", "xmjl", "href"]
        # wirteDataToExcel(infilename_jst_xmjlyj_href+ tablenamehouzui + "xmjlhref.xlsx", "Sheet1", columnRows1,datahref)
        # print("to excel scussce")

        # datahref = (read_excel_data(infilename_xmjl_href))[27:]
        # print(datahref)
        #得到每个项目经理的业绩
        get_xmjl_detail(driver,datahref,datalist_zb)

        # tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        # columnRows = ["href", "zhongbiaoren", "xmjl", "ggname", "zbdq","je","zbtime", "zbsl_count", "zbly", "zbly_href"]
        # wirteDataToExcel(infilename_jst_xmjlyj + tablenamehouzui + ".xlsx", "Sheet1", columnRows,datalist_zb)
        # print("to excel scussce")