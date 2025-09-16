_factory_singleton_instance = None
class FactoryManagedClass:
    def __init__(self, value="default"):
        self.value = value
def get_factory_managed_singleton(value="default_factory_value"):
    global _factory_singleton_instance
    if _factory_singleton_instance is None:
        _factory_singleton_instance = FactoryManagedClass(value)
    return _factory_singleton_instance
f1 = get_factory_managed_singleton("initial_factory_value")
f2 = get_factory_managed_singleton("another_factory_value")
assert f1 is f2
assert f1.value == "initial_factory_value"
f1.value = "changed_factory_value"
assert f2.value == "changed_factory_value"