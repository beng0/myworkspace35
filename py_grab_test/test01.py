#coding=utf-8

from py_grab_test.selenium_base import  *
from py_grab_test.base import *
import xlwt

book = xlwt.Workbook()
sheet = book.add_sheet("sheet1",cell_overwrite_ok=True)

se = Base_()

se.open_("http://hngcjs.hnjs.gov.cn/company/list?corpname=")
# driver.switch_to_frame("newsiframe")
# ele = se.get_position("css selector","select#CretType")
#
# s = Select(ele)
# s.select_by_value("1")
# 选择建筑业
se.select_by_value("css selector","select#CretType","7")
# 点击唤出企业注册地下拉框
se.click_("css selector",".filter_dropdown>span>span")
# 获取注册地的个数
ele = se.get_positions("css selector",".dropdown-menu.staff_dropdown>li")
print(ele)