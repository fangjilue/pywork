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