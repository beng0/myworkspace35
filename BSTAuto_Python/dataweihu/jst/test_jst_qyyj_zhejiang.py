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
        # try:

            for qu_text,entname,href,zbsl in datalist:
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
                            tmp = [href,qu_text,entname, ggname,xmjl,zbtime]  # tmp = [href,shi_text,entname, name,ggname,zbtime]
                            data.append(tmp)
                            print(data)
                            # df = pd.DataFrame(data=tmp, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
                            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

        # except BaseException as  msg:
        #     print(msg)
        #     print(data)
            # df = pd.DataFrame(data=data, columns=["href", "qu_text","entname","ggname","xmjl", "zbtime"])
            # db_write(df, tablename, dbtype='postgresql', datadict='postgresql-text', conp=conp, if_exists='append')

    def get_jst_qyyj2(self, data_page, driver, gotoyema, shengfen, yewu, datalist, shi=None):
        # 选择企业业绩
        data_page.select_yewu(yewu)
        # 选择省份
        data_page.select_shengfen(shengfen)

        if shi != None:
            data_page.select_szshi()

        shi_count = 2
        page = driver.page_source
        body = etree.HTML(page)
        # 遍历市
        print("*****1*******************************")
        all_shi_list = body.xpath(data_page.get_shilist_xpath())[3:]
        print(','.join(str(s) for s in all_shi_list if s not in [None]))
        for shis in all_shi_list:
            print("***********2*************************")
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
                print("****************3********************")
                entname = content.xpath(data_page.get_entname_xpath())[0].strip()
                zbsl = content.xpath(data_page.get_zbsl_xpath())[0].strip()
                # name = content.xpath(data_page.get_name_xpath())[0].strip()
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
        shengfen='zhejiang'
        tablename='jst_qyyj_zhejiang'+self.tablenamehouzui
        outfilename =r"D:\SVN\数据对比\数据准备\企业中标业绩\浙江\浙江建设通企业业绩_数据准备_胡金花"


        datalist=[]

        jst_qyyj_page = JstQyyjPage(self.driver,self.base_url)
        jst_qyyj_page.open()
        jst_qyyj_detali_page = JstQyyjDetailPage(self.driver,self.base_url)

        s = input("input  your  unm: ")
        if int(s) == 1:
            # 得到企业和对应的链接
            # for gotoyema  in  range(1,total_ye):
            #     self.get_jst_qyyj2(jst_qyyj_page,self.driver,gotoyema,shengfen,yewu,datalist)
            #     print("共获取" + str(total_ye-1) + "页，已完成" + str(gotoyema) + "页")

            datalist =[
                 ['温州', '浙江省省直建筑设计院', 'https://hhb.cbi360.net/sg_1117202/', '183'],
                 ['温州', '天尚设计集团有限公司', 'https://hhb.cbi360.net/sg_1255116/', '560'],
                 ['温州', '杭州高达交通设施工程有限公司', 'https://hhb.cbi360.net/sg_221611/', '144'],
                 ['温州', '中国美术学院风景建筑设计研究总院有限公司', 'https://hhb.cbi360.net/sg_1195375/', '610'],
                 ['温州', '桐庐昂业建设有限公司', 'https://hhb.cbi360.net/sg_1160551/', '16'],
                 ['温州', '杭州力耕建设有限公司', 'https://hhb.cbi360.net/sg_1239586/', '98'],
                 ['温州', '杭州宏钰建设有限公司', 'https://hhb.cbi360.net/sg_1499071/', '10'],
                 ['温州', '浙江众能工程技术有限公司', 'https://hhb.cbi360.net/sg_1615084/', '2'],
                 ['温州', '杭州横越测绘有限公司', 'https://hhb.cbi360.net/sg_1837815/', '1'],
                 ['温州', '浙江华东建设工程有限公司', 'https://hhb.cbi360.net/sg_2178/', '481'],
                 ['温州', '杭州中元照明工程有限公司', 'https://hhb.cbi360.net/sg_691537/', '151'],
                 ['嘉兴', '慈溪市万达建设工程有限公司', 'https://hhb.cbi360.net/sg_1019653/', '33'],
                 ['嘉兴', '宁波敬晔建设有限公司', 'https://hhb.cbi360.net/sg_1381634/', '18'],
                 ['嘉兴', '余姚市建筑工程有限公司', 'https://hhb.cbi360.net/sg_3957/', '167'],
                 ['嘉兴', '宁波晟铭建设工程有限公司', 'https://hhb.cbi360.net/sg_1716680/', '4'],
                 ['嘉兴', '宁波永屹建设有限公司', 'https://hhb.cbi360.net/sg_857954/', '57'],
                 ['嘉兴', '宁波冶金勘察设计研究股份有限公司', 'https://hhb.cbi360.net/sg_935142/', '1585'],
                 ['嘉兴', '宁波东弘生态建设有限公司', 'https://hhb.cbi360.net/sg_896370/', '279'],
                 ['嘉兴', '宁波中瑞信息科技有限公司', 'https://hhb.cbi360.net/sg_537798/', '9'],
                 ['嘉兴', '浙江泰来环保科技有限公司', 'https://hhb.cbi360.net/sg_262901/', '104'],
                 ['嘉兴', '宁波裕和建设有限公司', 'https://hhb.cbi360.net/sg_1196328/', '19'],
                 ['嘉兴', '宁波方旭市政园林工程有限公司', 'https://hhb.cbi360.net/sg_1466687/', '21'],
                 ['嘉兴', '慈溪市乐园建设工程有限公司', 'https://hhb.cbi360.net/sg_7197/', '35'],
                 ['嘉兴', '宁波昂达园林建设有限公司', 'https://hhb.cbi360.net/sg_841209/', '159'],
                 ['嘉兴', '宁波丰茂交通工程有限公司', 'https://hhb.cbi360.net/sg_1103642/', '1'],
                 ['嘉兴', '浙江银晖生态建设有限公司', 'https://hhb.cbi360.net/sg_1262385/', '6'],
                 ['湖州', '温州浚远建设工程有限公司', 'https://hhb.cbi360.net/sg_1198455/', '10'],
                 ['湖州', '浙江艺美建筑装饰工程有限公司', 'https://hhb.cbi360.net/sg_1737837/', '36'],
                 ['湖州', '温州金顺建设有限公司', 'https://hhb.cbi360.net/sg_1256139/', '12'],
                 ['湖州', '温州鸿福建设有限公司', 'https://hhb.cbi360.net/sg_1476477/', '8'],
                 ['湖州', '温州一业建设有限公司', 'https://hhb.cbi360.net/sg_1570977/', '5'],
                 ['湖州', '苍南县交通建设工程有限公司', 'https://hhb.cbi360.net/sg_4890/', '142'],
                 ['湖州', '浙江创为建设有限公司', 'https://hhb.cbi360.net/sg_1838545/', '1'],
                 ['湖州', '温州腾越建设有限公司', 'https://hhb.cbi360.net/sg_851210/', '118'],
                 ['湖州', '瑞安市东南市政工程建设有限公司', 'https://hhb.cbi360.net/sg_711082/', '142'],
                 ['湖州', '温州骏腾建设有限公司', 'https://hhb.cbi360.net/sg_1173343/', '20'],
                 ['湖州', '浙江竟成环保科技有限公司', 'https://hhb.cbi360.net/sg_835463/', '30'],
                 ['湖州', '温州楚天建设有限公司', 'https://hhb.cbi360.net/sg_990482/', '147'],
                 ['湖州', '浙江中梁建设有限公司', 'https://hhb.cbi360.net/sg_371298/', '86'],
                 ['湖州', '浙江正嘉建设有限公司', 'https://hhb.cbi360.net/sg_1183414/', '50'],
                 ['湖州', '浙江创力电子股份有限公司', 'https://hhb.cbi360.net/sg_1053057/', '20'],
                 ['绍兴', '浙江恒宏建设有限公司', 'https://hhb.cbi360.net/sg_1144019/', '161'],
                 ['绍兴', '嘉兴市华禹建设工程有限公司', 'https://hhb.cbi360.net/sg_1163548/', '74'],
                 ['绍兴', '嘉兴华伟建设有限公司', 'https://hhb.cbi360.net/sg_445201/', '281'],
                 ['绍兴', '浙江尚都建设有限公司', 'https://hhb.cbi360.net/sg_6060/', '501'],
                 ['绍兴', '浙江广屿建设有限公司', 'https://hhb.cbi360.net/sg_1496078/', '77'],
                 ['绍兴', '嘉兴市振宏建设有限公司', 'https://hhb.cbi360.net/sg_951284/', '150'],
                 ['绍兴', '嘉兴市禹禾建设工程有限公司', 'https://hhb.cbi360.net/sg_1581411/', '33'],
                 ['绍兴', '浙江鎏增古建园林工程有限公司', 'https://hhb.cbi360.net/sg_832717/', '225'],
                 ['绍兴', '浙江秀州建设有限公司', 'https://hhb.cbi360.net/sg_5951/', '491'],
                 ['绍兴', '浙江德盛信息科技有限公司', 'https://hhb.cbi360.net/sg_1078479/', '31'],
                 ['绍兴', '平湖市新信交通工程有限公司', 'https://hhb.cbi360.net/sg_1272896/', '9'],
                 ['绍兴', '巨鑫建设集团有限公司', 'https://hhb.cbi360.net/sg_1483712/', '476'],
                 ['绍兴', '嘉兴新禹园林建设有限公司', 'https://hhb.cbi360.net/sg_1075436/', '211'],
                 ['绍兴', '浙江恒欣建筑设计股份有限公司', 'https://hhb.cbi360.net/sg_1076446/', '2470'],
                 ['绍兴', '嘉兴市海发建设工程有限公司', 'https://hhb.cbi360.net/sg_966657/', '170'],
                 ['金华', '浙江长兴升旺建设有限公司', 'https://hhb.cbi360.net/sg_1129566/', '12'],
                 ['金华', '湖州恒申建设工程有限公司', 'https://hhb.cbi360.net/sg_1230716/', '44'],
                 ['金华', '湖州万华管道工程有限公司', 'https://hhb.cbi360.net/sg_1487986/', '5'],
                 ['金华', '湖州天辰建设工程有限公司', 'https://hhb.cbi360.net/sg_846148/', '151'],
                 ['金华', '湖州三通水利建设有限公司', 'https://hhb.cbi360.net/sg_236264/', '228'],
                 ['金华', '浙江长兴汇丰建设工程有限公司', 'https://hhb.cbi360.net/sg_406660/', '263'],
                 ['金华', '浙江长兴云达建设工程有限公司', 'https://hhb.cbi360.net/sg_773492/', '241'],
                 ['金华', '浙江长兴中远建设工程有限公司', 'https://hhb.cbi360.net/sg_860011/', '733'],
                 ['金华', '浙江长兴盛大建设有限公司', 'https://hhb.cbi360.net/sg_381966/', '464'],
                 ['金华', '浙江湖州环天交通工程有限公司', 'https://hhb.cbi360.net/sg_950938/', '144'],
                 ['金华', '浙江长兴中匠建设有限公司', 'https://hhb.cbi360.net/sg_1484914/', '61'],
                 ['金华', '浙江长兴大合建设有限公司', 'https://hhb.cbi360.net/sg_1612333/', '19'],
                 ['金华', '浙江长兴雨辰市政工程有限公司', 'https://hhb.cbi360.net/sg_1012164/', '63'],
                 ['金华', '安吉巨峰建筑有限公司', 'https://hhb.cbi360.net/sg_285268/', '210'],
                 ['金华', '湖州兆磊建设工程有限公司', 'https://hhb.cbi360.net/sg_1587218/', '4'],
                 ['衢州', '绍兴欣宸建筑工程有限公司', 'https://hhb.cbi360.net/sg_1519205/', '12'],
                 ['衢州', '嵊州和业建设工程有限公司', 'https://hhb.cbi360.net/sg_950143/', '67'],
                 ['衢州', '绍兴逸创建设有限公司', 'https://hhb.cbi360.net/sg_1485182/', '12'],
                 ['衢州', '浙江中帅建设有限公司', 'https://hhb.cbi360.net/sg_1270064/', '13'],
                 ['衢州', '嵊州卓巨装饰工程有限公司', 'https://hhb.cbi360.net/sg_1552115/', '4'],
                 ['衢州', '绍兴市越路交通工程有限公司', 'https://hhb.cbi360.net/sg_5836/', '99'],
                 ['衢州', '浙江上安建设有限公司', 'https://hhb.cbi360.net/sg_1105172/', '91'],
                 ['衢州', '浙江中和建筑设计有限公司', 'https://hhb.cbi360.net/sg_1212628/', '498'],
                 ['衢州', '绍兴市龙亦建设有限公司', 'https://hhb.cbi360.net/sg_1561675/', '15'],
                 ['衢州', '绍兴纬地建设有限公司', 'https://hhb.cbi360.net/sg_1599062/', '15'],
                 ['衢州', '浙江上风建设有限公司', 'https://hhb.cbi360.net/sg_800/', '123'],
                 ['衢州', '浙江天泰园林建设有限公司', 'https://hhb.cbi360.net/sg_5891/', '95'],
                 ['衢州', '绍兴中国轻纺城建筑工程有限公司', 'https://hhb.cbi360.net/sg_6213/', '76'],
                 ['衢州', '浙江宝厦建设有限公司', 'https://hhb.cbi360.net/sg_6401/', '124'],
                 ['衢州', '诸暨市鸿辉园林工程有限公司', 'https://hhb.cbi360.net/sg_854159/', '72'],
                 ['舟山', '新世纪建设集团有限公司', 'https://hhb.cbi360.net/sg_742819/', '457'],
                 ['舟山', '金华市捷胜建筑有限公司', 'https://hhb.cbi360.net/sg_1248552/', '31'],
                 ['舟山', '义乌洪城建设工程有限公司', 'https://hhb.cbi360.net/sg_1427184/', '4'],
                 ['舟山', '浙江尚拓建设有限公司', 'https://hhb.cbi360.net/sg_1232882/', '43'],
                 ['舟山', '浙江新时代建筑设计有限公司', 'https://hhb.cbi360.net/sg_1253534/', '262'],
                 ['舟山', '筑邦建设集团股份有限公司', 'https://hhb.cbi360.net/sg_1488214/', '246'],
                 ['舟山', '东阳市诚峰建设有限公司', 'https://hhb.cbi360.net/sg_1359619/', '15'],
                 ['舟山', '中天建设集团有限公司', 'https://hhb.cbi360.net/sg_622/', '4461'],
                 ['舟山', '武义县城南建筑工程有限公司', 'https://hhb.cbi360.net/sg_5994/', '27'],
                 ['舟山', '义乌市义宏市政工程有限公司', 'https://hhb.cbi360.net/sg_711633/', '57'],
                 ['舟山', '浙江华拓建设有限公司', 'https://hhb.cbi360.net/sg_1155809/', '14'],
                 ['舟山', '金华优安建设有限公司', 'https://hhb.cbi360.net/sg_1716688/', '1'],
                 ['舟山', '东阳聚诚建设有限公司', 'https://hhb.cbi360.net/sg_1241816/', '6'],
                 ['舟山', '武义广润建设工程有限公司', 'https://hhb.cbi360.net/sg_1211506/', '34'],
                 ['舟山', '武义兆翔建设有限公司', 'https://hhb.cbi360.net/sg_1427768/', '21'],
                 ['台州', '衢州市政园林股份有限公司', 'https://hhb.cbi360.net/sg_931539/', '476'],
                 ['台州', '浙江江山勘测设计有限公司', 'https://hhb.cbi360.net/sg_1291667/', '340'],
                 ['台州', '浙江中信检测有限公司', 'https://hhb.cbi360.net/sg_937799/', '142'],
                 ['台州', '浙江凌宇建设有限公司', 'https://hhb.cbi360.net/sg_1496091/', '275'],
                 ['台州', '浙江祥开建设有限公司', 'https://hhb.cbi360.net/sg_1466016/', '131'],
                 ['台州', '浙江红顺环境工程有限公司', 'https://hhb.cbi360.net/sg_1095912/', '114'],
                 ['台州', '衢州欣景环境建设有限公司', 'https://hhb.cbi360.net/sg_1678763/', '6'],
                 ['台州', '衢州万方建设有限公司', 'https://hhb.cbi360.net/sg_689129/', '195'],
                 ['台州', '浙江星禾建设有限公司', 'https://hhb.cbi360.net/sg_1681357/', '13'],
                 ['台州', '凌云环境建设集团有限公司', 'https://hhb.cbi360.net/sg_252282/', '460'],
                 ['台州', '浙江大衢建设有限公司', 'https://hhb.cbi360.net/sg_1208410/', '74'],
                 ['台州', '浙江巨化物流有限公司', 'https://hhb.cbi360.net/sg_1831845/', '1'],
                 ['台州', '衢州景丰建设有限公司', 'https://hhb.cbi360.net/sg_823532/', '131'],
                 ['台州', '浙江衢州久天建设有限公司', 'https://hhb.cbi360.net/sg_841671/', '103'],
                 ['台州', '浙江成艺环境建设有限公司', 'https://hhb.cbi360.net/sg_815601/', '359'],
                 ['丽水', '舟山市鼎力建设有限公司', 'https://hhb.cbi360.net/sg_174804/', '61'],
                 ['丽水', '舟山市大沙建筑工程有限公司', 'https://hhb.cbi360.net/sg_2331/', '248'],
                 ['丽水', '舟山恒山水利工程有限公司', 'https://hhb.cbi360.net/sg_971170/', '32'],
                 ['丽水', '舟山报业会展策划有限公司', 'https://hhb.cbi360.net/sg_1838735/', '1'],
                 ['丽水', '舟山市恒宇新能源科技有限公司', 'https://hhb.cbi360.net/sg_1269668/', '5'],
                 ['丽水', '舟山城星建设有限公司', 'https://hhb.cbi360.net/sg_1272825/', '18'],
                 ['丽水', '嵊泗县第一建筑工程有限责任公司', 'https://hhb.cbi360.net/sg_1765/', '107'],
                 ['丽水', '浙江恒昌建设有限公司', 'https://hhb.cbi360.net/sg_167143/', '282'],
                 ['丽水', '舟山市河川建设有限公司', 'https://hhb.cbi360.net/sg_1481965/', '1'],
                 ['丽水', '浙江万恒建设有限公司', 'https://hhb.cbi360.net/sg_442779/', '73'],
                 ['丽水', '浙江天隆工程管理有限公司', 'https://hhb.cbi360.net/sg_1178386/', '3'],
                 ['丽水', '浙江欣璐工程建设有限公司', 'https://hhb.cbi360.net/sg_1547597/', '33'],
                 ['丽水', '嵊泗县华丰市政工程有限公司', 'https://hhb.cbi360.net/sg_22482/', '22'],
                 ['丽水', '舟山恒航建设有限公司', 'https://hhb.cbi360.net/sg_1258789/', '20'],
                 ['丽水', '舟山市凯兴建筑工程有限责任公司', 'https://hhb.cbi360.net/sg_1383412/', '33'],
                 ['温州', '杭州骁博市政建设有限公司', 'https://hhb.cbi360.net/sg_1378755/', '25'],
                 ['温州', '杭州竣诚建设有限公司', 'https://hhb.cbi360.net/sg_1633656/', '1'],
                 ['温州', '浙江鑫格实业有限公司', 'https://hhb.cbi360.net/sg_1561964/', '14'],
                 ['温州', '浙江江天建设有限公司', 'https://hhb.cbi360.net/sg_1737964/', '100'],
                 ['温州', '杭州浩通建设工程有限公司', 'https://hhb.cbi360.net/sg_908462/', '109'],
                 ['温州', '杭州富裕建设有限公司', 'https://hhb.cbi360.net/sg_1139338/', '24'],
                 ['温州', '杭州河川建设有限公司', 'https://hhb.cbi360.net/sg_1084838/', '347'],
                 ['温州', '杭州中奕建筑工程有限公司', 'https://hhb.cbi360.net/sg_1228497/', '32'],
                 ['温州', '杭州永信建设有限公司', 'https://hhb.cbi360.net/sg_1355943/', '29'],
                 ['温州', '浙江经纬工程设计有限公司', 'https://hhb.cbi360.net/sg_1156127/', '482'],
                 ['温州', '浙江乾锦建设有限公司', 'https://hhb.cbi360.net/sg_1483704/', '114'],
                 ['温州', '浙江明杰建设有限公司', 'https://hhb.cbi360.net/sg_1887/', '135'],
                 ['温州', '杭州盈通科技有限公司', 'https://hhb.cbi360.net/sg_757774/', '3'],
                 ['温州', '杭州天涧水利工程有限公司', 'https://hhb.cbi360.net/sg_819921/', '194'],
                 ['温州', '浙江安道设计股份有限公司', 'https://hhb.cbi360.net/sg_1136407/', '11'],
                 ['嘉兴', '宁波日月交通安全设施工程有限公司', 'https://hhb.cbi360.net/sg_710777/', '207'],
                 ['嘉兴', '宁波欧天洋建设有限公司', 'https://hhb.cbi360.net/sg_1230468/', '3'],
                 ['嘉兴', '宁波姚江水利生态建设有限公司', 'https://hhb.cbi360.net/sg_1139638/', '431'],
                 ['嘉兴', '宁波甬新东方电气有限公司', 'https://hhb.cbi360.net/sg_533241/', '2'],
                 ['嘉兴', '华创电子股份有限公司', 'https://hhb.cbi360.net/sg_960398/', '232'],
                 ['嘉兴', '宁波欣承生态建设有限公司', 'https://hhb.cbi360.net/sg_1140215/', '33'],
                 ['嘉兴', '宁波丰信建设工程有限公司', 'https://hhb.cbi360.net/sg_1005929/', '7'],
                 ['嘉兴', '宁波金筑建设工程有限公司', 'https://hhb.cbi360.net/sg_1265065/', '21'],
                 ['嘉兴', '浙江信电技术股份有限公司', 'https://hhb.cbi360.net/sg_528614/', '21'],
                 ['嘉兴', '浙江艺峰装饰工程有限公司', 'https://hhb.cbi360.net/sg_3718/', '88'],
                 ['嘉兴', '慈溪市城乡建设建筑工程有限公司', 'https://hhb.cbi360.net/sg_709647/', '141'],
                 ['嘉兴', '宁波中科市政园林建设有限公司', 'https://hhb.cbi360.net/sg_889064/', '261'],
                 ['嘉兴', '宁波东元生态建设有限公司', 'https://hhb.cbi360.net/sg_968740/', '319'],
                 ['嘉兴', '慈溪市泰兴电子有限公司', 'https://hhb.cbi360.net/sg_903223/', '5'],
                 ['嘉兴', '宁波龙元盛宏生态建设工程有限公司', 'https://hhb.cbi360.net/sg_1132565/', '27'],
                 ['湖州', '浙江创立建设工程有限公司', 'https://hhb.cbi360.net/sg_1272716/', '22'],
                 ['湖州', '温州益坤电气股份有限公司', 'https://hhb.cbi360.net/sg_1494834/', '5'],
                 ['湖州', '鲲鹏建设集团有限公司', 'https://hhb.cbi360.net/sg_2760/', '876'],
                 ['湖州', '温州永立建筑工程有限公司', 'https://hhb.cbi360.net/sg_276648/', '119'],
                 ['湖州', '华宇市政园林建设有限公司', 'https://hhb.cbi360.net/sg_903759/', '245'],
                 ['湖州', '温州博众建设工程有限公司', 'https://hhb.cbi360.net/sg_1071492/', '13'],
                 ['湖州', '浙江骏泰建设工程有限公司', 'https://hhb.cbi360.net/sg_1459912/', '15'],
                 ['湖州', '浙江森唯建筑有限公司', 'https://hhb.cbi360.net/sg_1838528/', '1'],
                 ['湖州', '温州腾胜建设有限公司', 'https://hhb.cbi360.net/sg_1279692/', '11'],
                 ['湖州', '浙江柳建建设有限公司', 'https://hhb.cbi360.net/sg_1181435/', '26'],
                 ['湖州', '温州华睿建设有限公司', 'https://hhb.cbi360.net/sg_1392066/', '15'],
                 ['湖州', '浙江同鑫建设有限公司', 'https://hhb.cbi360.net/sg_1428009/', '19'],
                 ['湖州', '温州高速公路养护中心有限公司', 'https://hhb.cbi360.net/sg_1641330/', '24'],
                 ['湖州', '温州日力电梯有限公司', 'https://hhb.cbi360.net/sg_1125643/', '10'],
                 ['湖州', '浙江东晟建设工程有限公司', 'https://hhb.cbi360.net/sg_1109994/', '187'],
                 ['绍兴', '浙江永曜环境发展有限公司', 'https://hhb.cbi360.net/sg_1513686/', '2'],
                 ['绍兴', '嘉善星耘建设有限公司', 'https://hhb.cbi360.net/sg_1836939/', '1'],
                 ['绍兴', '嘉兴市水利工程建筑有限责任公司', 'https://hhb.cbi360.net/sg_710459/', '349'],
                 ['绍兴', '浙江尚博建设有限公司', 'https://hhb.cbi360.net/sg_814128/', '131'],
                 ['绍兴', '嘉兴市嘉翔建设有限公司', 'https://hhb.cbi360.net/sg_1194565/', '83'],
                 ['绍兴', '平湖市通顺交通设施有限公司', 'https://hhb.cbi360.net/sg_692337/', '340'],
                 ['绍兴', '嘉兴宇鸿建设工程有限公司', 'https://hhb.cbi360.net/sg_1498930/', '5'],
                 ['绍兴', '嘉兴骏腾电力建设有限公司', 'https://hhb.cbi360.net/sg_1675308/', '5'],
                 ['绍兴', '浙江嘉越建设有限公司', 'https://hhb.cbi360.net/sg_374710/', '286'],
                 ['绍兴', '海盐城市园林绿化工程有限责任公司', 'https://hhb.cbi360.net/sg_7249/', '47'],
                 ['绍兴', '平湖市腾达建设工程有限公司', 'https://hhb.cbi360.net/sg_670558/', '193'],
                 ['绍兴', '浙江辰基建设有限公司', 'https://hhb.cbi360.net/sg_931882/', '67'],
                 ['绍兴', '嘉兴市众鑫建设有限公司', 'https://hhb.cbi360.net/sg_861765/', '84'],
                 ['绍兴', '浙江东海岸园艺有限公司', 'https://hhb.cbi360.net/sg_1949/', '162'],
                 ['绍兴', '嘉兴巨昇建设有限公司', 'https://hhb.cbi360.net/sg_1247983/', '46'],
                 ['金华', '浙江长兴万发建筑工程有限公司', 'https://hhb.cbi360.net/sg_1110155/', '133'],
                 ['金华', '浙江长兴圣通建设有限公司', 'https://hhb.cbi360.net/sg_1145488/', '71'],
                 ['金华', '安吉宏瑞建设有限公司', 'https://hhb.cbi360.net/sg_1126282/', '20'],
                 ['金华', '浙江艺佳地理信息技术有限公司', 'https://hhb.cbi360.net/sg_1304305/', '1'],
                 ['金华', '长兴万达建设有限公司', 'https://hhb.cbi360.net/sg_381961/', '524'],
                 ['金华', '浙江安吉昌鑫建设有限公司', 'https://hhb.cbi360.net/sg_1275044/', '29'],
                 ['金华', '浙江鑫晟建设有限公司', 'https://hhb.cbi360.net/sg_1234879/', '56'],
                 ['金华', '浙江冠龙市政园林有限公司', 'https://hhb.cbi360.net/sg_947342/', '50'],
                 ['金华', '浙江长兴康华建筑安装工程有限公司', 'https://hhb.cbi360.net/sg_886409/', '203'],
                 ['金华', '恒达富士电梯有限公司', 'https://hhb.cbi360.net/sg_287946/', '806'],
                 ['金华', '湖州德超建设有限公司', 'https://hhb.cbi360.net/sg_1357677/', '29'],
                 ['金华', '浙江大成网络科技有限公司', 'https://hhb.cbi360.net/sg_1732849/', '2'],
                 ['金华', '德清县永恒建设有限公司', 'https://hhb.cbi360.net/sg_236269/', '183'],
                 ['金华', '长兴县雉城建筑工程公司', 'https://hhb.cbi360.net/sg_8328/', '58'],
                 ['金华', '长兴文远建设工程有限公司', 'https://hhb.cbi360.net/sg_1145578/', '74'],
                 ['衢州', '绍兴东茂环境建设有限公司', 'https://hhb.cbi360.net/sg_887947/', '155'],
                 ['衢州', '浙江文和环境建设有限公司', 'https://hhb.cbi360.net/sg_913416/', '228'],
                 ['衢州', '新昌县利鑫建设有限公司', 'https://hhb.cbi360.net/sg_922384/', '135'],
                 ['衢州', '华键建筑集团有限公司', 'https://hhb.cbi360.net/sg_1208859/', '33'],
                 ['衢州', '绍兴越州都市规划设计院', 'https://hhb.cbi360.net/sg_1287002/', '23'],
                 ['衢州', '诸暨新橙市政园林工程有限公司', 'https://hhb.cbi360.net/sg_1521010/', '18'],
                 ['衢州', '诸暨昱承建设有限公司', 'https://hhb.cbi360.net/sg_1389650/', '4'],
                 ['衢州', '博大环境集团有限公司', 'https://hhb.cbi360.net/sg_804769/', '490'],
                 ['衢州', '浙江禹东建设有限公司', 'https://hhb.cbi360.net/sg_1156628/', '93'],
                 ['衢州', '绍兴玉宸建设有限公司', 'https://hhb.cbi360.net/sg_1619465/', '37'],
                 ['衢州', '浙江双和环境建设有限公司', 'https://hhb.cbi360.net/sg_867528/', '197'],
                 ['衢州', '绍兴上虞德金建设有限公司', 'https://hhb.cbi360.net/sg_1520369/', '5'],
                 ['衢州', '浙江舜达建设工程有限公司', 'https://hhb.cbi360.net/sg_538893/', '130'],
                 ['衢州', '诸暨吉高建设有限公司', 'https://hhb.cbi360.net/sg_1559154/', '17'],
                 ['衢州', '诸暨市吉辰建设有限公司', 'https://hhb.cbi360.net/sg_1559164/', '9'],
                 ['舟山', '浙江中图建设有限公司', 'https://hhb.cbi360.net/sg_1492456/', '4'],
                 ['舟山', '义乌市煜鑫建设工程有限公司', 'https://hhb.cbi360.net/sg_1710349/', '4'],
                 ['舟山', '义乌市恒风路桥有限公司', 'https://hhb.cbi360.net/sg_711623/', '69'],
                 ['舟山', '浙江大自然园艺有限公司', 'https://hhb.cbi360.net/sg_2492/', '22'],
                 ['舟山', '金华市至臻环境建设有限公司', 'https://hhb.cbi360.net/sg_964929/', '25'],
                 ['舟山', '婺江装饰集团有限公司', 'https://hhb.cbi360.net/sg_1199652/', '66'],
                 ['舟山', '浙江省东阳市铿锵建设有限公司', 'https://hhb.cbi360.net/sg_1238260/', '14'],
                 ['舟山', '金华市三特建筑工程有限公司', 'https://hhb.cbi360.net/sg_1675663/', '1'],
                 ['舟山', '浙江跃辉建设工程有限公司', 'https://hhb.cbi360.net/sg_1659850/', '1'],
                 ['舟山', '义乌市大鸿建设工程有限公司', 'https://hhb.cbi360.net/sg_593903/', '125'],
                 ['舟山', '金华市鸿晟建设有限公司', 'https://hhb.cbi360.net/sg_757278/', '183'],
                 ['舟山', '浙江中叶建设有限公司', 'https://hhb.cbi360.net/sg_1737735/', '6'],
                 ['舟山', '武义鸿汇建筑工程有限公司', 'https://hhb.cbi360.net/sg_711571/', '93'],
                 ['舟山', '金华市国力建设有限公司', 'https://hhb.cbi360.net/sg_950972/', '164'],
                 ['舟山', '金华市中跃建设有限公司', 'https://hhb.cbi360.net/sg_1548173/', '2'],
                 ['台州', '衢州市交通设计有限公司', 'https://hhb.cbi360.net/sg_1062525/', '92'],
                 ['台州', '浙江常建建设有限公司', 'https://hhb.cbi360.net/sg_1402474/', '212'],
                 ['台州', '衢州三众建设有限公司', 'https://hhb.cbi360.net/sg_911591/', '130'],
                 ['台州', '云程环境建设集团有限公司', 'https://hhb.cbi360.net/sg_1078584/', '237'],
                 ['台州', '浙江顺成建设有限公司', 'https://hhb.cbi360.net/sg_1204632/', '192'],
                 ['台州', '浙江中禾市政工程有限公司', 'https://hhb.cbi360.net/sg_1479440/', '9'],
                 ['台州', '浙江开腾建设有限公司', 'https://hhb.cbi360.net/sg_1210288/', '81'],
                 ['台州', '衢州光明电力设计有限公司', 'https://hhb.cbi360.net/sg_1284345/', '15'],
                 ['台州', '江山市万豪公路养护工程有限公司', 'https://hhb.cbi360.net/sg_845069/', '107'],
                 ['台州', '衢州市德丰建筑工程有限公司', 'https://hhb.cbi360.net/sg_926556/', '370'],
                 ['台州', '衢州星昇建设有限公司', 'https://hhb.cbi360.net/sg_1836918/', '1'],
                 ['台州', '浙江宏昇达交通建设有限公司', 'https://hhb.cbi360.net/sg_1156217/', '7'],
                 ['台州', '浙江韩盛环境建设有限公司', 'https://hhb.cbi360.net/sg_1374270/', '22'],
                 ['台州', '衢州光明电力投资集团有限公司', 'https://hhb.cbi360.net/sg_1414074/', '16'],
                 ['台州', '衢州市衢美建设有限公司', 'https://hhb.cbi360.net/sg_1708555/', '17'],
                 ['丽水', '舟山市捷升水利科技开发有限公司', 'https://hhb.cbi360.net/sg_1256479/', '3'],
                 ['丽水', '浙江嵊泗景翔建设有限公司', 'https://hhb.cbi360.net/sg_961243/', '79'],
                 ['丽水', '舟山欣鸿建筑工程有限公司', 'https://hhb.cbi360.net/sg_1157822/', '8'],
                 ['丽水', '舟山市益民建筑安装工程有限公司', 'https://hhb.cbi360.net/sg_446980/', '133'],
                 ['丽水', '浙江舟山海洋输电研究院有限公司', 'https://hhb.cbi360.net/sg_1284647/', '3'],
                 ['丽水', '浙江康腾建设有限公司', 'https://hhb.cbi360.net/sg_6813/', '100'],
                 ['丽水', '和海建设科技集团有限公司', 'https://hhb.cbi360.net/sg_1492081/', '164'],
                 ['丽水', '舟山瑞思泳池设备有限公司', 'https://hhb.cbi360.net/sg_1836877/', '1'],
                 ['丽水', '浙江河海建设有限公司', 'https://hhb.cbi360.net/sg_538860/', '144'],
                 ['丽水', '浙江昌屹建设有限公司', 'https://hhb.cbi360.net/sg_371501/', '180'],
                 ['丽水', '浙江伟华市政工程有限公司', 'https://hhb.cbi360.net/sg_1508147/', '1'],
                 ['丽水', '浙江昌鼎建设有限公司', 'https://hhb.cbi360.net/sg_6310/', '193'],
                 ['丽水', '舟山大宏建设有限公司', 'https://hhb.cbi360.net/sg_8400/', '44'],
                 ['丽水', '舟山骏华建设工程有限公司', 'https://hhb.cbi360.net/sg_695217/', '63'],
                 ['丽水', '舟山市宏达交通工程有限责任公司', 'https://hhb.cbi360.net/sg_815873/', '191']]

            # datalist2=    [['湖州', '浙江艺美建筑装饰工程有限公司', 'https://hhb.cbi360.net/sg_1737837/', '36']]
            data = []
            #得到相应企业的全部中标业绩
            self.get_qyyj_detail(jst_qyyj_detali_page, conp, datalist, self.driver, tablename,data)

            # 到数据到excle中
            columnRows = ["href", "shi", "zhongbiaoren", "ggname", "xmjl", "zbtime"]
            wirteDataToExcel(outfilename, "jst_qyyj_zhejiang", columnRows, data)





if  __name__ == '__main__':
        unittest.main(verbosity=2)
        # print("%s 页面中未能找到 %s 元素" % ("2", "8"))

