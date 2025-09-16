class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        self.value = 1
s1 = Singleton()
s2 = Singleton()
assert s1 is s2
assert s1.value == 1
s1.value = 2
assert s2.value == 2