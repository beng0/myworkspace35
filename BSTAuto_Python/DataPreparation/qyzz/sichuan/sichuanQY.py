__author__ = 'Lyy'

from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Common import LoginUrl, textXpath, clickXpath
import requests
import json

zzcount=0

def getzzfromcompnay(url,href):
    headers = {
        'Host': '202.61.88.193:89',
        'Connection': 'keep - alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Origin': 'http://jst.sc.gov.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    response = requests.get(url, headers=headers)
    content = response.content.decode()
    st = json.loads(str(content))
    for i in st:
        zslxmc = i.get('ZSLXMC')
        zsDe = i.get('zsDetial')
        for j in zsDe:
            zzlisttemp = j.get('ZZX')
            if zzlisttemp != None:
                for k in zzlisttemp.split('<br>'):
                    global zzcount
                    zzcount = zzcount+1
                    print(zzcount,zslxmc, j.get('QYMC'), k,href)

def searchcompany(name,driver):
    divstr = '//*[@id="mc"]'
    resultLocator = (By.XPATH, divstr)
    WebDriverWait(driver, 120).until(EC.presence_of_element_located(resultLocator)).clear()
    WebDriverWait(driver, 120).until(EC.presence_of_element_located(resultLocator)).send_keys(name)

    divstr = '/html/body/form/div[5]/div/div/div/div[2]/table/tbody/tr[1]/td[1]/a'
    resultLocator = (By.XPATH, divstr)
    current = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
    a=current

    divstr = '//*[@id="MainContent_Button1"]'
    resultLocator = (By.XPATH, divstr)
    WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).click()

    href=''
    while(a==current):
        sleep(3)
        divstr = '/html/body/form/div[5]/div/div/div/div[2]/table/tbody/tr[1]/td[1]/a'
        resultLocator = (By.XPATH, divstr)
        a = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).text
        divstr = '/html/body/form/div[5]/div/div/div/div[2]/table/tbody/tr[1]/td[1]/a'
        resultLocator = (By.XPATH, divstr)
        href = WebDriverWait(driver, 1).until(EC.presence_of_element_located(resultLocator)).get_attribute('href')

    return href

def openquanguogw(driver2):

    divstr = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div/div[2]/span[4]'
    resultLocator = (By.XPATH, divstr)
    WebDriverWait(driver2, 120).until(EC.presence_of_element_located(resultLocator)).click()

    divstr = '/html/body/div/div/div/div[2]/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[1]/input'
    resultLocator = (By.XPATH, divstr)
    WebDriverWait(driver2, 2).until(EC.presence_of_element_located(resultLocator)).click()

    divstr = '/html/body/div[2]/div[1]/div[1]/ul/li[23]'
    resultLocator = (By.XPATH, divstr)
    WebDriverWait(driver2, 2).until(EC.presence_of_element_located(resultLocator)).click()

    divstr = '//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/span'
    resultLocator = (By.XPATH, divstr)
    current = WebDriverWait(driver2, 2).until(EC.presence_of_element_located(resultLocator)).text

    divstr = '//*[@id="app"]/div/div/div[2]/div[2]/div[3]/div[3]/div/span'
    resultLocator = (By.XPATH, divstr)
    WebDriverWait(driver2, 2).until(EC.presence_of_element_located(resultLocator)).click()

    a = current
    while (current == a):
        sleep(3)
        divstr = '//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/span'
        resultLocator = (By.XPATH, divstr)
        a = WebDriverWait(driver2, 2).until(EC.presence_of_element_located(resultLocator)).text

def readqyname(driver,driver2):
    flag = True
    stamp = 1
    while (flag):
        try:
            temp = textXpath('/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[' + str(
                stamp) + ']/td[3]/div/span', driver2)
            href = searchcompany(temp, driver)
            idlist=href.split('=')
            id = idlist[len(idlist)-1]
            url = "http://202.61.88.193:89//api/getdata/GetEnteZsList/" + id
            getzzfromcompnay(url,href)
            stamp += 1
        except:
            flag = False
            break

def currentpage(driver,driver2):
    flag = True
    stamp = 1
    while (flag):
        try:
            name = textXpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[' + str(stamp) + ']/td[3]/div/span',
                driver2)
            readqyname(driver,driver2)
            stamp += 1
        except:
            break

if __name__ == '__main__':
    driver = LoginUrl("http://jst.sc.gov.cn/xxgx/Enterprise/eList.aspx")
    driver2 = LoginUrl("http://jzsc.mohurd.gov.cn/data/company?complexname=")

    openquanguogw(driver2)

    print('input zznum:')
    zznum=input()
    flag=True
    stamp=1
    while(flag):
        readqyname(driver,driver2)
        try:
            current=textXpath('/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/span',driver2)
            a=current
            clickXpath('/html/body/div[1]/div/div/div[2]/div[3]/div[2]/button[2]/i',driver2)
            while(a==current):
                sleep(3)
                a=textXpath('/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/span',driver2)
        except:
            break
        if zzcount>int(zznum):
            flag=False