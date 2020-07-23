# def f1(lis = []):
#     print(lis[0])
#     print(lis[2]+lis[3])
#
# f1([1,2,3,4,5])

# def f2(*lis):
#     if type(lis) == list:
#         print(lis)
#         print(type(lis))
#     else:
#         print(0)
#         print(type(lis))
#         print(lis)
#
#
# f2([1,2,3])
#
# def f3(*lis):
#     for li in lis:
#         if type(li) == list:
#             print(1)
#         else:
#             print(0)
#     print(li)
#
# f3([1,2,3])

# 将嵌套数组、数组、单个参数转化为一个数组
def f4(lis_a,*lis):
    lis_a = list(lis_a) if isinstance(lis_a,(list,tuple)) else []
    for li in list(lis):
        if type(li) == list:
            for i in li:
                lis_a = f4(lis_a,i)
        else:
            print(li)
            lis_a.append(li)
    return lis_a


print(f4(0,[2, 1, [3, [4, 5], 6], 7, [8]],11,12))


# lis3 = [1,2,[3,4]]
# lis3.pop(-1)
# print(lis3)
# def f5(*lis):
#     lis_b = []
#     for li in list(lis):
#         if type(li) == list:
#             lis_b = lis_b + li
#         else:
#             lis_b.append(li)
#     return lis_b
#
# print(f5(["a","b",["c","d"]]))

# lis_c = ["a","b","c"]
# str_c = "_".join(lis_c)
# print(str_c)

# 将嵌套数组转化为单个数组
# def list_flatten(l, a=None):
#     a = list(a) if isinstance(a, (list, tuple)) else []
#     for i in l:
#         if isinstance(i, (list, tuple)):
#             a = list_flatten(i, a)
#         else:
#             a.append(i)
#     return a
#
# print(list_flatten([2, 1, [3, [4, 5], 6], 7, [8]]))

sheetname = "sheet1"
list1 = [1,2,3]
list2 = [sheetname,list1]
print(list2)

