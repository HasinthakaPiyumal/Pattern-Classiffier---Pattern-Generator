import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def tool_validate_transaction(transaction_data):
    transaction_id = transaction_data['id']
    account_id = transaction_data['account_id']
    amount = transaction_data['amount']
    print(f"[{time.time():.2f}] Validating transaction {transaction_id} for account {account_id} (Amount: ${amount:.2f})...")
    time.sleep(random.uniform(0.2, 0.8))
    if amount <= 0 or amount > 100000:
        print(f"[{time.time():.2f}] Transaction {transaction_id} validation FAILED: Invalid amount.")
        return False
    print(f"[{time.time():.2f}] Transaction {transaction_id} validated.")
    return True

def tool_check_fraud(transaction_id, amount, account_id):
    print(f"[{time.time():.2f}] Checking fraud for transaction {transaction_id}...")
    time.sleep(random.uniform(1.0, 2.5))
    if random.random() < 0.08:
        print(f"[{time.time():.2f}] Fraud ALERT for transaction {transaction_id}! Requires review.")
        return False
    print(f"[{time.time():.2f}] Fraud check PASSED for transaction {transaction_id}.")
    return True

def tool_update_account_balance(account_id, amount, transaction_type):
    print(f"[{time.time():.2f}] Updating balance for account {account_id} (Type: {transaction_type}, Amount: ${amount:.2f})...")
    time.sleep(random.uniform(0.5, 1.5))
    if random.random() < 0.02:
        print(f"[{time.time():.2f}] Balance update FAILED for account {account_id}.")
        return False
    print(f"[{time.time():.2f}] Balance updated for account {account_id}.")
    return True

def tool_log_transaction(transaction_id, details):
    print(f"[{time.time():.2f}] Logging transaction {transaction_id} to history...")
    time.sleep(random.uniform(0.3, 1.0))
    print(f"[{time.time():.2f}] Transaction {transaction_id} logged.")
    return True

def tool_send_user_notification(account_id, transaction_id, amount):
    print(f"[{time.time():.2f}] Sending notification for transaction {transaction_id} to account {account_id}...")
    time.sleep(random.uniform(0.4, 1.2))
    print(f"[{time.time():.2f}] Notification sent for transaction {transaction_id}.")
    return True

def process_financial_transaction(transaction_details):
    transaction_id = transaction_details['id']
    account_id = transaction_details['account_id']
    amount = transaction_details['amount']
    transaction_type = transaction_details['type']

    print(f"\n[{time.time():.2f}] Starting processing for Transaction {transaction_id}...")

    is_valid = tool_validate_transaction(transaction_details)
    if not is_valid:
        print(f"[{time.time():.2f}] Transaction {transaction_id} processing halted due to validation failure.")
        return False

    print(f"[{time.time():.2f}] Transaction validated. Initiating parallel tasks for Transaction {transaction_id}...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(tool_check_fraud, transaction_id, amount, account_id): "Fraud Check",
            executor.submit(tool_update_account_balance, account_id, amount, transaction_type): "Account Balance Update",
            executor.submit(tool_log_transaction, transaction_id, transaction_details): "Transaction Logging",
            executor.submit(tool_send_user_notification, account_id, transaction_id, amount): "User Notification"
        }

        results = {}
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result = future.result()
                results[task_name] = "SUCCESS" if result else "FAILURE"
            except Exception as exc:
                results[task_name] = f"ERROR: {exc}"
            print(f"[{time.time():.2f}] Task '{task_name}' completed with result: {results[task_name]}")

    overall_success = all(res == "SUCCESS" for task_name, res in results.items() if task_name != "Fraud Check")
    print(f"[{time.time():.2f}] All parallel tasks for Transaction {transaction_id} completed. Overall success (excluding fraud flag): {overall_success}")
    if results.get("Fraud Check") == "FAILURE":
        print(f"[{time.time():.2f}] Transaction {transaction_id} flagged for fraud review.")
    return overall_success

if __name__ == "__main__":
    transaction_1 = {
        'id': 'TXN-1001',
        'account_id': 'ACC-001',
        'amount': 500.00,
        'type': 'debit',
        'description': 'Online Purchase'
    }
    transaction_2 = {
        'id': 'TXN-1002',
        'account_id': 'ACC-002',
        'amount': 150000.00,
        'type': 'credit',
        'description': 'Salary Deposit'
    }
    transaction_3 = {
        'id': 'TXN-1003',
        'account_id': 'ACC-003',
        'amount': 75.00,
        'type': 'debit',
        'description': 'Coffee Shop'
    }

    process_financial_transaction(transaction_1)
    print("-" * 50)
    process_financial_transaction(transaction_2)
    print("-" * 50)
    process_financial_transaction(transaction_3)