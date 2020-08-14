__Author__ = "Lyy"

from urllib import parse
from time import sleep

import requests
import xlrd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, clickXpath, hrefXpath, sendKeyXpath, clickforname, getjson
from Common import textXpath
import json

zzcount=0
zznum=0

def readqyzz(js):
    qyname = js.get('QYMC')
    qylx = js.get('CERTTYPE')
    zzdjlist = js.get('ZZDJ').split(';')
    global zzcount
    for i in zzdjlist:
        zzcount += 1
        print(zzcount, '-', qyname, '-', qylx, '-', i)
    if zzcount>int(zznum):
        return False
    return True

if __name__ == '__main__':
    print('input current page:')
    currentpage = input()
    print('input pagesize(10/20/50/100/200/300/400):')
    pagesize = input()
    print("input stopnum:")
    zznum = input()
    url = "http://110.249.221.5:8005/api/queryPublicController/getPageInfoList?currentPage="+currentpage+"&pageSize="+pagesize+"&resId=cd78f6cd-6d02-4f5c-a1da-10aafa71c9df&queryStr=%7B%22value%22:%22%22,%22columnName%22:%22CERTID%22%7D,%7B%22value%22:%22%22,%22columnName%22:%22QYMC%22%7D,%7B%22value%22:%22%22,%22columnName%22:%22CERTTYPE%22%7D&sortStr="
    print(url)
    js = getjson(url)
    rslist = js.get("rows")
    for i in rslist:
        stopflag=readqyzz(i)
        if not stopflag:
            break
