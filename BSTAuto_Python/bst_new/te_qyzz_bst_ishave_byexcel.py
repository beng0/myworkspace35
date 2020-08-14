from util.my_read_excel import *
from util.my_to_excel import *
import psycopg2
from datetime import datetime


root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\合并_省平台qyzzwithzzcode_贺家斌_20200806.xlsx"
qyzz_datalist = read_excel(infilename1)
print(qyzz_datalist)
print(qyzz_datalist[0][1])
print(qyzz_datalist[0][1][1])
print(qyzz_datalist[0][1][1][3])
print(qyzz_datalist[0][1][1][6])

infilename2 = root_dir + r"\get_bst_ryzz_qyzz\bst_qyzz_贺家斌_20200806.xlsx"
bst_datalist = read_excel(infilename2)
print(bst_datalist)
print(bst_datalist[0][1][1])
print(bst_datalist[0][1][1][3])
print(bst_datalist[0][1][1][6])

qyzz_data = []
for qyzzlis in qyzz_datalist[0][1][1:]:
    ishave = ''
    qyname = qyzzlis[3]
    zzcode = qyzzlis[6]
    for bst_qyzz in bst_datalist[0][1]:
        if qyname == bst_qyzz[3] and zzcode == bst_qyzz[6]:
            ishave = '有'
            break
        else:
            ishave = "无"
    tmp = [qyzzlis[0], qyzzlis[1], qyzzlis[2],
           qyzzlis[3], qyzzlis[4], qyzzlis[5], qyzzlis[6],ishave]
    qyzz_data.append(tmp)

tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["sheng","shi","href", "entname","zslb", "zzdj","zzcode","ishave"]
outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\合并_省平台qyzzwithzzcode_bstishave_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyzz_data)
print("qyzz_data to  excel  success")