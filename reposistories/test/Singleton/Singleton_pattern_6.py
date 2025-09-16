import threading
class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.counter = 0
            self._initialized = True
ts1 = ThreadSafeSingleton()
ts2 = ThreadSafeSingleton()
assert ts1 is ts2
assert ts1.counter == 0
ts1.counter += 1
assert ts2.counter == 1