from util.my_read_excel import *
from util.my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
infilename1 = root_dir + r"\get_bst_qyyj\广东_云南_山西_bst_qyyj_get结果_胡金花_20200727_144002.xlsx"
qyyj_datalist = read_excel(infilename1)
print(qyyj_datalist)
print(qyyj_datalist[0][1])
print(qyyj_datalist[0][1][1])
print(qyyj_datalist[0][1][1][2])
print(qyyj_datalist[0][1][1][4])

infilename2 = root_dir + r"\get_jst_qyyj\广东_云南_山西建设通企业业绩_胡金花_20200727_115212.xlsx"
jst_datalist = read_excel(infilename2)
print(jst_datalist)
print(jst_datalist[0][1][1])
print(jst_datalist[0][1][1][2])
print(jst_datalist[0][1][1][3])

qyyj_data = []

for qyyjlis in qyyj_datalist[0][1][1:]:
    qyname = qyyjlis[2]
    xmjl = qyyjlis[5]
    qyyj = qyyjlis[3]
    for jstqyyjlis in jst_datalist[0][1][1:]:
        if qyname == jstqyyjlis[2] and xmjl == jstqyyjlis[5] and qyyj[:5] == jstqyyjlis[3][:5]:
            jsthave = "有"
            break
        else:
            jsthave = "无"
    tmp = [qyyjlis[0],qyyjlis[1],qyyjlis[2],qyyjlis[3],qyyjlis[4],qyyjlis[5],qyyjlis[6],
           qyyjlis[7],qyyjlis[3][:5],"bst",jsthave]
    qyyj_data.append(tmp)

for jstqyyjlis in jst_datalist[0][1][1:]:
    jstqyname = jstqyyjlis[2]
    jstxmjl = jstqyyjlis[5]
    jstqyyj = jstqyyjlis[3]
    for qyyjlis in qyyj_datalist[0][1][1:]:
        if jstqyname == qyyjlis[4] and jstxmjl == qyyjlis[5] and jstqyyj[:5] == qyyjlis[2][:5]:
            bsthave = "有"
            break
        else:
            bsthave = "无"
    tmp = [jstqyyjlis[0],jstqyyjlis[1],jstqyyjlis[2],jstqyyjlis[3],jstqyyjlis[4],jstqyyjlis[5],jstqyyjlis[6],
           jstqyyjlis[7],jstqyyjlis[3][:5],"jst",bsthave]
    qyyj_data.append(tmp)
tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["href","shi","entname", "ggname","diqu", "xmjl","zbtime","zbly","left5","bstjst","ishave"]
outfilename_gd_qyzz = root_dir + r"\get_bst_qyyj\项目经理业绩对比_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyyj_data)
print("qyyj_data to  excel  success")