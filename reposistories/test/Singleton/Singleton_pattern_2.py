class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
class MySingleton(metaclass=SingletonMeta):
    def __init__(self, data="default"):
        self.data = data
m1 = MySingleton("first")
m2 = MySingleton("second")
assert m1 is m2
assert m1.data == "first"
m1.data = "changed"
assert m2.data == "changed"