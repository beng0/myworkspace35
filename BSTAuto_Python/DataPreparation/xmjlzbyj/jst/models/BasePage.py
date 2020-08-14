from  selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):

    def __init__(self,driver,base_url):
        self.driver = driver
        self.base_url = base_url


    # def on_page(self,pagetitle):
    #     return pagetitle in self.driver.title

    # 以单下划线__开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。
    def __open(self,url):
        self.driver.get(url)
        self.driver.maximize_window()
        # assert self.on_page(pagetitle), u"打开页面失败 %s"%url


    def open_url(self):
        self.__open(self.base_url)

    # 重写元素定位方法
    def find_element(self,*loc):
        #return self.driver.find_element(*loc)
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print(u"%s 页面中未能找到 %s 元素"% (self, loc))

    # 重写switch_frame方法
    def switch_frame(self, loc):
        return self.driver.switch_to_frame(loc)

    # 定义script方法，用于执行js脚本，范围执行结果
    def script(self, js):
        self.driver.execute_script(js)

    # 重写定义send_keys方法
    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        try:
            loc = getattr(self, "_%s" % loc)  # getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))








