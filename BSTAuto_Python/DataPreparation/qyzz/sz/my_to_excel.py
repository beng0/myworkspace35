import os
import openpyxl

def  wirteDataToExcel(outfilename,sheetName,columnRows, recordRows):

    if os.path.exists(outfilename):
        raise FileExistsError("file exists")

    wb = openpyxl.Workbook()
    # wb.create_sheet(sheetName,0)
    # sheet =wb.get_sheet_by_name(sheetName)
    sheet=wb.active

    # 当列数超过26时，添加AA,AB,AC...
    myAlphbet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
    # 第一行写入数据库表列名:一维字符串数组
    for i in range(len(columnRows)):
        loc = myAlphbet[i]+str(1)
        sheet[loc]=columnRows[i]

    #写入数据库表所有数据，二维字符串数组
    for row in  range(len(recordRows)):
        sheet.append(recordRows[row])
        # for col in range(len(recordRows[row])):
        #     loc = myAlphbet[col]+str(row+2)
        #     sheet[loc] = recordRows[row][col]

    wb.save(outfilename)



