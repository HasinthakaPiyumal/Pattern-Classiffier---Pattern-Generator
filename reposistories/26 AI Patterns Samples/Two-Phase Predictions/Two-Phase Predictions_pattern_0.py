import random
import time

class Transaction:
    def __init__(self, user_id, amount, location, transaction_id):
        self.user_id = user_id
        self.amount = amount
        self.location = location
        self.transaction_id = transaction_id
        self.is_suspicious_light = False
        self.fraud_score_complex = 0.0
        self.risk_level_complex = "UNKNOWN"

    def __str__(self):
        return (f"ID:{self.transaction_id}, User:{self.user_id}, Amt:${self.amount:.2f}, Loc:{self.location}, "
                f"Suspicious(L):{self.is_suspicious_light}, Score(C):{self.fraud_score_complex:.2f}, "
                f"Risk(C):{self.risk_level_complex}")

class LightweightClientModel:
    def predict(self, transaction: Transaction) -> bool:
        print(f"[{transaction.transaction_id}] Phase 1 (Client): Checking...")
        is_suspicious = transaction.amount > 1000 or transaction.location == "UNUSUAL_IP_COUNTRY"
        transaction.is_suspicious_light = is_suspicious
        time.sleep(0.05)
        print(f"[{transaction.transaction_id}] Phase 1 (Client): Result - Suspicious:{is_suspicious}")
        return is_suspicious

class ComplexCloudModel:
    def predict(self, transaction: Transaction):
        print(f"[{transaction.transaction_id}] Phase 2 (Cloud): Analyzing...")
        base_score = 0.1
        if transaction.amount > 5000:
            base_score += 0.4
        if transaction.location == "UNUSUAL_IP_COUNTRY":
            base_score += 0.3
        if random.random() < 0.2:
            base_score += 0.5
        
        transaction.fraud_score_complex = min(1.0, base_score + random.uniform(0, 0.2))
        
        if transaction.fraud_score_complex >= 0.8:
            transaction.risk_level_complex = "HIGH"
        elif transaction.fraud_score_complex >= 0.5:
            transaction.risk_level_complex = "MEDIUM"
        else:
            transaction.risk_level_complex = "LOW"
        
        time.sleep(random.uniform(0.5, 2.0))
        print(f"[{transaction.transaction_id}] Phase 2 (Cloud): Result - Score:{transaction.fraud_score_complex:.2f}, Risk:{transaction.risk_level_complex}")

def process_transaction(transaction: Transaction, client_model: LightweightClientModel, cloud_model: ComplexCloudModel):
    print(f"\n--- Processing {transaction.transaction_id} ---")
    
    is_suspicious = client_model.predict(transaction)
    
    if is_suspicious or transaction.amount > 2000:
        print(f"[{transaction.transaction_id}] Triggering Phase 2.")
        cloud_model.predict(transaction)
    else:
        print(f"[{transaction.transaction_id}] Phase 2 skipped.")
        transaction.risk_level_complex = "VERY_LOW"

    print(f"Final status: {transaction}")

if __name__ == "__main__":
    client_model = LightweightClientModel()
    cloud_model = ComplexCloudModel()

    transactions = [
        Transaction("user1", 150.00, "USA", "TXN001"),
        Transaction("user2", 1200.00, "CANADA", "TXN002"),
        Transaction("user3", 50.00, "UK", "TXN003"),
        Transaction("user4", 7500.00, "UNUSUAL_IP_COUNTRY", "TXN004"),
        Transaction("user5", 300.00, "USA", "TXN005"),
        Transaction("user6", 2500.00, "GERMANY", "TXN006"),
    ]

    for txn in transactions:
        process_transaction(txn, client_model, cloud_model)
