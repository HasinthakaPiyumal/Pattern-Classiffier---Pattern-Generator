class LogStrategy:
    def log(self, message):
        raise NotImplementedError
class ConsoleLogStrategy(LogStrategy):
    def log(self, message):
        print(f"CONSOLE: {message}")
class FileLogStrategy(LogStrategy):
    def log(self, message):
        with open("app.log", "a") as f:
            f.write(f"FILE: {message}\n")
class Logger:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def write_log(self, message):
        self._strategy.log(message)
logger = Logger(ConsoleLogStrategy())
logger.write_log("Application started.")
logger.set_strategy(FileLogStrategy())
logger.write_log("User logged in.")