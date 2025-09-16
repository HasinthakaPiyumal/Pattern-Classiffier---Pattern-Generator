class Logger:
    def log(self, message):
        raise NotImplementedError

class FileLogger(Logger):
    def log(self, message):
        return f"Logging to file: {message}"

class ConsoleLogger(Logger):
    def log(self, message):
        return f"Logging to console: {message}"

class LoggerFactory:
    @staticmethod
    def get_logger(logger_type):
        if logger_type == "file":
            return FileLogger()
        elif logger_type == "console":
            return ConsoleLogger()
        else:
            raise ValueError("Invalid logger type")

if __name__ == "__main__":
    file_logger = LoggerFactory.get_logger("file")
    print(file_logger.log("This is a file log message."))
    console_logger = LoggerFactory.get_logger("console")
    print(console_logger.log("This is a console log message."))
    try:
        db_logger = LoggerFactory.get_logger("database")
        print(db_logger.log("This is a database log message."))
    except ValueError as e:
        print(e)