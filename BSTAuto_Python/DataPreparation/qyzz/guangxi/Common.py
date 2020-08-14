__Author__ = 'Lyy'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import requests
import json

def LoginUrl(url):
    d=webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe',                        desired_capabilities={ 'platform': 'ANY',
                                               'browserName': 'chrome',
                                               'version': "",
                                               'javascriptEnabled': True
                                            })
    #d.maximize_window()
    d.get(url)
    return d

def LoginUrlChrome(url):
    d=webdriver.Chrome()
    #d.maximize_window()
    d.get(url)
    return d

def LoginUrIE(url):
    d=webdriver.Ie()
    #d.maximize_window()
    d.get(url)
    return d

def textXpath(xpath,driver,wait=1):
    resultLocator = (By.XPATH, xpath)
    return WebDriverWait(driver, wait).until(EC.presence_of_element_located(resultLocator)).text

def clickXpath(xpath,driver,wait=1):
    resultLocator = (By.XPATH, xpath)
    return WebDriverWait(driver, wait).until(EC.presence_of_element_located(resultLocator)).click()

def hrefXpath(xpath,driver,wait=1):
    resultLocator = (By.XPATH, xpath)
    return WebDriverWait(driver, wait).until(EC.presence_of_element_located(resultLocator)).get_attribute('href')

def clickforname(xpathstart,stamp,xpathend,name,driver,wait=1):
    flag= True
    while(flag):
        resultLocator = (By.XPATH, xpathstart+str(stamp)+xpathend)
        try:
            bt=WebDriverWait(driver, wait).until(EC.presence_of_element_located(resultLocator))
        except:
            break
        if bt.text==name:
            return bt.click()
        else:
            stamp += 1

def sendKeyXpath(xpath,searchkey,driver,wait=1):
    resultLocator = (By.XPATH, xpath)
    key=WebDriverWait(driver, wait).until(EC.presence_of_element_located(resultLocator))
    key.clear()
    key.send_keys(searchkey)

def getjson(url):
    respone = requests.get(url)
    content = respone.content.decode()
    js=json.loads(str(content))
    return js