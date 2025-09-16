import functools
import time

def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"'{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling '{func.__name__}'...")
        result = func(*args, **kwargs)
        print(f"'{func.__name__}' finished.")
        return result
    return wrapper

@timer_decorator
@log_decorator
def complex_operation(a, b):
    time.sleep(0.1)
    return a * b

print(f"Result: {complex_operation(3, 4)}")