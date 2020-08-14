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
from bst.bst_datatest.test_case.models.my_read_excel import  *


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


    # 指定企业名和项目经理  (self.driver,jst_xmjl_page,zhongbiaoren,xmjl,xmjl_href_list)
    def get_jst_xmjl(self,driver,data_page,zhongbiaoren,xmjl,xmjl_href_list):
            # 选择项目经理
            data_page.select_yewu()
            # 输入项目经理名字
            xmjl_loc = (By.XPATH,'//*[@id="txt_builder_name"]')
            WebDriverWait(driver,20).until(EC.visibility_of_element_located(xmjl_loc)).clear()
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(xmjl_loc)).send_keys(str(xmjl))

            # 输入企业名字
            company_name_loc = (By.XPATH, '//*[@id="txt_company_name"]')
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).clear()
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(company_name_loc)).send_keys(str(zhongbiaoren))

            # 点击搜索按钮
            data_page.click_search_button()
            sleep(3)

            # 获得当前页面
            page = driver.page_source
            body = etree.HTML(page)
            xmjl_list = body.xpath(data_page.get_datas_xpath())
            xmjl_count = 1
            for content in xmjl_list:
                href = data_page.get_element_shuxinzhi('href', xmjl_count)
                xmjl_count += 1
                tmp = [zhongbiaoren, xmjl, href]
                xmjl_href_list.append(tmp)
                print(xmjl_href_list)
            # return datalist


    def get_xmjl_detail(self,driver,jst_xmjl_detali_page,xmjl_href_list,xmjl_zbyj):
        for  entname, name,href in xmjl_href_list:
            try:
                driver.get(href)
                sleep(3)
                zbsl_loc = (By.XPATH,'//*[@id="newriskWrap"]/div[2]/ul/li[1]/div[2]/i')
                zbsl2 = WebDriverWait(driver,30).until(EC.visibility_of_element_located(zbsl_loc)).text.strip()
                print(href)
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

                for gotoyema  in  range(1,total_ye+1):
                    if total_ye >1 :
                        # 获得当前页码
                        cur_yema = jst_xmjl_detali_page.get_cur_yema_detail()
                        # 翻页
                        if int(cur_yema) != int(gotoyema):
                            try:
                                jst_xmjl_detali_page.goto_yema_detail(gotoyema)
                            except BaseException as msg:
                                print(msg)
                            sleep(3)

                    page = driver.page_source
                    body = etree.HTML(page)
                    zbly_href_count=2
                    content_list = body.xpath(jst_xmjl_detali_page.get_datas_xpaht())[1:]
                    for content in content_list:
                        zbly_href = " "
                        ggname = content.xpath(jst_xmjl_detali_page.ggname_texts)[0].strip()
                        print(ggname)
                        print(len(content.xpath(jst_xmjl_detali_page.zbtime_texts)))
                        # 中标日期为空
                        if len(content.xpath(jst_xmjl_detali_page.zbtime_texts)) > 0 :
                            zbtime=content.xpath(jst_xmjl_detali_page.zbtime_texts)[0].strip()
                        else:
                            zbtime=" "
                        print(zbtime)

                        # 中标来源
                        if len(content.xpath(jst_xmjl_detali_page.zbly_text)) > 0:
                            zbly = content.xpath(jst_xmjl_detali_page.zbly_text)[0].strip()
                        else:
                            zbly = " "

                        zbly_href_loc = (By.XPATH, '//*[@id="newriskWrap"]/div[2]/ul/li[' + str(zbly_href_count) + ']/div[6]/a')
                        if WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zbly_href_loc)):
                            zbly_href = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zbly_href_loc)).get_attribute('href')

                        tmp = [href,entname, name,ggname,zbtime,zbsl_count,zbly,zbly_href.strip()]
                        xmjl_zbyj.append(tmp)
                        print(xmjl_zbyj)
            except BaseException as  msg:
                print(msg)
                print(xmjl_zbyj)
            continue
            # df = pd.DataFrame(data=data, columns=["href", "shi_text","entname", "name", "ggname", "zbtime"])
            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')



    def test_2_get_jst_xmjl_guangdong_sz(self):
        # conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        # tablename='jst_xmjl_yunnan'+self.tablenamehouzui

        infilename = r"D:\SVN\业务数据维护\项目经理业绩\数据准备\待测试项目经理业绩_胡金花_20200603_153200 - 副本.xlsx"
        outfilename = r"D:\SVN\业务数据维护\项目经理业绩\测试结果\项目经理业绩_建设通查询结果_胡金花"

        jst_xmjl_page = JstXmjlPage(self.driver,self.base_url)
        jst_xmjl_page.open()
        jst_xmjl_detali_page = JstXmjlDetailPage(self.driver,self.base_url)

        xmjl_href_list = []
        xmjl_zbyj = []

        fl=5
        while fl>0:
            try:
                s = input("input  your  unm: ")
                if int(s) == 1:
                        # 读要查询的项目经理和相应企业进来
                        all_sheet_data = read_excel(infilename)
                        # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
                        sheet1data = all_sheet_data[0][1][1:]
                        # print(sheet1data)
                        for row in sheet1data:
                            zhongbiaoren = row[1].strip()
                            print(zhongbiaoren)
                            xmjl = row[2].strip()
                            print(xmjl)
                            self.get_jst_xmjl(self.driver,jst_xmjl_page,zhongbiaoren,xmjl,xmjl_href_list)

                        # 到项目经理href数据到excel
                        columnRows1 = ["zhongbiaoren", "name", "href"]
                        wirteDataToExcel(outfilename + self.tablenamehouzui + "项目经理href.xlsx", "jst_xmjl_guangdong", columnRows1, xmjl_href_list)


                        # 得到每个项目经理的业绩
                        self.get_xmjl_detail(self.driver,jst_xmjl_detali_page, xmjl_href_list,xmjl_zbyj)

                        # 到数据到excle中
                        columnRows = ["href", "zhongbiaoren", "xmjl", "ggname", "zbtime", "zbsl_count","zbly","zbly_href"]
                        wirteDataToExcel(outfilename + self.tablenamehouzui + ".xlsx", "jst_xmjl_guangdong_detail", columnRows, xmjl_zbyj)
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

