import abc
import re

class ValidationStrategy(abc.ABC):
    @abc.abstractmethod
    def validate(self, data):
        pass

class EmailValidation(ValidationStrategy):
    def validate(self, data):
        if re.match(r"[^@]+@[^@]+\.[^@]+", data):
            print(f"'{data}' is a valid email.")
            return True
        print(f"'{data}' is NOT a valid email.")
        return False

class PhoneNumberValidation(ValidationStrategy):
    def validate(self, data):
        # Simple validation for (XXX) XXX-XXXX format or XXXXXXXXXX
        if re.match(r"^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$", data):
            print(f"'{data}' is a valid phone number.")
            return True
        print(f"'{data}' is NOT a valid phone number.")
        return False

class Validator:
    def __init__(self, strategy: ValidationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ValidationStrategy):
        self._strategy = strategy

    def validate_data(self, data):
        return self._strategy.validate(data)

if __name__ == "__main__":
    validator = Validator(EmailValidation())
    validator.validate_data("test@example.com")
    validator.validate_data("invalid-email")

    validator.set_strategy(PhoneNumberValidation())
    validator.validate_data("123-456-7890")
    validator.validate_data("(123) 456-7890")
    validator.validate_data("12345")