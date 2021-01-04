from BSTAuto_Python.bst_new.util.my_read_excel import *
from BSTAuto_Python.bst_new.util.my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\data'
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南省xmjlzz_数据准备_贺家斌_20201216_151948.xlsx"
ryzz_datalist = read_excel(infilename1)
print(ryzz_datalist)
print(ryzz_datalist[0][1])
print(ryzz_datalist[0][1][1])
print(ryzz_datalist[0][1][1][4]) #zzmc
print(ryzz_datalist[0][1][1][5]) #zhuanye

infilename2 = root_dir + r"\sys_dict\人员资质字典表05191129（孟飞用）.xlsx"
sys_datalist = read_excel(infilename2)
print(sys_datalist)
print(sys_datalist[0][1][1])

ryzz_data = []
ryzzcode = 'None'
for ryzzlis in ryzz_datalist[0][1][1:]:
    ryzzmc = ryzzlis[4]
    ryzzzy = ryzzlis[5]
    if ryzzmc == "三类人员":
        if "建安A" in ryzzlis[3]:
            ryzzmc = "建安A证"
        elif "建安B" in ryzzlis[3]:
            ryzzmc = "建安B证"
        elif "建安C" in ryzzlis[3]:
            ryzzmc = "建安C证"
        else:
            ryzzmc = ryzzlis[4]
    for syszzlis in sys_datalist[0][1]:
        if ryzzmc == syszzlis[0] and ryzzzy == syszzlis[1]:
            ryzzcode = syszzlis[3]
            break
        else:
            ryzzcode = 'None'
    tmp = [ryzzlis[0],ryzzlis[1],ryzzlis[2],ryzzlis[3],ryzzlis[4],ryzzlis[5],ryzzcode]
    ryzz_data.append(tmp)

tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["entname","name", "sfzh","zzmc","zsbh","zhuanye","ryzzcode"]
outfilename_gd_qyzz = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台xmjlzzwithzzcode_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, ryzz_data)
print("qyzz_data to  excel  success")
