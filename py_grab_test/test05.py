import xlwt
from bs4 import BeautifulSoup

# book = xlwt.Workbook()
# sheet = book.add_sheet("sheet1",cell_overwrite_ok=True)
#
# lis1 = [1,2,3]
# lis2 = [2,3,[4,5],6]
# lis3 = [7,[8,[10,11]]]
#
# for i in range(len(lis1)):
#     sheet.write(i+1,1,str(lis1[i]))
#
# book.save("E://mytest/test05.xls")
# print("success")

def excel_w(file_position,shee_name,*lis):
    book = xlwt.Workbook()
    sheet = book.add_sheet(shee_name,cell_overwrite_ok=True)
    print(lis)
    len_c = len(lis)
    for c in range(len_c):
        print(len_c)
        li = lis[c]
        len_r = len(li)
        for r in range(len_r):
            sheet.write(r+1,c+1,li[r])

    book.save(file_position)
    print("success")


excel_w("E://mytest/test005.xls","sheet1",["a","b","c"],[1,2,3])
