#coding=utf-8
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


def read_excel_data(infilename):
    jy_qyyj_data =[]
    # 读取标事通企业业绩
    all_sheet_data1 = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    jy_qyyj_data = all_sheet_data1[0][1][1:]
    # print(jy_qyyj_data)
    return jy_qyyj_data



# 得到企业和对应的链接,循环所有的市
def get_jst_qyyj(driver,datalist,sheng,shenfen_xpath,total_ye):
    # 得到企业和对应的链接
    for gotoyema in range(1, total_ye):
        # 选择企业业绩
        driver.find_element_by_xpath('//a[text()="查企业"]').click()

        # 选择省份
        driver.find_element_by_xpath(shenfen_xpath).click()

        shi_count = 2
        all_shi_list=[]
        shi_xpath ='//div[text()="企业注册市："]/following-sibling::div[1]/a'
        all_shi_list = driver.find_elements_by_xpath(shi_xpath)[1:]
        print(','.join(str(s) for s in all_shi_list if s not in [None]))
        for shis in all_shi_list:
            try:
                print(shi_count)
                driver.get("https://hhb.cbi360.net/companysoso/")
                # 选择省份
                driver.find_element_by_xpath(shenfen_xpath).click()
                sleep(3)
                shi_loc=(By.XPATH,shi_xpath+'[' + str(shi_count) + ']')
                WebDriverWait(driver,30).until(EC.visibility_of_element_located(shi_loc))
                shi_text = driver.find_element_by_xpath(shi_xpath+'[' + str(shi_count) + ']').text.strip()
                print(shi_text)
            except StaleElementReferenceException as msg:
                print(msg)
                driver.get("https://hhb.cbi360.net/companysoso/")
                # 选择省份
                driver.find_element_by_xpath(shenfen_xpath).click()
                sleep(3)
                shi_loc = (By.XPATH, shi_xpath+'[' + str(shi_count) + ']')
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located(shi_loc))
                shi_text = driver.find_element_by_xpath(shi_xpath+'[' + str(shi_count) + ']').text.strip()
                print(shi_text)

            # 选择市
            driver.find_element_by_xpath(shi_xpath+'[' + str(shi_count) + ']').click()
            sleep(3)

            # 点击搜索按钮
            driver.find_element_by_xpath('//span[text()="查询"]').click()
            sleep(3)

            # 获得当前页码
            cur_yema = driver.find_element_by_xpath('//*[@id="nav-company"]/div/div[2]/div[2]/div[16]/ul/li[5]/a').text
            # 翻页
            if int(cur_yema) != int(gotoyema):
                driver.find_element_by_xpath('//*[@id="nav-company"]/div/div[2]/div[2]/div[16]/ul/li[12]/input').clear()
                driver.find_element_by_xpath('//*[@id="nav-company"]/div/div[2]/div[2]/div[16]/ul/li[12]/input').send_keys(
                    str(gotoyema))
                sleep(3)

            loc = (By.XPATH, '//div[contains(text(),"共找到")]/../../following-sibling::div[1]/div[@class="table-con"]')
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(loc))

            href = ''
            entname2 = ''
            zbsl = ''
            qyyj_list = driver.find_elements_by_xpath('//div[contains(text(),"共找到")]/../../following-sibling::div[1]/div[@class="table-con"]')
            for content in qyyj_list:
                if content.find_element_by_xpath('./ul/li[2]/a'):
                    href = content.find_element_by_xpath('./ul/li[2]/a').get_attribute('href')
                print(href)

                if content.find_element_by_xpath('./ul/li[2]/a'):
                    entname = content.find_element_by_xpath('./ul/li[2]/a').text.strip()
                    if entname[-3:] == "已认证":
                        entname2 = entname[0:-4]
                    else:
                        entname2 = entname
                print(entname2)

                if content.find_element_by_xpath('.dl/dd[1]/a/strong'):
                    zbsl = content.find_element_by_xpath('.dl/dd[1]/a/strong').text.strip()
                print(zbsl)

                tmp = [sheng,shi_text, entname2, href, zbsl]
                datalist.append(tmp)
                print(datalist)
                break  # 有break就一个市拿一个企业，没有就拿整页
            shi_count += 1
            if shi_count > 6 : break   #只取5家企业
        print("共获取" + str(total_ye - 1) + "页，已完成" + str(gotoyema) + "页")



