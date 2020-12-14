# 槽（slots）允许使用__slots__属性来为指定的类设置一个静态属性列表，并在类的每个实例中跳过__dict__字典的创建过程
# 以下实例展示了限制类的语言动态特性
class Frozen:
    __slots__ = ['ice','cream']

print('__dict__' in dir(Frozen))

print('ice' in dir(Frozen))

frozen = Frozen()
frozen.ice = True
print(frozen.ice)
frozen.cream = None
# frozen.icy = True

# 派生类不会被限制
class Unfrozen(Frozen):
    pass

unfrozen = Unfrozen()
unfrozen.icy = False
print(unfrozen.icy)