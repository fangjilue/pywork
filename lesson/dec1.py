import time

def f1():
    print('This is a function f1')

# 在不修改原函数的情况下，增加打印时间戳
def print_current_time(func):
    print(time.time())
    func()

print_current_time(f1)
print(f1.__name__)
print(print_current_time.__name__)
