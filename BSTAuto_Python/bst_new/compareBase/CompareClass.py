import sys
import collections
sys.path.append(r'E:/myworkspace35/BSTAuto_Python/bst_new/util')
from my_read_excel import *
from my_to_excel import *
import psycopg2
from datetime import datetime



class CompareClass():
    # 参数示例：infilenames=[infilename1,infilename2],num=[0,3],outfilename=ourfilename
    def __init__(self,infilenames,num,outfilename,columnRows=None):
        self.infilenames = infilenames
        self.num = num
        self.outfilename = outfilename
        if columnRows is None:
            self.columnRows = ["a", "b", "c"]
        else:
            self.columnRows = columnRows

    """输入多个excel文件合并为一个excel文件并去重，多个文件的格式要一致，每一列的字段是一样的，
    num表示根据第几列来去重,hebin_filename表示合并文件存放位置"""
    def get_hebin_data(self, hebin_filename,columnRows):
        infilenames = self.infilenames
        num = self.num
        hebin_datalist = []
        for infilename in infilenames:
            hebin_datalist = hebin_datalist + read_excel(infilename)[0][1][1:]
            # print(read_excel(infilename))
            # print(read_excel(infilename)[0][1])
            # print(read_excel(infilename)[0][1][1])
            # print(read_excel(infilename)[0][1][1][0])
            # print(read_excel(infilename)[0][1][1][3])

        chong_dict = collections.OrderedDict()
        data_result = []
        chong_list = []

        # 合并后的qyzz
        for qyzz_data in hebin_datalist:
            chong_str = ''
            for n in num:
                chong_str = chong_str + str(qyzz_data[n])
            chong_dict[chong_str] = qyzz_data
            chong_list.append(chong_str)
        for value in chong_dict.values():
            data_result.append(value)

        tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
        wirteDataToExcel(hebin_filename + tablenamehouzui + ".xlsx", "sheet1", columnRows, data_result)
        self.hebin_filename = hebin_filename + tablenamehouzui + ".xlsx"
        print("get hebin data success")
        # 返回合并后的文件名
        return self.hebin_filename

    """
    输入对比标准文件（字符串），对比文件（数组），需要对比的列（数组），输出文件名（字符串），列名（数组）
    得到对比结果文件
    """
    def get_compare_result(self, hebin_filename):
        infilenames = self.infilenames
        num = self.num
        outfilename = self.outfilename
        columnRows = self.columnRows
        if columnRows is None:
            columnRows = ['a', 'b', 'c']
        ishaves_list = []
        hebin_datalist = read_excel(hebin_filename)[0][1][1:]
        print(hebin_datalist)
        # 先得到hebin数据字符串列表
        hebin_str_list = []  # 存放hebin数据关键字连接形成的字符串列表
        for hebin_datas in hebin_datalist:
            hcompare_str = ''
            for n in num:
                hcompare_str += str(hebin_datas[n])
            hebin_str_list.append(hcompare_str)
        print(hebin_str_list)
        # 得到每个文件的字符串列表
        for infilename in infilenames:
            compare_str_list = []  # 存放需要对比的数据关键字连接形成的字符串列表
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
        print("get compare result success,文件位置："+outfilename + tablenamehouzui + ".xlsx")