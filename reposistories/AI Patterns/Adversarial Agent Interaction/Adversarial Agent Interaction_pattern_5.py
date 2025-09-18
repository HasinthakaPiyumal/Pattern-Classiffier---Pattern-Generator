import random
import time

class Transaction:
    def __init__(self, sender_account, recipient_account, amount, transaction_type):
        self.sender_account = sender_account
        self.recipient_account = recipient_account
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = time.time()

    def __repr__(self):
        return f"Transaction(Sender: {self.sender_account}, Recipient: {self.recipient_account}, Amount: ${self.amount:.2f}, Type: {self.transaction_type})"

class TransactionGenerator:
    def generate_transaction(self, sender, recipient_pool, min_amount, max_amount):
        recipient = random.choice(recipient_pool)
        amount = round(random.uniform(min_amount, max_amount), 2)
        transaction_type = random.choice(["transfer", "payment", "withdrawal"])
        return Transaction(sender, recipient, amount, transaction_type)

class FraudDetectionSystem:
    def __init__(self, high_value_threshold=5000, suspicious_recipients=None, max_daily_transactions=5):
        self.high_value_threshold = high_value_threshold
        self.suspicious_recipients = suspicious_recipients if suspicious_recipients is not None else {"SCAMMER123", "FRAUDSTER456"}
        self.user_transaction_counts = {}

    def evaluate_transaction(self, transaction):
        issues = []

        if transaction.amount > self.high_value_threshold:
            issues.append(f"High value transaction detected: ${transaction.amount:.2f} exceeds threshold ${self.high_value_threshold:.2f}.")

        if transaction.recipient_account in self.suspicious_recipients:
            issues.append(f"Transaction to known suspicious recipient: {transaction.recipient_account}.")

        sender = transaction.sender_account
        self.user_transaction_counts[sender] = self.user_transaction_counts.get(sender, 0) + 1
        if self.user_transaction_counts[sender] > self.max_daily_transactions:
            issues.append(f"Excessive transactions from sender {sender}: {self.user_transaction_counts[sender]} today.")

        if issues:
            return False, issues
        else:
            return True, ["No issues detected."]

if __name__ == "__main__":
    generator = TransactionGenerator()
    fraud_detector = FraudDetectionSystem()

    sender_account = "USER_A123"
    recipient_accounts = ["BANK_B456", "MERCHANT_C789", "FRIEND_D012", "SCAMMER123", "UTILITY_E345"]

    print("--- Simulating Transaction Processing ---")
    for i in range(7):
        transaction = generator.generate_transaction(sender_account, recipient_accounts, 100, 10000)
        print(f"\nGenerated: {transaction}")
        is_safe, findings = fraud_detector.evaluate_transaction(transaction)
        if is_safe:
            print("  Status: Approved")
        else:
            print("  Status: Flagged for Review")
        for finding in findings:
            print(f"    - {finding}")

    fraud_detector.user_transaction_counts = {}
    print("\n--- Simulating another day with a high volume user ---")
    high_volume_user = "POWER_USER_X"
    for i in range(8):
        transaction = generator.generate_transaction(high_volume_user, recipient_accounts, 50, 500)
        print(f"\nGenerated: {transaction}")
        is_safe, findings = fraud_detector.evaluate_transaction(transaction)
        if is_safe:
            print("  Status: Approved")
        else:
            print("  Status: Flagged for Review")
        for finding in findings:
            print(f"    - {finding}")