# 得到企业和对应的链接,循环所有的市
def get_jst_qyyj2(driver,datalist,sheng,shenfen_xpath,total_ye):
    # 选择企业业绩
    driver.find_element_by_xpath('//a[text()="查企业"]').click()
    # 选择省份
    driver.find_element_by_xpath(shenfen_xpath).click()

    # 点击搜索按钮
    driver.find_element_by_xpath('//span[text()="查询"]').click()
    sleep(3)

    href = ''
    entname2 = ''
    zbsl = ''
    qyyj_list = driver.find_elements_by_xpath('//div[contains(text(),"共找到")]/../../following-sibling::div[1]/div[@class="table-con"]')[:5]
    for content in qyyj_list:
        if content.find_element_by_xpath('./ul/li[2]/a'):
            href = content.find_element_by_xpath('./ul/li[2]/a').get_attribute('href')
        print(href)

        if content.find_element_by_xpath('./ul/li[2]/a'):
            entname = content.find_element_by_xpath('./ul/li[2]/a').text.strip()
            if entname[-3:] == "已认证":
                entname2 = entname[0:-4]
            else:
                entname2 = entname
        print(entname2)

        if content.find_element_by_xpath('./dl/dd[1]/a/strong'):
            zbsl = content.find_element_by_xpath('./dl/dd[1]/a/strong').text.strip()
        print(zbsl)

        tmp = [sheng, "shi", entname2, href, zbsl]
        datalist.append(tmp)
        print(datalist)








def get_zhiding_qy_yj(driver,sheet1data,zhiding_qy_yj_href):
    loc = (By.XPATH,'//*[@id="jst-nav"]/a')
    WebDriverWait(driver,10).until(EC.visibility_of_element_located(loc))
    element = driver.find_element_by_xpath('//*[@id="jst-nav"]/a')
    ActionChains(driver).move_to_element(element).perform()
    cqy_loc =(By.XPATH,'//*[@id="jst-nav"]//label[text()="查企业"]')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(cqy_loc))
    cqy_element = driver.find_element_by_xpath('//*[@id="jst-nav"]//label[text()="查企业"]')
    ActionChains(driver).move_to_element(cqy_element).perform()
    cqy_element.click()
    sleep(5)

    qyname_xpath='//input[@placeholder="请输入企业名称关键字"]'
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,qyname_xpath)))


    for row in sheet1data:
        qyname = row[1].strip()
        driver.find_element_by_xpath(qyname_xpath).clear()
        driver.find_element_by_xpath(qyname_xpath).send_keys(qyname)
        driver.find_element_by_xpath('//*[@id="nav-company"]//span[text()="查询"]').click()
        sleep(3)

        data_href_list= driver.find_elements_by_xpath('//*[@id="nav-company"]/div/div[2]/div[2]/div[@class="table-con"]')
        for content in data_href_list:
            tmp = []
            qy_name = content.find_element_by_xpath('./ul/li[2]/a').text.strip()
            print("列表中的qy_name:   ",qy_name)
            print("excel中的qyname:   ",qyname)
            if qy_name == qyname:
                href = content.find_element_by_xpath('./ul/li[2]/a').get_attribute('href')
                tmp = [qy_name,href]
            print(tmp)
            if tmp:
                zhiding_qy_yj_href.append(tmp)
            print(zhiding_qy_yj_href)






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
                    locator = (By.XPATH, '//a[text()="点击查看更多>>"]')
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator)).click()
                    sleep(3)
                elif gotoyema > 2:
                    locator2 = (By.XPATH, '//*[@id="__layout"]/div/div[4]/div[2]/div/div[3]/div[3]/div/div/div/ul/li[12]/input')
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                    zhuandao_loc = (By.XPATH, '//a[text()="转到"]')
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
                    sleep(3)


                ggname = ' '
                diqu = ' '
                xmjl = ' '
                zbtime = ' '
                zbly_href = ' '
                zbly = ' '
                content_list = driver.find_elements_by_xpath('//dd[text()="来源"]/../following-sibling::div[1]/dl')
                # print(','.join(str(s) for s in content_list if s not in [None]))
                for content in content_list:
                    if content.find_element_by_xpath('./dd[2]/h2/a'):
                        ggname = content.find_element_by_xpath('./dd[2]/h2/a').text.strip()

                    if content.find_element_by_xpath('./dd[3]'):
                        diqu = content.find_element_by_xpath('./dd[3]').text.strip()

                    if content.find_element_by_xpath('./dd[4]'):
                        if   "--" not in content.find_element_by_xpath('./dd[4]').text:
                            xmjl = content.find_element_by_xpath('./dd[4]/a').text.strip()

                    if content.find_element_by_xpath('./dd[6]'):
                        zbtime = content.find_element_by_xpath('./dd[6]').text.strip()

                    if content.find_element_by_xpath('./dd[7]/a'):
                        zbly = content.find_element_by_xpath('./dd[7]/a').text.strip()

                    if content.find_element_by_xpath('./dd[7]/a'):
                        zbly_href = content.find_element_by_xpath('./dd[7]/a').get_attribute("href").strip()
                    tmp = [href, sheng,shi_text, entname, ggname, diqu, xmjl, zbtime,zbly_href,zbly]
                    data.append(tmp)
                    print(data)



