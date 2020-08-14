import csv
import codecs
from itertools import islice

def  read_text():
    infile=r"D:\pythonproject\bst\bst_datatest\data\user_info.txt"
    with(open(infile,'r')) as user_file:
        data =user_file.readlines()
    users =[]
    for line in data:
        user = line[:-1].split(':')
        users.append(user)
    print(users)
    print(users[0][1])

def read_csv():
    infile = r"D:\pythonproject\bst\bst_datatest\data\user_info.csv"
    data =csv.reader(codecs.open(infile,'r','utf-8'))
    users = []
    # islice返回迭代器，1开始的位置（0行没有读），结束位置
    for line in islice(data,1,None):
        users.append(line)
    print(users)
    print(users[0][1])

if __name__=='__main__':
    # read_text()
    read_csv()