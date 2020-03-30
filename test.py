class TestClass(object):
    def __init__(self):
        self.testVar = "Hallo"

    def __setattr__(self, key, value):
        import inspect
        print(inspect.findsource(value))
        print(inspect.getfile(value))


if __name__ == '__main__':
    a = TestClass()
    a.testVar = "hoi"
