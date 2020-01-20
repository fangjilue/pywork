class abc:
    def a(self):
        print("a")


if __name__ == '__main__':
    for num in range(1, 5):
        if num == 2:
            abc.test = "a"
        try:
            print(abc.test)
        except Exception as e:
            print(e)
    ss = "abc中国人"
    b = ss.encode('utf-8')
    print(len(b),b)
    print(b.decode('utf-8'),len(ss))
    a_file = open('aa.py',encoding='utf-8')
    print(a_file.mode,a_file.encoding)
    print(a_file.read())
    a_file.close()