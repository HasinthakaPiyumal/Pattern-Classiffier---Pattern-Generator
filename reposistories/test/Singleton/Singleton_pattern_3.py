def singleton_decorator(cls):
    _instances = {}
    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance
@singleton_decorator
class DecoratedSingleton:
    def __init__(self, name="default"):
        self.name = name
d1 = DecoratedSingleton("alice")
d2 = DecoratedSingleton("bob")
assert d1 is d2
assert d1.name == "alice"
d1.name = "charlie"
assert d2.name == "charlie"