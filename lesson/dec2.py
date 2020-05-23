import time
# 装饰器
def decorator(func):
    def rint_current_time(a):
        print('123')
        func(a)
    return rint_current_time

@decorator
def f1(a):
    print('This is a function'+a)

#f = decorator(f1)
#f('1')

f1('2')
print(f1.__name__)