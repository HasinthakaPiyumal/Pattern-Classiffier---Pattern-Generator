import random

class Transaction:
    def __init__(self, account_id, amount, recipient, location, type):
        self.account_id = account_id
        self.amount = amount
        self.recipient = recipient
        self.location = location
        self.type = type
        self.status = "PENDING"

    def __repr__(self):
        return f"Transaction(Account:{self.account_id}, Amount:${self.amount:.2f}, Status:{self.status})"

class TransactionProcessor:
    def propose_transaction(self, account_id, amount, recipient, location, type):
        print(f"TransactionProcessor: Proposing a {type} transaction for account {account_id} of ${amount:.2f} to {recipient} from {location}.")
        return Transaction(account_id, amount, recipient, location, type)

class FraudDetector:
    def __init__(self, high_risk_locations, max_daily_spend):
        self.high_risk_locations = high_risk_locations
        self.max_daily_spend = max_daily_spend
        self.account_daily_spend = {}

    def evaluate_transaction(self, transaction):
        issues = []

        if transaction.location in self.high_risk_locations:
            issues.append(f"Transaction from high-risk location: {transaction.location}")

        if transaction.type == "WIRE_TRANSFER" and transaction.amount > 5000:
            issues.append(f"Large wire transfer amount: ${transaction.amount:.2f}")

        current_spend = self.account_daily_spend.get(transaction.account_id, 0)
        if current_spend + transaction.amount > self.max_daily_spend:
            issues.append(f"Exceeds daily spend limit for account {transaction.account_id}. Current:${current_spend:.2f}, Proposed:${transaction.amount:.2f}, Limit:${self.max_daily_spend:.2f}")
        else:
            self.account_daily_spend[transaction.account_id] = current_spend + transaction.amount

        if issues:
            transaction.status = "REJECTED_FRAUD"
            print(f"FraudDetector: !!! Detected potential fraud for {transaction}. Issues: {'; '.join(issues)}")
            return False, issues
        else:
            transaction.status = "APPROVED"
            print(f"FraudDetector: Transaction {transaction} appears legitimate. Approved.")
            return True, []

if __name__ == "__main__":
    transaction_processor = TransactionProcessor()
    fraud_detector = FraudDetector(
        high_risk_locations=["NIGERIA", "RUSSIA", "NORTH_KOREA"],
        max_daily_spend=10000
    )

    transactions_to_process = [
        ("ACC123", 500, "John Doe", "USA", "PURCHASE"),
        ("ACC123", 7000, "Jane Smith", "NIGERIA", "WIRE_TRANSFER"),
        ("ACC456", 200, "Shop A", "CANADA", "PURCHASE"),
        ("ACC456", 9900, "Shop B", "CANADA", "PURCHASE"),
        ("ACC456", 500, "Shop C", "CANADA", "PURCHASE"),
        ("ACC789", 6000, "Global Inc.", "GERMANY", "WIRE_TRANSFER"),
    ]

    for acc, amt, rec, loc, typ in transactions_to_process:
        proposed_tx = transaction_processor.propose_transaction(acc, amt, rec, loc, typ)
        is_approved, reasons = fraud_detector.evaluate_transaction(proposed_tx)
        print("-" * 30)

    print("\nFinal Daily Spend for ACC456:", fraud_detector.account_daily_spend.get("ACC456", 0))