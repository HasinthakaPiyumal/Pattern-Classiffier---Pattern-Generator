def singleton(cls):
    _instances = {}
    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance
@singleton
class DecoratedSingleton:
    def __init__(self, value):
        self.value = value
s1 = DecoratedSingleton(1)
s2 = DecoratedSingleton(2)
print(s1 is s2)
print(s1.value)