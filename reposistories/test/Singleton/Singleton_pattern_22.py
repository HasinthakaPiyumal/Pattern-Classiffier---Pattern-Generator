class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ApplicationLogger(metaclass=SingletonMeta):
    def __init__(self, log_file="app.log"):
        self.log_file = log_file

    def log_message(self, level, message):
        with open(self.log_file, "a") as f:
            f.write(f"[{level}] {message}\n")

if __name__ == "__main__":
    logger1 = ApplicationLogger("production.log")
    logger2 = ApplicationLogger("test.log")

    logger1.log_message("INFO", "User 'admin' logged in.")
    logger2.log_message("ERROR", "Failed to connect to database.")

    print(f"Are logger1 and logger2 the same instance? {logger1 is logger2}")
    print(f"Logger1 log_file: {logger1.log_file}, Logger2 log_file: {logger2.log_file}")