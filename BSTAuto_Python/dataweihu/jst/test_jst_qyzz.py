import unittest
from bst.bst_datatest.test_case.page_obj.jst.JstQyzzPage import *
from selenium import webdriver
from time import sleep
from lxml import etree
from lmf.dbv2 import db_write
import pandas as pd
from selenium import webdriver
from bst.bst_datatest.test_case.models.get_driver_moni_ip import *
from bst.bst_datatest.test_case.models.get_db_excel import *

class  TestGetJstRyzz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tablenamehouzui = datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        cls.driver = get_driver_moni_ip()
        cls.base_url = "https://hhb.cbi360.net/tenderbangsoso/"

        # 查看本机ip，查看代理是否起作用
        cls.driver.get("http://httpbin.org/ip")
        print(cls.driver.page_source)


    @classmethod
    def tearDownClass(cls):
        pass
        # cls.driver.quit()

    def get_jst_qyzz(self,data_page,conp,total_ye,gotoyema,shengfen,yewu,tablename,data,shi=None,):
        # 选择企业资质
        data_page.select_yewu(yewu)
        # 选择省份
        data_page.select_shengfen(shengfen)
        # 选择市
        if shi != None:
            data_page.select_shi(shi)

        # 点击搜索按钮
        data_page.click_search_button()
        sleep(3)

        # 获得当前页码
        cur_yema = data_page.get_cur_yema()
        # 翻页
        if int(cur_yema) != int(gotoyema):
            data_page.goto_yema(gotoyema)
            sleep(3)


        page = self.driver.page_source
        body = etree.HTML(page)
        # print(body)
        # 得到当前页面所有的企业
        qys = body.xpath(data_page.get_qys_xpath())
        # print(qys)
        for qy  in  qys:
            qyname=qy.xpath(data_page.get_entname_xpath())[0].strip()
            print(qyname)
            #点击更多按钮
            data_page.click_gengduo_button()
            sleep(2)

            #获得一家企业的所有企业资质
            oneqy_all_qyzzs = qy.xpath(data_page.get_oneqy_allqyzz())
            print(','.join(str(s) for s in oneqy_all_qyzzs if s not in [None]))
            for qyzz  in  oneqy_all_qyzzs:
                qyzzname = qyzz.xpath(data_page.get_qyzzname_xpath())[0].strip()
                print(qyname)
                print(qyzzname)
                tmp=[qyname,qyzzname]
                data.append(tmp)
                print(data)
        print(data)
        df = pd.DataFrame(data=data, columns=["qyname", "qyzzname"])
        db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')





    def out_data(self,dbtype, conp, mySchema, tablename, outfilename):
        sql_query_all = '''select * from "{mySchema}"."{tablename}" '''.format(mySchema=mySchema, tablename=tablename)
        result = db_query(sql_query_all, dbtype=dbtype, conp=conp)
        read_db_2_excel(conp, outfilename, result)



    def test_1_get_jst_qyzz_guangdong_sz(self):
        conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        total_ye = 6
        yewu = 'qyzz'
        shengfen='guangdong'
        shi = 'sz'
        tablename='jst_qyzz_sz'+self.tablenamehouzui
        outfilename = r"D:\筑龙项目\企业资质测试\jst\sz\建设通深圳企业资质"
        data = []

        jst_qyzz_page = JstQyzzPage(self.driver, self.base_url)
        jst_qyzz_page.open()
        s = input("input  your  unm: ")
        if int(s) == 1:
            for gotoyema  in  range(3,total_ye):
                self.get_jst_qyzz(jst_qyzz_page, conp, total_ye,gotoyema, shengfen, yewu, tablename,data,shi)
                print("共获取" + str(total_ye - 1) + "页，已完成" + str(gotoyema) + "页")
        # 导出数据
        self.out_data('postgresql', conp, 'zl_test', tablename, outfilename)






if  __name__ == '__main__':
        unittest.main(verbosity=2)
        # print("%s 页面中未能找到 %s 元素" % ("2", "8"))