# 得到相应企业的全部中标业绩
def get_qyyj_detail2(driver,datalist, zhiding_qy_yj_data_zb,zhiding_qy_yj_data_sk,zhiding_qy_yj_data_qg,zhiding_qy_qyzz,zhiding_qy_ryzz,outfilename_qyyj_jst_zb,outfilename_qyyj_jst_sk,outfilename_qyyj_jst_qg,outfilename_qyzz_jst,outfilename_ryzz_jst):
    for entname, href in datalist:
        driver.get(href)
        print(href)
        sleep(3)
        zbsl = driver.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/h3').text
        zbsl2 = zbsl.split(' ')
        zbsl_count = int(zbsl2[-1])
        print(zbsl_count)
        if zbsl_count > 0:
            ye_count = total_yema(zbsl_count)
            get_detail_zb_data(href, entname, ye_count, zhiding_qy_yj_data_zb)

        # 四库一平台
        skyt_xpath='//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/h3'
        skyt = driver.find_element_by_xpath(skyt_xpath).text
        skyt2 = skyt.split(' ')
        skyt_count = int(skyt2[-1])
        print(skyt_count)
        if skyt_count > 0:
            driver.get(href)
            locator333 = (By.XPATH, skyt_xpath)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator333))

            driver.find_element_by_xpath(skyt_xpath).click()
            sleep(3)
            ye_count = total_yema(skyt_count)
            get_detail_sk_data(href, entname, ye_count, zhiding_qy_yj_data_sk)

        # qg_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/h3'
        # qg = driver.find_element_by_xpath(qg_xpath).text
        # qg2 = qg.split(' ')
        # qg_count = int(qg2[-1])
        # print(qg_count)
        # if qg_count > 0:
        #     driver.find_element_by_xpath(qg_xpath).click()
        #     sleep(3)
        #     ye_count = total_yema(qg_count)
        #     get_detail_qg_data(href, entname, ye_count, zhiding_qy_yj_data_qg)

        #获取人员资质
        get_ryzz(driver,entname,href,zhiding_qy_ryzz)
        #获取企业资质
        get_qyzz(driver, entname, href, zhiding_qy_qyzz)


        # jst 中标公示
        if zhiding_qy_yj_data_zb:
            tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
            columnRows = ["href", "zhongbiaoren", "ggname", "diqu", "xmjl", "je", "zbtime", "zbly_href", "zbly"]
            wirteDataToExcel(outfilename_qyyj_jst_zb + tablenamehouzui + ".xlsx", "qyyj", columnRows,
                                 zhiding_qy_yj_data_zb)
            print("zhiding_qy_yj_data_zb  to excel")

        # jst 四库一平台业绩
        if zhiding_qy_yj_data_sk:
            tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
            columnRows = ["href", "zhongbiaoren", "ggname", "项目类型", "工程用途", "je(中标/合同/竣工)", "time(中标/合同/竣工)",
                              "可截图栏目", "xmjl", "ggname_href"]
            wirteDataToExcel(outfilename_qyyj_jst_sk + tablenamehouzui + ".xlsx", "qyyj", columnRows,
                                 zhiding_qy_yj_data_sk)
            print("zhiding_qy_yj_data_sk  to excel")

        # jst  全国公路建设市场业绩
        if zhiding_qy_yj_data_qg:
            tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
            columnRows = ["href", "zhongbiaoren", "ggname", "diqu", "xmjl", "合同价格", "交工时间", "zbly_href", "zbly"]
            wirteDataToExcel(outfilename_qyyj_jst_qg + tablenamehouzui + ".xlsx", "qyyj", columnRows,zhiding_qy_yj_data_qg)
            print("zhiding_qy_yj_data_qg  to excel")

        # jst  ryzz
        if zhiding_qy_yj_data_qg:
            tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
            columnRows = ["href", "entname", "name", "lb_zhuanye", "zsh", "zsh", "zyyzh", "sfz", "yxq"]
            wirteDataToExcel(outfilename_ryzz_jst + tablenamehouzui + ".xlsx", "qyyj", columnRows,zhiding_qy_ryzz)
            print("zhiding_qy_ryzz  to excel")

        # jst qyzz
        if zhiding_qy_yj_data_qg:
            tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
            columnRows = ["href", "entname", "qyzz_name", "start_time", "end_time"]
            wirteDataToExcel(outfilename_qyzz_jst + tablenamehouzui + ".xlsx", "qyyj", columnRows,zhiding_qy_qyzz)
            print("zhiding_qy_qyzz  to excel")

    # return zhiding_qy_yj_data_zb, zhiding_qy_yj_data_sk, zhiding_qy_yj_data_qg


