import functools
import time
import random

def retry(max_attempts=3, delay=1):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed for {func.__name__}: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper_retry
    return decorator_retry

attempts_left = 3

@retry(max_attempts=3, delay=0.1)
def unstable_function():
    global attempts_left
    attempts_left -= 1
    if attempts_left > 0:
        print("Simulating failure...")
        raise ValueError("Something went wrong!")
    print("Simulating success!")
    return "Operation successful!"

print(unstable_function())