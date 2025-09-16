class DictSingleton:
    _instance_map = {}
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance_map:
            instance = super().__new__(cls)
            cls._instance_map[cls] = instance
        return cls._instance_map[cls]
    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value if value is not None else "default"
            self._initialized = True
ds1 = DictSingleton(1)
ds2 = DictSingleton(2)
print(ds1 is ds2)
print(ds1.value)