def get_ryzz(driver,entname,href,zhiding_qy_ryzz):
    driver.get(href)
    locator33 = (By.XPATH, '//*[@id="nav-list"]/div[4]/h3/span[2]')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator33))

    ry_count = driver.find_element_by_xpath('//*[@id="nav-list"]/div[4]/h3/span[2]').text.strip()
    ry_count2=int(ry_count)
    print("ry_count2:  ",ry_count2)
    if ry_count2>0:
        driver.find_element_by_xpath('//*[@id="nav-list"]/div[4]/h3/span[1]').click()
        sleep(3)
        ye_count = total_yema(ry_count2)
        ye_input_xpath2 ='//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[5]/div/div[2]/div[4]/div[1]/div/slot/div/input'
        go_to_button_xpath='//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[5]/div/div[2]/div[4]/div[1]/div/slot/button/span'
        for gotoyema in range(1, ye_count + 1):
            if gotoyema > 1:
                print("第" + str(gotoyema) + "页")
                locator2 = (By.XPATH, ye_input_xpath2)

                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                zhuandao_loc = (By.XPATH, go_to_button_xpath)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
                sleep(3)

            name=''
            lb_zhuanye = ''
            zsh = ''
            zyyzh = ''
            sfz = ''
            yxq = ''

            data_list=driver.find_elements_by_xpath('//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[5]/div/div[2]/div[3]/div/div[3]/table/tbody/tr')
            for content  in data_list:
                sleep(3)
                if content.find_element_by_xpath('./td[2]/div/div/h2/a'):
                    name = content.find_element_by_xpath('./td[2]/div/div/h2/a').text.strip()
                if content.find_element_by_xpath('./td[3]/div'):
                    lb_zhuanye = content.find_element_by_xpath('./td[3]/div').text.strip()
                if content.find_element_by_xpath('./td[4]/div/div/a'):
                    zsh = content.find_element_by_xpath('./td[4]/div/div/a').text.strip()
                if content.find_element_by_xpath('./td[5]/div/div'):
                    zyyzh = content.find_element_by_xpath('./td[5]/div/div').text.strip()
                if content.find_element_by_xpath('./td[6]/div/div'):
                    sfz = content.find_element_by_xpath('./td[6]/div/div').text.strip()
                if content.find_element_by_xpath('./td[7]/div/div'):
                    yxq = content.find_element_by_xpath('./td[7]/div/div').text.strip()
                tmp=[href,entname,name,lb_zhuanye,zsh,zyyzh,sfz,yxq]
                zhiding_qy_ryzz.append(tmp)
                print(zhiding_qy_ryzz)



