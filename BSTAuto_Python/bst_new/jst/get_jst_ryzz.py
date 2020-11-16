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


# 得到导入企业的链接
def get_zhiding_qy_yj(driver,outfilename,sheet1data,zhiding_qy_yj_data):
    # 选择企业业绩
    driver.find_element_by_css_selector('.nav-box>div:nth-child(1)>a').click()
    sleep(3)

    for row in sheet1data:
        qyname = row[1].strip()
        driver.find_element_by_css_selector('input[placeholder="请输入企业名称关键字"]').clear()
        driver.find_element_by_css_selector('input[placeholder="请输入企业名称关键字"]').send_keys(qyname)
        driver.find_element_by_xpath('//span[text()="查询"]').click()
        sleep(3)

        qy_name = driver.find_element_by_css_selector\
            ('.table>div:nth-child(2)>div:nth-child(1)>ul>li:nth-child(2)>a>em').text.strip()
        if qy_name[-3:] == "已认证":
            qy_name = qy_name[0:-4]
        # https://hhb.cbi360.net/sg_549433/
        href = driver.find_element_by_css_selector\
            ('.table>div:nth-child(2)>div:nth-child(1)>ul>li:nth-child(2)>a').get_attribute('href')
        # print(href)
        zbsl = driver.find_element_by_css_selector\
            ('.table>div:nth-child(2)>div:nth-child(1)>dl>dd>a>strong').text.strip()
        tmp = [qy_name,href,zbsl]
        zhiding_qy_yj_data.append(tmp)
        # print(zhiding_qy_yj_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["qy_name", "href", "zbsl"]
    wirteDataToExcel(outfilename+'href_' + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, zhiding_qy_yj_data)
    print("qyhref  to   excel  sucess")

# 得到相应企业的全部企业资质信息
def get_qyzz_detail(driver,outfilename,zhiding_qy_yj_data,ryzz_data):
    for qy_name, href,zbsl in zhiding_qy_yj_data:
        driver.get(href)
        print(href)
        sleep(3)

        ry_count = int((driver.find_element_by_xpath
                        ("//div[@class='module'][5]//div[@class='text-count']/span").text.strip())[1:-1])
        if ry_count == 0: break

        # 点击企业人员
        # driver.find_element_by_xpath('//*[@id="newrisk"]/li[4]/h3/a').click()
        # sleep(3)


        # 计算该企业中有几页人员数据
        if ry_count > 15:
            if ry_count % 10 == 0:
                total_ye = ry_count // 10
            else:
                total_ye = ry_count // 10 + 1
        else:
            total_ye = 1
        print("总页数：" + str(total_ye))
        if total_ye > 30: total_ye = 30

        cur_ye = driver.find_element_by_xpath("//div[@class='module'][4]//ul/li[@class='number active']").text.strip()
        print(cur_ye)
        for gotoyema in range(1, total_ye + 1):
            print("第" + str(gotoyema) + "页")
            if cur_ye != gotoyema:
                locator2 = (By.XPATH, "//div[@class='module'][4]//slot/div/input")
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                driver.find_element_by_xpath('//div[@class="module"][4]//slot/button').click()
                sleep(3)

            ryname = ''
            ryzz = ''
            content_list = driver.find_elements_by_xpath('//div[@class="module"][4]//tbody/tr')[:]
            # print(','.join(str(s) for s in content_list if s not in [None]))
            for content in content_list:
                if content.find_element_by_xpath('./td[2]//h2/a'):
                    ryname = content.find_element_by_xpath('./td[2]//h2/a').text.strip()
                if content.find_element_by_xpath('./td[3]/div'):
                    ryzz = content.find_element_by_xpath('./td[3]/div').text.strip()

                qy_name = qy_name

                tmp = [qy_name, ryname,ryzz]
                qyzz_data.append(tmp)
                print(qyzz_data)
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = [ "qy_name", "ryname","ryzz"]
    wirteDataToExcel(outfilename+"ryxx_" + tablenamehouzui + ".xlsx", "Sheet1", columnRows, qyzz_data)
    print("ryzz  to   excel  sucess")


if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\云南省企业列表_20200820.xlsx"
    outfilename = root_dir + r"\get_jst_qyyj\建设通企业业绩_数据准备_贺家斌_"
    url = "https://passport.cbi360.net/login?url=https%3A%2F%2Fwww.cbi360.net%2Fhyjd%2F20200528%2F203181.html"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    driver=open(url)
    zhiding_qy_yj_data = []
    qyyj_data = []
    ryzz_data = []
    s = input("input  your  unm: ")
    if int(s) == 1:
        # 得到导入企业的链接
        get_zhiding_qy_yj(driver,outfilename,sheet1data,zhiding_qy_yj_data)

        # datalist=[['广州', '广州敏城建设工程有限公司', 'https://hhb.cbi360.net/sg_47307/', '726']]


        # 得到导入企业的全部企业业绩
        # max_ye指定最多查询建设通多少页的业绩
        get_qyzz_detail(driver,outfilename,zhiding_qy_yj_data,ryzz_data)

        # print(zhiding_qy_yj_data)
        # 得到导入企业的全部人员信息
        # get_ryxx_detail(driver,outfilename, zhiding_qy_yj_data, ryxx_data)