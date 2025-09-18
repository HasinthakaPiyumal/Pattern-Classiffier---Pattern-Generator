import random

class TransactionRequestGenerator:
    def generate_transaction(self, account_id):
        amount = round(random.uniform(10.0, 5000.0), 2)
        transaction_type = random.choice(["deposit", "withdrawal", "transfer"])
        recipient = random.choice(["bank_A", "bank_B", "merchant_X", "individual_Y"]) if transaction_type == "transfer" else None
        print(f"Generating transaction request for account {account_id}: Type={transaction_type}, Amount=${amount:.2f}, Recipient={recipient if recipient else 'N/A'}")
        return {"account_id": account_id, "amount": amount, "type": transaction_type, "recipient": recipient}

class FraudDetectionSystem:
    def evaluate_transaction(self, transaction):
        print(f"  Safeguard: Evaluating transaction for account {transaction['account_id']}...")
        is_suspicious = False
        reasons = []

        if transaction["amount"] > 2000 and transaction["type"] == "transfer":
            is_suspicious = True
            reasons.append("High value transfer.")
        if transaction["account_id"] == "ACC007" and transaction["type"] == "withdrawal" and transaction["amount"] > 1000:
            is_suspicious = True
            reasons.append("Unusual large withdrawal from high-risk account.")
        if transaction["type"] == "deposit" and transaction["amount"] < 10:
            is_suspicious = True
            reasons.append("Very small deposit (potential test for stolen card).")

        if is_suspicious:
            print(f"  Safeguard: Transaction flagged as suspicious. Reasons: {', '.join(reasons)}")
            return {"status": "rejected", "issues": reasons}
        else:
            print("  Safeguard: Transaction approved.")
            return {"status": "approved", "issues": []}

if __name__ == "__main__":
    generator = TransactionRequestGenerator()
    safeguard = FraudDetectionSystem()

    transactions_to_test = [
        {"account_id": "ACC001", "amount": 150.00, "type": "withdrawal", "recipient": None},
        {"account_id": "ACC002", "amount": 2500.00, "type": "transfer", "recipient": "bank_C"}, 
        {"account_id": "ACC007", "amount": 1200.00, "type": "withdrawal", "recipient": None}, 
        {"account_id": "ACC003", "amount": 5.00, "type": "deposit", "recipient": None}, 
        {"account_id": "ACC004", "amount": 800.00, "type": "deposit", "recipient": None},
    ]

    for data in transactions_to_test:
        print("-" * 30)
        transaction = generator.generate_transaction(data["account_id"])
        transaction.update(data) # Override with specific test data for predictable results
        result = safeguard.evaluate_transaction(transaction)
        if result["status"] == "approved":
            print(f"Transaction for account {transaction['account_id']} processed successfully.")
        else:
            print(f"Transaction for account {transaction['account_id']} rejected. Issues: {', '.join(result['issues'])}")