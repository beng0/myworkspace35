from selenium.webdriver.common.by import By
from  bst.bst_datatest.test_case.models.BasePage import BasePage

class  JstQyyjPage(BasePage):
    # 查企业
    qyyj_loc =(By.XPATH,'//*[@id="ul_search_list_menu"]/a[1]')
    # 云南省
    yunnansheng_loc =(By.XPATH,'//*[@id="div_province"]/a[25]')
    # 广东省
    guangdong_loc = (By.XPATH, '//*[@id="div_province"]/a[20]')
    # 所有的市
    all_shi_xpath='//*[@id="div_city"]/a'
    # 深圳市
    szshi_loc=(By.XPATH,'//*[@id="div_city"]/a[4]')  #//*[@id="div_city"]/a[4]
    #所有的区
    sz_all_qu_xpath='//*[@id="div_area"]/a'   #从2开始  //*[@id="div_area"]/a[3]
    # 查询按钮
    searchbutton_loc =(By.XPATH,'//*[@id="btn_search_company"]')
    # 当前页所有的企业信息
    datas_xpath ='/html/body/div[8]/div[2]/div[2]/ul/li'
    entname_text = './div[2]/div[1]/h2/a/text()'

    # 当前页码
    cur_ye = (By.XPATH, '/html/body/div[8]/div[2]/div[2]/div/div/div/label')

    # 返回当前页码
    def get_cur_yema(self):
        return self.find_element(*self.cur_ye).text

    # 要点击的某页
    def goto_yema_xpath(self, yema):
        return '/html/body/div[8]/div[2]/div[2]/div/div/div/a['+str(yema-1)+']'

    # 点击相应页面的页码
    def goto_yema(self, yema):
        self.goto_yema_loc = (By.XPATH, self.goto_yema_xpath(yema))
        self.find_element(*self.goto_yema_loc).click()

    def open(self):
        self.open_url()

    # 选择业务
    def select_yewu(self,yewu):
        if 'qyyj' == yewu:
            self.find_element(*self.qyyj_loc).click()

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
    def  get_element_shuxinzhi(self,suxin,qyyj_count,count=0):
                                # /html/body/div[8]/div[2]/div[2]/ul/li[1                      ]/div[2]/div[1]/h2/a
        element_loc = (By.XPATH, '/html/body/div[8]/div[2]/div[2]/ul/li[' + str(qyyj_count) + ']/div[2]/div[1]/h2/a')
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

    # 得到所有的市
    def  get_shilist_xpath(self):
        return  self.all_shi_xpath

    # 选择市
    def  select_shi(self,shi_count):
        self.all_shi_loc = (By.XPATH,self.all_shi_xpath+'['+str(shi_count)+']')
        return  self.find_element(*self.all_shi_loc).click()

    # 得到所有的区
    def get_sz_allqu_xpath(self):
        return self.sz_all_qu_xpath

    # 选择区
    def select_qu(self, qu_count):
        self.all_qu_loc = (By.XPATH, self.sz_all_qu_xpath + '[' + str(qu_count) + ']')
        return self.find_element(*self.all_qu_loc).click()