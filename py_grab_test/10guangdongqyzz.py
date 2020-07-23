#coding= utf-8

from py_grab_test.selenium_base import *

se = Base_()
bs = Bsoup()
de = Doexcel()

se.open_("http://data.gdcic.net/Dop/Open/EnterpriseList.aspx")

se.get_position("xpath","//span/input[@placeholder='企业名称']").send_keys("深圳远鹏装饰集团有限公司")

se.get_position("xpath","//span/input[@placeholder='验证码']").send_keys("8888")

# todo 验证码识别输入