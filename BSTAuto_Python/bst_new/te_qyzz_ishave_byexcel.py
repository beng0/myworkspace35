import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime


root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'

# 省平台qyzz
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzzwithzzcode_贺家斌_20201109_184203.xlsx"
sheng_datalist = read_excel(infilename1)
print(sheng_datalist)
print(sheng_datalist[0][1])
print(sheng_datalist[0][1][1])
print(sheng_datalist[0][1][1][2])
print(sheng_datalist[0][1][1][7])

# 标事通qyzz
infilename2 = root_dir + r"\get_bst_ryzz_qyzz\云南bst企业资质_贺家斌_20201111_114644.xlsx"
bst_datalist = read_excel(infilename2)
# print(bst_datalist)
# print(bst_datalist[0][1][1])
print(bst_datalist[0][1][1][2])
print(bst_datalist[0][1][1][7])

# 建设通qyzz
infilename3 = root_dir + r"\get_jst_ryzz_qyzz\云南_建设通qyzzwithzzcode_贺家斌_20201112_110118.xlsx"
jst_datalist = read_excel(infilename3)
# print(jst_datalist)
# print(jst_datalist[0][1][1])
print(jst_datalist[0][1][1][2])
print(jst_datalist[0][1][1][7])

# 合并后的qyzz
infilename4 = root_dir + r"\hebin\合并qyzz_sheng_jst_bst.xlsx"
hb_datalist =  read_excel(infilename4)
print(hb_datalist[0][1][1][2])
print(hb_datalist[0][1][1][7])


# 存放合并对比后的数据
qyzz_data = []
for qyzzlis in hb_datalist[0][1][1:]:
    bstishave = ''
    jstishave = ''
    shengishave = ''
    qyname = qyzzlis[2]
    zzcode = qyzzlis[7]
    # print(qyname,zzcode)
    # print(bst_datalist[0][1:])
    # 测试合并资质标事通是否有
    for bst_qyzz in bst_datalist[0][1][1:]:
        # print(bst_qyzz[3],bst_qyzz[6])
        if bst_qyzz[2] == qyname and bst_qyzz[7] == str(zzcode):
            bstishave = '有'
            break
        else:
            bstishave = "无"
    # 测试合并资质建设通是否有
    for jst_qyzz in jst_datalist[0][1][1:]:
        if jst_qyzz[2] == qyname and str(jst_qyzz[7]) == str(zzcode):
            jstishave = '有'
            break
        else:
            jstishave = '无'
    # 测试合并资质省平台是否有
    for sheng_qyzz in sheng_datalist[0][1][1:]:
        if sheng_qyzz[2] == qyname and str(sheng_qyzz[7]) == str(zzcode):
            shengishave = '有'
            break
        else:
            shengishave = '无'

    tmp = [qyzzlis[0], qyzzlis[1], qyzzlis[2],
           qyzzlis[3], qyzzlis[4], qyzzlis[5], qyzzlis[6],qyzzlis[7],qyzzlis[8],bstishave,jstishave,shengishave]
    qyzz_data.append(tmp)

# 测试标事通资质云南省平台是否有
# qyzz1_data = []
# for qyzzlis1 in bst_datalist[0][1][1:]:
#     ishave = ''
#     for qyzz in  sheng_datalist[0][1][1:]:
#         if qyzz[2] == qyzzlis1[3] and str(qyzz[7]) == qyzzlis1[6]:
#             ishave = '有'
#             break
#         else:
#             ishave = '无'
#     tmp1 = [qyzzlis1[0],qyzzlis1[1],qyzzlis1[2],qyzzlis1[3],qyzzlis1[4],qyzzlis1[5],qyzzlis1[6],ishave]
#     qyzz1_data.append(tmp1)



tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["sheng","shi","entname", "zzdj","zslb", "date","date","zzcode","source","标事通是否有","建设通是否有","省平台是否有"]
# outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzzwithzzcode_bstishave_贺家斌_"
# outfilename2_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzzwithzzcode_shenghave_贺家斌_"
outfilename_hebin_qyzz = root_dir + r"\hebin\云南_合并后qyzz各平台是否有_贺家斌_"
wirteDataToExcel(outfilename_hebin_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyzz_data)
# wirteDataToExcel(outfilename2_qyzz + tablenamehouzui + '.xlsx',"qyzz_data",columnRows,qyzz1_data)
print("qyzz_data to  excel  success")