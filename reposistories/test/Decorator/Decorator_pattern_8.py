import functools

def uppercase_result(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            return result.upper()
        return result
    return wrapper

@uppercase_result
def get_greeting(name):
    return f"hello, {name}!"

@uppercase_result
def get_number():
    return 123

print(get_greeting("alice"))
print(get_number())