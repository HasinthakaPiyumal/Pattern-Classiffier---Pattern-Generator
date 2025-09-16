import functools

def log_method_calls(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling method {self.__class__.__name__}.{func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(self, *args, **kwargs)
        print(f"Method {self.__class__.__name__}.{func.__name__} returned: {result}")
        return result
    return wrapper

class Calculator:
    def __init__(self, value):
        self.value = value

    @log_method_calls
    def add(self, x):
        self.value += x
        return self.value

    @log_method_calls
    def subtract(self, x):
        self.value -= x
        return self.value

calc = Calculator(10)
print(calc.add(5))
print(calc.subtract(2))