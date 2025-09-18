import abc

class InterestCalculationStrategy(abc.ABC):
    @abc.abstractmethod
    def calculate_interest(self, balance):
        pass

class SavingsInterest(InterestCalculationStrategy):
    def calculate_interest(self, balance):
        rate = 0.015
        interest = balance * rate / 12
        print(f"Calculated savings interest: ${interest:.2f} (1.5% annual rate)")
        return interest

class CheckingInterest(InterestCalculationStrategy):
    def calculate_interest(self, balance):
        if balance > 1000:
            rate = 0.0025
            interest = balance * rate / 12
            print(f"Calculated checking interest: ${interest:.2f} (0.25% annual rate for balance > $1000)")
            return interest
        else:
            print("No checking interest for balances $1000 or less.")
            return 0.0

class LoanInterest(InterestCalculationStrategy):
    def __init__(self, loan_term_months):
        self._loan_term_months = loan_term_months

    def calculate_interest(self, principal):
        annual_rate = 0.045
        monthly_rate = annual_rate / 12
        interest = principal * monthly_rate
        print(f"Calculated loan interest: ${interest:.2f} (4.5% annual rate, monthly on principal)")
        return interest

class BankAccount:
    def __init__(self, account_number, balance, strategy: InterestCalculationStrategy):
        self._account_number = account_number
        self._balance = balance
        self._interest_strategy = strategy

    def set_interest_strategy(self, strategy: InterestCalculationStrategy):
        self._interest_strategy = strategy

    def deposit(self, amount):
        self._balance += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")
            return True
        print(f"Insufficient funds to withdraw ${amount:.2f}.")
        return False

    def apply_interest(self):
        interest_amount = self._interest_strategy.calculate_interest(self._balance)
        self._balance += interest_amount
        print(f"Interest applied. Current balance: ${self._balance:.2f}")
        return interest_amount

    def get_balance(self):
        return self._balance

if __name__ == "__main__":
    savings_account = BankAccount("SA123", 5000.00, SavingsInterest())
    print(f"\n--- Savings Account {savings_account._account_number} ---")
    savings_account.apply_interest()
    savings_account.deposit(200)
    savings_account.apply_interest()

    checking_account = BankAccount("CA456", 800.00, CheckingInterest())
    print(f"\n--- Checking Account {checking_account._account_number} ---")
    checking_account.apply_interest()
    checking_account.deposit(500)
    checking_account.apply_interest()

    loan_account = BankAccount("LA789", 10000.00, LoanInterest(60))
    print(f"\n--- Loan Account {loan_account._account_number} ---")
    loan_account.apply_interest()
    loan_account.withdraw(500)
    loan_account.apply_interest()