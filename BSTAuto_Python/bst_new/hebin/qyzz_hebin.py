import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime
import collections



root_dir = os.path.dirname(os.path.abspath('.')) + '\\data'
print(root_dir)
# 省平台qyzz

infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzzwithzzcode_贺家斌_20201215_145400.xlsx"
infilename2 = root_dir + r"\get_bst_ryzz_qyzz\云南bst企业资质_贺家斌_20201215_145515.xlsx"

# 获得合并并去重后的数据
# 参数示例：infilenames=[infilename1,infilename2],num=[0,3]
def get_hebin_qyzzdata(infilenames,num):
    hebin_datalist = []
    for infilename in infilenames:
        hebin_datalist = hebin_datalist + read_excel(infilename)[0][1][1:]
        print(read_excel(infilename))
        print(read_excel(infilename)[0][1])
        print(read_excel(infilename)[0][1][1])
        print(read_excel(infilename)[0][1][1][0])
        print(read_excel(infilename)[0][1][1][3])

    chong_dict = collections.OrderedDict()
    qyzz_data_result = []
    chong_list = []

    # 合并后的qyzz
    for qyzz_data in hebin_datalist:
        chong_str = ''
        for n in num:
            chong_str = chong_str + str(qyzz_data[n])
        chong_dict[chong_str] = qyzz_data
        chong_list.append(chong_str)
    print(chong_list)
    print(chong_dict)
    for value in chong_dict.values():
        qyzz_data_result.append(value)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    columnRows = ["entname", "zzmc", "youxiao_date", "zzcode"]
    outfilename_gd_qyzz = root_dir + r"\hebin\hebin云南_省平台qyzzwithzzcode_贺家斌_"
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyzz_data_result)
    print("qyzz_data to  excel  success")

get_hebin_qyzzdata(infilenames=[infilename1,infilename2],num=[0,3])