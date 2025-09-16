def cache_decorator(func):
    _cache = {}
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in _cache:
            print(f"Cache miss for {func.__name__} with {key}. Calculating...")
            _cache[key] = func(*args, **kwargs)
        else:
            print(f"Cache hit for {func.__name__} with {key}.")
        return _cache[key]
    return wrapper

@cache_decorator
def expensive_calculation(a, b):
    import time
    time.sleep(0.1) # Simulate expensive operation
    return a * b

if __name__ == '__main__':
    print(expensive_calculation(2, 3))
    print(expensive_calculation(2, 3)) # Should be cached
    print(expensive_calculation(5, 10))
    print(expensive_calculation(5, 10)) # Should be cached
    print(expensive_calculation(b=3, a=2))