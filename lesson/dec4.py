def my_decorator(func):
    def wrapper(message):
        print('wrapper of decorator')
        func(message)
    return wrapper


@my_decorator #相当于 greet == wrapper(message)
def greet(message):
    print(message)

greet('hello world')
# 输出
#wrapper of decorator
#hello world