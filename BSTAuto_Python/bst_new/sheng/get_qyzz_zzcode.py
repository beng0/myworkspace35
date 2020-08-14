from util.my_read_excel import *
from util.my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\data'
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzz_贺家斌_20200805_163031.xlsx"
qyzz_datalist = read_excel(infilename1)
print(qyzz_datalist)
print(qyzz_datalist[0][1])
print(qyzz_datalist[0][1][1])
print(qyzz_datalist[0][1][1][5])

infilename2 = root_dir + r"\get_bst_ryzz_qyzz\bst_qyzz_贺家斌_20200806.xlsx"
sys_datalist = read_excel(infilename2)
print(sys_datalist)
print(sys_datalist[0][1][1])

qyzz_data = []
for i in range(1,len(qyzz_datalist[0][1])):
    qyzz = qyzz_datalist[0][1][i][5]
    for sys_row in sys_datalist[0][1]:
        if qyzz == sys_row[0] or qyzz == sys_row[1]:
            zzcode = sys_row[2]
            break
        else:
            zzcode = ''
    tmp = [qyzz_datalist[0][1][i][0],qyzz_datalist[0][1][i][1],qyzz_datalist[0][1][i][2],
            qyzz_datalist[0][1][i][3],qyzz_datalist[0][1][i][4],qyzz_datalist[0][1][i][5],zzcode]
    qyzz_data.append(tmp)



tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["sheng","shi","href", "entname","zslb", "zzdj","zzcode"]
outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzzwithzzcode_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyzz_data)
print("qyzz_data to  excel  success")