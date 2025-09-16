def method_logger(func):
    def wrapper(self, *args, **kwargs):
        print(f"Calling method '{func.__name__}' of {self.__class__.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(self, *args, **kwargs)
        print(f"Method '{func.__name__}' returned: {result}")
        return result
    return wrapper

class MyClass:
    def __init__(self, value):
        self.value = value

    @method_logger
    def add_value(self, x):
        return self.value + x

    @method_logger
    def multiply_value(self, y):
        return self.value * y

if __name__ == '__main__':
    obj = MyClass(10)
    print(obj.add_value(5))
    print(obj.multiply_value(3))