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
import os

def  open(url):
    # 代理IP
    # driver = get_driver_moni_ip()
    # driver.get("http://httpbin.org/ip")
    # print(driver.page_source)

    driver = webdriver.Chrome()
    driver.get(url)
    return driver

# 得到企业和对应的链接,循环所有的市
def get_jst_qyyj(driver,datalist,sheng,shenfen_xpath,total_ye):
    # 得到企业和对应的链接
    for gotoyema in range(1, total_ye):
        # 选择企业业绩
        driver.find_element_by_xpath('//*[@id="ul_search_list_menu"]/li[1]/a').click()

        # 选择省份
        driver.find_element_by_xpath(shenfen_xpath).click()

        shi_count = 2
        all_shi_list=[]

        all_shi_list = driver.find_elements_by_xpath('//*[@id="div_city"]/a')[5:]
        print(','.join(str(s) for s in all_shi_list if s not in [None]))
        for shis in all_shi_list:
            try:
                print(shi_count)
                driver.get("https://hhb.cbi360.net/companysoso/")
                # 选择省份
                driver.find_element_by_xpath(shenfen_xpath).click()
                sleep(3)
                shi_loc=(By.XPATH,'//*[@id="div_city"]/a[' + str(shi_count) + ']')
                WebDriverWait(driver,30).until(EC.visibility_of_element_located(shi_loc))
                shi_text = driver.find_element_by_xpath('//*[@id="div_city"]/a[' + str(shi_count) + ']').text.strip()
                print(shi_text)
            except StaleElementReferenceException as msg:
                print(msg)
                driver.get("https://hhb.cbi360.net/companysoso/")
                # 选择省份
                driver.find_element_by_xpath(shenfen_xpath).click()
                sleep(3)
                shi_loc = (By.XPATH, '//*[@id="div_city"]/a[' + str(shi_count) + ']')
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located(shi_loc))
                shi_text = driver.find_element_by_xpath('//*[@id="div_city"]/a[' + str(shi_count) + ']').text.strip()
                print(shi_text)

            # 选择市
            driver.find_element_by_xpath('//*[@id="div_city"]/a[' + str(shi_count) + ']').click()
            sleep(3)

            # 点击搜索按钮
            driver.find_element_by_xpath('//*[@id="btn_search_company"]').click()
            sleep(3)

            # 获得当前页码
            cur_yema = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div/div/div/label').text
            # 翻页
            if int(cur_yema) != int(gotoyema):
                driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div/div/div/input[1]').clear()
                driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div/div/div/input[1]').send_keys(
                    str(gotoyema))
                sleep(3)

            loc = (By.XPATH, '/html/body/div[8]/div[2]/div[2]/ul/li')
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(loc))

            href = ''
            entname2 = ''
            zbsl = ''
            qyyj_list = driver.find_elements_by_xpath('/html/body/div[8]/div[2]/div[2]/ul/li')
            for content in qyyj_list:
                if content.find_element_by_xpath('./div[2]/div[1]/h2/a'):
                    href = content.find_element_by_xpath('./div[2]/div[1]/h2/a').get_attribute('href')
                print(href)

                if content.find_element_by_xpath('./div[2]/div[1]/h2/a'):
                    entname = content.find_element_by_xpath('./div[2]/div[1]/h2/a').text.strip()
                    if entname[-3:] == "已认证":
                        entname2 = entname[0:-4]
                    else:
                        entname2 = entname
                print(entname2)

                if content.find_element_by_xpath('./div[2]/div[2]/dl/dd[1]/a/strong'):
                    zbsl = content.find_element_by_xpath('./div[2]/div[2]/dl/dd[1]/a/strong').text.strip()
                print(zbsl)

                tmp = [sheng,shi_text, entname2, href, zbsl]
                datalist.append(tmp)
                print(datalist)
                break  # 有break就一个市拿一个企业，没有就拿整页
            shi_count += 1
            if shi_count > 6 : break   #只取5家企业
        print("共获取" + str(total_ye - 1) + "页，已完成" + str(gotoyema) + "页")


def get_zhiding_qy_yj(driver,sheet1data,zhiding_qy_yj_data):
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
        href = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/h2/a').get_attribute('href')
        tmp = [qy_name,href]
        zhiding_qy_yj_data.append(tmp)
        print(zhiding_qy_yj_data)






# 得到相应企业的全部中标业绩
def get_qyyj_detail(driver,datalist,data):
        for sheng,shi_text,entname,href,zbsl in datalist:
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
                        if   "--" not in content.find_element_by_xpath('./div[4]').text:
                            xmjl = content.find_element_by_xpath('./div[4]/a').text.strip()

                    if content.find_element_by_xpath('./div[6]'):
                        zbtime = content.find_element_by_xpath('./div[6]').text.strip()

                    if content.find_element_by_xpath('./div[7]/a'):
                        zbly = content.find_element_by_xpath('./div[7]/a').text.strip()

                    tmp = [href, sheng,shi_text, entname, ggname, diqu, xmjl, zbtime, zbly]
                    data.append(tmp)
                    print(data)


if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data/qyyj/'
    outfilename = root_dir+"广东_云南_山西建设通企业业绩_胡金花_"

    url = "https://passport.cbi360.net/login?url=https%3A%2F%2Fwww.cbi360.net%2Fhyjd%2F20200528%2F203181.html"
    # 选择广东省份
    guangdong_shenfen_xpath = '//*[@id="div_province"]/a[20]'
    # 选择云南省份
    yunnan_shenfen_xpath = '//*[@id="div_province"]/a[25]'
    # 选择山西省份
    shanxi_shenfen_xpath = '//*[@id="div_province"]/a[8]'

    shenfen_list=[["广东省",guangdong_shenfen_xpath],["云南省",yunnan_shenfen_xpath],["山西省",shanxi_shenfen_xpath]]
    total_ye = 2
    driver=open(url)

    datalist = []
    data = []
    s = input("input  your  unm: ")
    if int(s) == 1:
        for sheng,shenfen_xpath in shenfen_list:

            # 得到页面随机企业和对应的链接
            get_jst_qyyj(driver,datalist,sheng,shenfen_xpath,total_ye)


        # 得到相应企业的全部中标业绩
        get_qyyj_detail(driver,datalist,data)



        tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 到数据到excle中
        columnRows = ["sheng","shi_text", "entname", "href", "zbsl"]
        wirteDataToExcel(outfilename+"href_" + tablenamehouzui + ".xlsx", "qy_href", columnRows, datalist)

        tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 到数据到excle中
        columnRows = ["href","sheng", "shi", "zhongbiaoren", "ggname", "diqu", "xmjl", "zbtime", "zbly"]
        wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "qyyj", columnRows, data)