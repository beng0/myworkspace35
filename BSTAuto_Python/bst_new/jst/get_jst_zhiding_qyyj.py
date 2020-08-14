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


# 得到导入企业的链接
def get_zhiding_qy_yj(driver,outfilename,sheet1data,zhiding_qy_yj_data):
    # 选择企业业绩
    driver.find_element_by_xpath('//*[@id="ul_search_list_menu"]/li[1]/a').click()
    sleep(3)

    for row in sheet1data:
        qyname = row[0].strip()
        driver.find_element_by_xpath('//*[@id="txt_company_name"]').clear()
        driver.find_element_by_xpath('//*[@id="txt_company_name"]').send_keys(qyname)
        driver.find_element_by_xpath('//*[@id="btn_search_company"]').click()
        sleep(3)

        qy_name = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/h2/a/em').text.strip()
        if qy_name[-3:] == "已认证":
            qy_name = qy_name[0:-4]

        href = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/h2/a').get_attribute('href')
        zbsl = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[2]/dl/dd[1]/a/strong').text.strip()
        tmp = [qy_name,href,zbsl]
        zhiding_qy_yj_data.append(tmp)
        # print(zhiding_qy_yj_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["qy_name", "href", "zbsl"]
    wirteDataToExcel(outfilename+'href_' + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, zhiding_qy_yj_data)
    print("qyhref  to   excel  sucess")




