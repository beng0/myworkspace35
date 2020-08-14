__Author__ = 'Lyy'

from time import sleep
from urllib import parse

import requests
import xlrd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, clickXpath, hrefXpath, sendKeyXpath, clickforname
from Common import textXpath
import json

zzcount=0
zznum=0

def readzz(href):
    backend = href.split('personnum=')[1]
    backend= str(backend).replace('+','%2B')
    backend = str(backend).replace(' ', '%20')
    url = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getPersonDetail&personnum='+backend
    respone = requests.get(url)
    content = respone.content.decode()
    js = json.loads(str(content))
    if js.get('data') != None:
        zzl = js.get('data').get('ds1')
        global zzcount
        for i in zzl:
            name = i.get('personname')
            specialtytypename = i.get('specialtytypename')
            corpname = i.get('corpname')
            zczyname=i.get('zczyname')
            zzcount+=1
            print(zzcount,'-',corpname, '-', name, '-' ,zczyname,'-', specialtytypename,'-',href)
    if zzcount>int(zznum):
        zzcount=0
        return False
    return True

def readpage(driver):
    flag = True
    stamp = 1
    while (flag):
        try:
            href = hrefXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[' + str(stamp) + ']/td[2]/a', driver, 1)
        except:
            break
        stopflag=readzz(href)
        stamp += 1
        if not stopflag:
            return False
    return True

def jumpage(startpage,driver):
    currentindex = ''
    stamp = 1
    max = 5
    while (currentindex != str(startpage)):
        try:
            currentindex = textXpath('/html/body/div[3]/div/section[2]/div/nav/ul/li[' + str(stamp) + ']/a', driver)
        except:
            try:
                current = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
                a = current
                clickforname('/html/body/div[3]/div/section[2]/div/nav/ul/li[', 1, ']/a', str(max), driver)
                while (current == a):
                    sleep(3)
                    a = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
                max += 5
                stamp = 0
                current = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
                a = current
                clickforname('/html/body/div[3]/div/section[2]/div/nav/ul/li[', 1, ']/a', '下一页', driver)
                while (current == a):
                    sleep(3)
                    a = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
            except:
                break
        stamp += 1

def readlx(startpage,driver):
    jumpage(startpage, driver)

    flag = True
    while (flag):
        stopflag = readpage(driver)
        if not stopflag:
            break
        try:
            current = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
            a = current
            clickforname('/html/body/div[3]/div/section[2]/div/nav/ul/li[', 1, ']/a', '下一页', driver)
            while (current == a):
                sleep(3)
                a = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
        except:
            break

if __name__ == '__main__':
    driver = LoginUrl('http://gcxm.hunanjs.gov.cn/dataservice.html')
    print("*页面打开后拖动验证条")
    print("*选择从业人员\人员类别")
    print("每类输入需要的资质数:")
    zznum=input()
    print("输入起始页:")
    startpage=input()
    clickXpath('//*[@id="Chkitem2"]',driver)
    sleep(3)
    clickXpath('//*[@id="persontype_2"]',driver,5)
    flag=True
    stamp=2
    while(flag):
        try:
            clickXpath('/html/body/ul[3]/li[1]/div[1]/select/option['+str(stamp)+']',driver,1)
        except:
            break
        stamp+=1
        current = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
        a = current
        clickXpath('//*[@id="btnSearch2"]', driver)
        while (current == a):
            sleep(3)
            a = textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a', driver)
        readlx(startpage,driver)

    print('exit 0')