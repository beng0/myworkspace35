from selenium.webdriver.common.by import By
from  bst.bst_datatest.test_case.models.BasePage import BasePage

class  JstQyyjDetailPage(BasePage):
    # 当前页所有的公告信息
    datas_xpath ='/html/body/div[8]/div[4]/div[2]/ul/li'
                # /html/body/div[8]/div[4]/div[2]/ul/li[2]
    ggname_texts = './div[2]/h2/a/text()'
    xmjl_texts = './div[4]/a/text()'   #/html/body/div[8]/div[4]/div[2]/ul/li[2]/div[4]/a
    zbtime_texts ='./div[6]/text()'


    def open(self):
        self.open_url()

    def get_datas_xpaht(self):
        return self.datas_xpath

    def get_ggname(self):
        return  self.find_element(*self.ggname_loc).text.strip()

    def get_xmjl(self):
        pass

    def get_zbtime(self):
        return  self.find_element(*self.zbtime_loc).text.strip()
