# python装饰器的作用是使函数包装和方法包装变得更容易阅读和理解

# 没有装饰器
class WithoutDecorators:
    def some_static_method():
        print("this is static method")
    some_static_method = staticmethod(some_static_method)

    def some_class_method(cls):
        print('this is class method')
    some_class_method = classmethod(some_class_method)

# 使用装饰器
class WithDecorators:
    @staticmethod
    def some_static_method():
        print('this is static method')

    @classmethod
    def some_class_method(cls):
        print('this is class method')

# 自定义装饰器
# 1.作为一个函数
def mydecorator(function):
    def wrapped(*args,**kwargs):
        # 在调用原始函数之前，做点什么
        result = function(*args,**kwargs)
        # 在调用函数之后，做点什么
        return result
    return wrapped
# 2.作为一个类
class DecoratorAsClass:
    def __init__(self,function):
        self.function = function
    def __call__(self, *args, **kwargs):
        # 在调用函数之前，做点什么
        result = self.function(*args,**kwargs)
        # 在调用函数之后，做点什么
        # 返回结果
        return result
# 3.参数化装饰器
def repeat(number=3):
    # number表示重复次数
    def actual_decorator(function):
        def wrapper(*args,**kwargs):
            result = None
            for _ in range(number):
                result = function(*args,**kwargs)
            return result
        return wrapper
    return actual_decorator

@repeat(2)
def foo():
    print("foo")
foo()
repeat()

# 4.保持内省的装饰器
# 1）.未内省
def dummy_decorator(function):
    def wrapped(*args,**kwargs):
        """包装函数内部文档"""
        return function(*args,**kwargs)
    return wrapped

@dummy_decorator
def function_with_important_docstring():
    """这是我们想要保存的重要文档字符串。"""
print(function_with_important_docstring.__name__)
print(function_with_important_docstring.__doc__)
# 2>.使用保存内省的装饰器
from functools import wraps
def presserving_decorator(function):
    @wraps(function)
    def wrapped(*args,**kwargs):
        """包装函数内部文档"""
        return function(*args,**kwargs)
    return wrapped

@presserving_decorator
def function_with_important_docstring():
    """这是我们想要保存的重要文档字符串。"""
print(function_with_important_docstring.__name__)
print(function_with_important_docstring.__doc__)




# 装饰器用法



























