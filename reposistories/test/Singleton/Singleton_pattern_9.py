_global_singleton_registry = {}
class RegistrySingletonA:
    def __new__(cls, *args, **kwargs):
        if cls not in _global_singleton_registry:
            _global_singleton_registry[cls] = super().__new__(cls)
        return _global_singleton_registry[cls]
    def __init__(self, config_a="default_a"):
        if not hasattr(self, '_initialized'):
            self.config_a = config_a
            self._initialized = True
class RegistrySingletonB:
    def __new__(cls, *args, **kwargs):
        if cls not in _global_singleton_registry:
            _global_singleton_registry[cls] = super().__new__(cls)
        return _global_singleton_registry[cls]
    def __init__(self, config_b="default_b"):
        if not hasattr(self, '_initialized'):
            self.config_b = config_b
            self._initialized = True
ra1 = RegistrySingletonA("initial_a")
ra2 = RegistrySingletonA("another_a")
rb1 = RegistrySingletonB("initial_b")
rb2 = RegistrySingletonB("another_b")
assert ra1 is ra2
assert ra1.config_a == "initial_a"
assert rb1 is rb2
assert rb1.config_b == "initial_b"
assert ra1 is not rb1