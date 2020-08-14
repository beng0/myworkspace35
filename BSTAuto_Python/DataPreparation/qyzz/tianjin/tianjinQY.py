__author__ = 'Lyy'

from time import sleep
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, textXpath, clickXpath, hrefXpath, LoginUrlChrome, clickforname, LoginUrIE, initwait
import requests
import json

zzcount=0
zznum=0

def readzz(driver):
    initwait('//*[@id="Table2"]/tbody/tr/td/strong',driver)
    name = textXpath('//*[@id="FormView1_qymcLabel"]',driver)
    href = driver.current_url
    global zzcount
    stamp = 1
    while(True):
        try:
            zz =textXpath('//*[@id="zz_new"]/td[4]/li['+str(stamp)+']',driver)
            stamp+=1
            if zz!= '':
                zzcount+=1
                print(zzcount,name,zz,href)
        except:break
    stamp=3
    while(True):
        try:
            beforeXpath = '//*[@id="form1"]/table[2]/tbody/tr['+str(stamp)+']/td[3]'
            zz=textXpath(beforeXpath,driver)
            stamp+=1
            if zz!='':
                zzstamp = 1
                while(True):
                    try:
                        zzin = textXpath(beforeXpath+'/li['+str(zzstamp)+']',driver)
                        zzstamp+=1
                        if zzin!='':
                            zzcount+=1
                            print(zzcount,name,zzin,href)
                    except:break
        except:break
    if zzcount>int(zznum):
        return False
    else:
        return True

def readpage(driver):
    flag = True
    stamp = 1
    while (flag):
        try:
            handle = driver.current_window_handle
            clickXpath('/html/body/form/div[3]/div/div/table/tbody/tr/td/table[1]/tbody/tr['+str(stamp)+']/td[7]/a',driver)
            stamp+=1
            handles = driver.window_handles
            for newhandle in handles:
                if newhandle != handle:
                    driver.switch_to.window(newhandle)
                    try:
                        flag = readzz(driver)
                    except:
                        driver.close()
                        continue
                    driver.close()
                    driver.switch_to.window(handle)
                    if not flag:
                        return False

        except:
            driver.switch_to.window(handle)
            break
    return True

if __name__ == '__main__':
    url='http://218.69.33.182/epr/Search/C_Common/CE/index.aspx'
    driver = LoginUrlChrome(url)
    print("input zznum:")
    zznum=input()
    stamp = 5
    while (True):
        flag = readpage(driver)
        if not flag:
            break
        current = textXpath('/html/body/form/div[3]/div/div/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]', driver)
        clickforname('//*[@id="ASPxGridView2_ctl04"]/tbody/tr/td/table/tbody/tr/td[', stamp, ']', '下一页', driver)
        while (current == textXpath('/html/body/form/div[3]/div/div/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]', driver,3)):
            sleep(3)
    driver.quit()