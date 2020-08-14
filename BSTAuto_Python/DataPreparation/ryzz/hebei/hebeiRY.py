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

zzcount = 0
zznum = 0

if __name__ == '__main__':
    print('input current page:')
    currentpage = input()
    print('input pagesize(10/20/50/100/200/300/400):')
    pagesize = input()
    print("input stopnum:")
    zznum = input()
    url = "http://110.249.221.5:8005/api/queryPublicController/getPageInfoList?currentPage="+currentpage+"&pageSize="+pagesize+"&resId=76e2ec90-4f64-4fff-b752-555f7911a155&queryStr=%7B%22value%22:%22%22,%22columnName%22:%22XM%22%7D,%7B%22value%22:%22%22,%22columnName%22:%22CertID%22%7D&sortStr="
    # url = "http://110.249.221.5:8005/api/queryPublicController/getPageInfoList?currentPage=20&pageSize=20&resId=76e2ec90-4f64-4fff-b752-555f7911a155&queryStr=%7B%22value%22:%22%22,%22columnName%22:%22XM%22%7D,%7B%22value%22:%22%22,%22columnName%22:%22CertID%22%7D&sortStr="
    js=getjson(url)
    for i in js.get('rows'):
        zzcount+=1
        lxlist = i.get('ZSYXQJSSJ').split('（')
        if len(lxlist)<2 :
            lx = ''
        else:
            lx = lxlist[1].replace('）','')
        zhongbiaoren=i.get('QYMC')
        xmjl=i.get('XM')
        zz=i.get('SPECIALTYTYP')
        print(zzcount,'-',lx,'-',zhongbiaoren,'-',xmjl,'-',zz)
        if zzcount>int(zznum):
            break