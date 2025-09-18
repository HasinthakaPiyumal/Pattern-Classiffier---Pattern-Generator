import random

class Transaction:
    def __init__(self, account_id, amount, recipient_id, is_international=False):
        self.account_id = account_id
        self.amount = amount
        self.recipient_id = recipient_id
        self.is_international = is_international

    def __str__(self):
        status = 'International' if self.is_international else 'Domestic'
        return f"Transaction(Acc:{self.account_id}, Amt:${self.amount:.2f}, Rec:{self.recipient_id}, Type:{status})"

class TransactionInitiator:
    def generate_transaction(self, account_id):
        amount = round(random.uniform(50, 50000), 2)
        recipient_id = random.randint(100000, 999999)
        is_international = random.choice([True, False, False, False]) # Less frequent international
        print(f"[Initiator] Proposing a transaction for account {account_id}.")
        return Transaction(account_id, amount, recipient_id, is_international)

class FraudDetectionSystem:
    HIGH_RISK_THRESHOLD = 10000.00
    INTERNATIONAL_SURCHARGE_FACTOR = 1.2
    KNOWN_FRAUD_RECIPIENTS = {987654, 123456}

    def evaluate_transaction(self, transaction):
        print(f"[FraudDetector] Evaluating {transaction}...")
        issues = []

        if transaction.amount > self.HIGH_RISK_THRESHOLD:
            issues.append(f"High value transaction (${transaction.amount:.2f})")
        
        if transaction.is_international:
            if transaction.amount * self.INTERNATIONAL_SURCHARGE_FACTOR > self.HIGH_RISK_THRESHOLD:
                issues.append(f"International transaction with adjusted high value (${transaction.amount * self.INTERNATIONAL_SURCHARGE_FACTOR:.2f})")
            if random.random() < 0.1: # Simulate occasional international transfer flags
                issues.append("Unusual international destination detected")
        
        if transaction.recipient_id in self.KNOWN_FRAUD_RECIPIENTS:
            issues.append(f"Recipient {transaction.recipient_id} is on a known fraud list")

        if not issues:
            print(f"[FraudDetector] Transaction {transaction.account_id} -> {transaction.recipient_id} (Amount: ${transaction.amount:.2f}) passed all checks. Approved.")
            return True, "Approved"
        else:
            print(f"[FraudDetector] Transaction {transaction.account_id} -> {transaction.recipient_id} (Amount: ${transaction.amount:.2f}) flagged with issues: {', '.join(issues)}. Denied.")
            return False, issues

# --- Simulation --- 
if __name__ == "__main__":
    initiator = TransactionInitiator()
    detector = FraudDetectionSystem()

    print("\n--- Running Transaction Simulations ---")
    for i in range(5):
        account_id = f"ACC{1000 + i}"
        proposed_transaction = initiator.generate_transaction(account_id)
        approved, feedback = detector.evaluate_transaction(proposed_transaction)
        print(f"Overall Result for {proposed_transaction.account_id}: {'Success' if approved else 'Failed'} - {feedback}\n")

    # Example of a transaction designed to be flagged
    print("\n--- Testing a known high-risk scenario ---")
    high_risk_transaction = Transaction("ACC_RISK", 15000.00, 987654, True)
    print(f"[Initiator] Proposing a high-risk transaction: {high_risk_transaction}")
    approved, feedback = detector.evaluate_transaction(high_risk_transaction)
    print(f"Overall Result for {high_risk_transaction.account_id}: {'Success' if approved else 'Failed'} - {feedback}\n")
