__author__ = 'Lyy'

from time import sleep
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import xlrd
from Common import LoginUrl, textXpath, clickXpath, hrefXpath, LoginUrlChrome, clickforname, LoginUrIE, initwait, \
    sendKeyXpath
import requests
import json

zzcount=0
zzallcount=0
zznum=0

def readzz(driver):
    initwait('//*[@id="Table2"]/tbody/tr[1]/td/strong',driver)
    name = textXpath('//*[@id="FormView1_xmLabel"]',driver)
    qyname = textXpath('//*[@id="FormView1"]/tbody/tr/td/table/tbody/tr[1]/td[4]/a', driver)
    href = driver.current_url
    global zzcount
    global zzallcount
    stamp = 1
    while(True):
        try:
            zz =textXpath('/html/body/form/div[3]/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr['+str(stamp)+']/td[1]',driver)
            zzlx =textXpath('/html/body/form/div[3]/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr['+str(stamp)+']/td[5]',driver)
            zzdj = textXpath('/html/body/form/div[3]/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr['+str(stamp)+']/td[4]',driver)
            stamp+=1
            if zz!= '':
                zzcount+=1
                zzallcount+=1
                print(zzallcount,zzlx,qyname,name,zz,zzdj,href)
        except:break
    if zzcount>int(zznum):
        zzcount=0
        return False
    else:
        return True

def readpage(driver):
    flag = True
    stamp = 1
    global zzcount
    while (flag):
        try:
            handle = driver.current_window_handle
            clickXpath('/html/body/form/div[3]/div/table[5]/tbody/tr/td/table[1]/tbody/tr['+str(stamp)+']/td[7]/a',driver)
            stamp+=1
            handles = driver.window_handles
            for newhandle in handles:
                if newhandle != handle:
                    driver.switch_to.window(newhandle)
                    try:
                        flag = readzz(driver)
                    except:
                        driver.close()
                        driver.switch_to.window(handle)
                        continue
                    driver.close()
                    driver.switch_to.window(handle)
                    if not flag:
                        return False

        except:
            break
    zzcount=0
    return True

def readexcel(driver):
    data = xlrd.open_workbook('F:\workplace\SVN\数据对比\数据准备\企业资质\天津\天津企业资质数据准备_赖逸咏_20200518.xlsx')
    table = data.sheet_by_name('Sheet5')
    stamp = 0
    while (True):
        try:
            key = table.cell(stamp, 0).value
        except:
            break
        if key != '':
            searchKey(driver,key)
            stamp += 1

def searchKey(driver,key):
    sendKeyXpath('/html/body/form/div[3]/div/table[3]/tbody/tr/td/table/tbody/tr[2]/td[6]/input',key,driver)
    try:
        current = textXpath('/html/body/form/div[3]/div/table[5]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]',driver)
    except:
        current=''
    clickXpath('/html/body/form/div[3]/div/table[3]/tbody/tr/td/table/tbody/tr[4]/td/input[1]',driver)
    try:
        while (current == textXpath('/html/body/form/div[3]/div/table[5]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]', driver,3)):
            sleep(3)
    except:
        return
    readpage(driver)


if __name__ == '__main__':
    url='http://218.69.33.182/epr/Search/C_Common/CP/index.aspx'
    driver = LoginUrlChrome(url)
    print("input each ent zznum:")
    zznum=input()

    readexcel(driver)

    # stamp = 5
    # while (True):
    #     flag = readpage(driver)
    #     if not flag:
    #         break
    #     current = textXpath('/html/body/form/div[3]/div/div/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]', driver)
    #     clickforname('//*[@id="ASPxGridView2_ctl04"]/tbody/tr/td/table/tbody/tr/td[', stamp, ']', '下一页', driver)
    #     while (current == textXpath('/html/body/form/div[3]/div/div/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]', driver,3)):
    #         sleep(3)
    driver.quit()