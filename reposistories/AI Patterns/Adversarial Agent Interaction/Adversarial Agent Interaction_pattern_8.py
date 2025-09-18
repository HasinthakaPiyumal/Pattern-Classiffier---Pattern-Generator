import random
import time

class Transaction:
    def __init__(self, account_id, amount, location, type):
        self.account_id = account_id
        self.amount = amount
        self.location = location
        self.type = type
        self.timestamp = time.time()

    def __str__(self):
        return f"Account: {self.account_id}, Amount: ${self.amount:.2f}, Location: {self.location}, Type: {self.type}"

class TransactionProcessorAgent:
    def generate_transaction(self, account_id):
        amount = round(random.uniform(10, 5000), 2)
        locations = ["New York", "London", "Paris", "Tokyo", "Sydney", "Remote"] # Real-world locations
        transaction_types = ["purchase", "withdrawal", "transfer"]
        location = random.choice(locations)
        transaction_type = random.choice(transaction_types)
        return Transaction(account_id, amount, location, transaction_type)

class FraudDetectionAgent:
    def __init__(self):
        self.suspicious_threshold_amount = 2000 # Example rule: large transaction
        self.suspicious_locations = {"Remote"} # Example rule: high-risk location

    def evaluate_transaction(self, transaction):
        is_suspicious = False
        reasons = []

        if transaction.amount > self.suspicious_threshold_amount:
            is_suspicious = True
            reasons.append(f"High amount transaction (${transaction.amount:.2f} > ${self.suspicious_threshold_amount:.2f})")

        if transaction.location in self.suspicious_locations:
            is_suspicious = True
            reasons.append(f"Transaction from suspicious location: {transaction.location}")

        if transaction.type == "purchase" and transaction.amount < 50 and random.random() < 0.1: # Simulation of frequent small purchase pattern
             is_suspicious = True
             reasons.append("Potentially part of a frequent small purchase pattern")

        return is_suspicious, reasons

if __name__ == "__main__":
    processor = TransactionProcessorAgent()
    fraud_detector = FraudDetectionAgent()

    print("--- Simulating Banking Fraud Detection (Real-world: Fraud prevention systems) ---")
    account_ids = ["ACC001", "ACC002", "ACC003"]
    
    simulated_transactions = []
    for _ in range(5): # Generate normal transactions
        simulated_transactions.append(processor.generate_transaction(random.choice(account_ids)))
    
    # Add transactions designed to trigger fraud rules (simulation pattern)
    susp_tx1 = Transaction("ACC001", 3500.00, "Remote", "transfer") # High amount, suspicious location
    simulated_transactions.append(susp_tx1)
    
    susp_tx2 = Transaction("ACC002", 2500.00, "New York", "purchase") # High amount
    simulated_transactions.append(susp_tx2)

    susp_tx3 = Transaction("ACC003", 25.00, "London", "purchase") # Candidate for frequent small purchase
    simulated_transactions.append(susp_tx3)
    
    for i, tx in enumerate(simulated_transactions):
        print(f"\nProcessing Transaction {i+1}: {tx}")
        is_suspicious, reasons = fraud_detector.evaluate_transaction(tx)
        if is_suspicious:
            print(f"  ALERT: Suspicious transaction detected! Reasons: {', '.join(reasons)}")
        else:
            print("  Transaction deemed normal.")
