from selenium.webdriver.common.by import By
from  bst.bst_datatest.test_case.models.BasePage import BasePage

class  JstXmjlDetailPage(BasePage):
    # 当前页所有的公告信息
    datas_xpath ='//*[@id="newriskWrap"]/div[2]/ul/li'
                # //*[@id="newriskWrap"]/div[2]/ul/li[2]/div[2]/h2/a
    ggname_texts = './div[2]/h2/a/text()'
    zbtime_texts ='./div[5]/text()'


    def open(self):
        self.open_url()

    def get_datas_xpaht(self):
        return self.datas_xpath

    def get_ggname(self):
        return  self.find_element(*self.ggname_loc).text.strip()

    def get_zbtime(self):
        return  self.find_element(*self.zbtime_loc).text.strip()
