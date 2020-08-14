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
zznum=0

def readpage(driver):
    stamp =1
    global zzcount
    while(True):
        try:
            name = textXpath('/html/body/form/div[5]/div[2]/div/table/tbody/tr[' + str(stamp) +']/td[2]/a', driver)
            href = hrefXpath('/html/body/form/div[5]/div[2]/div/table/tbody/tr[' + str(stamp) +']/td[2]/a', driver)
            zz = textXpath(
                '/html/body/form/div[5]/div[2]/div/table/tbody/tr[' + str(stamp) + ']/td[4]',
                driver)
            qy = textXpath('/html/body/form/div[5]/div[2]/div/table/tbody/tr[' + str(stamp) +']/td[5]', driver)
            zzl=zz.split(';')
            for i in zzl:
                if i!='':
                    zzcount+=1
                    print(zzcount,'|',qy,'|',name,'|',i,'|',href)
            if zzcount>int(zznum):
                return False
        except:
            break
        stamp += 1
    return True

def readtype(driver):
    stamp = 1
    global zzcount
    while (True):
        flag = readpage(driver)
        if not flag:
            zzcount=0
            return False
        current = textXpath('/html/body/form/div[5]/div[2]/div/table/tbody/tr[1]/td[2]/a', driver)
        clickforname('/html/body/form/div[5]/div[2]/div/div/div/ul/li[', stamp, ']/a', '下一页', driver)
        try:
            while (current == textXpath('/html/body/form/div[5]/div[2]/div/table/tbody/tr[1]/td[2]/a', driver,30)):
                sleep(3)
        except:
            zzcount=0
            return True
    zzcount=0
    return True

if __name__ == '__main__':
    driver = LoginUrl('http://110.16.70.26/nmjgpublisher/UserInfo/CertifiedEngineersObtain.aspx')
    print('input zznum:')
    zznum=input()

    stamp=2
    while(True):
        clickXpath('//*[@id="ddlSpecialty"]', driver)
        try:
            clickXpath('/html/body/form/div[4]/div[2]/table[1]/tbody/tr[1]/td[4]/select/option['+str(stamp)+']',driver)
        except:
            break
        stamp +=1
        try:
            current = textXpath('/html/body/form/div[5]/div[2]/div/table/tbody/tr[1]/td[2]/a', driver,10)
        except:
            current=''
        clickXpath('//*[@id="btnSearch"]',driver)
        sleep(3)
        try:
            while (current == textXpath('/html/body/form/div[5]/div[2]/div/table/tbody/tr[1]/td[2]/a', driver, 10)):
                sleep(3)
        except:
            stamp+=1
            continue
        readtype(driver)
