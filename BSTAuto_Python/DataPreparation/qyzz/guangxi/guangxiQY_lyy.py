__author__ = 'Lyy'

from time import sleep
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, textXpath, clickXpath, hrefXpath, LoginUrlChrome, clickforname, LoginUrIE
import requests
import json

zzcount=0
zznum=0

def readzz(url):
    respone = requests.get(url)
    content = respone.content.decode()
    qynamel = re.findall('<span id="ContentPlaceHolder1_DanWeiName_8344" style="display:inline-block;">(.+?)</span>', content)
    if len(qynamel)!=0:
        qyname = qynamel[0]
    else:
        return True
    qydql = re.findall('<span id="ContentPlaceHolder1_AreaName_8344" style="display:inline-block;">(.+?)</span>', content)
    if len(qydql)!=0:
        qydq = qydql[0]
    else:
        qydq = ''
    tllist = re.findall('<td class="company_details_more_content_table_field_value" style="width:250px">(.+?)</td>',
                        content)
    global zzcount
    for i in tllist:
        if i.find('<br/>') >= 0:
            zzl = i.split('<br/>')
            for j in zzl:
                if j != '':
                    zzcount += 1
                    print(zzcount, '-', qydq, '-', qyname, '-', j)
    if zzcount>int(zznum):
        return False
    else:
        return True

def readpage(driver):
    flag = True
    stamp = 1
    while (flag):
        stamp += 1
        try:
            href = hrefXpath('//*[@id="ContentPlaceHolder1_List_Datagrid1"]/tbody/tr[' + str(stamp) + ']/td[2]/a',
                             driver)
            if not readzz(href):
                return False
            else:
                _=1
        except:
            flag = False
            break
    return True

if __name__ == '__main__':
    url='http://dn4.gxzjt.gov.cn:1141/WebInfo/Default.aspx'
    driver = LoginUrIE(url)
    print('input zznum:')
    zznum=input()

    flag = True
    stamp = 1

    while(flag):
        if not readpage(driver):
            break
        current = textXpath('//*[@id="ContentPlaceHolder1_List_Datagrid1"]/tbody/tr[2]/td[2]/a',driver)
        clickforname('//*[@id="ContentPlaceHolder1_List_Pager"]/table/tbody/tr/td[2]/a[', stamp, ']', '下一页>', driver)
        while(current==textXpath('//*[@id="ContentPlaceHolder1_List_Datagrid1"]/tbody/tr[2]/td[2]/a',driver,3)):
            sleep(3)
