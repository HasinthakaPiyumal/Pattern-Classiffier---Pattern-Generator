import abc

class Logger(abc.ABC):
    @abc.abstractmethod
    def log(self, message: str):
        pass

class FileLogger(Logger):
    def log(self, message: str):
        return f"Logging to file: {message}"

class ConsoleLogger(Logger):
    def log(self, message: str):
        return f"Logging to console: {message}"

class LoggerFactory:
    @staticmethod
    def create_logger(logger_type: str) -> Logger:
        if logger_type == "file":
            return FileLogger()
        elif logger_type == "console":
            return ConsoleLogger()
        else:
            raise ValueError("Invalid logger type")

if __name__ == "__main__":
    file_logger = LoggerFactory.create_logger("file")
    print(file_logger.log("Application started"))
    console_logger = LoggerFactory.create_logger("console")
    print(console_logger.log("User logged in"))