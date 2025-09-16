import functools

def enforce_types(a_type, b_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(a, b):
            if not isinstance(a, a_type):
                print(f"Warning: Converting 'a' from {type(a)} to {a_type}")
                a = a_type(a)
            if not isinstance(b, b_type):
                print(f"Warning: Converting 'b' from {type(b)} to {b_type}")
                b = b_type(b)
            return func(a, b)
        return wrapper
    return decorator

@enforce_types(int, int)
def divide(a, b):
    return a / b

print(divide(10, 2))
print(divide("10", "2"))
print(divide(10.5, 2.5))