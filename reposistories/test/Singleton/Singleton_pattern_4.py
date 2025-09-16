class SingletonBase:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
class MySingletonClass(SingletonBase):
    def __init__(self, id_val="default_id"):
        if not hasattr(self, '_initialized'):
            self.id = id_val
            self._initialized = True
b1 = MySingletonClass("first_id")
b2 = MySingletonClass("second_id")
assert b1 is b2
assert b1.id == "first_id"
b1.id = "updated_id"
assert b2.id == "updated_id"