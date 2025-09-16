import threading
class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value if value is not None else "default"
            self._initialized = True
ts1 = ThreadSafeSingleton(1)
ts2 = ThreadSafeSingleton(2)
print(ts1 is ts2)
print(ts1.value)