def get_qyzz(driver,entname,href,zhiding_qy_qyzz):
    driver.get(href)
    locator3 = (By.XPATH, '//*[@id="nav-list"]/div[6]/h3/span[2]')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator3))

    qy_count = driver.find_element_by_xpath('//*[@id="nav-list"]/div[6]/h3/span[2]').text.strip()
    qy_count2=int(qy_count)
    print("qy_count  ",qy_count)
    if qy_count2>0:

        driver.find_element_by_xpath('//*[@id="nav-list"]/div[6]/h3/span[1]').click()
        sleep(3)
        ye_count = total_yema(qy_count2)
        ye_input_xpath2 ='//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[7]/div/div[3]/div[2]/div/slot/div/input'
        go_to_button_xpath='//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[7]/div/div[3]/div[2]/div/slot/button/span'
        for gotoyema in range(1, ye_count + 1):
            if gotoyema > 1:
                print("第" + str(gotoyema) + "页")
                locator2 = (By.XPATH, ye_input_xpath2)

                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                zhuandao_loc = (By.XPATH, go_to_button_xpath)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
                sleep(3)

            qyzz_name=''
            start_time = ''
            end_time = ''

            data_list=driver.find_elements_by_xpath('//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[7]/div/div[3]/div[1]/div/div[3]/table/tbody/tr')
            for content  in data_list:
                sleep(3)
                if content.find_element_by_xpath('./td[2]/div/div/span'):
                    qyzz_name = content.find_element_by_xpath('./td[2]/div/div/span').text.strip()
                if content.find_element_by_xpath('./td[3]/div/div'):
                    start_time = content.find_element_by_xpath('./td[3]/div/div').text.strip()
                if content.find_element_by_xpath('./td[4]/div/div'):
                    end_time = content.find_element_by_xpath('./td[4]/div/div').text.strip()
                tmp=[href,entname,qyzz_name,start_time,end_time]
                zhiding_qy_qyzz.append(tmp)
                print(zhiding_qy_qyzz)





def total_yema(zbsl):
    zbsl_count = int(zbsl)
    if zbsl_count > 10:
        if zbsl_count % 10 == 0:
            total_ye = zbsl_count // 10
        else:
            total_ye = zbsl_count // 10 + 1
    else:
        total_ye = 1
    print("总页数：" + str(total_ye))
    # if total_ye > 8: total_ye = 8
    return total_ye


#                     (href, entname, ye_count, zhiding_qy_yj_data_zb)
def get_detail_zb_data(href, entname, ye_count,zhiding_qy_yj_data_zb):
    ye_input_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[2]/div/div/slot/div/input'
    go_to_button_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[2]/div/div/slot/button/span'
    data_list_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div/div[3]/table/tbody/tr'

    for gotoyema in range(1, ye_count + 1):
        if gotoyema > 1:
            print("第" + str(gotoyema) + "页")
            locator2 = (By.XPATH,ye_input_xpath)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

            zhuandao_loc = (By.XPATH,go_to_button_xpath)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
            sleep(3)

        ggname = ' '
        diqu = ' '
        xmjl = ' '
        je = ' '
        zbtime = ' '
        zbly_href = ' '
        zbly = ' '
        content_list = driver.find_elements_by_xpath(data_list_xpath)
        # print(','.join(str(s) for s in content_list if s not in [None]))
        for content in content_list:
            sleep(3)
            if content.find_element_by_xpath('./td[2]/div/h2/a'):
                ggname = content.find_element_by_xpath('./td[2]/div/h2/a').text.strip()

            if content.find_element_by_xpath('./td[3]/div/span'):
                diqu = content.find_element_by_xpath('./td[3]/div/span').text.strip()

            if content.find_element_by_xpath('./td[4]/div/a'):
                # if "--" not in content.find_element_by_xpath('./td[4]/div/a').text:
                xmjl = content.find_element_by_xpath('./td[4]/div/a').text.strip()

            if content.find_element_by_xpath('./td[5]/div/span'):
                je = content.find_element_by_xpath('./td[5]/div/span').text.strip()

            if content.find_element_by_xpath('./td[6]/div/span'):
                zbtime = content.find_element_by_xpath('./td[6]/div/span').text.strip()

            if content.find_element_by_xpath('./td[7]/div/a'):
                zbly = content.find_element_by_xpath('./td[7]/div/a').text.strip()
                zbly_href = content.find_element_by_xpath('./td[7]/div/a').get_attribute("href").strip()

            tmp = [href, entname, ggname, diqu, xmjl, je, zbtime, zbly_href, zbly]
            zhiding_qy_yj_data_zb.append(tmp)
            print(zhiding_qy_yj_data_zb)
        # break

