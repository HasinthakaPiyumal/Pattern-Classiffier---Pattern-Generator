import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

@timer_decorator
def long_running_task(duration):
    time.sleep(duration)
    return f"Slept for {duration} seconds"

@timer_decorator
def calculate_factorial(n):
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

if __name__ == '__main__':
    print(long_running_task(0.5))
    print(calculate_factorial(100000))