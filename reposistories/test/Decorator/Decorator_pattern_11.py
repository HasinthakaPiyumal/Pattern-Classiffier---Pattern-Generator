def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print("--- Before function call ---")
        result = func(*args, **kwargs)
        print("--- After function call ---")
        return result
    return wrapper

@simple_decorator
def greet(name):
    return f"Hello, {name}!"

if __name__ == '__main__':
    print(greet("Alice"))