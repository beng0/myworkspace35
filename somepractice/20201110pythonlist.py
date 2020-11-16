# 列表推导

# 1. 普通循环
evens = []
for i in range(10):
    if i % 2 == 0:
        evens.append(i)
print(evens)

# 2. 列表推导
enens2 = [i for i in range(10) if i % 2 == 0]
print(enens2)

lis3 = [i for i in range(10)]
print(lis3)

# enumerate枚举
# 1. 普通的
i = 0
for element in ['one','two','shree']:
    print(i,element)
    i+=1

# 2. 使用枚举
for i,element in enumerate(["four","five","six"]):
    print(i,element)

# 一个一个合并多个列表zip
for item in zip([1,2,3],[4,5,6]):
    print(item)

z = zip(['a','b'],['b','c'])
print(z)

print(zip(['a','b'],['c','d']))

# 对zip函数返回的结果再次调用zip()，可以使其恢复原状
for item in zip(*zip([1,2,3],[4,5,6])):
    print(item)

# 序列解包，使用与任意序列类型，包括字符串和字节序列，赋值运算符左边的变量要和序列中的元素数目相等
first,second,third = 'foo','bar',100
print(first,second,third)

# 利用带*号的表达式解包
f,s,*rest = 0,1,2,3
print(f)
print(s)
print(rest)

f1,*s1,last = 0,1,2,3
print(f1)
print(s1)
print(last)

# 嵌套解包
(a,b),(c,d) = (1,2),(3,4)
print(a,b,c,d)
















