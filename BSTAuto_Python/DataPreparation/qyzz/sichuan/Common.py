__Author__ = 'Lyy'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

def LoginUrl(url):
    d=webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe')
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