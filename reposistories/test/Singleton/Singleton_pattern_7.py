class LazySingleton:
    __instance = None
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    def __init__(self, message="default_message"):
        if not hasattr(self, '_initialized'):
            self.message = message
            self._initialized = True
l1 = LazySingleton("first message")
l2 = LazySingleton("second message")
assert l1 is l2
assert l1.message == "first message"
l1.message = "updated message"
assert l2.message == "updated message"