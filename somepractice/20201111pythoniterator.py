# 迭代器基于两个方法，__next__：返回容器的下一个元素。__iter__：返回迭代器本身

# 创建迭代器,可以使用内置的iter函数和一个序列来创建
i = iter('abc')
print(next(i))
print(next(i))
print(next(i))
# print(next(i))

# 创建自定义迭代器
class CountDown:
    def __init__(self,step):
        self.step = step
    def __next__(self):
        """Return the next element"""
        if  self.step <= 0:
            raise StopIteration
        self.step -= 1
        return self.step
    def __iter__(self):
        """Return the iterator itself"""
        return self

c = CountDown(4)
print(c.__next__())
print(c.__next__())
print(c.__next__())
print(c.__next__())
# print(c.__next__())

