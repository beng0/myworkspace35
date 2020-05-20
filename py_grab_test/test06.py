#coding=utf-8

from py_grab_test.selenium_base import *
from bs4 import BeautifulSoup

se = Base_()
se.open_("http://cx.jlsjsxxw.com/corpinfo/CorpInfo.aspx")

se.select_by_index("css selector","select#ddlCity",2)

se.select_by_index("css selector","select#ddlZzlx",2)
se.click_("xpath","//select[@id='ddlZzlx']/../../td[7]/input")

def get_soup(selector):
    strjs = '''return document.querySelector('%s').outerHTML'''%(selector)
    html = driver.execute_script(strjs)
    soup = BeautifulSoup(html,"html.parser")
    return soup

def get_soups(selectors):
    strjs = '''return document.querySelectorAll('%s')'''%(selectors)


soup = get_soup('#tbody_CorpInfo')
print(soup)