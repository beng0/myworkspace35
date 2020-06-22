#coding=utf-8
import re
str = "所属企业名称：吉林省建苑设计集团有限公司发证单位：注册专业：建筑工程注册专业有效期：2011年12月01日所属企业名称：吉林省建苑设计集团有限公司发证单位,注册专业：房屋建筑工程注册有效期："

# matchobj = re.search(r"注册专业：(.*?)注册专业有效期：",str)
# print(matchobj)
# print(matchobj.group(1))

#
# str1 = "东西:计算机系统:"
#
# print(re.search(r"东西:(.*?)系统:",str1).group(1))

it = re.findall(r"注册专业：(.*?)注册",str)
for i in it:
    print(i)


lis = [1,2.3]
str2 = ''
lis.append(str2)
print(lis)