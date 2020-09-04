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

        qy_name = driver.find_element_by_css_selector('.table>div:nth-child(2)>div:nth-child(1)>ul>li:nth-child(2)>a>em').text.strip()
        if qy_name[-3:] == "已认证":
            qy_name = qy_name[0:-4]
        # https://hhb.cbi360.net/sg_549433/
        href = driver.find_element_by_css_selector('.table>div:nth-child(2)>div:nth-child(1)>ul>li:nth-child(2)>a').get_attribute('href')
        # print(href)
        zbsl = driver.find_element_by_css_selector('.table>div:nth-child(2)>div:nth-child(1)>dl>dd>a>strong').text.strip()
        tmp = [qy_name,href,zbsl]
        zhiding_qy_yj_data.append(tmp)
        # print(zhiding_qy_yj_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["qy_name", "href", "zbsl"]
    wirteDataToExcel(outfilename+'href_' + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, zhiding_qy_yj_data)
    print("qyhref  to   excel  sucess")




# 得到相应企业的全部中标业绩
def get_qyyj_detail(driver,outfilename,zhiding_qy_yj_data,qyyj_data,max_ye):
    for qy_name, href, zbsl in zhiding_qy_yj_data:
        driver.get(href)
        driver.maximize_window()
        # print(href)
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
        if total_ye > max_ye: total_ye = max_ye
        print("爬取页数："+str(max_ye))

        for gotoyema in range(1, total_ye + 1):
            # print("第" + str(gotoyema) + "页")
            if gotoyema == 1:
                locator = (By.XPATH, '//a[text()="点击查看更多>>"]')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator)).click()
                sleep(3)

            elif gotoyema > 1:
                locator2 = (By.XPATH, '//input[@class="jumpnum"]')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                zhuandao_loc = (By.XPATH, '//a[text()="转到"]')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
                sleep(3)

            ggname = ' '
            diqu = ' '
            xmjl = ' '
            zbtime = ' '
            zbly = ' '
            content_list = driver.find_elements_by_xpath('//div[@class="table"]/div/dl')
            # print(','.join(str(s) for s in content_list if s not in [None]))
            for content in content_list:
                if content.find_element_by_xpath('./dd[2]//a'):
                    ggname = content.find_element_by_xpath('./dd[2]//a').text.strip()

                if content.find_element_by_xpath('./dd[3]'):
                    diqu = content.find_element_by_xpath('./dd[3]').text.strip()

                if content.find_element_by_xpath('./dd[4]/a'):
                    if  content.find_element_by_xpath('./dd[4]/a').text:
                        xmjl = content.find_element_by_xpath('./dd[4]/a').text.strip()

                if content.find_element_by_xpath('./dd[6]'):
                    zbtime = content.find_element_by_xpath('./dd[6]').text.strip()

                if content.find_element_by_xpath('./dd[7]/a'):
                    zbly = content.find_element_by_xpath('./dd[7]/a').text.strip()

                tmp = [href, qy_name, ggname, diqu, xmjl, zbtime, zbly]
                qyyj_data.append(tmp)
                # print(qyyj_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href", "zhongbiaoren", "ggname", "diqu", "xmjl", "zbtime", "zbly"]
    wirteDataToExcel(outfilename+"qyyj_" + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, qyyj_data)
    print("qyyj  to   excel  sucess")
    print("企业业绩文件存放在"+outfilename+"qyyj_" + tablenamehouzui + ".xlsx")


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
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename = root_dir + r"\qy_list\企业抽取_模板.xlsx"
    outfilename = root_dir + r"\get_jst_qyyj\建设通企业业绩_数据准备_贺家斌_"
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
        # max_ye指定最多查询建设通多少页的业绩
        get_qyyj_detail(driver,outfilename,zhiding_qy_yj_data,qyyj_data,max_ye=6)

        # print(zhiding_qy_yj_data)
        # 得到导入企业的全部人员信息
        # get_ryxx_detail(driver,outfilename, zhiding_qy_yj_data, ryxx_data)