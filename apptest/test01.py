#coding=utf-8
import os
from time import sleep
import unittest
import unittest
from apptest.HTMLRunnerTest import HTMLTestRunner

from appium import webdriver

# Returns abs path relative to this file and not cwd

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '10'
desired_caps['deviceName'] = 'BKL_AL20'
desired_caps['appPackage'] = 'com.zhulong.escort'
desired_caps['appActivity'] = '.mvp.activity.welcome.WelcomeActivity'


desired_caps['resetKeyboard'] = True


driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

driver.find_element_by_id("tv_agree").click()

sleep(3)

def swipe_left(t):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x*0.9,y*0.5,x*0.1,y*0.5,t)

swipe_left(1000)
swipe_left(1000)
swipe_left(1000)

# 点击进入首页
driver.find_element_by_id("com.zhulong.escort:id/tv_button").click()
# sleep(3)

# 点击授权
# driver.find_element_by_id("com.android.permissioncontroller:id/permission_allow_always_button").click()
# driver.tap([(500,1500)],1000)
sleep(1)
# 关闭维护弹窗和升级弹窗
# 维护
# driver.find_element_by_id("com.zhulong.escort:id/iv_close").click()
# 升级
# driver.find_element_by_id("com.zhulong.escort:id/btn_close").click()
# 点击授权正式环境
driver.find_element_by_id("android:id/button1").click()
sleep(1)
# 点击我的，跳转到登录页面
driver.find_element_by_xpath("//*[@text='我的']").click()
sleep(1)
# 输入手机号
driver.find_element_by_id("com.zhulong.escort:id/tv_phone_num").send_keys("17600000024")

# 点击注册登录
driver.find_element_by_id("com.zhulong.escort:id/tv_regist").click()
# 输入密码
driver.find_element_by_id("com.zhulong.escort:id/tv_login_pwd").send_keys("a123456")
# 点击登录
driver.find_element_by_id("com.zhulong.escort:id/tv_login").click()
sleep(0.5)
ele =  driver.find_element_by_xpath("//*[@class='android.widget.Toast']")
print(ele)
log_txt = ele.text
print(log_txt)

class Mytest(unittest.TestCase):
    def tearDown(self):
        print("111")
    def setUp(self):
        print("2222")

    @classmethod
    def tearDownClass(self):
        print("444444")
    @classmethod
    def setUpClass(self):
        print("33333")

    def test_login_success(self):
        self.assertEqual(log_txt,"登录成功")

    def test_login_failure(self):
        self.assertEqual(log_txt,"登录失败")

if __name__ == '__main__':
    testunit = unittest.TestSuite()
    testunit.addTest(Mytest("test_login_success"))
    testunit.addTest(Mytest("test_login_failure"))
    fp = open('./result.html','wb')
    runner = HTMLTestRunner(stream=fp,title='hetest',description='测试报告')
    runner.run(testunit)
    fp.close()























