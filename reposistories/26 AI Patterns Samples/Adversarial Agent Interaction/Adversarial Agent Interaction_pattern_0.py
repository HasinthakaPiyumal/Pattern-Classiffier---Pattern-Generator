import random
import time

class Transaction:
    def __init__(self, transaction_id, account_id, amount, transaction_type):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.status = "pending"

    def __str__(self):
        return f"ID: {self.transaction_id}, Account: {self.account_id}, Amount: ${self.amount:.2f}, Type: {self.transaction_type}, Status: {self.status}"

class TransactionProposer:
    def __init__(self, account_ids):
        self.account_ids = account_ids
        self.transaction_counter = 0

    def propose_transaction(self):
        self.transaction_counter += 1
        account_id = random.choice(self.account_ids)
        amount = round(random.uniform(10.00, 5000.00), 2)
        transaction_type = random.choice(["deposit", "withdrawal", "transfer", "purchase"])
        return Transaction(f"TRX{self.transaction_counter:04d}", account_id, amount, transaction_type)

class FraudDetector:
    def __init__(self, daily_limit=2000.00, suspicious_accounts=None, max_transactions_per_hour=5):
        self.daily_limit = daily_limit
        self.suspicious_accounts = suspicious_accounts if suspicious_accounts else []
        self.max_transactions_per_hour = max_transactions_per_hour
        self.transaction_history = {} # {account_id: [(timestamp, amount)]}

    def _check_daily_limit(self, transaction):
        if transaction.transaction_type in ["withdrawal", "transfer", "purchase"]:
            current_day_total = sum(t[1] for t in self.transaction_history.get(transaction.account_id, []) if time.time() - t[0] < 86400)
            if current_day_total + transaction.amount > self.daily_limit:
                return False, "Exceeds daily transaction limit."
        return True, ""

    def _check_suspicious_account(self, transaction):
        if transaction.account_id in self.suspicious_accounts:
            return False, "Transaction from a suspicious account."
        return True, ""

    def _check_velocity(self, transaction):
        current_hour_transactions = [t for t in self.transaction_history.get(transaction.account_id, []) if time.time() - t[0] < 3600]
        if len(current_hour_transactions) >= self.max_transactions_per_hour:
            return False, "High transaction velocity for account."
        return True, ""

    def evaluate(self, transaction):
        checks = [
            self._check_daily_limit,
            self._check_suspicious_account,
            self._check_velocity
        ]

        for check_func in checks:
            is_valid, reason = check_func(transaction)
            if not is_valid:
                return False, reason

        if transaction.account_id not in self.transaction_history:
            self.transaction_history[transaction.account_id] = []
        self.transaction_history[transaction.account_id].append((time.time(), transaction.amount))
        return True, "Transaction approved."

if __name__ == "__main__":
    account_ids = ["ACC001", "ACC002", "ACC003", "ACC004", "ACC005"]
    suspicious_accounts = ["ACC003"]
    
    proposer = TransactionProposer(account_ids)
    detector = FraudDetector(daily_limit=3000.00, suspicious_accounts=suspicious_accounts, max_transactions_per_hour=3)

    print("--- Simulating Transaction Processing with Fraud Detection ---")
    simulated_transactions = []

    for _ in range(5):
        simulated_transactions.append(proposer.propose_transaction())
    
    simulated_transactions.append(Transaction("TRX0006", "ACC001", 3500.00, "withdrawal"))
    simulated_transactions.append(Transaction("TRX0007", "ACC003", 100.00, "purchase"))
    
    for i in range(4):
        simulated_transactions.append(Transaction(f"TRX000{8+i}", "ACC002", 50.00, "purchase"))
        time.sleep(0.1)

    for transaction in simulated_transactions:
        print(f"\nProposing: {transaction}")
        is_safe, reason = detector.evaluate(transaction)
        if is_safe:
            transaction.status = "approved"
            print(f"  Safeguard (Fraud Detector): {reason}")
        else:
            transaction.status = "declined"
            print(f"  Safeguard (Fraud Detector) REJECTED: {reason}")
        print(f"  Final Status: {transaction.status}")
        time.sleep(0.2)
