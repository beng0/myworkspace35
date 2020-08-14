from time import sleep

import xlrd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl

if __name__ == '__main__':
    driver = LoginUrl(u'http://jg.hbcic.net.cn/web/RyManage/RySearch.aspx')

    # init
    divstr = '//*[@id="form1"]/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]'
    resultLocator = (By.XPATH, divstr)
    WebDriverWait(driver, 120).until(EC.presence_of_element_located(resultLocator))

    flag=True #下一页面总循环开关
    print('需要爬取的资质数：')
    zzcount = input()
    zznum=0
    page=201
    while(flag):
            # init
            divstr = '//*[@id="form1"]/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]'
            resultLocator = (By.XPATH, divstr)
            WebDriverWait(driver, 120).until(EC.presence_of_element_located(resultLocator))

            #点开所有人员名链接
            divflag=True #遍历人员数开关
            divTemp=2 #序号起始点
            name =''
            qyname=''
            zzname=''
            namehref=''
            zzlx=''
            zzlx2=''
            while(divflag):
                try:
                    divstr='/html/body/form/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr['+str(divTemp)+']/td[2]/a'
                    resultLocator=(By.XPATH,divstr)
                    linkbt=WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator))

                    #企业名
                    divstr='/html/body/form/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr['+str(divTemp)+']/td[7]'
                    resultLocator=(By.XPATH,divstr)
                    qyname=WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                    divstr='//*[@id="form1"]/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr['+str(divTemp)+']/td[5]'
                    resultLocator=(By.XPATH,divstr)
                    zztemp=WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
                    #资质为空则跳过
                    if zztemp!='无' :
                        namehref = driver.current_url
                        divstr = '//*[@id="form1"]/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[' + str(
                            divTemp) + ']/td[5]'
                        resultLocator = (By.XPATH, divstr)
                        zztemp = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                        linkbt.click()
                        handle = driver.current_window_handle
                        handles = driver.window_handles
                        for newhandle in handles:
                            if newhandle != handle:
                                driver.switch_to.window(newhandle)
                                # init&姓名
                                divstr = '//*[@id="XM"]'
                                resultLocator = (By.XPATH, divstr)
                                name=WebDriverWait(driver, 120).until(EC.presence_of_element_located(resultLocator)).text

                                # 注册类
                                zcflag = True
                                zctemp = 1
                                #获取单个资质时
                                try:
                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr/td[1]'
                                    resultLocator = (By.XPATH, divstr)
                                    temp = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr/td[2]'
                                    resultLocator = (By.XPATH, divstr)
                                    zzname = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr/td[4]'
                                    resultLocator = (By.XPATH, divstr)
                                    zzlx = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                                    print(zznum+1,qyname,name,zzname,zzlx)
                                    zznum+=1
                                except:
                                    zctemp = 2
                                #获取多个资质时
                                zctemp = 1
                                while(zcflag):
                                    try:
                                        divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr['+str(zctemp)+']/td[1]'
                                        resultLocator = (By.XPATH, divstr)
                                        temp=WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                                        divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr['+str(zctemp)+']/td[2]'
                                        resultLocator = (By.XPATH, divstr)
                                        zzname = WebDriverWait(driver, 1).until(
                                            EC.presence_of_element_located(resultLocator)).text

                                        divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr['+str(zctemp)+']td[4]'
                                        resultLocator = (By.XPATH, divstr)
                                        zzlx = WebDriverWait(driver, 1).until(
                                            EC.presence_of_element_located(resultLocator)).text

                                        print(zznum+1, qyname, name, zzname, zzlx)
                                        zznum+=1
                                        zctemp+=1
                                    except :
                                        zcflag=False

                                # 非注册类
                                zcflag = True
                                zctemp = 1
                                #获取单个资质时
                                try:
                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[1]/ul/li[2]'
                                    resultLocator = (By.XPATH, divstr)
                                    WebDriverWait(driver, 1).until(
                                        EC.presence_of_element_located(resultLocator)).click()

                                    sleep(2)

                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr/td[1]'
                                    resultLocator = (By.XPATH, divstr)
                                    temp = WebDriverWait(driver, 3).until(EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr/td[2]'
                                    resultLocator = (By.XPATH, divstr)
                                    zzname = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr/td[3]'
                                    resultLocator = (By.XPATH, divstr)
                                    zzlx = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr/td[4]'
                                    resultLocator = (By.XPATH, divstr)
                                    zzlx2 = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                                    print(zznum+1,qyname,name,str(zzlx)+str(zzlx2),zzname)
                                    zznum+=1
                                except:
                                    zctemp = 2
                                #获取多个资质时
                                zctemp = 2
                                while(zcflag):
                                    try:
                                        divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr['+str(zctemp)+']/td[1]'
                                        resultLocator = (By.XPATH, divstr)
                                        temp = WebDriverWait(driver, 3).until(
                                            EC.presence_of_element_located(resultLocator)).text

                                        divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr['+str(zctemp)+']/td[2]'
                                        resultLocator = (By.XPATH, divstr)
                                        zzname = WebDriverWait(driver, 1).until(
                                            EC.presence_of_element_located(resultLocator)).text

                                        divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr['+str(zctemp)+']/td[3]'
                                        resultLocator = (By.XPATH, divstr)
                                        zzlx = WebDriverWait(driver, 1).until(
                                            EC.presence_of_element_located(resultLocator)).text

                                        divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr['+str(zctemp)+']/td[4]'
                                        resultLocator = (By.XPATH, divstr)
                                        zzlx2 = WebDriverWait(driver, 1).until(
                                            EC.presence_of_element_located(resultLocator)).text

                                        print(zznum+1,qyname,name,str(zzlx)+str(zzlx2),zzname)
                                        zznum += 1
                                        zctemp+=1
                                    except :
                                        zcflag=False

                                driver.close()
                        driver.switch_to.window(handles[0])

                    divTemp += 1

                except:
                    #当前页面结束
                    divflag=False
                    #page += 1
            try:
                # divstr = '//*[@id="txtPageIndex"]'
                # resultLocator = (By.XPATH, divstr)
                # WebDriverWait(driver, 1).until(
                #     EC.presence_of_element_located(resultLocator)).send_keys(page)
                #
                # divstr = '//*[@id="lbtnGo"]'
                # resultLocator = (By.XPATH, divstr)
                # WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).click()
                divstr = '//*[@id="lbtnNext"]'
                resultLocator = (By.XPATH, divstr)
                WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).click()
            except:
                flag= False

            if  zznum>=int(zzcount) :
                flag = False

            # divTemp=3
            # divflag=True
            # name=''
            # zz=''
            # bh=''
            # dj=''
            # rq=''
            # while(divflag):
            #     try:
            #         divstr='/html/body/form/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr['+str(divTemp)+']/td[2]/a'
            #         resultLocator=(By.XPATH,divstr)
            #         linkbt=WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator))
            #         linkname=linkbt.text
            #
            #         if linkname!='':
            #             linkbt.click()
            #         divTemp += 1
            #
            #     except:
            #         divflag=False

            #         haszz=False
            #         zzflag=True
            #         zztmp=2
            #         while(zzflag):
            #             try:
            #                 divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[1]'
            #                 resultLocator = (By.XPATH, divstr)
            #                 bh = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
            #
            #                 divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[2]'
            #                 resultLocator = (By.XPATH, divstr)
            #                 zz = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
            #
            #                 divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[3]'
            #                 resultLocator = (By.XPATH, divstr)
            #                 dj = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
            #
            #                 divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[4]'
            #                 resultLocator = (By.XPATH, divstr)
            #                 rq = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
            #                 zztmp+=1
            #                 zzcount += 1
            #                 print(zzcount,name,bh,zz+dj,rq)
            #                 haszz=True
            #             except :
            #                 zzflag = False
            #         zzlxflag = True
            #         zzlxtmp = 2
            #         while (zzlxflag):
            #             try:
            #                 haszz = False
            #                 zzflag = True
            #                 zztmp = 2
            #                 while (zzflag):
            #                     try:
            #                         divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
            #                             zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
            #                             zztmp) + ']/td[1]'
            #                         resultLocator = (By.XPATH, divstr)
            #                         bh = WebDriverWait(driver, 1).until(
            #                             EC.presence_of_element_located(resultLocator)).text
            #
            #                         divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
            #                             zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
            #                             zztmp) + ']/td[2]'
            #                         resultLocator = (By.XPATH, divstr)
            #                         zz = WebDriverWait(driver, 1).until(
            #                             EC.presence_of_element_located(resultLocator)).text
            #
            #                         divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
            #                             zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
            #                             zztmp) + ']/td[3]'
            #                         resultLocator = (By.XPATH, divstr)
            #                         dj = WebDriverWait(driver, 1).until(
            #                             EC.presence_of_element_located(resultLocator)).text
            #
            #                         divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
            #                             zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
            #                             zztmp) + ']/td[4]'
            #                         resultLocator = (By.XPATH, divstr)
            #                         rq = WebDriverWait(driver, 1).until(
            #                             EC.presence_of_element_located(resultLocator)).text
            #                         zztmp += 1
            #                         zzcount += 1
            #                         print(zzcount, name, bh, zz + dj, rq)
            #                         haszz = True
            #                     except:
            #                         zzflag = False
            #                         zzlxflag = False
            #                 zzlxtmp += 1
            #             except:
            #                 zzlxflag = False
            #         if haszz:
            #             qycount+=1
            #
            #         driver.close()
            # driver.switch_to.window(handles[0])
            # try:
            #     np ='//*[@id="lbtnNext"]'
            #     resultLocatorNp = (By.XPATH, np)
            #     clickbt = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocatorNp))
            #     if  clickbt.text=='下一页':
            #         clickbt.click()
            # except:
            #     flag = False
            # if  zzcount>=int(a) & int(a)!=0 :
            #     flag = False
            # if  qycount>=int(b) & int(b)!=0:
            #     flag = False

    print('over')