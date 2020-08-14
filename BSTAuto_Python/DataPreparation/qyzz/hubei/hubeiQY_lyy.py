import xlrd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl

if __name__ == '__main__':
    driver = LoginUrl(u'http://jg.hbcic.net.cn/web/QyManage/QyList.aspx')

    flag=True
    row=1
    print('需要爬取的资质数：')
    a=input()
    print('需要爬取的企业数：')
    b=input()
    zzcount = 0
    qycount = 0
    while(flag):
            # init
            divstr = '/html/body/form/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr[3]/td[2]/a'
            resultLocator = (By.XPATH, divstr)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(resultLocator))

            divTemp=3
            divflag=True
            name=''
            zz=''
            bh=''
            dj=''
            rq=''
            while(divflag):
                try:
                    divstr='/html/body/form/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr['+str(divTemp)+']/td[2]/a'
                    resultLocator=(By.XPATH,divstr)
                    linkbt=WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator))
                    linkname=linkbt.text

                    if linkname!='':
                        linkbt.click()
                    divTemp += 1

                except:
                    divflag=False
            handle = driver.current_window_handle
            handles = driver.window_handles
            for newhandle in handles:
                if newhandle != handle:
                    driver.switch_to.window(newhandle)
                    # init
                    divstr = '//*[@id="QYMC"]'
                    resultLocator = (By.XPATH, divstr)
                    name=WebDriverWait(driver, 60).until(EC.presence_of_element_located(resultLocator)).text

                    haszz=False
                    zzflag=True
                    zztmp=2
                    while(zzflag):
                        try:
                            divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[1]'
                            resultLocator = (By.XPATH, divstr)
                            bh = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                            divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[2]'
                            resultLocator = (By.XPATH, divstr)
                            zz = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                            divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[3]'
                            resultLocator = (By.XPATH, divstr)
                            dj = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text

                            divstr='/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table/tbody/tr[2]/td/table/tbody/tr['+str(zztmp)+']/td[4]'
                            resultLocator = (By.XPATH, divstr)
                            rq = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
                            zztmp+=1
                            zzcount += 1
                            print(zzcount,name,bh,zz+dj,rq)
                            haszz=True
                        except :
                            zzflag = False
                    zzlxflag = True
                    zzlxtmp = 2
                    while (zzlxflag):
                        try:
                            haszz = False
                            zzflag = True
                            zztmp = 2
                            while (zzflag):
                                try:
                                    divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
                                        zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
                                        zztmp) + ']/td[1]'
                                    resultLocator = (By.XPATH, divstr)
                                    bh = WebDriverWait(driver, 1).until(
                                        EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
                                        zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
                                        zztmp) + ']/td[2]'
                                    resultLocator = (By.XPATH, divstr)
                                    zz = WebDriverWait(driver, 1).until(
                                        EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
                                        zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
                                        zztmp) + ']/td[3]'
                                    resultLocator = (By.XPATH, divstr)
                                    dj = WebDriverWait(driver, 1).until(
                                        EC.presence_of_element_located(resultLocator)).text

                                    divstr = '/html/body/form/div[2]/div[2]/div/div[2]/div/div[1]/ul/li/table[' + str(
                                        zzlxtmp) + ']/tbody/tr[2]/td/table/tbody/tr[' + str(
                                        zztmp) + ']/td[4]'
                                    resultLocator = (By.XPATH, divstr)
                                    rq = WebDriverWait(driver, 1).until(
                                        EC.presence_of_element_located(resultLocator)).text
                                    zztmp += 1
                                    zzcount += 1
                                    print(zzcount, name, bh, zz + dj, rq)
                                    haszz = True
                                except:
                                    zzflag = False
                                    zzlxflag = False
                            zzlxtmp += 1
                        except:
                            zzlxflag = False
                    if haszz:
                        qycount+=1

                    driver.close()
            driver.switch_to.window(handles[0])
            try:
                np ='//*[@id="lbtnNext"]'
                resultLocatorNp = (By.XPATH, np)
                clickbt = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocatorNp))
                if  clickbt.text=='下一页':
                    clickbt.click()
            except:
                flag = False
            if  zzcount>=int(a) & int(a)!=0 :
                flag = False
            if  qycount>=int(b) & int(b)!=0:
                flag = False

    print('over')