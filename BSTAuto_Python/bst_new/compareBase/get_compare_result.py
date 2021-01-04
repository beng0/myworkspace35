import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime


root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'

"""
输入对比标准文件（字符串），对比文件（数组），需要对比的列（数组），输出文件名（字符串），列名（数组）
得到对比结果文件
"""
def get_compare_result(hebin_filename,infilenames,num,outfilename,columnRows=None):
    if columnRows is None:
        columnRows = ['a', 'b', 'c']
    ishaves_list = []
    hebin_str_list = [] # 存放hebin数据关键字连接形成的字符串列表
    compare_str_list = [] # 存放需要对比的数据关键字连接形成的字符串列表
    hebin_datalist = read_excel(hebin_filename)[0][1][1:]
    print(hebin_datalist)
    # 先得到hebin数据字符串列表
    for hebin_datas in hebin_datalist:
        compare_str = ''
        for n in num:
            compare_str += str(hebin_datas[n])
        hebin_str_list.append(compare_str)
    print(compare_str_list)
    # 得到每个文件的字符串列表
    for infilename in infilenames:
        ishaves = []
        datalist = read_excel(infilename)[0][1][1:]
        for datas in datalist:
            compare_str1 = ''
            for n in num:
                compare_str1 += str(datas[n])
            compare_str_list.append(compare_str1)
        print(compare_str_list)
        """遍历hebin数据字符串列表，检查在每个文件字符串列表里是否有"""
        for compare_str in hebin_str_list:
            if compare_str in compare_str_list:
                is_have = "有"
            else:
                is_have = "无"
            ishaves.append(is_have)
        ishaves_list.append(ishaves)
        for i in range(len(hebin_datalist)):
            hebin_datalist[i].append(ishaves[i])
    # 返回得到每个文件是否有信息之后的合并嵌套列表

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    wirteDataToExcel(outfilename + tablenamehouzui + ".xlsx", "sheet1", columnRows, hebin_datalist)
    print("get compare result success")


