import time
import concurrent.futures

def validate_account_balance(account_id, amount):
    time.sleep(1.0)
    if amount < 10000:
        return True, f"Account {account_id}: Balance sufficient for ${amount:.2f}."
    else:
        time.sleep(1.5)
        return False, f"Account {account_id}: Balance insufficient or requires manual review for ${amount:.2f}."

def perform_fraud_check(transaction_id, amount, sender_id, recipient_id):
    time.sleep(2.5)
    if amount > 50000:
        return False, f"Transaction {transaction_id}: High-value fraud alert for ${amount:.2f}."
    return True, f"Transaction {transaction_id}: Fraud check passed."

def update_sender_account(account_id, amount):
    time.sleep(2.0)
    return f"Sender {account_id}: Debited ${amount:.2f}."

def update_recipient_account(account_id, amount):
    time.sleep(2.0)
    return f"Recipient {account_id}: Credited ${amount:.2f}."

def notify_compliance(transaction_id, amount):
    time.sleep(1.2)
    if amount > 10000:
        return f"Transaction {transaction_id}: Compliance notified for large transfer of ${amount:.2f}."
    return f"Transaction {transaction_id}: No compliance notification needed."

def generate_transaction_receipt(transaction_id, sender_update_status, recipient_update_status):
    time.sleep(0.8)
    if "Debited" in sender_update_status and "Credited" in recipient_update_status:
        return f"Transaction {transaction_id}: Receipt generated successfully."
    return f"Transaction {transaction_id}: Receipt generation failed due to account update issues."

def process_financial_transaction(transaction_data):
    transaction_id = transaction_data["transaction_id"]
    sender_account = transaction_data["sender_account"]
    recipient_account = transaction_data["recipient_account"]
    amount = transaction_data["amount"]

    print(f"--- Starting processing for Transaction {transaction_id} ---")

    balance_ok, balance_msg = validate_account_balance(sender_account, amount)
    print(balance_msg)
    if not balance_ok:
        print(f"Transaction {transaction_id}: Aborting due to insufficient balance or review required.")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_fraud = executor.submit(perform_fraud_check, transaction_id, amount, sender_account, recipient_account)
        future_sender_update = executor.submit(update_sender_account, sender_account, amount)
        future_recipient_update = executor.submit(update_recipient_account, recipient_account, amount)
        future_compliance = executor.submit(notify_compliance, transaction_id, amount)

        fraud_ok, fraud_msg = future_fraud.result()
        print(fraud_msg)
        if not fraud_ok:
            print(f"Transaction {transaction_id}: Aborting due to fraud alert.")
            return

        sender_update_status = future_sender_update.result()
        print(sender_update_status)

        recipient_update_status = future_recipient_update.result()
        print(recipient_update_status)

        compliance_notification = future_compliance.result()
        print(compliance_notification)

    receipt_status = generate_transaction_receipt(transaction_id, sender_update_status, recipient_update_status)
    print(receipt_status)

    print(f"--- Finished processing for Transaction {transaction_id} ---")

if __name__ == "__main__":
    transaction_1 = {
        "transaction_id": "TXN123456",
        "sender_account": "ACC001",
        "recipient_account": "ACC002",
        "amount": 7500.00
    }
    process_financial_transaction(transaction_1)

    print("\n" + "="*50 + "\n")

    transaction_2 = {
        "transaction_id": "TXN789012",
        "sender_account": "ACC003",
        "recipient_account": "ACC004",
        "amount": 60000.00
    }
    process_financial_transaction(transaction_2)