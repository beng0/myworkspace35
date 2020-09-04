import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
infilename1 = root_dir + r"\get_bst_xmjlyj\云南_bst_xmjlyj_获取结果_20200827.xlsx"
qyyj_datalist = read_excel(infilename1)
print(qyyj_datalist)
print(qyyj_datalist[0][1])
print(qyyj_datalist[0][1][1])
print(qyyj_datalist[0][1][1][1])
print(qyyj_datalist[0][1][1][2])
print(qyyj_datalist[0][1][1][3])

infilename2 = root_dir + r"\xmjl_list\云南__jst_xmjlyj_获取结果_贺家斌_20200827_112025.xlsx"
jst_datalist = read_excel(infilename2)
print(jst_datalist)
print(jst_datalist[0][1][1])
print(jst_datalist[0][1][1][1])
print(jst_datalist[0][1][1][2])
print(jst_datalist[0][1][1][3])

qyyj_data = []

for qyyjlis in qyyj_datalist[0][1][1:]:
    qyname = qyyjlis[1]
    xmjl = qyyjlis[2]
    qyyj = qyyjlis[3]
    for jstqyyjlis in jst_datalist[0][1][1:]:
        if qyname == jstqyyjlis[1] and xmjl == jstqyyjlis[2] and qyyj[:9] == jstqyyjlis[3][:9]:
            jsthave = "有"
            break
        else:
            jsthave = "无"
    tmp = [qyyjlis[0],qyyjlis[1],qyyjlis[2],qyyjlis[3],qyyjlis[4],qyyjlis[5],qyyjlis[6],
           qyyjlis[7],qyyjlis[8],qyyjlis[3][:5],"bst",jsthave]
    qyyj_data.append(tmp)

for jstqyyjlis in jst_datalist[0][1][1:]:
    jstqyname = jstqyyjlis[1]
    jstxmjl = jstqyyjlis[2]
    jstqyyj = jstqyyjlis[3]
    for qyyjlis in qyyj_datalist[0][1][1:]:
        if jstqyname == qyyjlis[1] and jstxmjl == qyyjlis[2] and jstqyyj[:9] == qyyjlis[3][:9]:
            bsthave = "有"
            break
        else:
            bsthave = "无"
    tmp = [jstqyyjlis[0],jstqyyjlis[1],jstqyyjlis[2],jstqyyjlis[3],jstqyyjlis[4],jstqyyjlis[5],jstqyyjlis[6],
           jstqyyjlis[7],jstqyyjlis[8],jstqyyjlis[3][:5],"jst",bsthave]
    qyyj_data.append(tmp)
tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["href","shi","entname", "ggname","diqu", "xmjl","zbtime","zbly","href","left9","bstjst","ishave"]
outfilename_gd_qyzz = root_dir + r"\get_bst_xmjlyj\项目经理业绩对比_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyyj_data)
print("qyyj_data to  excel  success")