# get_detail_sk_data(href, entname, ye_count, zhiding_qy_yj_data_sk)
def get_detail_sk_data(href, entname, ye_count,zhiding_qy_yj_data_sk):

    ye_input_xpath = '//*[@id="mohurd-list"]/div[3]/div/div/slot/div/input'
    go_to_button_xpath = '//*[@id="mohurd-list"]/div[3]/div/div/slot/button/span'
    data_list_xpath = '//*[@id="mohurd-list"]/div[2]/div/div[3]/table/tbody/tr'

    for gotoyema in range(1, ye_count + 1):
        if gotoyema > 1:
            print("第" + str(gotoyema) + "页")
            locator2 = (By.XPATH, ye_input_xpath)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

            zhuandao_loc = (By.XPATH, go_to_button_xpath)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
            sleep(3)

        ggname = ' '
        ggname_href =' '
        xmlx = ' '
        gcyt = ' '
        je = ' '
        zbtime = ' '
        jt = ' '
        xmjl = ' '
        content_list = driver.find_elements_by_xpath(data_list_xpath)
        # print(','.join(str(s) for s in content_list if s not in [None]))
        for content in content_list:
            sleep(3)
            if content.find_element_by_xpath('./td[2]/div/h2/a'):
                ggname = content.find_element_by_xpath('./td[2]/div/h2/a').text.strip()
                ggname_href = content.find_element_by_xpath('./td[2]/div/h2/a').get_attribute('href')

            if content.find_element_by_xpath('./td[3]/div/div'):
                xmlx = content.find_element_by_xpath('./td[3]/div/div').text.strip()

            if content.find_element_by_xpath('./td[4]/div'):
                gcyt = content.find_element_by_xpath('./td[4]/div').text.strip()

            if content.find_element_by_xpath('./td[5]/div/div'):
                je = content.find_element_by_xpath('./td[5]/div/div').text.strip()

            if content.find_element_by_xpath('./td[6]/div/div'):
                zbtime = content.find_element_by_xpath('./td[6]/div/div').text.strip()

            if content.find_element_by_xpath('./td[7]/div/div'):
                jt = content.find_element_by_xpath('./td[7]/div/div').text.strip()
                                                 # /td[8]/div/div
            if content.find_element_by_xpath('./td[8]/div/div'):
                xmjl_tmp = content.find_element_by_xpath('./td[8]/div/div').text.strip()
                if "--" ==xmjl_tmp:
                    xmjl="--"
                else:
                    xmjl = content.find_element_by_xpath('./td[8]/div/div/div/a').text.strip()
            tmp = [href, entname, ggname, xmlx, gcyt, je, zbtime, jt, xmjl,ggname_href]
            zhiding_qy_yj_data_sk.append(tmp)
            print(zhiding_qy_yj_data_sk)
        # break


def get_detail_qg_data(href, entname, ye_count,zhiding_qy_yj_data_qg):
    ye_input_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[2]/div/div/slot/div/input'
    go_to_button_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[2]/div/div/slot/button/span'
    data_list_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div/div[3]/table/tbody/tr'

    for gotoyema in range(1, ye_count + 1):
        if gotoyema > 1:
            print("第" + str(gotoyema) + "页")
            locator2 = (By.XPATH,ye_input_xpath)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

            zhuandao_loc = (By.XPATH,go_to_button_xpath)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
            sleep(3)

        ggname = ' '
        diqu = ' '
        xmjl = ' '
        je = ' '
        zbtime = ' '
        zbly_href = ' '
        zbly = ' '
        content_list = driver.find_elements_by_xpath(data_list_xpath)
        # print(','.join(str(s) for s in content_list if s not in [None]))
        for content in content_list:
            sleep(3)
            if content.find_element_by_xpath('./td[2]/div/h2/a'):
                ggname = content.find_element_by_xpath('./td[2]/div/h2/a').text.strip()

            if content.find_element_by_xpath('./td[3]/div/span'):
                diqu = content.find_element_by_xpath('./td[3]/div/span').text.strip()

            if content.find_element_by_xpath('./td[4]/div/a'):
                # if "--" not in content.find_element_by_xpath('./td[4]/div/a').text:
                xmjl = content.find_element_by_xpath('./td[4]/div/a').text.strip()

            if content.find_element_by_xpath('./td[5]/div/span'):
                je = content.find_element_by_xpath('./td[5]/div/span').text.strip()

            if content.find_element_by_xpath('./td[6]/div/span'):
                zbtime = content.find_element_by_xpath('./td[6]/div/span').text.strip()

            if content.find_element_by_xpath('./td[7]/div/a'):
                zbly = content.find_element_by_xpath('./td[7]/div/a').text.strip()
                zbly_href = content.find_element_by_xpath('./td[7]/div/a').get_attribute("href").strip()


            tmp = [href, entname, ggname, diqu, xmjl, je, zbtime, zbly_href, zbly]
            zhiding_qy_yj_data_qg.append(tmp)
            print(zhiding_qy_yj_data_qg)
    # return zhiding_qy_yj_data_zb

