import unittest
from bst.bst_datatest.test_case.page_obj.jst.JstQyyjPage import *
from bst.bst_datatest.test_case.page_obj.jst.JstQyyjDetailPage import *
from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
from bst.bst_datatest.test_case.models.moni_ip import *
from time import sleep
from lxml import etree
from lmf.dbv2 import db_write
import pandas as pd
from bst.bst_datatest.test_case.models.get_db_excel import  *

class  TestGetJstRyzz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tablenamehouzui = datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        # chromeOptions = webdriver.ChromeOptions()
        # ip = get_ip()
        # # 设置代理
        # chromeOptions.add_argument("--proxy-server=http://%s" % (ip))
        # # cls.driver = webdriver.Chrome()
        # cls.driver = webdriver.Chrome(chrome_options=chromeOptions)
        # cls.base_url = "https://hhb.cbi360.net/tenderbangsoso/"
        #
        # # 查看本机ip，查看代理是否起作用
        # cls.driver.get("http://httpbin.org/ip")
        # print(cls.driver.page_source)

        cls.driver = webdriver.Chrome()
        cls.base_url ="https://hhb.cbi360.net/tenderbangsoso/"


    @classmethod
    def tearDownClass(cls):
        pass
        # cls.driver.quit()
    # 遍历所有的市
    def get_jst_qyyj(self,data_page,driver,gotoyema,shengfen,yewu,datalist,shi=None):
        # try:
            # 选择企业业绩
            data_page.select_yewu(yewu)
            # 选择省份
            data_page.select_shengfen(shengfen)

            if shi != None:
                data_page.select_szshi()

            qu_count = 4
            page = driver.page_source
            body = etree.HTML(page)
            # 遍历区//*[@id="div_area"]/a[3]
            sz_allqu_list= body.xpath(data_page.get_sz_allqu_xpath())[3:]
            print(','.join(str(s) for s in sz_allqu_list if s not in [None]))
            for qus in sz_allqu_list:
                qu_text = qus.text.strip()
                print(qu_text)
                # 选择区
                data_page.select_qu(qu_count)
                # 点击搜索按钮
                data_page.click_search_button()
                sleep(3)

                # 获得当前页码
                cur_yema = data_page.get_cur_yema()
                # 翻页
                if int(cur_yema) != int(gotoyema):
                    try:
                        data_page.goto_yema(gotoyema)
                    except BaseException as msg:
                        print(msg)
                    sleep(3)

                # 获得当前页面
                page = driver.page_source
                body = etree.HTML(page)
                qyyj_list = body.xpath(data_page.get_datas_xpath())
                qyyj_count = 1
                for content in qyyj_list:
                    entname = content.xpath(data_page.get_entname_xpath())[0].strip()
                    # name = content.xpath(data_page.get_name_xpath())[0].strip()
                    href= data_page.get_element_shuxinzhi('href',qyyj_count)
                    qyyj_count += 1
                    tmp = [qu_text,entname,href]
                    datalist.append(tmp)

            qu_count  += 1
        # except BaseException as  msg:
        #     print(msg)
            print(datalist)
            return datalist


    def get_qyyj_detail(self,detail_page,conp,datalist,driver,tablename):
        # try:
            data = []
            for qu_text,entname,href in datalist:
                driver.get(href)
                sleep(3)
                page = driver.page_source
                body = etree.HTML(page)
                print(body)
                content_list = body.xpath(detail_page.get_datas_xpaht())[1:]
                print(','.join(str(s) for s in content_list if s not in [None]))
                for content in content_list:
                    print(href)
                    print(entname)
                    ggname = content.xpath(detail_page.ggname_texts)[0].strip()
                    print(ggname)
                    xmjl = content.xpath(detail_page.xmjl_texts)[0].strip()
                    print(xmjl)
                    if content.xpath(detail_page.zbtime_texts):
                        zbtime=content.xpath(detail_page.zbtime_texts)[0].strip()
                    print(zbtime)
                    tmp = [href,qu_text,entname, ggname,xmjl,zbtime]
                    data.append(tmp)
                    print(data)
                    # df = pd.DataFrame(data=tmp, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
                    # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

        # except BaseException as  msg:
        #     print(msg)
            print(data)
            # df = pd.DataFrame(data=data, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')




    def out_data(self,dbtype, conp, mySchema, tablename, outfilename):
        sql_query_all = '''select * from "{mySchema}"."{tablename}" '''.format(mySchema=mySchema, tablename=tablename)
        result = db_query(sql_query_all, dbtype=dbtype, conp=conp)
        read_db_2_excel(conp, outfilename, result)


    def test_1_get_jst_xmjl_yunnan(self):
        conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        total_ye = 5
        yewu = 'qyyj'
        shengfen='guangdong'
        shi='sz'
        tablename='jst_qyyj_yunnan'+self.tablenamehouzui
        outfilename =r"D:\筑龙项目\企业业绩\jst\sz\建设通深圳企业业绩"
        datalist=[]
        jst_qyyj_page = JstQyyjPage(self.driver,self.base_url)
        jst_qyyj_page.open()
        jst_qyyj_detali_page = JstQyyjDetailPage(self.driver,self.base_url)
        s = input("input  your  unm: ")
        if int(s) == 1:
            # self.get_jst_qyyj(jst_qyyj_page, self.driver, 2, shengfen, yewu, datalist, shi)
            for gotoyema  in  range(1,total_ye):
                self.get_jst_qyyj(jst_qyyj_page,self.driver,gotoyema,shengfen,yewu,datalist,shi)
                print("共获取" + str(total_ye-1) + "页，已完成" + str(gotoyema) + "页")

        # 得每个项目的中标业绩
        self.get_qyyj_detail(jst_qyyj_detali_page, conp, datalist, self.driver, tablename)
        # 导出数据
        # self.out_data('postgresql', conp, 'zl_test', tablename, outfilename)




if  __name__ == '__main__':
        unittest.main(verbosity=2)
        # print("%s 页面中未能找到 %s 元素" % ("2", "8"))

