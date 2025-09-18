import random

class TransactionProposer:
    def __init__(self, account_id):
        self.account_id = account_id

    def propose_transaction(self, recipient_id, amount, transaction_type="transfer"):
        return {
            "sender_account": self.account_id,
            "recipient_account": recipient_id,
            "amount": amount,
            "type": transaction_type
        }

class FraudDetectionSystem:
    def __init__(self, high_risk_threshold=10000.0, suspicious_recipients=None):
        self.high_risk_threshold = high_risk_threshold
        self.suspicious_recipients = suspicious_recipients if suspicious_recipients is not None else {"risky_corp_inc", "offshore_fund_ltd"}

    def evaluate_transaction(self, transaction):
        sender = transaction["sender_account"]
        recipient = transaction["recipient_account"]
        amount = transaction["amount"]
        trans_type = transaction["type"]

        if amount > self.high_risk_threshold:
            return False, f"High-risk transaction: Amount ${amount:.2f} exceeds threshold of ${self.high_risk_threshold:.2f}."
        if recipient in self.suspicious_recipients:
            return False, f"Suspicious recipient: '{recipient}' is on the watch list."
        if trans_type == "withdrawal" and amount > 5000:
            return False, f"Large withdrawal: ${amount:.2f} for withdrawal type."

        return True, "Transaction appears legitimate."

if __name__ == "__main__":
    user_account = "ACC12345"
    proposer = TransactionProposer(user_account)
    fraud_checker = FraudDetectionSystem()

    tx1 = proposer.propose_transaction("REC67890", 500.00)
    print(f"Proposing transaction: {tx1}")
    is_valid, reason = fraud_checker.evaluate_transaction(tx1)
    print(f"FraudDetectionSystem: Status: {'VALID' if is_valid else 'REJECTED'} - {reason}\n")

    tx2 = proposer.propose_transaction("REC11223", 15000.00)
    print(f"Proposing transaction: {tx2}")
    is_valid, reason = fraud_checker.evaluate_transaction(tx2)
    print(f"FraudDetectionSystem: Status: {'VALID' if is_valid else 'REJECTED'} - {reason}\n")

    tx3 = proposer.propose_transaction("risky_corp_inc", 2000.00)
    print(f"Proposing transaction: {tx3}")
    is_valid, reason = fraud_checker.evaluate_transaction(tx3)
    print(f"FraudDetectionSystem: Status: {'VALID' if is_valid else 'REJECTED'} - {reason}\n")

    tx4 = proposer.propose_transaction("CASH_OUTLET", 6000.00, transaction_type="withdrawal")
    print(f"Proposing transaction: {tx4}")
    is_valid, reason = fraud_checker.evaluate_transaction(tx4)
    print(f"FraudDetectionSystem: Status: {'VALID' if is_valid else 'REJECTED'} - {reason}\n")