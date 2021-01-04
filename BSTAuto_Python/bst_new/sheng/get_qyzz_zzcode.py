from BSTAuto_Python.bst_new.util.my_read_excel import *
from BSTAuto_Python.bst_new.util.my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\data'
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzz_贺家斌_20201215_144648.xlsx"
qyzz_datalist = read_excel(infilename1)
print(qyzz_datalist)
print(qyzz_datalist[0][1])
print(qyzz_datalist[0][1][1])
print(qyzz_datalist[0][1][1][1])

infilename2 = root_dir + r"\sys_dict\企业资质字典表05061512（孟飞用）.xlsx"
sys_datalist = read_excel(infilename2)
print(sys_datalist)
print(sys_datalist[0][1][1])

qyzz_data = []
for i in range(1,len(qyzz_datalist[0][1])):
    qyzz = qyzz_datalist[0][1][i][1]
    for sys_row in sys_datalist[0][1]:
        if qyzz == sys_row[0] or qyzz == sys_row[1]:
            zzcode = sys_row[2]
            break
        else:
            zzcode = 'None'
    tmp = [qyzz_datalist[0][1][i][0],qyzz_datalist[0][1][i][1],qyzz_datalist[0][1][i][2],zzcode]
    qyzz_data.append(tmp)



tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["entname","zzmc", "youxiao_date","zzcode"]
outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzzwithzzcode_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyzz_data)
print("qyzz_data to  excel  success")