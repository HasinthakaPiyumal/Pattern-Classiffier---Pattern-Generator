import random
import time

class Transaction:
    def __init__(self, sender_account, receiver_account, amount, transaction_id=None):
        self.transaction_id = transaction_id if transaction_id else f"TXN-{int(time.time())}-{random.randint(1000, 9999)}"
        self.sender_account = sender_account
        self.receiver_account = receiver_account
        self.amount = amount
        self.is_approved = False
        self.fraud_flags = []

    def __str__(self):
        return f"Transaction ID: {self.transaction_id}, From: {self.sender_account}, To: {self.receiver_account}, Amount: ${self.amount:.2f}, Approved: {self.is_approved}, Flags: {', '.join(self.fraud_flags) if self.fraud_flags else 'None'}"

class TransactionGenerator:
    def generate_transaction(self, sender_account, receiver_account, amount):
        print(f"Generator: Proposing a transaction from {sender_account} to {receiver_account} for ${amount:.2f}...")
        return Transaction(sender_account, receiver_account, amount)

class FraudDetector:
    HIGH_RISK_THRESHOLD = 5000.00
    SUSPICIOUS_ACCOUNTS = {"REC-98765", "REC-11223"} # Example of known suspicious accounts

    def evaluate_transaction(self, transaction: Transaction):
        print(f"FraudDetector: Evaluating transaction {transaction.transaction_id}...")
        if transaction.amount > self.HIGH_RISK_THRESHOLD:
            transaction.fraud_flags.append("HighAmount")
            print(f"  - Flagged: High transaction amount (${transaction.amount:.2f})")
        if transaction.receiver_account in self.SUSPICIOUS_ACCOUNTS:
            transaction.fraud_flags.append("SuspiciousRecipient")
            print(f"  - Flagged: Recipient account is suspicious ({transaction.receiver_account})")
        if len(transaction.fraud_flags) > 0:
            print(f"FraudDetector: Transaction {transaction.transaction_id} flagged for potential fraud.")
            return False
        else:
            print(f"FraudDetector: Transaction {transaction.transaction_id} appears legitimate.")
            return True

class BankingSystem:
    def __init__(self):
        self.generator = TransactionGenerator()
        self.detector = FraudDetector()
        self.transactions = []

    def process_transaction_request(self, sender, receiver, amount):
        new_transaction = self.generator.generate_transaction(sender, receiver, amount)
        is_safe = self.detector.evaluate_transaction(new_transaction)
        if is_safe:
            new_transaction.is_approved = True
            print(f"System: Transaction {new_transaction.transaction_id} APPROVED.")
        else:
            new_transaction.is_approved = False
            print(f"System: Transaction {new_transaction.transaction_id} REJECTED due to fraud flags.")
        self.transactions.append(new_transaction)
        print(new_transaction)
        print("-" * 50)

if __name__ == "__main__":
    bank_system = BankingSystem()
    bank_system.process_transaction_request("ACC-12345", "ACC-67890", 150.00)
    bank_system.process_transaction_request("ACC-54321", "ACC-98765", 7500.00) # High amount, suspicious recipient
    bank_system.process_transaction_request("ACC-11111", "ACC-22222", 3000.00)
    bank_system.process_transaction_request("ACC-99999", "REC-11223", 100.00) # Suspicious recipient