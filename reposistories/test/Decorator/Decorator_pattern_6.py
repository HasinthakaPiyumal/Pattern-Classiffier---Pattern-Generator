import functools

def call_counter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print(f"Function {func.__name__} has been called {wrapper.calls} times.")
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@call_counter
def say_hello():
    return "Hello!"

@call_counter
def say_goodbye():
    return "Goodbye!"

print(say_hello())
print(say_hello())
print(say_goodbye())
print(say_hello())