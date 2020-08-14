import unittest
from bst.bst_datatest.test_case.page_obj.jst.JstQyyjPage import *
from bst.bst_datatest.test_case.page_obj.jst.JstQyyjDetailPage import *
from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as  EC
from bst.bst_datatest.test_case.models.get_driver_moni_ip import get_driver_moni_ip
from time import sleep
from lxml import etree
from lmf.dbv2 import db_write
import pandas as pd
from bst.bst_datatest.test_case.models.get_db_excel import  *
from bst.bst_datatest.test_case.models.my_to_excel import  *

class  TestGetJstRyzz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tablenamehouzui = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cls.driver = get_driver_moni_ip()

        # 查看本机ip，查看代理是否起作用
        cls.driver.get("http://httpbin.org/ip")
        print(cls.driver.page_source)

        cls.driver = webdriver.Chrome()
        cls.base_url ="https://hhb.cbi360.net/tenderbangsoso/"


    @classmethod
    def tearDownClass(cls):
        pass
        # cls.driver.quit()



    def get_qyyj_detail(self,detail_page,conp,datalist,driver,tablename,data):
        for qu_text,entname,href,zbsl in datalist:
            try:
                driver.get(href)
                sleep(3)
                # print(zbsl)
                # 计算该企业中标有几页数据
                zbsl_count = int(zbsl)
                if zbsl_count > 15:
                    if  zbsl_count % 15  == 0 : total_ye = zbsl_count//15
                    else:total_ye = zbsl_count//15 + 1
                else: total_ye =1
                print(total_ye)
                if total_ye> 8: total_ye= 8

                for gotoyema  in  range(1,total_ye+1):
                    print(gotoyema)
                    if  gotoyema==2:
                        locator = (By.XPATH,'/html/body/div[8]/div[4]/div[2]/div/a')
                        WebDriverWait(driver,10).until(EC.visibility_of_element_located(locator)).click()
                        sleep(3)
                    elif  gotoyema > 2 :
                        # locator2 = (By.XPATH, '/html/body/div[8]/div[4]/div[2]/div/div/div/a[6]')
                        # WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).click()
                        # sleep(3)

                        locator2 = (By.XPATH, '/html/body/div[8]/div[4]/div[2]/div/div/div/input[1]')
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                        zhuandao_loc = (By.XPATH, '/html/body/div[8]/div[4]/div[2]/div/div/div/input[2]')
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
                        sleep(3)






                    page = driver.page_source
                    body = etree.HTML(page)
                    # print(body)
                    content_list = body.xpath(detail_page.get_datas_xpaht())[1:]
                    # print(','.join(str(s) for s in content_list if s not in [None]))
                    for content in content_list:
                            # print(href)
                            # print(entname)
                            ggname = content.xpath(detail_page.ggname_texts)[0].strip()
                            # print(ggname)
                            xmjl = content.xpath(detail_page.xmjl_texts)[0].strip()
                            # print(xmjl)
                            if content.xpath(detail_page.zbtime_texts):
                                zbtime=content.xpath(detail_page.zbtime_texts)[0].strip()
                            # print(zbtime)
                            tmp = [href,qu_text,entname, ggname,xmjl,zbtime]
                            data.append(tmp)
                            print(data)
                            # df = pd.DataFrame(data=tmp, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
                            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

            except BaseException as  msg:
                print(msg)
            finally: print(data)
            continue

            # df = pd.DataFrame(data=data, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

    def get_jst_qyyj2(self, data_page, driver, gotoyema, shengfen, yewu, datalist, shi=None):
        # 选择企业业绩
        data_page.select_yewu(yewu)
        # 选择省份
        data_page.select_shengfen(shengfen)

        if shi != None:
            data_page.select_szshi()

        shi_count = 1
        page = driver.page_source
        body = etree.HTML(page)
        # 遍历市
        all_shi_list = body.xpath(data_page.get_shilist_xpath())[1:]
        # print(','.join(str(s) for s in all_shi_list if s not in [None]))
        for shis in all_shi_list:
            shi_text = shis.text.strip()
            print(shi_text)
            # 选择市
            data_page.select_shi(shi_count)
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
            qyyj_list = body.xpath(data_page.get_datas_xpath())
            qyyj_count = 1
            for content in qyyj_list:
                entname = content.xpath(data_page.get_entname_xpath())[0].strip()
                zbsl = content.xpath(data_page.get_zbsl_xpath())[0].strip()
                href = data_page.get_element_shuxinzhi('href', qyyj_count)
                qyyj_count += 1
                tmp = [shi_text, entname, href, zbsl]
                datalist.append(tmp)
                print(datalist)
            shi_count += 1



    def out_data(self,dbtype, conp, mySchema, tablename, outfilename):
        sql_query_all = '''select * from "{mySchema}"."{tablename}" '''.format(mySchema=mySchema, tablename=tablename)
        result = db_query(sql_query_all, dbtype=dbtype, conp=conp)
        read_db_2_excel(conp, outfilename, result)


    def test_1_get_jst_xmjl_zhejiang(self):
        conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        total_ye = 3
        yewu = 'qyyj'
        shengfen='guangdong'
        tablename='jst_qyyj_guangdong'+self.tablenamehouzui
        outfilename =r"D:\SVN\数据对比\数据准备\企业中标业绩\广东\广东建设通企业业绩_数据准备_胡金花"


        datalist=[]

        jst_qyyj_page = JstQyyjPage(self.driver,self.base_url)
        jst_qyyj_page.open()
        jst_qyyj_detali_page = JstQyyjDetailPage(self.driver,self.base_url)

        s = input("input  your  unm: ")
        if int(s) == 1:
            # 得到企业和对应的链接
            for gotoyema  in  range(1,total_ye):
                self.get_jst_qyyj2(jst_qyyj_page,self.driver,gotoyema,shengfen,yewu,datalist)
                print("共获取" + str(total_ye-1) + "页，已完成" + str(gotoyema) + "页")



            data = []
            #得到相应企业的全部中标业绩
            self.get_qyyj_detail(jst_qyyj_detali_page, conp, datalist, self.driver, tablename,data)

            # 到数据到excle中
            columnRows = ["href", "shi", "zhongbiaoren", "ggname", "xmjl", "zbtime"]
            wirteDataToExcel(outfilename, "jst_qyyj_zhejiang", columnRows, data)





if  __name__ == '__main__':
        unittest.main(verbosity=2)
        # print("%s 页面中未能找到 %s 元素" % ("2", "8"))

