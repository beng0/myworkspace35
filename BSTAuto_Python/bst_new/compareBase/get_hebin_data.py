import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
from datetime import datetime
import collections

"""输入多个excel文件合并为一个excel文件并去重，多个文件的格式要一致，每一列的字段是一样的，num表示根据第几列来去重"""
# 参数示例：infilenames=[infilename1,infilename2],num=[0,3],outfilename=ourfilename
def get_hebin_data(infilenames,num,outfilename,columnRows=None):
    if columnRows is None:
        columnRows = ["a","b","c"]
    hebin_datalist = []
    for infilename in infilenames:
        hebin_datalist = hebin_datalist + read_excel(infilename)[0][1][1:]
        # print(read_excel(infilename))
        # print(read_excel(infilename)[0][1])
        # print(read_excel(infilename)[0][1][1])
        # print(read_excel(infilename)[0][1][1][0])
        # print(read_excel(infilename)[0][1][1][3])

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
    for value in chong_dict.values():
        qyzz_data_result.append(value)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, qyzz_data_result)
    print("get hebin data success")
