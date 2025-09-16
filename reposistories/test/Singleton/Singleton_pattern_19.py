class InitControlledSingleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    def __init__(self, value=None):
        if not self._initialized:
            self.value = value if value is not None else "default"
            self._initialized = True
ics1 = InitControlledSingleton(1)
ics2 = InitControlledSingleton(2)
print(ics1 is ics2)
print(ics1.value)