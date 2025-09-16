class GenericSingletonRegistry:
    _instances = {}
    @classmethod
    def get_instance(cls, target_cls, *args, **kwargs):
        if target_cls not in cls._instances:
            instance = target_cls(*args, **kwargs)
            cls._instances[target_cls] = instance
        return cls._instances[target_cls]
class MyGenericSingleton:
    def __init__(self, value):
        self.value = value
s1 = GenericSingletonRegistry.get_instance(MyGenericSingleton, 1)
s2 = GenericSingletonRegistry.get_instance(MyGenericSingleton, 2)
print(s1 is s2)
print(s1.value)