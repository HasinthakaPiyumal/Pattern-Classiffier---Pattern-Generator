class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value if value is not None else "default"
            self._initialized = True
s1 = Singleton(1)
s2 = Singleton(2)
print(s1 is s2)
print(s1.value)