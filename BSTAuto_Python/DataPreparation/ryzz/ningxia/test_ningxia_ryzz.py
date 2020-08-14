__Author__ = 'hjh'
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
from datetime import datetime
from time import sleep
from bst.bst_datatest.test_case.models.my_to_excel import wirteDataToExcel
from selenium.webdriver.support.select import Select



def get_1_jz_ryzz(driver,data):
    # 一级建造师
    driver.get('http://www.coc.gov.cn/coc/webview/fRegConstructor.jspx')
    sleep(3)

    locator = (By.XPATH, '//*[@id="provinceId"]')
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(locator))

    # 选择宁夏
    sel = driver.find_element(By.XPATH, '//*[@id="provinceId"]')
    Select(sel).select_by_value('640000')

    driver.find_element(By.XPATH, '//*[@id="query"]').click()
    sleep(3)

    # 得到总页数
    total_ye = driver.find_element(By.XPATH, '//*[@id="bottomPage"]/font[1]').text
    total_ye_str = total_ye.split(' ')[5]
    print(type(total_ye_str))


    for goto_ye in range(2, int(total_ye_str)):
        get_nixia_qy(driver, data,goto_ye)






def  get_nixia_qy(driver,data,goto_ye):
    if goto_ye != 1:
        driver.find_element(By.XPATH,'//*[@id="nonstopPageNo2"]').click()
        driver.find_element(By.XPATH, '//*[@id="nonstopPageNo2"]').send_keys(str(goto_ye))
        driver.find_element(By.XPATH,'//*[@id="bottomPage"]/input[2]').click()
        sleep(5)


    content_list = driver.find_elements(By.XPATH,'//*[@id="table_style1"]/tbody/tr')[2:]
    for content in content_list:
        qyname = content.find_element(By.XPATH,'.//td[2]/a').text.strip()
        href = content.find_element(By.XPATH,'.//td[2]/a').get_attribute('href')
        temp=[href,qyname]
        data.append(temp)



def  get_detail(driver,data,ryzz_data):

    for  href,qyname  in data:
        driver.get(href)
        sleep(3)


        # 得到总页数
        total_ye = driver.find_element(By.XPATH, '//*[@id="bottomPage"]/font[1]').text
        total_ye_str = total_ye.split(' ')[5]

        if  1 != int(total_ye_str):
            for goto_ye in range(1, int(total_ye_str)+1):
                get_detail_meiye(driver,ryzz_data,href,goto_ye)
        else:
            get_detail_meiye(driver, ryzz_data, href)


def  get_detail_meiye(driver,ryzz_data,href,goto_ye=None):
    # 翻页
    if goto_ye not in [1,None]:
        driver.find_element(By.XPATH, '//*[@id="nonstopPageNo2"]').click()
        driver.find_element(By.XPATH, '//*[@id="nonstopPageNo2"]').send_keys(str(goto_ye))
        driver.find_element(By.XPATH, '//*[@id="bottomPage"]/input[2]').click()
        sleep(5)

    content_list = driver.find_elements(By.XPATH, '//*[@id="table_style1"]/tbody/tr')[1:]
    print(href)
    for content in content_list:
        try:
            texts = content.text.split(' ')
            print(texts)
            xh = texts[0]
            qyname = texts[1]
            name = texts[2]
            zch = texts[3]
            zczsbh = texts[4]
            zczy = texts[5]
            yxq = texts[6]
            temp = [href, xh, qyname, name, zch, zczsbh, zczy, yxq]
            ryzz_data.append(temp)
            print(ryzz_data)
        except:
            continue

def get_two_level_jz(driver,two_level_jz_data):
    driver.get("http://jzsgl.coc.gov.cn/archisearch/cxejjzs/rylist.aspx?sjbm=640000&qymc=&xm=&zclb=00&zczy=%E5%85%A8%E9%83%A8&zczsbh=&zch=&zyzgzsbh=")
    locator = (By.XPATH,'//*[@id="divTable"]/table/tbody/tr[1]')
    WebDriverWait(driver,10).until(EC.visibility_of_element_located(locator))

    total_ye = driver.find_element(By.XPATH,'//*[@id="divPager2"]/div/span[2]/span[3]/label').text.strip()
    print(total_ye)
    total_ye_count= int(total_ye)

    # 翻页
    if  total_ye_count not in [1,None] :
        for goto_ye  in   range(1,11):
            driver.find_element(By.XPATH,'//*[@id="divPager2"]/div/span[1]/span[10]/a').click()
            sleep(5)

            content_list = driver.find_elements(By.XPATH,'//*[@id="divTable"]/table/tbody/tr')
            for content in content_list:
                qyname=content.find_element(By.XPATH,'.//td[2]/a').text.strip()
                name=content.find_element(By.XPATH,'.//td[3]/a').text.strip()
                zch=content.find_element(By.XPATH,'.//td[4]').text.strip()
                zczsbh=content.find_element(By.XPATH,'.//td[5]').text.strip()
                zyzsbh=content.find_element(By.XPATH,'.//td[6]').text.strip()
                zzlb="二级注册建造师"
                temp=[qyname,name,zch,zczsbh,zyzsbh,zzlb]
                two_level_jz_data.append(temp)
                print(two_level_jz_data)

