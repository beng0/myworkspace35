from selenium import webdriver

def LoginUrl(url):
    d=webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe')
    d.maximize_window()
    d.get(url)
    return d