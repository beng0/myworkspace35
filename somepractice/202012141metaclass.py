# 用class创建的每个类都隐式的使用type作为其元类，可以通过向class语句提供metacalss关键字参数来改变这一默认行为
class ClassWithAMetaclass(metaclass=type):
    pass


class Metaclass(type):
    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls, name, bases, namespace, **kwargs):
        super.__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


