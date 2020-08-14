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
from bst.bst_datatest.test_case.models.my_read_excel import  *

class  TestGetJstRyzz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tablenamehouzui = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        # cls.driver = get_driver_moni_ip()
        # #
        # # 查看本机ip，查看代理是否起作用
        # cls.driver.get("http://httpbin.org/ip")
        # print(cls.driver.page_source)

        cls.base_url ="https://hhb.cbi360.net/tenderbangsoso/"
        cls.driver = webdriver.Chrome()


    @classmethod
    def tearDownClass(cls):
        pass
        # cls.driver.quit()


    def get_qyyj_detail(self,driver,jst_qyyj_detali_page ,qy_href, qyyj_data):
        for zhongbiaoren, href, zbsl in qy_href:
            # try:
                driver.get(href)
                sleep(3)
                print(href)
                # 计算该企业中标有几页数据
                zbsl_count = int(zbsl)
                if zbsl_count > 15:
                    if  zbsl_count % 15  == 0 : total_ye = zbsl_count//15
                    else:total_ye = zbsl_count//15 + 1
                else: total_ye =1
                print(total_ye)

                for gotoyema  in  range(1,total_ye+1):
                    print(gotoyema)
                    if  gotoyema==2:
                        locator = (By.XPATH,'/html/body/div[8]/div[4]/div[2]/div/a')
                        WebDriverWait(driver,10).until(EC.visibility_of_element_located(locator)).click()
                        sleep(3)
                    elif  gotoyema > 2 :
                        locator2 = (By.XPATH, '/html/body/div[8]/div[4]/div[2]/div/div/div/input[1]')
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).clear()
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator2)).send_keys(str(gotoyema))

                        zhuandao_loc = (By.XPATH, '/html/body/div[8]/div[4]/div[2]/div/div/div/input[2]')
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zhuandao_loc)).click()
                        sleep(3)

                    page = driver.page_source
                    body = etree.HTML(page)

                    zbly_href_count=2
                    content_list = body.xpath(jst_qyyj_detali_page.get_datas_xpaht())[1:]
                    # print(','.join(str(s) for s in content_list if s not in [None]))
                    for content in content_list:
                            zbtime=" "
                            zbly=" "
                            zbly_href = " "
                            ggname = content.xpath(jst_qyyj_detali_page.ggname_texts)[0]
                            xmjl = content.xpath(jst_qyyj_detali_page.xmjl_texts)[0]
                            if content.xpath(jst_qyyj_detali_page.zbtime_texts):
                                zbtime=content.xpath(jst_qyyj_detali_page.zbtime_texts)[0]
                            if content.xpath(jst_qyyj_detali_page.zbly_text):
                                zbly=content.xpath(jst_qyyj_detali_page.zbly_text)[0]

                            zbly_href_loc =(By.XPATH,'/html/body/div[8]/div[4]/div[2]/ul/li[' + str(zbly_href_count) + ']/div[7]/a')
                            if WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zbly_href_loc)):
                                zbly_href = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(zbly_href_loc)).get_attribute('href')

                            tmp = [href.strip(),zhongbiaoren.strip(), ggname.strip(),xmjl.strip(),zbtime.strip(),zbly.strip(),zbly_href.strip(),zbsl.strip()]
                            qyyj_data.append(tmp)
                            print(qyyj_data)
                            zbly_href_count += 1
                            # df = pd.DataFrame(data=tmp, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
                            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

            # except:
            #     print(msg)
            # finally: print(qyyj_data)
            # continue

            # df = pd.DataFrame(data=data, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

    def get_jst_qyyj(self,driver, jst_qyyj_page,yewu,zhongbiaoren,qy_href):
        # 选择企业业绩
        jst_qyyj_page.select_yewu(yewu)

        # 输入企业名
        qyname_loc=(By.XPATH,'//*[@id="txt_company_name"]')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(qyname_loc)).clear()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(qyname_loc)).send_keys(str(zhongbiaoren))

        # 点击搜索按钮
        jst_qyyj_page.click_search_button()
        sleep(3)

        # 获得当前页面
        page = driver.page_source
        body = etree.HTML(page)
        qyyj_list = body.xpath(jst_qyyj_page.get_datas_xpath())
        qyyj_count = 1
        for content in qyyj_list:
            zhongbiaoren2 =" "
            if content.xpath('/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/h2/a/em/text()'):
                zhongbiaoren2 = content.xpath('/html/body/div[8]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/h2/a/em/text()')[0]
            zbsl = content.xpath(jst_qyyj_page.get_zbsl_xpath())[0]
            href = jst_qyyj_page.get_element_shuxinzhi('href', qyyj_count)
            qyyj_count += 1
            tmp = [ zhongbiaoren2.strip(), href.strip(), zbsl.strip()]
            qy_href.append(tmp)
            print(qy_href)
            break



    def out_data(self,dbtype, conp, mySchema, tablename, outfilename):
        sql_query_all = '''select * from "{mySchema}"."{tablename}" '''.format(mySchema=mySchema, tablename=tablename)
        result = db_query(sql_query_all, dbtype=dbtype, conp=conp)
        read_db_2_excel(conp, outfilename, result)


    def test_1_get_jst_xmjl_zhejiang(self):
        # conp=["zl_reader", "zl_reader", "192.168.60.61:5433", "biaost", "zl_test", "public"]
        # tablename='jst_qyyj_guangdong'+self.tablenamehouzui

        infilename=r"D:\SVN\业务数据维护\企业业绩\数据准备\待测试企业业绩业绩_纪道灶_20200622.xlsx"
        outfilename =r"D:\SVN\业务数据维护\企业业绩\测试结果\企业业绩业绩_建设通查询结果_纪道灶_"
        yewu='qyyj'

        qy_href=[]
        qyyj_data = []

        jst_qyyj_page = JstQyyjPage(self.driver,self.base_url)
        jst_qyyj_page.open()
        jst_qyyj_detali_page = JstQyyjDetailPage(self.driver,self.base_url)

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
                self.get_jst_qyyj(self.driver, jst_qyyj_page, yewu, zhongbiaoren, qy_href)

            # 到企业href数据到excel
            columnRows1 = ["zhongbiaoren", "href", "zbsl"]
            wirteDataToExcel(outfilename + self.tablenamehouzui + "企业href.xlsx", "jst_xmjl_guangdong", columnRows1,qy_href)

            # qy_href=[
            #     ['控制技术研究所', 'https://hhb.cbi360.net/sg_1818754/', '1'],
            #     ['中铁二十四局集团有限公司', 'https://hhb.cbi360.net/sg_358069/', '436'],
            #     ['南', 'https://hhb.cbi360.net/sg_1518195/', '0'],
            #     ['胜利园林有限公司', 'https://hhb.cbi360.net/sg_1004215/', '153'],
            #     ['甘肃省安装建设集团公司', 'https://hhb.cbi360.net/sg_941742/', '1073'],
            #     ['中智科技有限公司', 'https://hhb.cbi360.net/sg_1176771/', '1'],
            #     ['四川', 'https://hhb.cbi360.net/sg_1215686/', '1'],
            #     ['中交二公局第一工程有限公司', 'https://hhb.cbi360.net/sg_693549/', '35'],
            #     ['中建五洲工程装备有限公司', 'https://hhb.cbi360.net/sg_1120341/', '1'],
            #     ['广东华峰', 'https://hhb.cbi360.net/sg_1801123/', '0'],
            #     ['福建省', 'https://hhb.cbi360.net/sg_1583544/', '0'],
            #     ['宁波万里管道有限公司', 'https://hhb.cbi360.net/sg_4742/', '20']
            # ]

            # 得到每个企业的业绩
            self.get_qyyj_detail(self.driver, jst_qyyj_detali_page, qy_href, qyyj_data)

            # 到数据到excle中
            columnRows = ["href", "zhongbiaoren", "ggname", "xmjl", "zbtime", "zbly", "zbly_href", "zbsl"]
            wirteDataToExcel(outfilename + self.tablenamehouzui + ".xlsx", "jst_xmjl_guangdong_detail", columnRows,
                             qyyj_data)



        # fl = 5
        # while fl > 0:
        #     try:
        #         s = input("input  your  unm: ")
        #         if int(s) == 1:
        #             # 读要查询的项目经理和相应企业进来
        #             all_sheet_data = read_excel(infilename)
        #
        #             # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
        #             sheet1data = all_sheet_data[0][1][1:]
        #             # print(sheet1data)
        #
        #             for row in sheet1data:
        #                 zhongbiaoren = row[1].strip()
        #                 print(zhongbiaoren)
        #                 self.get_jst_qyyj(self.driver, jst_qyyj_page,yewu, zhongbiaoren,qy_href)
        #
        #             # 到企业href数据到excel
        #             columnRows1 = ["zhongbiaoren", "href","zbsl"]
        #             wirteDataToExcel(outfilename + self.tablenamehouzui + "企业href.xlsx", "jst_xmjl_guangdong", columnRows1, qy_href)
        #
        #
        #             # 得到每个企业的业绩
        #             self.get_qyyj_detail(self.driver, jst_qyyj_detali_page, qy_href, qyyj_data)
        #
        #             # 到数据到excle中
        #             columnRows = ["href", "zhongbiaoren", "ggname", "xmjl", "zbtime", "zbly","zbly_href","zbsl"]
        #             wirteDataToExcel(outfilename + self.tablenamehouzui + ".xlsx", "jst_xmjl_guangdong_detail",columnRows, qyyj_data)
        #
        #             break
        #     except  BaseException as msg:
        #         print(msg)
        #         # self.driver= get_driver_moni_ip()
        #         # # 查看本机ip，查看代理是否起作用
        #         # self.driver.get("http://httpbin.org/ip")
        #         # print(self.driver.page_source)
        #
        #         self.driver = webdriver.Chrome()
        #
        #         jst_qyyj_page = JstQyyjPage(self.driver, self.base_url)
        #         jst_qyyj_page.open()
        #         jst_qyyj_detali_page = JstQyyjDetailPage(self.driver, self.base_url)
        #         sleep(3)
        #         fl -= 1


if  __name__ == '__main__':
        unittest.main(verbosity=2)
        # print("%s 页面中未能找到 %s 元素" % ("2", "8"))

