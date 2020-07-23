# str = "kf;jfks;"
# lis = str.split(";")
# print(lis)
# lis.pop(-1)
# print(lis)
#
# # lis1 = []
# # lis1.pop()
# #
# # print(lis1)
# str1 = ""
#
# lis3 = str1.split(";")
# lis3.pop()
# print(lis3)
#
# for li in lis3:
#     lis.append(li)
#
# print(lis)
# import re
#
# str =  "首页 | 上一页 | 下一页 | 尾页 　 当前显示 71 - 75 条　共 75 条 | 第页 / 共 6 页　 条/页   "
# str1 = "ssshello world"
# pattern = re.compile(r'.*?共 (\d) 页')
# match = pattern.match(str)
#
# print(match.group(1))
from py_grab_test.selenium_base import *
de = Doexcel()
qy_lis = de.read_excel("D:\mydocument\svn - 副本\数据对比\对比结果\广东、深圳每周数据对比结果\山西企业列表.xlsx","Sheet1")

for qy_r in qy_lis:
    qyname = qy_r[1]
    print(len(qy_lis))
    print(qyname)