# 得到相应企业的全部中标业绩
def get_qyyj_detail(driver,outfilename,zhiding_qy_yj_data,qyyj_data):
    for qy_name, href, zbsl in zhiding_qy_yj_data:
        driver.get(href)
        print(href)
        sleep(3)

        # 计算该企业中标有几页数据
        zbsl_count = int(zbsl)
        if zbsl_count > 15:
            if zbsl_count % 15 == 0:
                total_ye = zbsl_count // 15
            else:
                total_ye = zbsl_count // 15 + 1
        else:
            total_ye = 1
        print("总页数：" + str(total_ye))
        if total_ye > 8: total_ye = 8

        for gotoyema in range(1, total_ye + 1):
            print("第" + str(gotoyema) + "页")
            if gotoyema == 2:
                locator = (By.XPATH, '/html/body/div[7]/div[4]/div[2]/div/a')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator)).click()
                sleep(3)
            elif gotoyema > 2:
                locator2 = (By.XPATH, '/html/body/div[7]/div[4]/div[2]/div/div/div/input[1]')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                zhuandao_loc = (By.XPATH, '/html/body/div[7]/div[4]/div[2]/div/div/div/input[2]')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
                sleep(3)

            ggname = ' '
            diqu = ' '
            xmjl = ' '
            zbtime = ' '
            zbly = ' '
            content_list = driver.find_elements_by_xpath('/html/body/div[7]/div[4]/div[2]/ul/li')[1:]
            # print(','.join(str(s) for s in content_list if s not in [None]))
            for content in content_list:
                if content.find_element_by_xpath('./div[2]/h2/a'):
                    ggname = content.find_element_by_xpath('./div[2]/h2/a').text.strip()

                if content.find_element_by_xpath('./div[3]'):
                    diqu = content.find_element_by_xpath('./div[3]').text.strip()

                if content.find_element_by_xpath('./div[4]'):
                    if "--" not in content.find_element_by_xpath('./div[4]').text:
                        xmjl = content.find_element_by_xpath('./div[4]/a').text.strip()

                if content.find_element_by_xpath('./div[6]'):
                    zbtime = content.find_element_by_xpath('./div[6]').text.strip()

                if content.find_element_by_xpath('./div[7]/a'):
                    zbly = content.find_element_by_xpath('./div[7]/a').text.strip()

                tmp = [href, qy_name, ggname, diqu, xmjl, zbtime, zbly]
                qyyj_data.append(tmp)
                print(qyyj_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href", "zhongbiaoren", "ggname", "diqu", "xmjl", "zbtime", "zbly"]
    wirteDataToExcel(outfilename+"qyyj_" + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, qyyj_data)
    print("qyyj  to   excel  sucess")


# 得到相应企业的全部人员信息
def get_ryxx_detail(driver,outfilename,zhiding_qy_yj_data,ryxx_data):
    for qy_name, href,zbsl in zhiding_qy_yj_data:
        driver.get(href)
        print(href)
        sleep(3)

        ry_count = int((driver.find_element_by_xpath('//*[@id="newrisk"]/li[4]/h3/a/span').text.strip())[1:-1])
        if ry_count == 0: break

        # 点击企业人员
        driver.find_element_by_xpath('//*[@id="newrisk"]/li[4]/h3/a').click()
        sleep(3)


        # 计算该企业中有几页人员数据
        if ry_count > 15:
            if ry_count % 15 == 0:
                total_ye = ry_count // 15
            else:
                total_ye = ry_count // 15 + 1
        else:
            total_ye = 1
        print("总页数：" + str(total_ye))
        if total_ye > 8: total_ye = 8

        cur_ye = driver.find_element_by_xpath('/html/body/div[7]/div[4]/div[2]/div/div/div/label').text.strip()
        print(cur_ye)
        for gotoyema in range(1, total_ye + 1):
            print("第" + str(gotoyema) + "页")
            if cur_ye != gotoyema:
                locator2 = (By.XPATH, '/html/body/div[7]/div[4]/div[2]/div/div/div/input[1]')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                driver.find_element_by_xpath('/html/body/div[7]/div[4]/div[2]/div/div/div/input[2]').click()
                sleep(3)

            name = ' '
            zclb = ' '
            zsbh = ' '
            zyyzh = ' '
            sfz = ' '
            yxq = ' '
            content_list = driver.find_elements_by_xpath('/html/body/div[7]/div[4]/div[2]/ul/li')[1:]
            # print(','.join(str(s) for s in content_list if s not in [None]))
            for content in content_list:
                if content.find_element_by_xpath('./div[2]/h2/a'):
                    name = content.find_element_by_xpath('./div[2]/h2/a').text.strip()

                if content.find_element_by_xpath('./div[3]/h2'):
                    zclb = content.find_element_by_xpath('./div[3]/h2').text.strip()

                if content.find_element_by_xpath('./div[4]/a'):
                    zsbh = content.find_element_by_xpath('./div[4]/a').text.strip()

                if content.find_element_by_xpath('./div[5]'):
                    zyyzh = content.find_element_by_xpath('./div[5]').text.strip()

                if content.find_element_by_xpath('./div[6]'):
                    sfz = content.find_element_by_xpath('./div[6]').text.strip()

                if content.find_element_by_xpath('./div[7]'):
                    yxq = content.find_element_by_xpath('./div[7]').text.strip()

                tmp = [href, qy_name, name, zclb, zsbh, zyyzh, sfz,yxq]
                ryxx_data.append(tmp)
                print(ryxx_data)
    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href", "qy_name", "name", "zclb", "zsbh", "zyyzh", "sfz", "yxq"]
    wirteDataToExcel(outfilename+"ryxx_" + tablenamehouzui + ".xlsx", "Sheet1", columnRows, ryxx_data)
    print("ryxx  to   excel  sucess")

if  __name__ == '__main__':
    infilename = r"D:\SVN\业务数据维护\企业业绩\数据准备\企业抽取.xlsx"
    outfilename = r"D:\SVN\业务数据维护\企业业绩\数据准备\广东建设通企业业绩_数据准备_胡金花"
    url = "https://passport.cbi360.net/login?url=https%3A%2F%2Fwww.cbi360.net%2Fhyjd%2F20200528%2F203181.html"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    driver=open(url)
    zhiding_qy_yj_data = []
    qyyj_data = []
    ryxx_data = []
    s = input("input  your  unm: ")
    if int(s) == 1:
        # 得到导入企业的链接
        get_zhiding_qy_yj(driver,outfilename,sheet1data,zhiding_qy_yj_data)

        # datalist=[['广州', '广州敏城建设工程有限公司', 'https://hhb.cbi360.net/sg_47307/', '726']]


        # 得到导入企业的全部中标业绩
        get_qyyj_detail(driver,outfilename,zhiding_qy_yj_data,qyyj_data)

        print(zhiding_qy_yj_data)
        # 得到导入企业的全部人员信息
        get_ryxx_detail(driver,outfilename, zhiding_qy_yj_data, ryxx_data)