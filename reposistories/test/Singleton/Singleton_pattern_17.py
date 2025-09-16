_factory_instance = None
def get_factory_singleton(value=None):
    global _factory_instance
    if _factory_instance is None:
        class FactorySingletonClass:
            def __init__(self, val):
                self.value = val
        _factory_instance = FactorySingletonClass(value if value is not None else "initial")
    return _factory_instance
s1 = get_factory_singleton(1)
s2 = get_factory_singleton(2)
print(s1 is s2)
print(s1.value)