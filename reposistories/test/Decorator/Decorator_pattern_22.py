class BankAccount:
    def __init__(self, account_number, balance=0):
        self._account_number = account_number
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

class AccountDecorator:
    def __init__(self, decorated_account):
        self._decorated_account = decorated_account

    def deposit(self, amount):
        return self._decorated_account.deposit(amount)

    def withdraw(self, amount):
        return self._decorated_account.withdraw(amount)

    def get_balance(self):
        return self._decorated_account.get_balance()

    def get_account_number(self):
        return self._decorated_account.get_account_number()

class LoggingDecorator(AccountDecorator):
    def deposit(self, amount):
        print(f"LOG: Attempting deposit of ${amount:.2f} to account {self.get_account_number()}")
        result = super().deposit(amount)
        if result:
            print(f"LOG: Deposit successful. New balance: ${self.get_balance():.2f}")
        else:
            print(f"LOG: Deposit failed.")
        return result

    def withdraw(self, amount):
        print(f"LOG: Attempting withdrawal of ${amount:.2f} from account {self.get_account_number()}")
        result = super().withdraw(amount)
        if result:
            print(f"LOG: Withdrawal successful. New balance: ${self.get_balance():.2f}")
        else:
            print(f"LOG: Withdrawal failed.")
        return result

class SecurityCheckDecorator(AccountDecorator):
    def __init__(self, decorated_account, required_pin="1234"):
        super().__init__(decorated_account)
        self._required_pin = required_pin

    def _authenticate(self, entered_pin):
        return entered_pin == self._required_pin

    def deposit(self, amount, pin_attempt=""):
        if self._authenticate(pin_attempt):
            print(f"SECURITY: PIN authenticated for deposit.")
            return super().deposit(amount)
        else:
            print(f"SECURITY ERROR: Invalid PIN for deposit.")
            return False

    def withdraw(self, amount, pin_attempt=""):
        if self._authenticate(pin_attempt):
            print(f"SECURITY: PIN authenticated for withdrawal.")
            return super().withdraw(amount)
        else:
            print(f"SECURITY ERROR: Invalid PIN for withdrawal.")
            return False

if __name__ == "__main__":
    my_account = BankAccount("123456789", 1000.00)
    print(f"Initial balance for account {my_account.get_account_number()}: ${my_account.get_balance():.2f}")

    logged_account = LoggingDecorator(my_account)
    logged_account.deposit(200)
    logged_account.withdraw(50)
    logged_account.withdraw(2000)

    print("-" * 30)

    secure_logged_account = SecurityCheckDecorator(LoggingDecorator(BankAccount("987654321", 500.00)), "5678")
    print(f"Initial balance for account {secure_logged_account.get_account_number()}: ${secure_logged_account.get_balance():.2f}")

    secure_logged_account.deposit(100, "wrong_pin")
    secure_logged_account.deposit(100, "5678")
    secure_logged_account.withdraw(50, "5678")
    secure_logged_account.withdraw(1000, "5678")
    secure_logged_account.withdraw(20, "wrong_pin")