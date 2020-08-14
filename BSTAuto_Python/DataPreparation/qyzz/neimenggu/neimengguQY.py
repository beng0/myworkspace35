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

zzcount =0

def readzz():
    try:
        initwait('//*[@id="form1"]/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[2]',driver)
    except:
        return True
    name = textXpath('//*[@id="form1"]/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[2]',driver)
    qys = textXpath('//*[@id="Td2"]', driver)
    stamp=1
    global zzcount
    while(True):
        try:
            qylx = textXpath('//*[@id="form1"]/div[3]/div[2]/div[2]/div[3]/div[1]/div['+str(stamp)+']/span',driver)
            zzmclist=textXpath('//*[@id="form1"]/div[3]/div[2]/div[2]/div[3]/div[1]/table['+str(stamp)+']/tbody/tr[3]/td[2]',driver).split(';')
            for i in zzmclist:
                if i!='':
                    zzcount+=1
                    print(zzcount,'|',qys,'|',qylx,'|',name,'|', i)
            stamp += 1
        except:
            break
    if zzcount>int(zznum):
        return False
    else:
        return True

def readpage(driver):
    stamp = 1
    while (True):
        try:
            clickXpath('//*[@id="acBody"]/tr[' + str(stamp) + ']/td[2]/a', driver)
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
    driver= LoginUrl('http://110.16.70.26/nmjgpublisher/corpinfo/CorpInfoObtain.aspx#')
    print('input zznum:')
    zznum=input()

    stamp = 1
    while (True):
        flag = readpage(driver)
        if not flag:
            break
        current = textXpath('/html/body/form/div[4]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]', driver)
        clickforname('/html/body/form/div[4]/div[2]/div[1]/div[2]/div/div/div/div/ul/li[', stamp, ']/a', '下一页', driver)
        while (current == textXpath('/html/body/form/div[4]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]', driver)):
            sleep(3)
