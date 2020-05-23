class Student(object):

    def __init__(self,name,score):
        self.__name=name
        self.__score=score

    def print(self):
        print('%s:%s' % (self.__name,self.__score))

bart = Student('Bart Simpson', 59)
lisa = Student('Lisa Simpson', 87)
bart.print()
lisa.print()
print(bart._Student__name)
print(isinstance(bart,Student))
print(type(bart))
print(dir(bart))
print(hasattr(bart,'name'))