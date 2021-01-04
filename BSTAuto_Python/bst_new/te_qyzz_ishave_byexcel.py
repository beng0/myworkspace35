import sys

sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime


root_dir = os.path.dirname(os.path.abspath('.')) + '\\bst_new\\data'

# infilname1,infilename2,hebinfilename,num表示需要对比的列
def get_compare_result(hebin_filename,infilenames,num):
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
    # 返回得到每个文件是否有信息之后的合并列表
    return hebin_datalist

hebin_infilename = root_dir + r"\hebin\hebin云南_省平台qyzzwithzzcode_贺家斌_20201215_171230.xlsx"
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台qyzzwithzzcode_贺家斌_20201215_145400.xlsx"
infilename2 = root_dir + r"\get_bst_ryzz_qyzz\云南bst企业资质_贺家斌_20201215_145515.xlsx"
hebin_datalist = get_compare_result(hebin_infilename,infilenames=[infilename1,infilename2],num=[0,3])
print(hebin_datalist)

tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
columnRows = ["entname", "zzmc","youxiao_date", "zzcode", "省平台是否有", "标事通是否有"]
outfilename_hebin_qyzz = root_dir + r"\hebin\云南_合并后qyzz各平台是否有_贺家斌_"
wirteDataToExcel(outfilename_hebin_qyzz + tablenamehouzui + ".xlsx", "qyzz_data", columnRows, hebin_datalist)
# wirteDataToExcel(outfilename2_qyzz + tablenamehouzui + '.xlsx',"qyzz_data",columnRows,qyzz1_data)
print("qyzz_data to  excel  success")


