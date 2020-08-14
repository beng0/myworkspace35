from selenium.webdriver.common.by import By
from  bst.bst_datatest.test_case.models.BasePage import BasePage

class  JstXmjlDetailPage(BasePage):
    # 当前页所有的公告信息
    datas_xpath ='//*[@id="newriskWrap"]/div[2]/ul/li'
    # //*[@id="newriskWrap"]/div[2]/ul/li[2]/div[2]/h2/a
    ggname_texts = './div[2]/h2/a/text()'
    # 中标日期
    zbtime_texts ='./div[5]/text()'
    # 中标来源
    zbly_text='./div[6]/a/text()'

    zbsl_text='//*[@id="newriskWrap"]/div[2]/ul/li[1]/div[2]/i'

    # 当前页码
    cur_ye = (By.XPATH, '//*[@id="newriskWrap"]/div[2]/div/div/div/label')

    # 返回当前页码
    def get_cur_yema_detail(self):
        return self.find_element(*self.cur_ye).text


    def open(self):
        self.open_url()

    def get_datas_xpaht(self):
        return self.datas_xpath

    def get_ggname(self):
        return  self.find_element(*self.ggname_loc).text.strip()

    def get_zbtime(self):
        return  self.find_element(*self.zbtime_loc).text.strip()

    def  goto_yema_detail(self,yema):
        self.goto_yema_loc2 =(By.XPATH,'//*[@id="newriskWrap"]/div[2]/div/div/div/input[1]')
        self.find_element(*self.goto_yema_loc2).clear()
        self.find_element(*self.goto_yema_loc2).send_keys(str(yema))
        #
        self.zhuandao_loc=(By.XPATH,'//*[@id="newriskWrap"]/div[2]/div/div/div/input[2]')
        self.find_element(*self.zhuandao_loc).click()
