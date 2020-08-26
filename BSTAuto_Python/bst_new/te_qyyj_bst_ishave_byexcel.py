import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
infilename1 = root_dir + r"\get_bst_qyyj\标事通企业业绩_数据准备_贺家斌_20200826_133840.xlsx"
qyyj_datalist = read_excel(infilename1)
print(qyyj_datalist)
print(qyyj_datalist[0][1])
print(qyyj_datalist[0][1][1])
print(qyyj_datalist[0][1][1][1])
print(qyyj_datalist[0][1][1][2])

infilename2 = root_dir + r"\get_jst_qyyj\建设通企业业绩_数据准备_贺家斌_qyyj_20200826_120336.xlsx"
jst_datalist = read_excel(infilename2)
print(jst_datalist)
print(jst_datalist[0][1][1])
print(jst_datalist[0][1][1][1])
print(jst_datalist[0][1][1][2])

qyyj_data = []

for qyyjlis in qyyj_datalist[0][1][1:]:
    qyname = qyyjlis[1]
    qyyj = qyyjlis[2]
    for jstqyyjlis in jst_datalist[0][1][1:]:
        if qyname == jstqyyjlis[1] and qyyj[:9] == jstqyyjlis[2][:9]:
            jsthave = "有"
            break
        else:
            jsthave = "无"
    tmp = [qyyjlis[0],qyyjlis[1],qyyjlis[2],qyyjlis[3],qyyjlis[4],qyyjlis[5],qyyjlis[6],
           qyyjlis[2][:9],"bst",jsthave]
    qyyj_data.append(tmp)

for jstqyyjlis in jst_datalist[0][1][1:]:
    jstqyname = jstqyyjlis[1]
    jstqyyj = jstqyyjlis[2]
    for qyyjlis in qyyj_datalist[0][1][1:]:
        if jstqyname == qyyjlis[1] and jstqyyj[:9] == qyyjlis[2][:9]:
            bsthave = "有"
            break
        else:
            bsthave = "无"
    tmp = [jstqyyjlis[0],jstqyyjlis[1],jstqyyjlis[2],jstqyyjlis[3],jstqyyjlis[4],jstqyyjlis[5],jstqyyjlis[6],
           jstqyyjlis[2][:9],"jst",bsthave]
    qyyj_data.append(tmp)
tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["href","entname", "ggname","diqu", "xmjl","zbtime","zbly","left9","bstjst","ishave"]
outfilename_gd_qyzz = root_dir + r"\get_bst_qyyj\企业业绩对比结果_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyyj_data)
print("qyyj_data to  excel  success")