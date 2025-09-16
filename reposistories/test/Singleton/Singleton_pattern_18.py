class SingletonFactory:
    _instance = None
    class _SingletonProduct:
        def __init__(self, value="default"):
            self.value = value
    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._SingletonProduct(*args, **kwargs)
        return self._instance
factory = SingletonFactory()
s1 = factory(1)
s2 = factory(2)
print(s1 is s2)
print(s1.value)