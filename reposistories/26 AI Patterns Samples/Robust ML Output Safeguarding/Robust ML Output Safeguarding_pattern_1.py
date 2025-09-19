import random

class MLFraudDetectionModel:
    """Simulates an ML model for transaction fraud detection."""
    def predict(self, transaction_data):
        # In a real scenario, this would be a complex ML inference.
        # For simulation, we'll generate a random fraud prediction and score.
        amount = transaction_data.get('amount', 100)
        location_mismatch = transaction_data.get('location_mismatch', False)
        new_device = transaction_data.get('new_device', False)

        fraud_score = random.uniform(0.01, 0.99)
        is_fraudulent_prediction = False

        if amount > 5000:
            fraud_score += random.uniform(0.1, 0.3)
        if location_mismatch:
            fraud_score += random.uniform(0.2, 0.4)
        if new_device:
            fraud_score += random.uniform(0.1, 0.2)

        fraud_score = min(max(fraud_score, 0.01), 0.99) # Keep score within bounds

        if fraud_score > 0.7: # ML's internal threshold
            is_fraudulent_prediction = True

        # Introduce some instability/vulnerability for demonstration
        if random.random() < 0.05 and amount < 100: # 5% chance of misclassifying small legit transaction as fraud
            is_fraudulent_prediction = True
            fraud_score = random.uniform(0.75, 0.85)
        elif random.random() < 0.05 and amount > 50000: # 5% chance of missing large fraud
            is_fraudulent_prediction = False
            fraud_score = random.uniform(0.1, 0.3)

        return is_fraudulent_prediction, fraud_score

class FraudDetectionSafeguard:
    """Encapsulates the ML model with deterministic rule-based safeguards for fraud detection."""
    KNOWN_FRAUD_ACCOUNTS = {"fraudster_acc_123", "scammer_wallet_XYZ"}
    HIGH_VALUE_THRESHOLD = 5000
    CRITICAL_VALUE_THRESHOLD = 20000

    def __init__(self, ml_model):
        self.ml_model = ml_model
        # Could also include a secondary, simpler rule-based model here for redundancy
        # self.secondary_rule_engine = SimpleFraudRules()

    def _apply_deterministic_rules(self, ml_prediction, ml_score, transaction_data):
        final_decision = "Allow Transaction"
        action = "ML Recommendation"
        risk_level = "Low"

        # Rule 1: Known fraudulent accounts override ML
        if transaction_data.get('recipient_account') in self.KNOWN_FRAUD_ACCOUNTS:
            final_decision = "Block Transaction"
            action = "Deterministic Override: Known Fraud Account"
            risk_level = "Critical"
            return final_decision, action, risk_level

        # Rule 2: Critical transaction value always requires human review, regardless of ML score
        if transaction_data.get('amount', 0) > self.CRITICAL_VALUE_THRESHOLD:
            final_decision = "Hold for Manual Review"
            action = "Deterministic Override: Critical Transaction Value"
            risk_level = "High"
            return final_decision, action, risk_level

        # Rule 3: High ML fraud score
        if ml_prediction and ml_score >= 0.95:
            final_decision = "Block Transaction"
            action = "ML High Confidence Fraud"
            risk_level = "High"
        elif ml_prediction and ml_score >= 0.8:
            final_decision = "Review & Potentially Block"
            action = "ML Moderate Confidence Fraud, requires human check"
            risk_level = "Moderate"
        elif ml_prediction and ml_score < 0.8: # ML predicted fraud but with low confidence
            final_decision = "Hold for Manual Review"
            action = "ML Low Confidence Fraud, human review needed"
            risk_level = "Moderate"
        else: # ML predicted not fraudulent
            if ml_score > 0.6: # Still some suspicious activity according to ML, but not enough to flag as fraud
                final_decision = "Allow Transaction (Monitor)"
                action = "ML Low Risk, but monitor"
                risk_level = "Low-Moderate"

        # Rule 4: High value transaction with any suspicious indicator
        if transaction_data.get('amount', 0) > self.HIGH_VALUE_THRESHOLD and \
           (transaction_data.get('location_mismatch') or transaction_data.get('new_device')):
            if final_decision == "Allow Transaction" or final_decision == "Allow Transaction (Monitor)":
                final_decision = "Hold for Manual Review"
                action = "Escalate: High Value & Suspicious Indicators"
                risk_level = "High"

        # Rule 5: Low ML confidence on a high-value transaction
        if ml_score < 0.5 and transaction_data.get('amount', 0) > self.HIGH_VALUE_THRESHOLD:
            final_decision = "Hold for Manual Review"
            action = "Escalate: High Value with Low ML Confidence"
            risk_level = "High"

        return final_decision, action, risk_level

    def get_safe_transaction_decision(self, transaction_data):
        ml_is_fraud, ml_fraud_score = self.ml_model.predict(transaction_data)
        final_decision, action, risk_level = self._apply_deterministic_rules(ml_is_fraud, ml_fraud_score, transaction_data)

        # Real-world usage simulation
        print(f"--- Transaction ID: {transaction_data.get('id', 'N/A')} ---")
        print(f"Transaction Amount: ${transaction_data.get('amount', 0):.2f}")
        print(f"ML Predicted Fraud: {ml_is_fraud} (Score: {ml_fraud_score:.2f})")
        print(f"Safeguard Decision: {final_decision}")
        print(f"Action Taken: {action}")
        print(f"Overall Risk Level: {risk_level}\n")
        return final_decision, action, risk_level

