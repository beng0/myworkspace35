import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime


root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台ryzzwithzzcode_贺家斌_20200820_195210.xlsx"
ryzz_datalist = read_excel(infilename1)
print(ryzz_datalist)
print(ryzz_datalist[0][1])
print(ryzz_datalist[0][1][1])
print(ryzz_datalist[0][1][1][2])
print(ryzz_datalist[0][1][1][3])
print(ryzz_datalist[0][1][1][8])

infilename2 = root_dir + r"\get_bst_ryzz_qyzz\云南bst人员资质_贺家斌_20200820_151519.xlsx"
bst_datalist = read_excel(infilename2)
print(bst_datalist)
print(bst_datalist[0][1][1])
print(bst_datalist[0][1][1][3])
print(bst_datalist[0][1][1][4])
print(bst_datalist[0][1][1][8])

ryzz_data = []
for ryzzlis in ryzz_datalist[0][1][1:]:
    ishave = ''
    qyname = ryzzlis[2]
    ryname = ryzzlis[3]
    zzcode = ryzzlis[8]
    for bst_ryzz in bst_datalist[0][1][1:]:
        if qyname == bst_ryzz[3] and ryname == bst_ryzz[4] and str(zzcode) == bst_ryzz[8]:
            ishave = '有'
            break
        else:
            ishave = "无"
    tmp = [ryzzlis[0], ryzzlis[1], ryzzlis[2],
           ryzzlis[3], ryzzlis[4], ryzzlis[5], ryzzlis[6],ryzzlis[7],ryzzlis[8],ishave]
    ryzz_data.append(tmp)

tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["sheng","shi","href", "entname","name", "zsbh","zzdj","zhuanye","ryzzcode","ishave"]
outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台ryzzwithzzcode_bstishave_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, ryzz_data)
print("qyzz_data to  excel  success")