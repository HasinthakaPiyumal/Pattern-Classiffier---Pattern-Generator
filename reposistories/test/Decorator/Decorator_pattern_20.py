import time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Attempt {attempt} for {func.__name__}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise Exception(f"Function {func.__name__} failed after {max_attempts} attempts.")
        return wrapper
    return decorator

_call_count = 0

@retry(max_attempts=3, delay=0.1)
def unreliable_function():
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise ValueError("Failed intentionally!")
    return "Success after retries!"

if __name__ == '__main__':
    try:
        print(unreliable_function())
    except Exception as e:
        print(f"Caught final exception: {e}")

    _call_count = 0
    @retry(max_attempts=2, delay=0.1)
    def always_fails():
        global _call_count
        _call_count += 1
        raise RuntimeError("Always failing!")

    try:
        print(always_fails())
    except Exception as e:
        print(f"Caught final exception: {e}")