# Real-world usage simulation
if __name__ == "__main__":
    ml_model = MLFraudDetectionModel()
    safeguarded_system = FraudDetectionSafeguard(ml_model)

    # Scenario 1: ML says not fraud, but known fraud account
    transaction1 = {"id": "T001", "amount": 150, "recipient_account": "fraudster_acc_123", "location_mismatch": False, "new_device": False}
    safeguarded_system.get_safe_transaction_decision(transaction1)

    # Scenario 2: High value, critical threshold (should always be reviewed)
    transaction2 = {"id": "T002", "amount": 25000, "recipient_account": "legit_bank", "location_mismatch": False, "new_device": False}
    safeguarded_system.get_safe_transaction_decision(transaction2)

    # Scenario 3: ML high confidence fraud
    transaction3 = {"id": "T003", "amount": 7000, "recipient_account": "random_user", "location_mismatch": True, "new_device": True}
    safeguarded_system.get_safe_transaction_decision(transaction3)

    # Scenario 4: ML low confidence, but high value with suspicious indicators (escalated)
    transaction4 = {"id": "T004", "amount": 6000, "recipient_account": "another_user", "location_mismatch": True, "new_device": False}
    safeguarded_system.get_safe_transaction_decision(transaction4)

    # Scenario 5: ML low risk, allow (monitor)
    transaction5 = {"id": "T005", "amount": 500, "recipient_account": "merchant_A", "location_mismatch": False, "new_device": False}
    safeguarded_system.get_safe_transaction_decision(transaction5)

    # Scenario 6: ML instability (missed large fraud) caught by safeguards
    print("--- Testing ML instability catch (missing large fraud) ---")
    for _ in range(3): # Run a few times to potentially hit the random misclassification
        transaction_instability = {"id": "T_INST", "amount": 60000, "recipient_account": "unknown_user", "location_mismatch": True, "new_device": True}
        safeguarded_system.get_safe_transaction_decision(transaction_instability)

    # Scenario 7: ML instability (false positive on small transaction) caught by safeguards (or mitigated)
    print("--- Testing ML instability catch (false positive) ---")
    for _ in range(3): # Run a few times to potentially hit the random misclassification
        transaction_instability_fp = {"id": "T_INST_FP", "amount": 50, "recipient_account": "legit_shop", "location_mismatch": False, "new_device": False}
        safeguarded_system.get_safe_transaction_decision(transaction_instability_fp)
