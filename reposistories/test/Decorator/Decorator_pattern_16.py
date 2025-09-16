import datetime

def log_calls(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] {func.__name__} returned: {result}")
        return result
    return wrapper

@log_calls
def calculate_sum(a, b):
    return a + b

@log_calls
def power(base, exp):
    return base ** exp

if __name__ == '__main__':
    print(calculate_sum(10, 20))
    print(power(2, 3))