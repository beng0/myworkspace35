# 类装饰器
def short_repr(cls):
    cls.__repr__ = lambda self:super(cls,self).__repr__()[:8]
    return cls


@short_repr
class ClassWithRelativelyLongName:
    pass


print(ClassWithRelativelyLongName())


class ClassWithRelativeLongName1:
    pass


print(ClassWithRelativeLongName1())


# 优化类装饰器
def parametrized_short_repr(max_width=8):
    """缩短表示的参数化装饰器"""
    def parametrized(cls):
        """内部包装函数，是实际的装饰器"""
        class ShortlyRepresented(cls):
            """提供装饰器行为的子类"""
            def __repr__(self):
                return super().__repr__()[:max_width]
        return ShortlyRepresented
    return parametrized


@parametrized_short_repr(10)
class ClassWithLittleBitLongerLongName:
    pass


print(ClassWithLittleBitLongerLongName())
# 类装饰器的这种用法会使类的元数据发生变化
print(ClassWithLittleBitLongerLongName().__class__)
print(ClassWithLittleBitLongerLongName().__doc__)
































