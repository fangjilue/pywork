import time
import functools
# 装饰器
def decorator(func):
    # * 为可变参数, ** 为关键字参数
    @functools.wraps(func)
    def rint_current_time(*args, **kw):
        print(time.time())
        func(*args, **kw)
    return rint_current_time

# 装饰器名字
@decorator
def f1(func_name,**kw):
    print('This is a function {},{b},{a}'.format(func_name,**kw))

f1('test func', a=1, b='2')
print(f1.__name__)