__author__ = 'Lyy'

from time import sleep
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, textXpath, clickXpath, hrefXpath, LoginUrlChrome, clickforname, LoginUrIE, initwait
import requests
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
import json

zzcount=0
zznum=0

def readzz():
    initwait('/html/body/form/div[6]/div[2]/div/div[1]/h2',driver)
    name = textXpath('//*[@id="ContentPlaceHolder1_PersonName"]', driver)
    qyname = textXpath('//*[@id="company_certificates"]/div[1]/table/tbody/tr[1]/td[2]/a', driver)
    flag = True
    stamp = 1
    global zzcount
    while (flag):
        try:
            zzname = textXpath('//*[@id="company_certificates"]/div[' + str(stamp) + ']/div', driver)
            if zzname.split('▪')[0] =='' :
                return True
            else:
                stamp += 1
                zzcount += 1
                print(zzcount, '|', name, '|', zzname, '|', qyname)
        except:
            break
    if zzcount > int(zznum):
        return False
    else:
        return True

def readpage(driver):
    stamp = 2
    while (True):
        try:
            clickXpath('/html/body/form/div[6]/div[2]/div[2]/div/table/tbody/tr[' + str(stamp) + ']/td[2]/a', driver)
            stamp += 1
        except:
            break
    handle = driver.current_window_handle
    handles = driver.window_handles
    for newhandle in handles:
        if newhandle != handle:
            driver.switch_to.window(newhandle)
            flag=readzz()
            driver.close()
            if not flag:
                return False
    driver.switch_to.window(handle)
    return True

if __name__ == '__main__':
    url='http://dn4.gxzjt.gov.cn:1141/WebInfo/Person/Person.aspx'
    driver = LoginUrl(url)
    print('input zznum:')
    zznum=input()

    stamp = 1
    '/html/body/form/div[6]/div[2]/div[2]/div/div/table/tbody/tr/td[2]/a[' ']'
    while(True):
        flag=readpage(driver)
        if not flag:
            break
        current=textXpath('/html/body/form/div[6]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/a',driver)
        clickforname('/html/body/form/div[6]/div[2]/div[2]/div/div/table/tbody/tr/td[2]/a[',stamp,']','下一页>',driver)
        while(current==textXpath('/html/body/form/div[6]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/a',driver)):
            sleep(3)