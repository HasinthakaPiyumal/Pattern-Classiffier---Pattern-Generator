class SingletonBase:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
class ChildSingleton(SingletonBase):
    def __init__(self, value):
        if not self._initialized:
            self.value = value
            self._initialized = True
cs1 = ChildSingleton(1)
cs2 = ChildSingleton(2)
print(cs1 is cs2)
print(cs1.value)