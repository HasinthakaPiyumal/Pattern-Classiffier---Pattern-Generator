import time
import concurrent.futures

def perform_fraud_check(transaction_id: str, amount: float, account_id: str) -> dict:
    time.sleep(1.7) # Simulate complex AI/ML fraud detection model
    # print(f"  Performing fraud check for Tx {transaction_id}...")
    if amount > 5000 and account_id == "ACC789": # Simple rule for simulation
        return {"task": "fraud_check", "success": False, "flagged": True, "message": "High-risk transaction flagged for manual review"}
    return {"task": "fraud_check", "success": True, "flagged": False, "message": "No fraud detected"}

def check_regulatory_compliance(transaction_id: str, country_code: str, amount: float) -> dict:
    time.sleep(1.3) # Simulate checking against KYC/AML rules
    # print(f"  Checking regulatory compliance for Tx {transaction_id}...")
    if country_code == "IR" and amount > 1000: # Example sanction rule
        return {"task": "compliance_check", "success": False, "flagged": True, "message": "Compliance violation: Sanctioned country transaction"}
    return {"task": "compliance_check", "success": True, "flagged": False, "message": "Compliance OK"}

def update_customer_credit_score(account_id: str, transaction_impact: float) -> dict:
    time.sleep(1.0) # Simulate credit scoring model update
    # print(f"  Updating credit score for account {account_id}...")
    # In a real system, this would involve a more complex calculation
    return {"task": "credit_score_update", "success": True, "message": f"Credit score updated for {account_id}"}

def log_transaction_to_ledger(transaction_id: str, details: dict, status: str) -> dict:
    time.sleep(0.5) # Simulate database write for ledger
    # print(f"  Logging Tx {transaction_id} to ledger with status '{status}'...")
    return {"task": "ledger_logging", "success": True, "message": f"Transaction {transaction_id} logged as {status}"}

def process_financial_transaction(transaction_data: dict):
    print(f"\n--- Processing Transaction {transaction_data['transaction_id']} ---")
    start_time = time.perf_counter()

    tx_id = transaction_data['transaction_id']
    amount = transaction_data['amount']
    account_id = transaction_data['account_id']
    country_code = transaction_data['country_code']

    # Independent tasks: Fraud check and Regulatory compliance check
    # These are often critical and can run in parallel to minimize latency.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_fraud = executor.submit(perform_fraud_check, tx_id, amount, account_id)
        future_compliance = executor.submit(check_regulatory_compliance, tx_id, country_code, amount)

        fraud_result = future_fraud.result()
        compliance_result = future_compliance.result()

    print(f"[Parallel Step 1 Results]:")
    print(f"  - {fraud_result['message']}")
    print(f"  - {compliance_result['message']}")

    # Dependent tasks: Update credit score and Log to ledger
    # These typically proceed only if the initial checks pass, or log a specific failure status.
    final_tx_status = "FAILED"
    if fraud_result['success'] and compliance_result['success']:
        print("[Sequential Step 2: Post-Transaction Actions]")
        credit_update_result = update_customer_credit_score(account_id, amount)
        print(f"  - {credit_update_result['message']}")
        final_tx_status = "APPROVED"
    else:
        print("  Transaction halted due to fraud or compliance flags.")
        final_tx_status = "REJECTED"
    
    # Ledger logging is almost always the final step, regardless of approval/rejection
    log_result = log_transaction_to_ledger(tx_id, transaction_data, final_tx_status)
    print(f"  - {log_result['message']}")

    end_time = time.perf_counter()
    print(f"--- Transaction {tx_id} Processing {final_tx_status} in {end_time - start_time:.2f} seconds ---")

if __name__ == "__main__":
    transaction1 = {
        "transaction_id": "TXN001",
        "account_id": "ACC123",
        "amount": 150.75,
        "currency": "USD",
        "country_code": "US"
    }
    transaction2 = {
        "transaction_id": "TXN002",
        "account_id": "ACC789", # High risk account for fraud simulation
        "amount": 6000.00,
        "currency": "USD",
        "country_code": "CA"
    }
    transaction3 = {
        "transaction_id": "TXN003",
        "account_id": "ACC456",
        "amount": 1200.00,
        "currency": "EUR",
        "country_code": "IR" # Sanctioned country for compliance simulation
    }

    process_financial_transaction(transaction1)
    process_financial_transaction(transaction2)
    process_financial_transaction(transaction3)
