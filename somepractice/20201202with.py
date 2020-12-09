import os
print(os.path.abspath('..'))
# 读取文件

# 使用try语句
doc = open(os.path.abspath('..')+'/readme.txt')
try:
    for line in doc:
        if line.startswith("#"):
            continue
        print(line.strip())
finally:
    doc.close()

# 使用with语句
with open(os.path.abspath('..')+'/readme.txt') as doc:
    for line in doc:
        print(line.strip())
# with 语句的一般语法
'''
#1.最简单形式
with context_manager:
    #代码块
    
# 2.使用as子句保存局部变量
with context_manager as context:
    #代码块

# 3.多个上下文管理器
with A() as a,B() as b:
    #代码块

# 等价于
with A() as a:
    with B() as b:
        # 代码块
'''
# 1.作为一个类
# 任何实现了上下文管理器协议的对象都可以作为上下文管理器。该协议包含__enter__和__exit__两个特殊方法
# 执行with语句的过程如下
# 1.调用__enter__方法。返回值绑定到指定的as子句
# 2.执行内部代码块
# 3.调用__exit__方法

# class ContextIllustration:
#     def __enter__(self):
#         print('entering context')
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('leaving context')
#
#         if exc_type is None:
#             print('with no error')
#         else:
#             print('with an error (%s)'%exc_val)
# with ContextIllustration():
#     print('inside')
#
# with ContextIllustration():
#     raise RuntimeError('raise within "with"')

# 2. 作为一个函数 --contextlib
from contextlib import contextmanager
@contextmanager
def context_illustration():
    print('entering context')

    try:
        yield
    except Exception as e:
        print('leaving context')
        print('with an error (%s)'%e)
        raise
    else:
        print('leaving context')
        print("with no error")

with context_illustration():
    print('inside')
