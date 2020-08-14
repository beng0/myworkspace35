import unittest
from bst.bst_datatest.test_case.page_obj.jst.JstXmjlPage import *
from bst.bst_datatest.test_case.page_obj.jst.JstXmjlDetailPage import *
from selenium  import webdriver
from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
from time import sleep
from lxml import etree
from lmf.dbv2 import db_write
import pandas as pd
from bst.bst_datatest.test_case.models.get_db_excel import  *
from bst.bst_datatest.test_case.models.my_to_excel import  *

class  TestGetJstRyzz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tablenamehouzui = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        # cls.driver = get_driver_moni_ip()
        cls.driver = webdriver.Chrome()
        cls.base_url = "https://hhb.cbi360.net/tenderbangsoso/"

        # # 查看本机ip，查看代理是否起作用
        # cls.driver.get("http://httpbin.org/ip")
        # print(cls.driver.page_source)



    @classmethod
    def tearDownClass(cls):
        pass
        # cls.driver.quit()
    # 遍历所有的市
    def get_jst_xmjl_shi(self,data_page,detail_page,driver,conp,gotoyema,shengfen,yewu,tablename,datalist):
        # try:
            # 选择项目经理
            data_page.select_yewu()
            # 选择省份
            data_page.select_shengfen(shengfen)
            shi_count = 2
            page = driver.page_source
            body = etree.HTML(page)
            # 遍历市
            shi_list= body.xpath(data_page.get_shilist_xpath())[1:]
            for shis in shi_list:
                shi_text = shis.text.strip()
                # 选择市
                data_page.select_shi(shi_count)
                shi_count +=1
                # 点击搜索按钮
                data_page.click_search_button()
                sleep(3)

                # # 获得当前页码
                # cur_yema = data_page.get_cur_yema()
                # # 翻页
                # if int(cur_yema) != int(gotoyema):
                #     try:
                #         data_page.goto_yema(gotoyema)
                #     except BaseException as msg:
                #         print(msg)
                #     sleep(3)

                # 获得当前页面
                page = driver.page_source
                body = etree.HTML(page)
                xmjl_list = body.xpath(data_page.get_datas_xpath())
                xmjl_count = 1
                for content in xmjl_list:
                    entname = content.xpath(data_page.get_entname_xpath())[0].strip()
                    name = content.xpath(data_page.get_name_xpath())[0].strip()
                    href= data_page.get_element_shuxinzhi('href',xmjl_count)
                    xmjl_count += 1
                    tmp = [shi_text,entname, name,href]
                    datalist.append(tmp)
        # except BaseException as  msg:
        #     print(msg)
            print(datalist)
            return datalist

    # 指定市
    def get_jst_xmjl(self,data_page,detail_page,driver,conp,gotoyema,shengfen,yewu,tablename,datalist,shi=None):
            # 选择项目经理
            data_page.select_yewu()
            # 选择省份
            data_page.select_shengfen(shengfen)
            if shi != None:
                data_page.select_szshi()
            # 点击搜索按钮
            data_page.click_search_button()
            sleep(3)

            # 获得当前页码
            cur_yema = data_page.get_cur_yema()
            # 翻页
            if int(cur_yema) != int(gotoyema):
                try:
                    data_page.goto_yema2(gotoyema)
                except BaseException as msg:
                    print(msg)
                sleep(3)

            # 获得当前页面
            page = driver.page_source
            body = etree.HTML(page)
            xmjl_list = body.xpath(data_page.get_datas_xpath())
            xmjl_count = 1
            for content in xmjl_list:
                entname = content.xpath(data_page.get_entname_xpath())[0].strip()
                name = content.xpath(data_page.get_name_xpath())[0].strip()
                href = data_page.get_element_shuxinzhi('href', xmjl_count)
                zbsl =content.xpath(data_page.get_zbsl_xpath())[0].strip()
                xmjl_count += 1
                tmp = [entname, name, href,zbsl]
                datalist.append(tmp)
                print(datalist)
            # return datalist



    def get_xmjl_detail(self,detail_page,conp,datalist,driver,tablename,data):
        for  entname, name,href,zbsl in datalist:
        # for shi_text,entname, name,href in datalist:
            try:
                driver.get(href)
                sleep(3)
                #                     //*[@id="newriskWrap"]/div[2]/ul/li[1]/div[2]/i
                zbsl_loc = (By.XPATH,'//*[@id="newriskWrap"]/div[2]/ul/li[1]/div[2]/i')
                zbsl2 = WebDriverWait(driver,30).until(EC.visibility_of_element_located(zbsl_loc)).text.strip()
                print(href)
                print(zbsl)
                print(zbsl2)
                # 计算该项目经理中标有几页数据
                zbsl_count = int(zbsl2)
                if zbsl_count > 15:
                    if zbsl_count % 15 == 0:
                        total_ye = zbsl_count // 15
                    else:
                        total_ye = zbsl_count // 15 + 1
                else:
                    total_ye = 1
                print(total_ye)
                # if total_ye > 8: total_ye = 8

                for gotoyema  in  range(1,total_ye+1):
                    if total_ye >1 :
                        # 获得当前页码
                        cur_yema = detail_page.get_cur_yema_detail()
                        # 翻页
                        if int(cur_yema) != int(gotoyema):
                            try:
                                detail_page.goto_yema_detail(gotoyema)
                            except BaseException as msg:
                                print(msg)
                            sleep(3)

                    page = driver.page_source
                    body = etree.HTML(page)
                    content_list = body.xpath(detail_page.get_datas_xpaht())[1:]
                    for content in content_list:
                        ggname = content.xpath(detail_page.ggname_texts)[0].strip()
                        print(ggname)
                        print(len(content.xpath(detail_page.zbtime_texts)))

                        if len(content.xpath(detail_page.zbtime_texts)) > 0 :
                            zbtime=content.xpath(detail_page.zbtime_texts)[0].strip()
                        else:
                            zbtime=" "

                        print(zbtime)
                        tmp = [href,entname, name,ggname,zbtime,zbsl_count]
                        # tmp = [href,shi_text,entname, name,ggname,zbtime]
                        data.append(tmp)
                        print(data)
            except BaseException as  msg:
                print(msg)
                print(data)
            continue
            # df = pd.DataFrame(data=data, columns=["href", "shi_text","entname", "name", "ggname", "zbtime"])
            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')



    def test_2_get_jst_xmjl_guangdong_sz(self):
        conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        total_ye = 13
        yewu = 'xmjl'
        shengfen='shanxi'
        # shi='sz'
        tablename='jst_xmjl_shanxi'+self.tablenamehouzui
        outfilename =r"D:\SVN\数据对比\数据准备\项目经理中标业绩\山西\山西建设通项目经理业绩_数据准备_胡金花"
        datalist=[]

        jst_xmjl_page = JstXmjlPage(self.driver,self.base_url)
        jst_xmjl_page.open()
        jst_xmjl_detali_page = JstXmjlDetailPage(self.driver,self.base_url)

        data = []

        fl=5
        while fl>0:
            outfilename = r"D:\SVN\数据对比\数据准备\项目经理中标业绩\山西\山西建设通项目经理业绩_数据准备_胡金花"
            try:
                s = input("input  your  unm: ")
                if int(s) == 1:
                        for gotoyema  in  range(3,total_ye):
                            # 得到项目经理链接
                            self.get_jst_xmjl(jst_xmjl_page,jst_xmjl_detali_page,self.driver,conp,gotoyema,shengfen,yewu,tablename,datalist)
                            print("共获取" + str(total_ye-1) + "页，已完成" + str(gotoyema) + "页")


                        # 到数据到excle中  , entname, href, zbsl
                        columnRows1 = ["zhongbiaoren", "name", "href","zbsl_count"]
                        wirteDataToExcel(outfilename + self.tablenamehouzui + "1.xlsx", "jst_xmjl_guangdong", columnRows1, datalist)



                        # 得到每个项目经理的业绩
                        self.get_xmjl_detail(jst_xmjl_detali_page, conp, datalist, self.driver,tablename,data)

                        # 到数据到excle中
                        columnRows = ["href", "zhongbiaoren", "xmjl", "ggname", "zbtime", "zbsl_count"]
                        wirteDataToExcel(outfilename + self.tablenamehouzui + ".xlsx", "jst_xmjl_guangdong_detail", columnRows, data)
                        break
            except  BaseException as msg:
                print(msg)
                # self.driver= get_driver_moni_ip()
                # # 查看本机ip，查看代理是否起作用
                # self.driver.get("http://httpbin.org/ip")
                # print(self.driver.page_source)

                self.driver = webdriver.Chrome()

                jst_xmjl_page = JstXmjlPage(self.driver, self.base_url)
                jst_xmjl_page.open()
                jst_xmjl_detali_page = JstXmjlDetailPage(self.driver, self.base_url)
                sleep(3)
                fl-=1







if  __name__ == '__main__':
        unittest.main(verbosity=2)
        # print("%s 页面中未能找到 %s 元素" % ("2", "8"))

