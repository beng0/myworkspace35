import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
# 标事通项目经理业绩
infilename1 = root_dir + r"\get_bst_xmjlyj\云南_bst_xmjlyj_获取结果_20201112_181120.xlsx"
bst_datalist = read_excel(infilename1)
print(bst_datalist)
print(bst_datalist[0][1])
print(bst_datalist[0][1][1])
print(bst_datalist[0][1][1][1])
print(bst_datalist[0][1][1][2])
print(bst_datalist[0][1][1][3])

# 建设通项目经理业绩
infilename2 = root_dir + r"\get_jst_xmjlyj\建设通企业业绩_中标公示_贺家斌_20201112_095806.xlsx"
jst_datalist = read_excel(infilename2)
print(jst_datalist)
print(jst_datalist[0][1][1])
print(jst_datalist[0][1][1][1])
print(jst_datalist[0][1][1][2])
print(jst_datalist[0][1][1][3])

# 合并项目经理业绩
infilename3 = root_dir + r"\hebin\合并项目经理业绩_bst_jst.xlsx"
hb_datalist = read_excel(infilename3)

xmjlyj_data = []
for xmjlyjlis in hb_datalist[0][1][1:]:
    qyname = xmjlyjlis[1]
    xmjl = xmjlyjlis[2]
    xmjlyj = xmjlyjlis[3]
    bsthave = ''
    jsthave = ''
    # 测试合并业绩标事通是否有
    for bst_xmjlyj in bst_datalist[0][1][1:]:
        if qyname == bst_xmjlyj[1] and xmjl == bst_xmjlyj[2] and xmjlyj[:9] == bst_xmjlyj[3][:9]:
            bsthave = "有"
            break
        else:
            bsthave = "无"
    # 测试合并项目经理业绩建设通是否有
    for jst_xmjlyj in jst_datalist[0][1][1:]:
        if qyname == jst_xmjlyj[1] and xmjl == jst_xmjlyj[2] and xmjlyj[:9] == jst_xmjlyj[3][:9]:
            jsthave = "有"
            break
        else:
            jsthave = "无"
    tmp = [xmjlyjlis[0],xmjlyjlis[1],xmjlyjlis[2],xmjlyjlis[3],xmjlyjlis[4],xmjlyjlis[5],xmjlyjlis[6],
           xmjlyjlis[7],xmjlyjlis[8],xmjlyjlis[9],bsthave,jsthave]
    xmjlyj_data.append(tmp)

# for jstqyyjlis in jst_datalist[0][1][1:]:
#     jstqyname = jstqyyjlis[1]
#     jstxmjl = jstqyyjlis[2]
#     jstqyyj = jstqyyjlis[3]
#     for qyyjlis in qyyj_datalist[0][1][1:]:
#         if jstqyname == qyyjlis[1] and jstxmjl == qyyjlis[2] and jstqyyj[:9] == qyyjlis[3][:9]:
#             bsthave = "有"
#             break
#         else:
#             bsthave = "无"
#     tmp = [jstqyyjlis[0],jstqyyjlis[1],jstqyyjlis[2],jstqyyjlis[3],jstqyyjlis[4],jstqyyjlis[5],jstqyyjlis[6],
#            jstqyyjlis[7],jstqyyjlis[8],jstqyyjlis[3][:5],"jst",bsthave]
#     qyyj_data.append(tmp)

tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["href","entname","name", "ggname","xzqh",
              "fabu_time","person_key","quyu","11","source","bsthave","jsthave"]
outfilename_gd_qyzz = root_dir + r"\hebin\合并项目经理业绩各平台是否有_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, xmjlyj_data)
print("qyyj_data to  excel  success")