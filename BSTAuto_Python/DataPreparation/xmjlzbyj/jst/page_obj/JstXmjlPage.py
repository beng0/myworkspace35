from selenium.webdriver.common.by import By
from  bst.bst_datatest.test_case.models.BasePage import BasePage

class  JstXmjlPage(BasePage):
    # 项目经理
    xmjl_loc =(By.XPATH,'//*[@id="ul_search_list_menu"]/a[4]')
    # 云南省
    yunnansheng_loc =(By.XPATH,'//*[@id="div_province"]/a[25]')
    # 广东省
    guangdong_loc = (By.XPATH, '//*[@id="div_province"]/a[20]')
    # 所有的市
    all_shi_xpath='//*[@id="div_city"]/a'
    # 深圳市
    szshi_loc=(By.XPATH,'//*[@id="div_city"]/a[4]')
    # 查询按钮
    searchbutton_loc =(By.XPATH,'//*[@id="btn_search"]')
    # 当前页所有的人员信息
    datas_xpath ='/html/body/div[8]/div[2]/div[2]/ul/li'
    entname_text = './div[2]/div[1]/h2/a/text()'
    name_text='./div[2]/div[1]/h2/strong/a/text()'
    name_xpath='./div[2]/div[1]/h2/strong/a'
    # 当前页码
    cur_ye = (By.XPATH, '/html/body/div[8]/div[2]/div[2]/div/div/div/div/div/label')
                       # /html/body/div[8]/div[2]/div[2]/div/div/div/div/div/label

    # 返回当前页码
    def get_cur_yema(self):
        return self.find_element(*self.cur_ye).text

    # 要点击的某页
    def goto_yema_xpath(self, yema):
        return '/html/body/div[8]/div[2]/div[2]/div/div/div/div/div/a['+str(yema-1)+']'

    # 点击相应页面的页码
    def goto_yema(self, yema):
        self.goto_yema_loc = (By.XPATH, self.goto_yema_xpath(yema))
        self.find_element(*self.goto_yema_loc).click()

    def open(self):
        self.open_url()

    # 选择业务
    def select_yewu(self):
        self.find_element(*self.xmjl_loc).click()

    #选择省份
    def select_shengfen(self,shengfen):
        if 'yunnan' == shengfen:
            self.find_element(*self.yunnansheng_loc).click()
        elif 'shanxi' == shengfen:
            self.find_element(*self.shanxi_loc).click()
        elif 'guangdong' == shengfen:
            self.find_element(*self.guangdong_loc).click()

    def select_szshi(self):
        self.find_element(*self.szshi_loc).click()

    # 点击查询按钮
    def click_search_button(self):
        self.find_element(*self.searchbutton_loc).click()

    def  get_datas_xpath(self):
        return  self.datas_xpath

    # 返回企业名对应的xpath
    def get_entname_xpath(self,count=0):
        # return '/html/body/div[8]/div[2]/div[2]/ul/li['+str(count)+']/div[2]/div[1]/h2/a'
        return self.entname_text


    # 返回元素属性值
    def  get_element_shuxinzhi(self,suxin,xmjl_count,count=0):
        element_loc = (By.XPATH, '/html/body/div[8]/div[2]/div[2]/ul/li[' + str(xmjl_count) + ']/div[2]/div[1]/h2/strong/a')
        return self.find_element(*element_loc).get_attribute(suxin)

    def get_name_xpath(self, count=0):
        return self.name_text

    def  get_name_xpath2(self):
        return self.name_xpath


    # 返回人员资质对应的xpath
    def get_ryzz_xpath(self, count=0):
        # return '/html/body/div[8]/div[2]/div[2]/ul/li['+str(count)+']/div[2]/div[2]/dl/dd[1]'
        return self.ryzz_xpath

    # 返回人员资质
    def get_ryzz(self,count=0):
        self.ryzz_xpath =self.get_ryzz_xpath(count)
        return self.find_element(*self.ryzz_xpath).text.strip()


    def  get_shilist_xpath(self):
        return  self.all_shi_xpath

    def  select_shi(self,shi_count):
        self.all_shi_loc = (By.XPATH,self.all_shi_xpath+'['+str(shi_count)+']')
        return  self.find_element(*self.all_shi_loc).click()