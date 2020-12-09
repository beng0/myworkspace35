# 缓存

import time
import hashlib
import pickle

cache = {}
def is_obsolete(entry,duration):
    return time.time() -entry['time'] > duration

def compute_key(function,args,kw):
    key = pickle.dumps((function.__name__,args,kw))
    return hashlib.sha1(key).hexdigest()

def memoize(duration=10):
    def _memoize(function):
        def __memoize(*args,**kw):
            key = compute_key(function,args,kw)

            # 是否已经拥有它了？
            if(key in cache and not is_obsolete(cache[key],duration)):
                print('we got a winner')
                return cache[key]['value']
            # 计算
            result = function(*args,**kw)
            # 保存结果
            cache[key] = {
                'value':result,
                'time':time.time()
            }
            return result
        return __memoize
    return _memoize

# @memoize()
# def very_very_very_complex_stuff(a,b):
#     #如果在执行这个计算时计算机过热
#     #请考虑终止程序
#     return a+b
# print(very_very_very_complex_stuff(2,2))
#
# print(very_very_very_complex_stuff(2,2))

@memoize(1)
def very_very_very_complex_stuff(a,b):
    return a + b
print(very_very_very_complex_stuff(2,2))
time.sleep(2)
print(very_very_very_complex_stuff(2,2))

















