import abc
import datetime

class LogOutputStrategy(abc.ABC):
    @abc.abstractmethod
    def log(self, message):
        pass

class ConsoleLogStrategy(LogOutputStrategy):
    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] CONSOLE: {message}")

class FileLogStrategy(LogOutputStrategy):
    def __init__(self, filename="app.log"):
        self.filename = filename

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a") as f:
            f.write(f"[{timestamp}] FILE: {message}\n")
        print(f"[{timestamp}] Logged to file '{self.filename}': {message}")

class Logger:
    def __init__(self, strategy: LogOutputStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: LogOutputStrategy):
        self._strategy = strategy

    def write_log(self, message):
        self._strategy.log(message)

if __name__ == "__main__":
    logger = Logger(ConsoleLogStrategy())
    logger.write_log("Application started.")

    logger.set_strategy(FileLogStrategy("my_app.log"))
    logger.write_log("User logged in.")
    logger.write_log("Data processed successfully.")