if  __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/data'
    infilename_qy = root_dir + r"\qy_list\云南省企业列表_20201111.xlsx"
    infilename_qy_href = root_dir + r"\get_jst_qyyj\建设通企业业绩_数据准备_贺家斌_href_20201111_152217.xlsx"
    outfilename_qyyj_jst_href = root_dir + r"\get_jst_qyyj\建设通企业业绩_href_贺家斌_"
    outfilename_qyyj_jst_zb = root_dir + r"\get_jst_qyyj\建设通企业业绩_中标公示_贺家斌_"
    outfilename_qyyj_jst_sk = root_dir + r"\get_jst_qyyj\建设通企业业绩_四库一平台业绩_贺家斌_"
    outfilename_qyyj_jst_qg = root_dir + r"\get_jst_qyyj\建设通企业业绩_全国公路建设市场业绩_贺家斌_"
    outfilename_qyzz_jst = root_dir + r"\get_jst_qyyj\建设通企业资质_贺家斌_"
    outfilename_ryzz_jst = root_dir + r"\get_jst_qyyj\建设通人员资质_贺家斌_"

    outfilename_gg = root_dir + r"\get_jst_qyyj\建设通标讯_贺家斌_"

    url = "https://passport.cbi360.net/login?url=https%3A%2F%2Fwww.cbi360.net%2Fhyjd%2F20200528%2F203181.html"
    # # 选择广东省份
    # guangdong_shenfen_xpath = '//*[@id="link-box"]/a[text()="广东"]'
    # # 选择云南省份
    # yunnan_shenfen_xpath = '//*[@id="link-box"]/a[text()="云南"]'
    # # 选择山西省份
    # shanxi_shenfen_xpath = '//*[@id="link-box"]/a[text()="山西"]'
    #
    # shenfen_list=[["广东省",guangdong_shenfen_xpath],["云南省",yunnan_shenfen_xpath],["山西省",shanxi_shenfen_xpath]]
    # shenfen_list = [["广东省", guangdong_shenfen_xpath]]
    driver=open(url)

    jst_qyyj_data = (read_excel_data(infilename_qy))[:50]
    # jst_qyyj_data = (read_excel_data(infilename_qy))[:50]
    print(jst_qyyj_data)

    zhiding_qy_yj_href = []
    zhiding_qy_yj_href = (read_excel_data(infilename_qy_href))
    print(zhiding_qy_yj_href)
    zhiding_qy_yj_data_zb=[]
    zhiding_qy_yj_data_sk = []
    zhiding_qy_yj_data_qg = []
    zhiding_qy_qyzz=[]
    zhiding_qy_ryzz = []
    s = input("input  your  unm: ")
    if int(s) == 1:
        # for sheng,shenfen_xpath in shenfen_list:
        #
        #     # 得到页面随机企业和对应的链接
        #     get_jst_qyyj2(driver,datalist,sheng,shenfen_xpath,total_ye)
        #
        # tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        # # 到数据到excle中
        # columnRows = ["sheng","shi_text", "entname", "href", "zbsl"]
        # wirteDataToExcel(outfilename+"href_" + tablenamehouzui + ".xlsx", "qy_href", columnRows, datalist)

        get_zhiding_qy_yj(driver, jst_qyyj_data, zhiding_qy_yj_href)
        tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 到数据到excle中
        columnRows = ["entname", "href"]
        wirteDataToExcel(outfilename_qyyj_jst_href+ tablenamehouzui + ".xlsx", "qy_href", columnRows, zhiding_qy_yj_href)




        # 得到相应企业的全部中标业绩
        # get_qyyj_detail2(driver, zhiding_qy_yj_href, zhiding_qy_yj_data_zb,zhiding_qy_yj_data_sk,zhiding_qy_yj_data_qg,zhiding_qy_qyzz,zhiding_qy_ryzz,outfilename_qyyj_jst_zb,outfilename_qyyj_jst_sk,outfilename_qyyj_jst_qg,outfilename_qyzz_jst,outfilename_ryzz_jst)
        for entname,href in zhiding_qy_yj_href:
            driver.get(href)
            print(href)
            sleep(3)
            zbsl = driver.find_element_by_xpath( '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/h3').text
            zbsl2 = zbsl.split(' ')
            zbsl_count = int(zbsl2[-1])
            print(zbsl_count)
            if zbsl_count > 0:
                ye_count = total_yema(zbsl_count)
                get_detail_zb_data(href, entname, ye_count, zhiding_qy_yj_data_zb)

            # 四库一平台
            skyt_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/h3'
            skyt = driver.find_element_by_xpath(skyt_xpath).text
            skyt2 = skyt.split(' ')
            skyt_count = int(skyt2[-1])
            print(skyt_count)
            if skyt_count > 0:
                driver.get(href)
                locator336 = (By.XPATH, skyt_xpath)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator336))

                driver.find_element_by_xpath(skyt_xpath).click()
                sleep(3)
                ye_count = total_yema(skyt_count)
                get_detail_sk_data(href, entname, ye_count, zhiding_qy_yj_data_sk)

            # qg_xpath = '//*[@id="__layout"]/div/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/h3'
            # qg = driver.find_element_by_xpath(qg_xpath).text
            # qg2 = qg.split(' ')
            # qg_count = int(qg2[-1])
            # print(qg_count)
            # if qg_count > 0:
            #     driver.find_element_by_xpath(qg_xpath).click()
            #     sleep(3)
            #     ye_count = total_yema(qg_count)
            #     get_detail_qg_data(href, entname, ye_count, zhiding_qy_yj_data_qg)

            # 获取人员资质
            get_ryzz(driver, entname, href, zhiding_qy_ryzz)
            # 获取企业资质
            get_qyzz(driver, entname, href, zhiding_qy_qyzz)

            # jst 中标公示
            if zhiding_qy_yj_data_zb:
                tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
                columnRows = ["href", "zhongbiaoren", "ggname", "diqu", "xmjl", "je", "zbtime", "zbly_href", "zbly"]
                wirteDataToExcel(outfilename_qyyj_jst_zb + tablenamehouzui + ".xlsx", "qyyj", columnRows,zhiding_qy_yj_data_zb)
                print("zhiding_qy_yj_data_zb  to excel")

            # jst 四库一平台业绩
            if zhiding_qy_yj_data_sk:
                tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
                columnRows = ["href", "zhongbiaoren", "ggname", "项目类型", "工程用途", "je(中标/合同/竣工)", "time(中标/合同/竣工)","可截图栏目", "xmjl", "ggname_href"]
                wirteDataToExcel(outfilename_qyyj_jst_sk + tablenamehouzui + ".xlsx", "qyyj", columnRows,zhiding_qy_yj_data_sk)
                print("zhiding_qy_yj_data_sk  to excel")

            # jst  全国公路建设市场业绩
            if zhiding_qy_yj_data_qg:
                tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
                columnRows = ["href", "zhongbiaoren", "ggname", "diqu", "xmjl", "合同价格", "交工时间", "zbly_href", "zbly"]
                wirteDataToExcel(outfilename_qyyj_jst_qg + tablenamehouzui + ".xlsx", "qyyj", columnRows,zhiding_qy_yj_data_qg)
                print("zhiding_qy_yj_data_qg  to excel")

            # jst  ryzz
            if zhiding_qy_ryzz:
                tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
                columnRows = ["href", "entname", "name", "lb_zhuanye", "zsh", "zsh", "zyyzh", "sfz", "yxq"]
                wirteDataToExcel(outfilename_ryzz_jst + tablenamehouzui + ".xlsx", "qyyj", columnRows, zhiding_qy_ryzz)
                print("zhiding_qy_ryzz  to excel")

            # jst qyzz
            if zhiding_qy_qyzz:
                tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
                columnRows = ["href", "entname", "qyzz_name", "start_time", "end_time"]
                wirteDataToExcel(outfilename_qyzz_jst + tablenamehouzui + ".xlsx", "qyyj", columnRows, zhiding_qy_qyzz)
                print("zhiding_qy_qyzz  to excel")
