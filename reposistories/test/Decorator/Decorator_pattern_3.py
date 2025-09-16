import time
import functools

class Timer:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {self.func.__name__} took {end_time - start_time:.4f} seconds.")
        return result

@Timer
def long_running_task():
    time.sleep(0.5)
    return "Task completed"

print(long_running_task())