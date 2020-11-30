import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime



root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
# 省平台人员资质
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台xmjlzzwithzzcode_贺家斌_20201117_195300.xlsx"
sheng_datalist = read_excel(infilename1)
print(sheng_datalist)
print(sheng_datalist[0][1])
print(sheng_datalist[0][1][1])
print(sheng_datalist[0][1][1][2])
print(sheng_datalist[0][1][1][3])
print(sheng_datalist[0][1][1][8])

# 标事通人员资质
infilename2 = root_dir + r"\get_bst_ryzz_qyzz\标事通xmjlzz_数据准备_贺家斌_20201117_170420.xlsx"
bst_datalist = read_excel(infilename2)
print(bst_datalist)
print(bst_datalist[0][1][1])
print(bst_datalist[0][1][1][2])
print(bst_datalist[0][1][1][3])
print(bst_datalist[0][1][1][8])

# 建设通人员资质
infilename3 = root_dir + r"\get_jst_ryzz_qyzz\云南_建设通xmjl_ryzzwithzzcode_贺家斌_20201117_101035.xlsx"
jst_datalist = read_excel(infilename3)

# 合并人员资质
infilename4 = root_dir + r"\hebin\合并xmjlzz_sheng_jst_bst.xlsx"
hb_datalist = read_excel(infilename4)


ryzz_data = []
for ryzzlis in hb_datalist[0][1][1:]:
    bstishave = ''
    jstishave = ''
    shengishave = ''
    qyname = ryzzlis[2]
    ryname = ryzzlis[3]
    zzcode = ryzzlis[8]
    # 测试合并资质标事通是否有
    for bst_ryzz in bst_datalist[0][1][1:]:
        if qyname == bst_ryzz[2] and ryname == bst_ryzz[3] and str(zzcode) == bst_ryzz[8]:
            bstishave = '有'
            break
        else:
            bstishave = "无"
    # 测试合并人员资质建设通是否有
    for jst_ryzz in jst_datalist[0][1][1:]:
        if qyname == jst_ryzz[2] and ryname == jst_ryzz[3] and str(zzcode) == str(jst_ryzz[8]):
            jstishave = '有'
            break
        else:
            jstishave = '无'
    for sheng_ryzz in sheng_datalist[0][1][1:]:
        if qyname == sheng_ryzz[2] and ryname == sheng_ryzz[3] and str(zzcode) == str(sheng_ryzz[8]):
            shengishave = '有'
            break
        else:
            shengishave = '无'
    tmp = [ryzzlis[0], ryzzlis[1], ryzzlis[2],
           ryzzlis[3], ryzzlis[4], ryzzlis[5],
           ryzzlis[6],ryzzlis[7],ryzzlis[8],ryzzlis[9],bstishave,jstishave,shengishave]
    ryzz_data.append(tmp)

# # 测试标事通有云南省没有的资质
#
# ryzz1_data = []
# for bst_ryzz1 in bst_datalist[0][1][1:]:
#     ishave = ''
#     for ryzzlis1 in sheng_datalist[0][1][1:]:
#         if ryzzlis1[2] == bst_ryzz1[3] and ryzzlis1[3] == bst_ryzz1[4] and str(ryzzlis1[8]) == bst_ryzz1[8]:
#             ishave = '有'
#             break
#         else:
#             ishave = "无"
#     tmp1 = [bst_ryzz1[0], bst_ryzz1[1], bst_ryzz1[2],
#            bst_ryzz1[3], bst_ryzz1[4], bst_ryzz1[5], bst_ryzz1[6],bst_ryzz1[7],bst_ryzz1[8],ishave]
#     ryzz1_data.append(tmp1)


tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["sheng","shi","entname", "name","sfz", "zzmc",
              "zzdj","zhuanye","ryzzcode","source","bstishave","jstishave","shengishave"]
# outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台ryzzwithzzcode_bstishave_贺家斌_"
# outfilename2 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台ryzzwithzzcode_shengishave_贺家斌_"
outfilename_hebin_ryzz = root_dir + r"\hebin\云南_合并后ryzz各平台是否有_贺家斌_"
wirteDataToExcel(outfilename_hebin_ryzz + tablenamehouzui + ".xlsx", "ryzz_data", columnRows, ryzz_data)
# wirteDataToExcel(outfilename2 + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, ryzz1_data)
print("qyzz_data to  excel  success")