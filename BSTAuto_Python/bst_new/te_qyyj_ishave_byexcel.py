import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
# 标事通企业业绩
infilename1 = root_dir + r"\get_bst_qyyj\标事通企业业绩_数据准备_贺家斌_20201111_143049.xlsx"
bst_datalist = read_excel(infilename1)
print(bst_datalist)
print(bst_datalist[0][1])
print(bst_datalist[0][1][1])
print(bst_datalist[0][1][1][1])
print(bst_datalist[0][1][1][2])

# 建设通企业业绩
infilename2 = root_dir + r"\get_jst_qyyj\建设通企业业绩_中标公示_贺家斌_20201111_193040.xlsx"
jst_datalist = read_excel(infilename2)
print(jst_datalist)
print(jst_datalist[0][1][1])
print(jst_datalist[0][1][1][1])
print(jst_datalist[0][1][1][2])

# 剑鱼企业业绩
infilename3 = root_dir + r"\jianyu\jianyuqyyjs_20201105_182813.xlsx"
jy_datalist = read_excel(infilename3)

# 合并企业业绩
infilename4 = root_dir + r"\hebin\合并qyyj_jianyu_jst_bst.xlsx"
hb_datalist = read_excel(infilename4)


qyyj_data = []
for qyyjlis in hb_datalist[0][1][1:]:
    qyname = qyyjlis[1]
    qyyj = qyyjlis[2]
    bstishave = ''
    jstishave = ''
    jyishave = ''
    # 测试合并业绩标事通是否有
    for bst_qyyj in bst_datalist[0][1][1:]:
        if qyname == bst_qyyj[1] and qyyj[:9] == bst_qyyj[2][:9]:
            bstishave = "有"
            break
        else:
            bstishave = "无"
    # 测试合并业绩建设通是否有
    for jst_qyyj in jst_datalist[0][1][1:]:
        if qyname == jst_qyyj[1] and qyyj[:9] == jst_qyyj[2][:9]:
            jstishave = "有"
            break
        else:
            jstishave = "无"
    # 测试合并业绩剑鱼是否有
    for jy_qyyj in jy_datalist[0][1][1:]:
        if qyname == jy_qyyj[1] and qyyj[:9] == jy_qyyj[2][:9]:
            jyishave = "有"
            break
        else:
            jyishave = "无"


    tmp = [qyyjlis[0],qyyjlis[1],qyyjlis[2],qyyjlis[3],qyyjlis[4],qyyjlis[5],qyyjlis[6],
           qyyjlis[7],qyyjlis[8],qyyjlis[9],bstishave,jstishave,jyishave]
    qyyj_data.append(tmp)

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
columnRows = ["href","entname", "ggname","diqu", "xmjl","jia",
              "fabu_time","11","zbly","source","bstishave","jstishave","jyishave"]
outfilename_gd_qyzz = root_dir + r"\hebin\云南_合并后qyyj各平台是否有_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyyj_data)
print("qyyj_data to  excel  success")