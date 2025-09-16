def repeat_decorator(num_times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(num_times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat_decorator(num_times=3)
def print_message(message):
    return f"Repeating: {message}"

if __name__ == '__main__':
    print(print_message("Python is fun!"))