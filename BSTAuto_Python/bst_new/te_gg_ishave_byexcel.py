import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
# 标事通标讯
infilename1 = root_dir + r"\get_bst_gg\标事通标讯_数据准备_贺家斌_20201112_172453.xlsx"
bst_datalist = read_excel(infilename1)
print(bst_datalist)
print(bst_datalist[0][1])
print(bst_datalist[0][1][1])
print(bst_datalist[0][1][1][0])
print(bst_datalist[0][1][1][1])

# 剑鱼标讯
infilename2 = root_dir + r"\jianyu\jianyuggnames_20201112_154240.xlsx"
jy_datalist = read_excel(infilename2)
print(jy_datalist)
print(jy_datalist[0][1][1])
print(jy_datalist[0][1][1][0])
print(jy_datalist[0][1][1][1])

# 合并标讯
infilename4 = root_dir + r"\hebin\合并标讯_bst_jianyu.xlsx"
hb_datalist = read_excel(infilename4)


gg_data = []
for qyyjlis in hb_datalist[0][1][1:]:
    qyname = qyyjlis[0]
    gg = qyyjlis[1]
    bstishave = ''
    jyishave = ''
    # 测试合并标讯标事通是否有
    for bst_gg in bst_datalist[0][1][1:]:
        if qyname == bst_gg[0] and gg[:9] == bst_gg[1][:9]:
            bstishave = "有"
            break
        else:
            bstishave = "无"
    # 测试合并标讯剑鱼是否有
    for jy_gg in jy_datalist[0][1][1:]:
        if qyname == jy_gg[0] and gg[:9] == jy_gg[1][:9]:
            jyishave = "有"
            break
        else:
            jyishave = "无"


    tmp = [qyyjlis[0],qyyjlis[1],qyyjlis[2],qyyjlis[3],qyyjlis[4],bstishave,jyishave]
    gg_data.append(tmp)

# for jstqyyjlis in jst_datalist[0][1][1:]:
#     jstqyname = jstqyyjlis[1]
#     jstqyyj = jstqyyjlis[2]
#     for qyyjlis in qyyj_datalist[0][1][1:]:
#         if jstqyname == qyyjlis[1] and jstqyyj[:9] == qyyjlis[2][:9]:
#             bsthave = "有"
#             break
#         else:
#             bsthave = "无"
#     tmp = [jstqyyjlis[0],jstqyyjlis[1],jstqyyjlis[2],jstqyyjlis[3],jstqyyjlis[4],jstqyyjlis[5],jstqyyjlis[6],
#            jstqyyjlis[2][:9],"jst",bsthave]
#     qyyj_data.append(tmp)


tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["kw", "ggname","fabu_time", "html_key",
              "source","bstishave","jyishave"]
outfilename_gd_qyzz = root_dir + r"\hebin\云南_合并后标讯各平台是否有_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, gg_data)
print("qyyj_data to  excel  success")