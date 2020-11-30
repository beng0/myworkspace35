from BSTAuto_Python.bst_new.util.my_read_excel import *
from BSTAuto_Python.bst_new.util.my_to_excel import *
import psycopg2
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath('.')) + '\\data'
infilename1 = root_dir + r"\get_jst_ryzz_qyzz\建设通xmjlzz_数据准备_贺家斌_qyyj_20201117_100021.xlsx"
ryzz_datalist = read_excel(infilename1)
print(ryzz_datalist)
print(ryzz_datalist[0][1])
print(ryzz_datalist[0][1][1])
print(ryzz_datalist[0][1][1][5]) #zzdj
print(ryzz_datalist[0][1][1][7]) #zzzy

infilename2 = root_dir + r"\sys_dict\人员资质字典表05191129（孟飞用）.xlsx"
sys_datalist = read_excel(infilename2)
print(sys_datalist)
print(sys_datalist[0][1][1])

ryzz_data = []

for ryzzlis in ryzz_datalist[0][1][1:]:
    ryzzcode = ''
    ryzzmc = ryzzlis[5].replace("-","_")
    print(ryzzmc)
    if "A" in ryzzmc or "B" in ryzzmc or "C" in ryzzmc:
        ryzzmc = ryzzmc.split("_")[1]
    for syszzlis in sys_datalist[0][1]:
        if ryzzmc == syszzlis[2]:
            ryzzcode = syszzlis[3]
            break
        else:
            ryzzcode = ''
    tmp = [ryzzlis[0],ryzzlis[1],ryzzlis[2],ryzzlis[3],ryzzlis[4],ryzzlis[5],ryzzlis[6],ryzzlis[7],ryzzcode]
    ryzz_data.append(tmp)

tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["sheng","shi","entname","name", "sfz","zzdj","zczsh","zhuanye","ryzzcode"]
outfilename_gd_qyzz = root_dir + r"\get_jst_ryzz_qyzz\云南_建设通xmjl_ryzzwithzzcode_贺家斌_"
wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, ryzz_data)
print("qyzz_data to  excel  success")