def get_two_linshi_level_jz(driver,two_level_jz_data):
    driver.get("http://jzsgl.coc.gov.cn/archisearch/cxejlsjzs/rylist.aspx?sjbm=640000&qymc=&xm=&zclb=00&zczy=%E5%85%A8%E9%83%A8&zczsbh=&zch=")
    locator = (By.XPATH,'//*[@id="divTable"]/table/tbody/tr[1]')
    WebDriverWait(driver,10).until(EC.visibility_of_element_located(locator))

    for goto_ye  in   range(1,4):
        if goto_ye !=1:
            driver.find_element(By.XPATH,'//*[@id="divPager2"]/div/span[1]/span[10]/a').click()
            sleep(5)

        content_list = driver.find_elements(By.XPATH,'//*[@id="divTable"]/table/tbody/tr')
        for content in content_list:
                qyname=content.find_element(By.XPATH,'.//td[2]/a').text.strip()
                name=content.find_element(By.XPATH,'.//td[3]/a').text.strip()
                zch=content.find_element(By.XPATH,'.//td[4]').text.strip()
                zczsbh=content.find_element(By.XPATH,'.//td[5]').text.strip()
                zczy=content.find_element(By.XPATH,'.//td[6]').text.strip()
                zcyxq=content.find_element(By.XPATH,'.//td[7]').text.strip()
                zclb=content.find_element(By.XPATH,'.//td[8]').text.strip()
                zzlb="二级建造师临时执业证书"
                temp=[qyname,name,zch,zczsbh,zczy,zcyxq,zclb,zzlb]
                two_level_jz_data.append(temp)
                print(two_level_jz_data)

def get_jianli_data(driver,goto_ye,jianli_data):
    if 1 != goto_ye:
        driver.find_element(By.XPATH,'//*[@id="AspNetPager1_input"]').clear()
        driver.find_element(By.XPATH, '//*[@id="AspNetPager1_input"]').send_keys(goto_ye)
        driver.find_element(By.XPATH, '//*[@id="AspNetPager1_btn"]').click()
        # driver.find_element(By.XPATH,'//*[@id="AspNetPager1"]/table/tbody/tr/td[2]/a[10]/img').click()
        sleep(3)

    content_list = driver.find_elements(By.XPATH,'//*[@id="dgResult"]/tbody/tr')[1:]
    for content in content_list:
        texts =content.text.split(' ')
        # print(texts)
        xh = texts[0]
        name = texts[1]
        xb = texts[2]
        qyname = texts[3]
        zczsbh = texts[4]
        zch = texts[5]
        zy1 = texts[6]
        zy2 = texts[7]
        yxq = texts[8]
        temp = [xh,name,xb, qyname, zczsbh,zch, zy1, zy2,yxq]
        jianli_data.append(temp)
        print(jianli_data)




def get_zigelei_data(driver,goto_ye,data):
    if 1 != goto_ye:  #//*[@id="pagenation"]/li[2]/a
        if goto_ye == 2:
            driver.find_element(By.XPATH, '//*[@id="pagenation"]/li[2]/a').click()
        elif goto_ye > 2:
            driver.find_element(By.XPATH, '//*[@id="pagenation"]/li['+str(goto_ye+1)+']/a').click()

        sleep(3)

    content_list = driver.find_elements(By.XPATH,'//*[@id="zy_web_person_info"]/tr')
    for content in content_list:
        texts =content.text.split(' ')
        # print(texts)
        xh = texts[0]
        name = texts[1]
        qyname = texts[2]
        zz = texts[3]
        zy = texts[4]
        zh = texts[5]
        fzrq = texts[6]
        temp = [xh,name,qyname, zz,zy, zh, fzrq]
        data.append(temp)
        print(data)






if __name__=='__main__':
    now_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    driver = webdriver.Chrome()
    data = []

    # 得到宁夏一级建造师
    get_1_jz_ryzz(driver,data)
    print(data)

    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\人员资质测试\nixia\数据准备\省平台宁夏人员资质_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['href','企业名称']
    wirteDataToExcel(outfilename, "sheetName", columnRows, data)
    print("out data to excel success")

    ryzz_data = []
    get_detail(driver, data,ryzz_data)

    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质一级注册建造师_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['href','序号','企业名称','姓名','注册号','注册证书编号','注册专业','注册有效期']
    wirteDataToExcel(outfilename, "sheetName", columnRows, ryzz_data)
    print("out data to excel success")

