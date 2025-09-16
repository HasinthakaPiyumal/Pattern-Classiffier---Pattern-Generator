def uppercase_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def exclamation_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "!!!"
    return wrapper

@exclamation_decorator
@uppercase_decorator
def get_text(word):
    return f"Hello {word}"

if __name__ == '__main__':
    print(get_text("world"))