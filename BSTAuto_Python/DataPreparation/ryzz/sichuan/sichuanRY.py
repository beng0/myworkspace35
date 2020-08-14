__Author__ = 'Lyy'
# 四川人员官网数据准备
# 官网无翻页功能，准备方式为每类型人员获取一页数据

from time import sleep

import requests
import xlrd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, clickXpath, hrefXpath, sendKeyXpath
from Common import textXpath
import json

zzcount=0

def readryzz(href):
    global zzcount
    idt = href.split('=')
    id=idt[len(idt)-1]
    url='http://202.61.88.193:89//api/getdata/GetryZsList/'+id
    headers = {
        'Host': '202.61.88.193:89',
        'Connection': 'keep - alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Origin': 'http://jst.sc.gov.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    respones = requests.get(url, headers=headers)
    content = respones.content.decode()
    st = json.loads(str(content))
    for i in st:
        name = i.get('XM')
        zczy = i.get('ZCZY')
        zslxname = i.get('ZSLXNAME')
        zshsname = i.get('ZSJSNAME')
        qymc = i.get('QYMC')
        zzcount+=1
        print(zzcount,'-',qymc,'-',name, '-', zczy, '-', zslxname, '-', zshsname,'-',href)

def readpage(driver):
    flag = True
    stamp = 1
    while (flag):
        try:
            href = hrefXpath('/html/body/form/div[5]/div/div/div/div[2]/table/tbody/tr[' + str(stamp) + ']/td[2]/a',
                             driver)
        except:
            break
        stamp += 1
        readryzz(href)

if __name__ == '__main__':
    driver= LoginUrl('http://jst.sc.gov.cn/xxgx/Person/rList.aspx')
    href = hrefXpath('/html/body/form/div[5]/div/div/div/div[2]/table/tbody/tr[1]/td[2]/a', driver, 120)

    flag=True
    stamp=2
    while(flag):
        clickXpath('/html/body/form/div[5]/div/div/div/div[1]/div/fieldset/table/tbody/tr[1]/td[2]/select', driver)
        try:
            clickXpath('/html/body/form/div[5]/div/div/div/div[1]/div/fieldset/table/tbody/tr[1]/td[2]/select/option['+str(stamp)+']',driver)
        except:
            break
        next = True
        try:
            current=textXpath('/html/body/form/div[5]/div/div/div/div[2]/table/tbody/tr[1]/td[2]/a',driver)
        except:
            current=''
        a = current
        clickXpath('//*[@id="MainContent_Button1"]', driver)
        while(a==current):
            sleep(3)
            try:
                a=textXpath('/html/body/form/div[5]/div/div/div/div[2]/table/tbody/tr[1]/td[2]/a',driver)
            except:
                next=False
                break
        stamp+=1
        if next:
            readpage(driver)

    print(0)