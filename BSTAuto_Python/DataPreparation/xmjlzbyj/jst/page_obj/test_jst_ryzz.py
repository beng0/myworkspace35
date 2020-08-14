import unittest
from bst.bst_datatest.test_case.page_obj.jst.JstRyzzPage import *
from selenium  import webdriver
from time import sleep
from lxml import etree
from lmf.dbv2 import db_write
import pandas as pd
from bst.bst_datatest.test_case.models.get_db_excel import  *
from bst.bst_datatest.test_case.models.moni_ip import *

class  TestGetJstRyzz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tablenamehouzui = datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        # cls.driver = webdriver.Chrome()
        # cls.base_url ="https://hhb.cbi360.net/tenderbangsoso/"
        chromeOptions = webdriver.ChromeOptions()
        ip = get_ip()
        # 设置代理
        chromeOptions.add_argument("--proxy-server=http://%s" % (ip))
        # cls.driver = webdriver.Chrome()
        cls.driver = webdriver.Chrome(chrome_options=chromeOptions)
        cls.base_url = "https://hhb.cbi360.net/tenderbangsoso/"

        # 查看本机ip，查看代理是否起作用
        cls.driver.get("http://httpbin.org/ip")
        print(cls.driver.page_source)


    @classmethod
    def tearDownClass(cls):
        # pass
        cls.driver.quit()

    def get_jst_ryzz(self,jst_ryzz_page,conp,total_ye,shengfen,yewu,tablename,shi=None,):
            # 选择人员资质
            jst_ryzz_page.select_yewu()
            # 选择省份
            jst_ryzz_page.select_shengfen(shengfen)
            # 选择市
            if shi != None:
                jst_ryzz_page.select_shi(shi)

            page = self.driver.page_source
            # print(page)
            body = etree.HTML(page)
            ryzzlb_count =2
            # 得到所有的人员资质类别
            ryzzs = body.xpath(jst_ryzz_page.get_ryzzs_xpath())[2:]
            # print("ryzzs  "+ryzzs)
            for ryzzlb  in  ryzzs:
                # print("ryzzlb  " + ryzzlb)
                # 选择人员资质类别
                jst_ryzz_page.select_ryzzlb(ryzzlb_count)
                sleep(5)
                ryzzlb_count +=1
                # 点击搜索按钮
                jst_ryzz_page.click_search_button()
                sleep(3)
                for  gotoyema in range(1,total_ye):
                    # 获得当前页面
                    cur_yema = jst_ryzz_page.get_cur_yema()
                    # 翻页
                    if int(cur_yema) != int(gotoyema):
                        jst_ryzz_page.goto_yema(gotoyema)
                        sleep(3)

                    data =[]
                    page = self.driver.page_source
                    # print(page)
                    body = etree.HTML(page)
                    content_list = body.xpath(jst_ryzz_page.get_datas_xpath())
                    for content in content_list:
                        entname = content.xpath(jst_ryzz_page.get_entname_xpath())[0].strip()
                        print("entname  " + entname)
                        name = content.xpath(jst_ryzz_page.get_name_xpath())[0].strip()
                        print("name  " + name)
                        ryzz =content.xpath(jst_ryzz_page.get_ryzz_xpath())[0].strip()
                        print("ryzz  " + ryzz)
                        tmp = [entname,name, ryzz]
                        data.append(tmp)
                    # print(data)
                    df = pd.DataFrame(data=data, columns=["entname", "name", "ryzz"])
                    db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

    def out_data(self,dbtype, conp, mySchema, tablename, outfilename):
        sql_query_all = '''select * from "{mySchema}"."{tablename}" '''.format(mySchema=mySchema, tablename=tablename)
        result = db_query(sql_query_all, dbtype=dbtype, conp=conp)
        read_db_2_excel(conp, outfilename, result)


    def qtest_1_get_jst_ryzz_yunnan(self):
        conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        total_ye = 3
        yewu = 'ryzz'
        shengfen='yunnan'
        tablename='jst_ryzz_yunnan'+self.tablenamehouzui
        outfilename =r"D:\筑龙项目\人员资质测试\jianshetong\建设通云南人员资质"

        jst_ryzz_page = JstRyzzPage(self.driver, self.base_url)
        jst_ryzz_page.open()
        s = input("input  your  unm: ")
        if int(s) == 1:
            for gotoyema  in  range(1,total_ye):
                self.get_jst_ryzz(jst_ryzz_page,conp,gotoyema,shengfen,yewu,tablename)
                print("共获取" + str(total_ye-1) + "页，已完成" + str(gotoyema) + "页")
        #            (dbtype, conp, mySchema, tablename, outfilename)
        self.out_data('postgresql', conp, 'zl_test', tablename, outfilename)

    def qtest_2_get_jst_ryzz_shanxi(self):
        conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        total_ye = 3
        yewu = 'ryzz'
        shengfen='shanxi'
        tablename='jst_ryzz_shanxi'+self.tablenamehouzui
        outfilename = r"D:\筑龙项目\人员资质测试\jianshetong\建设通山西人员资质"

        jst_ryzz_page = JstRyzzPage(self.driver, self.base_url)
        # jst_ryzz_page.open()
        # s = input("input  your  unm: ")
        # if int(s) == 1:
        for gotoyema in range(1, total_ye):
            self.get_jst_ryzz(jst_ryzz_page, conp, gotoyema, shengfen, yewu, tablename)
            print("共获取" + str(total_ye - 1) + "页，已完成" + str(gotoyema) + "页")

        self.out_data('postgresql', conp, 'zl_test', tablename, outfilename)

    def test_1_get_jst_ryzz_guangdong(self):
        conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        total_ye = 3
        yewu = 'ryzz'
        shengfen='guangdong'
        shi = 'sz'
        tablename='jst_ryzz_sz'+self.tablenamehouzui
        outfilename = r"D:\筑龙项目\人员资质测试\jianshetong\建设通深圳人员资质"

        jst_ryzz_page = JstRyzzPage(self.driver, self.base_url)
        jst_ryzz_page.open()
        s = input("input  your  unm: ")
        if int(s) == 1:
            self.get_jst_ryzz(jst_ryzz_page, conp, total_ye, shengfen, yewu, tablename,shi)
            # print("共获取" + str(total_ye - 1) + "页，已完成" + str(gotoyema) + "页")
        self.out_data('postgresql', conp, 'zl_test', tablename, outfilename)






if  __name__ == '__main__':
        unittest.main(verbosity=2)
        # print("%s 页面中未能找到 %s 元素" % ("2", "8"))

