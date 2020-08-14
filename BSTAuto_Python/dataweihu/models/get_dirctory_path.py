import os
def get_dirctory_path(dirctory):
# 获取文件路径
    dirPath = os.path.join(os.getcwd(), str(dirctory))
    return dirPath

if __name__ == '__main__':
    dirPath=get_dirctory_path('ExcelData')
    print(dirPath)