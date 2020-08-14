__Author__ = 'Lyy'

from time import sleep

import requests
import xlrd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, clickXpath, hrefXpath, clickforname
from Common import textXpath
import json

zzcount = 0
zznum=0
def readzzfromurl(href,qys):
    corpidtemp = href.split('=')
    corpid=corpidtemp[len(corpidtemp)-1]
    url = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid='+str(corpid)+'&isout='
    global zzcount
    respone = requests.get(url)
    content = respone.content.decode()
    data = json.loads(str(content)).get('data').get('ds1')
    qyname = json.loads(str(content)).get('data').get('ds')
    qyname1 = ''
    for i in qyname:
        qyname1 = i.get('corpname')
    for i in data:
        if i.get('mark') != None:
            zzcount=zzcount+1
            print(zzcount,qyname1, i.get('aptitudekindname'), i.get('mark'),href,qys)
    if zzcount>int(zznum):
        return False
    return True

def readpage(driver):
    flag = True
    stamp = 1
    # init
    textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[1]', driver, 120)

    while (flag):
        try:
            href = hrefXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[' + str(stamp) + ']/td[2]/a', driver, 1)
            qys=textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr['+str(stamp)+']/td[5]',driver)
            stopflag=readzzfromurl(href,qys)
            stamp += 1
            if not stopflag:
                print(zzcount, zznum)
                return False
        except:
            break
    return True

if __name__ == '__main__':
    driver= LoginUrl('http://gcxm.hunanjs.gov.cn/dataservice.html?queryType=0&keyword=')

    print("*1、页面拖动验证条；2、先选好起始爬取页")
    print("输入爬取资质数：")
    zznum=input()

    flag=True
    stamp=1
    while(flag):
        stopflag=readpage(driver)
        if not stopflag:
            break
        try:
            current=textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a',driver)
            a=current
            clickforname('/html/body/div[3]/div/section[2]/div/nav/ul/li[',1,']/a','下一页',driver)
            while(current==a):
                sleep(3)
                a=textXpath('/html/body/div[3]/div/section[1]/table/tbody/tr[1]/td[2]/a',driver)
        except:
            break
    print(0)