###############################################################################################################################

    # two_level_jz_data=[]
    # # 得到二级建造师
    # get_two_level_jz(driver,two_level_jz_data)
    # # 把数据导出到xlsx
    # outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质二级注册建造师_胡金花' + str(now_time) + '.xlsx'
    # columnRows = ['企业名称','姓名','注册号','注册证书编号','执业资格证书编号','资质类别']
    # wirteDataToExcel(outfilename, "sheetName", columnRows, two_level_jz_data)
    # print("out data to excel success")

##############################################################################################################################

    # two_linshi_level_jz_data = []
    # # 得到二级建造师临时执业证书
    # get_two_linshi_level_jz(driver, two_linshi_level_jz_data)
    # # 把数据导出到xlsx
    # outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质二级建造师临时执业证书_胡金花' + str(now_time) + '.xlsx'
    # columnRows = ['企业名称', '姓名', '注册号', '注册证书编号', '注册专业','注册有效期','注册类别', '资质类别']
    # wirteDataToExcel(outfilename, "sheetName", columnRows, two_linshi_level_jz_data)
    # print("out data to excel success")

##################################################################################################################################
    # # 监理师
    # driver.get("http://jlgcs.cein.gov.cn/jlgcsSearch/index.aspx")
    # sleep(3)
    #
    #
    # WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="areacode"]')))
    # sel =  driver.find_element(By.XPATH,'//*[@id="areacode"]')
    # Select(sel).select_by_value("宁夏")
    # driver.find_element(By.XPATH,'//*[@id="IBSearch"]').click()
    # sleep(3)
    #
    # get_yeshu =  10
    # jianli_data=[]
    # for goto_ye in range(1,get_yeshu):
    #     get_jianli_data(driver,goto_ye,jianli_data)
    #
    # # 把数据导出到xlsx
    # outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质监理师_胡金花' + str(now_time) + '.xlsx'
    # columnRows = ['序号', '姓名','性别', '注册号','企业名称', '注册证书编号', '注册号','注册专业1','注册专业2','有效期']
    # wirteDataToExcel(outfilename, "sheetName", columnRows, jianli_data)
    # print("out data to excel success")

########################################################################################################################

    driver.get("http://www.nxjscx.com.cn/rysj.htm#")
    driver.maximize_window()
    sleep(3)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div[3]')))
    # 资格类
    driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[3]').click()
    sleep(3)

    get_yeshu=6

    # 三类人员
    driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/ol[3]/li[1]/a').click()
    sleep(30)

    iframe= driver.find_element(By.XPATH,'/html/body/div[4]/div[3]/div[2]/iframe')
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="zy_web_person_info"]/tr[1]')))
    sl_data = []
    for goto_ye in range(1, get_yeshu):
        get_zigelei_data(driver, goto_ye, sl_data)

    driver.switch_to.default_content()
    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质三类人员_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['序号', '姓名', '从业单位', '资格信息',  '专业', '证号', '发证日期']
    wirteDataToExcel(outfilename, "sheetName", columnRows, sl_data)
    print("out data to excel success")

    # 特征作业人员
    driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/ol[3]/li[2]/a').click()
    sleep(30)

    iframe = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[2]/iframe')
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="zy_web_person_info"]/tr[1]')))
    sl_data = []
    for goto_ye in range(1, get_yeshu):
        get_zigelei_data(driver, goto_ye, sl_data)

    driver.switch_to.default_content()
    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质特征作业人员_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['序号', '姓名', '从业单位', '资格信息', '专业', '证号', '发证日期']
    wirteDataToExcel(outfilename, "sheetName", columnRows, sl_data)
    print("out data to excel success")

    # 行业八员
    driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/ol[3]/li[3]/a').click()
    sleep(30)

    iframe = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[2]/iframe')
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="zy_web_person_info"]/tr[1]')))
    sl_data = []
    for goto_ye in range(1, get_yeshu):
        get_zigelei_data(driver, goto_ye, sl_data)

    driver.switch_to.default_content()
    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质行业八员_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['序号', '姓名', '从业单位', '资格信息', '专业', '证号', '发证日期']
    wirteDataToExcel(outfilename, "sheetName", columnRows, sl_data)
    print("out data to excel success")

    # 土建劳务人员
    driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/ol[3]/li[4]/a').click()
    sleep(30)

    iframe = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[2]/iframe')
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="zy_web_person_info"]/tr[1]')))
    sl_data = []
    for goto_ye in range(1, get_yeshu):
        get_zigelei_data(driver, goto_ye, sl_data)

    driver.switch_to.default_content()
    # 把数据导出到xlsx
    outfilename = r'D:\筑龙项目\人员资质测试\ningxia\数据准备\省平台宁夏人员资质土建劳务人员_胡金花' + str(now_time) + '.xlsx'
    columnRows = ['序号', '姓名', '从业单位', '资格信息', '专业', '证号', '发证日期']
    wirteDataToExcel(outfilename, "sheetName", columnRows, sl_data)
    print("out data to excel success")








    driver.quit()