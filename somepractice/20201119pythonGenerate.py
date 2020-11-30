# 基于yield语句，生成器可以暂停函数并返回一个中间结果。该函数会保存上下文，稍后在必要时可以恢复

def fibonacci():
    a,b = 0,1
    while True:
        yield a
        a,b = b,a+b
fib = fibonacci()

# print(next(fib))
print([next(fib) for i in range(10)])

# 需要返回一个序列的函数，或在循环中运行的函数时，可以考虑使用生成器

# 示例：对读取的每一行生成token
import tokenize
reader = open('__init__.py').readline
tokens = tokenize.generate_tokens(reader)
print(next(tokens))
print(next(tokens))
print(next(tokens))
print(next(tokens))
print(next(tokens))
print(next(tokens))

# 示例：定义多个函数，每个函数都对序列进行一定的处理，然后合起来使用
def power(values):
    for value in values:
        print('powering %s'%value)
        yield value

def adder(values):
    for value in values:
        print('adding to %s'%value)
        if value%2 == 0:
            yield value + 3
        else:
            yield value + 2

elements = [1,2,3,4,5]
next(power(elements))
next(adder(elements))
next(adder(power(elements)))

# 保持代码简单，而不是保持数据简单。最好编写多个处理序列值的简单可迭代函数，而不要编写一个复杂函数。


# 生成器可以利用next函数与调用的代码进行交互。yield变成了一个表达式，值通过名为send的方法来传递

def psychologist():
    print('Please tell me your problems')
    while True:
        answer = (yield)
        if answer is not None:
            if answer.endswith('?'):
                print("Don`t ask yourself too much questions")
            elif 'good' in answer:
                print('Ahh that`s good, go on')
            elif 'bad' in answer:
                print("Don`t be so negative")

free = psychologist()
next(free)
free.send('i fell bad')
free.send('why i shouldn`t')
free.send('good for me')

# throw close 处理异常




















