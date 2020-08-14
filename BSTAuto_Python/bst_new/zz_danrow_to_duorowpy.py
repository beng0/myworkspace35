from util.my_read_excel import *
from util.my_to_excel import *
from datetime import datetime
import re

# 一个公司在一行有多条资质,zzdj在第4开始
def  danrow_to_duorow(new_data,sheet1data,outfilename_gd_qyzz):
    for content in sheet1data:
        row_length =len(content)
        print(row_length)
        print(content)
        for col_count in range(3,row_length):
            print(col_count)
            if col_count == 3:
                tmp = [content[0],content[1],content[2],content[3]]
                new_data.append(tmp)
                print(new_data)
            else:
                if content[col_count]:
                    tmp = [content[0], content[1],content[2], content[col_count]]
                    new_data.append(tmp)
                    print(new_data)
                else: break

    print(new_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中 href	entname	zzdj
    columnRows = ["href", "entname","zzlb", "zzdj"]
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, new_data)
    print("to excel  success")

# 一个公司在一行有多条资质,zzdj在第2列开始
def  danrow_to_duorow2(new_data,sheet1data,outfilename_gd_qyzz):
    for content in sheet1data:
        row_length =len(content)
        print(row_length)
        print(content)
        for col_count in range(1,row_length):
            print(col_count)
            if col_count == 1 :
                tmp = [content[0],content[1]]
                new_data.append(tmp)
                print(new_data)
            else:
                if content[col_count]:
                    tmp = [content[0],content[col_count]]
                    new_data.append(tmp)
                    print(new_data)
                else: break

    print(new_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中 href	entname	zzdj
    columnRows = ["entname","qyzz"]
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, new_data)
    print("to excel  success")


def split_zz(sheet1data,new_data):
    for row in sheet1data:
        zz = row[5].split('；')
        for col in zz:
            if col != '':
                tmp=[row[0],row[1],row[2],row[3],row[4],col]
                new_data.append(tmp)
                print(new_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中 href	entname	zzdj
    columnRows = ["sheng","shi","href", "entname","zzlb", "zzdj"]
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, new_data)
    print("to excel  success")


def yunnan_ryzz_split_zz(sheet1data, new_data):
    for row in sheet1data:
        zz = row[7].split(',')
        print(zz)
        for col in zz:
            if col != '':
                tmp=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],col]
                new_data.append(tmp)
                print(new_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["sheng","shi","zbr", "name","sfz", "zclb_jb","zczsh", "zczy"]
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, new_data)
    print("to excel  success")


def shanxi_qyzz_split_zz(sheet1data, new_data):
    for row in sheet1data:
        zz = (re.sub("[\s+]", '@', row[3])).split('@')
        for col in zz:
            if col != '':
                tmp=[row[0],row[1],row[2],col]
                new_data.append(tmp)
                print(new_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["sheng","shi","qyname", "qyzz"]
    wirteDataToExcel(outfilename_gd_qyzz + tablenamehouzui + ".xlsx", "Sheet1", columnRows, new_data)
    print("to excel  success")


if  __name__=='__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/bst_new/data'
    infilename = root_dir + r"\get_sheng_ryzz_qyzz\山西_省平台qyzz_胡金花_20200728_142205.xlsx"
    outfilename_gd_qyzz = root_dir + r"\test_sheng_zz_result\山西_省平台qyzz_整理后_胡金花_"

    # infilename = r"D:\SVN\数据对比\对比结果\每周云南广东对比\山西\山西_省平台qyzz_胡金花_20200716_164739.xlsx"
    # outfilename = r"D:\SVN\数据对比\对比结果\每周云南广东对比\山西\山西_省平台qyzz_整理后_胡金花_"

    # 读要查询的项目经理和相应企业进来
    all_sheet_data = read_excel(infilename)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    sheet1data = all_sheet_data[0][1][1:]
    print(sheet1data)

    new_data=[]



    # 广东省qyzz情况
    # split_zz(sheet1data,new_data)

    # 云南省ryzz情况
    # yunnan_ryzz_split_zz(sheet1data, new_data)

    # 山西省qyzz情况
    shanxi_qyzz_split_zz(sheet1data, new_data)



    # # 一行有多列资质
    # danrow_to_duorow(new_data,sheet1data,outfilename_gd_qyzz)
