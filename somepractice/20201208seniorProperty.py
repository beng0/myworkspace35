# 每当在一个属性前加上__前缀，解释器就会将其重命名
# class MyClass:
#     __secret_value = 1
#
# instance_of = MyClass()
# # instance_of.__secret_value
#
# print(dir(MyClass))
# print(instance_of._MyClass__secret_value)

# 描述符：描述符允许你自定义在引用一个对象的属性时应该完成的事情
# 描述符基于3个特殊方法：__set__，__get__，__delete__。
# 实现了__get__和__set__方法的描述符被称为数据描述符，只实现了__get__方法的被称为非数据描述符
# 每次通过点号或getattr函数调用来执行查找时，会隐式调用__getattribute__，它按以下顺序查找属性
# 数据描述符，__dict__，非数据描述符
class RevealAccess(object):
    """一个数据描述符，正常设定值并返回值，同时打印出记录访问的信息"""

    def __init__(self,initval=None,name='var'):
        self.val = initval
        self.name = name

    def __get__(self,obj,objtype):
        print('Retrieving',self.name)
        return self.val

    def __set__(self,obj,val):
        print('Updating',self.name)
        self.val = val

class MyClass(object):
    x = RevealAccess(10,'var"x"')
    y = 5

m = MyClass()
# print(m.x)
#
# m.x = 20
# print(m.x)

print(m.y)

# 函数对象是非数据描述符
def function():pass
print(hasattr(function,'__get__'))
print(hasattr(function,'__set__'))



















