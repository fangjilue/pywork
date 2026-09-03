import time
import datetime


def f1():
    print('This is a function f1')

# 在不修改原函数的情况下，增加打印时间戳
def print_current_time(func):
    print(time.time()*1000)
    func()

print_current_time(f1)
print(f1.__name__)
print(print_current_time.__name__)

#当月1号
print(datetime.date(datetime.date.today().year,datetime.date.today().month,1).strftime('%Y-%m-%d'))
#当月1号
print(datetime.date.today().replace(day=1).strftime('%Y-%m-%d'))
#上月1号
print((datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d'))