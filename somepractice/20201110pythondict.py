# 使用推导创建字典
dic1 = {number:number**2 for number in range(100)}
print(dic1)

# 注意：字典的keys()、values()、items()返回的不是列表，而是视图对象。视图对象可以动态查看字典的内容
words = {"foo":"bar","fizz":"bazz"}
items = words.items()
words['span'] = 'eggs'
print(items)
# 在keys()和values()方法返回的视图中，键和值的顺序是完全对应的

# 字典的顺序不一定是元素的添加顺序
print({number:None for number in range(10)}.keys())
print({str(number):None for number in range(10)}.keys())

# 有序字典 OrderedDict
