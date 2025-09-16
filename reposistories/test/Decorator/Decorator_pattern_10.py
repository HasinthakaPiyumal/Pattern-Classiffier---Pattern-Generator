import functools

def cache_result(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items()))) # Create a hashable key
        if key not in cache:
            print(f"Caching result for {func.__name__}{key}...")
            cache[key] = func(*args, **kwargs)
        else:
            print(f"Returning cached result for {func.__name__}{key}...")
        return cache[key]
    return wrapper

@cache_result
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(5))
print(fibonacci(5))
print(fibonacci(3))