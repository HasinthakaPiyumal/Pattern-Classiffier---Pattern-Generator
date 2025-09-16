class ClassDecorator:
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        print("--- Class Decorator: Before ---")
        result = self.func(*args, **kwargs)
        print("--- Class Decorator: After ---")
        return result

@ClassDecorator
def say_hi(name):
    return f"Hi there, {name}!"

if __name__ == '__main__':
    print(say_hi("Bob"))