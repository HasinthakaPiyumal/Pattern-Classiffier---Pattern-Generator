class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event_type, amount):
        for observer in self._observers:
            observer.update(self, event_type, amount)

class BankAccount(Subject):
    def __init__(self, account_number, initial_balance):
        super().__init__()
        self.account_number = account_number
        self._balance = initial_balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount
        print(f"Banking: Account {self.account_number}: Deposited {amount}. New balance: {self._balance}")
        self.notify("deposit", amount)

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            print(f"Banking: Account {self.account_number}: Withdrew {amount}. New balance: {self._balance}")
            self.notify("withdrawal", amount)
        else:
            print(f"Banking: Account {self.account_number}: Insufficient funds for withdrawal of {amount}.")

class SMSNotifier:
    def update(self, account, event_type, amount):
        print(f"Banking: SMS: Account {account.account_number} - {event_type.capitalize()} of {amount}. Balance: {account.balance}")

class EmailNotifier:
    def update(self, account, event_type, amount):
        print(f"Banking: Email: Detailed notification for account {account.account_number}: {event_type} of {amount}. Current balance: {account.balance}.")

class TransactionLogger:
    def update(self, account, event_type, amount):
        print(f"Banking: Logger: Logged transaction for {account.account_number}: Type={event_type}, Amount={amount}, Balance={account.balance}")

account123 = BankAccount("123-456-789", 1000)

sms_alert = SMSNotifier()
email_alert = EmailNotifier()
trans_logger = TransactionLogger()

account123.attach(sms_alert)
account123.attach(email_alert)
account123.attach(trans_logger)

print("--- Banking Simulation: Initial State ---")
print(f"Account {account123.account_number} balance: {account123.balance}")

print("\n--- Banking Simulation: Deposit ---")
account123.deposit(500)

print("\n--- Banking Simulation: Withdrawal ---")
account123.withdraw(200)

print("\n--- Banking Simulation: Detach SMS notifier and another withdrawal ---")
account123.detach(sms_alert)
account123.withdraw(800)

print("\n--- Banking Simulation: Attempt overdraft ---")
account123.withdraw(1000)