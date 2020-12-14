# 元类是定义其它类的一种类
# 所有类定义的基类都是type类
# 实例：调用type()可以创建class类
def method(self):
    print(1)


klass = type('MyClass', (object,), {'method': method})
instance = klass()
instance.method()
