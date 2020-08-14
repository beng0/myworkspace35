from selenium.webdriver.common.by import By
from  bst.bst_datatest.test_case.models.BasePage import BasePage

class  JstRyzzPage(BasePage):
    # 人员资质
    ryzz_loc =(By.XPATH,'//*[@id="ul_search_list_menu"]/a[3]')
    # 云南省
    yunnansheng_loc =(By.XPATH,'//*[@id="div_province"]/a[25]')
    # 山西省
    shanxi_loc = (By.XPATH, '//*[@id="div_province"]/a[8]')
    # 广东省
    guangdong_loc = (By.XPATH, '//*[@id="div_province"]/a[20]')
    # 深圳市
    sz_loc=(By.XPATH,'//*[@id="div_city"]/a[4]')
    # 浙江
    zhejiang_loc=(By.XPATH,'//*[@id="div_province"]/a[12]')


    # 查询按钮
    searchbutton_loc =(By.XPATH,'//*[@id="btn_search"]')
    # 当前页所有的人员信息
    datas_xpath ='/html/body/div[8]/div[2]/div[2]/ul/li'
    entname_xpath = './div[2]/div[1]/h2/a/text()'
    name_xpath='./div[2]/div[1]/h2/strong/a/text()'
    ryzz_xpath = './div[2]/div[2]/dl/dd[1]/text()'
    # 获取所有的人员资质类别
    ryzzs_xpath='//*[@id="div_category"]/a'


    # 当前页码         /html/body/div[8]/div[2]/div[2]/div/div/div/label
    cur_ye=(By.XPATH,'/html/body/div[8]/div[2]/div[2]/div/div/div/label')


    def open(self):
        self.open_url()

    # 选择业务
    def select_yewu(self):
        self.find_element(*self.ryzz_loc).click()

    #选择省份
    def select_shengfen(self,shengfen):
        if 'yunnan' == shengfen:
            self.find_element(*self.yunnansheng_loc).click()
        elif 'shanxi' == shengfen:
            self.find_element(*self.shanxi_loc).click()
        elif 'guangdong' == shengfen:
            self.find_element(*self.guangdong_loc).click()
        elif 'zhejiang' == shengfen:
            self.find_element(*self.zhejiang_loc).click()

    # 选择市
    def select_shi(self, shi):
        if 'sz' == shi:
            self.find_element(*self.sz_loc).click()

    # 得到所有的人员资质xapth
    def  get_ryzzs_xpath(self):
        return  self.ryzzs_xpath

    def  get_ryzzlb_count_xpath(self,ryzzlb_count):
        return '//*[@id="div_category"]/a['+str(ryzzlb_count)+']'
    # 选择人员资质类别
    def  select_ryzzlb(self,ryzzlb_count):
        self.ryzzlb_loc=(By.XPATH,self.get_ryzzlb_count_xpath(ryzzlb_count))
        self.find_element(*self.ryzzlb_loc).click()

    # 点击查询按钮
    def click_search_button(self):
        self.find_element(*self.searchbutton_loc).click()

    def  get_datas_xpath(self):
        return  self.datas_xpath

    # 返回企业名对应的xpath
    def get_entname_xpath(self,count=0):
        # return '/html/body/div[8]/div[2]/div[2]/ul/li['+str(count)+']/div[2]/div[1]/h2/a'
        return self.entname_xpath


    # 返回企业名
    def get_entname(self,count=0):
        self.entname_xpath =self.get_entname_xpath(count)
        return self.find_element(*self.entname_xpath).text.strip()


    # 返回姓名对应的xpath
    def get_name_xpath(self, count=0):
        # return '/html/body/div[8]/div[2]/div[2]/ul/li[' + str(count) + ']/div[2]/div[1]/h2/strong/a'
        return self.name_xpath

    # 返回姓名
    def get_name(self,count=0):
        self.name_xpath =self.get_entname_xpath(count)
        return self.find_element(*self.name_xpath).text.strip()

    # 返回人员资质对应的xpath
    def get_ryzz_xpath(self, count=0):
        # return '/html/body/div[8]/div[2]/div[2]/ul/li['+str(count)+']/div[2]/div[2]/dl/dd[1]'
        return self.ryzz_xpath

    # 返回人员资质
    def get_ryzz(self,count=0):
        self.ryzz_xpath =self.get_ryzz_xpath(count)
        return self.find_element(*self.ryzz_xpath).text.strip()

    # 返回当前页码
    def get_cur_yema(self):
        return self.find_element(*self.cur_ye).text

    # 跳到某个页码输入框的xpath
    def goto_yema_xpath(self,yema):
        return '/html/body/div[8]/div[2]/div[2]/div/div/div/a['+str(yema-1)+']'
    #           /html/body/div[8]/div[2]/div[2]/div/div/div/a[1]

    def  goto_yema(self,yema):
        self.goto_yema_loc =(By.XPATH,self.goto_yema_xpath(yema))
        self.find_element(*self.goto_yema_loc).click()

    #
    def  goto_yema2(self,yema):
        self.goto_yema_loc2 =(By.XPATH,'/html/body/div[8]/div[2]/div[2]/div/div/div/input[1]')
        self.find_element(*self.goto_yema_loc2).clear()
        self.find_element(*self.goto_yema_loc2).send_keys(str(yema))
        #                            /html/body/div[8]/div[2]/div[2]/div/div/div/input[2]
        self.zhuandao_loc=(By.XPATH,'/html/body/div[8]/div[2]/div[2]/div/div/div/input[2]')
        self.find_element(*self.zhuandao_loc).click()
