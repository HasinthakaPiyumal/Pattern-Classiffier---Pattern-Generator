class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
class MetaclassSingleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value
ms1 = MetaclassSingleton(1)
ms2 = MetaclassSingleton(2)
print(ms1 is ms2)
print(ms1.value)