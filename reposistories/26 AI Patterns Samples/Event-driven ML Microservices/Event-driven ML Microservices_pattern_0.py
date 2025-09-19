import uuid
import time
import random

class Event:
    def __init__(self, type, payload):
        self.type = type
        self.payload = payload
        self.timestamp = time.time()
        self.id = str(uuid.uuid4())

class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event):
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                callback(event)

class TransactionIngestionService:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def ingest_transaction(self, transaction_data):
        print(f"Ingestion: Receiving transaction {transaction_data['transaction_id']}")
        event = Event("NewTransactionEvent", transaction_data)
        self.event_bus.publish(event)

class FeatureExtractionService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        event_bus.subscribe("NewTransactionEvent", self.extract_features)

    def extract_features(self, event):
        transaction = event.payload
        transaction_id = transaction['transaction_id']
        amount = transaction['amount']
        user_id = transaction['user_id']
        is_high_value = amount > 1000
        is_first_purchase = random.choice([True, False])
        features = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "amount": amount,
            "is_high_value": is_high_value,
            "transaction_velocity": random.randint(1, 10),
            "device_change": random.choice([True, False])
        }
        print(f"FeatureExtraction: Extracted features for {transaction_id}")
        self.event_bus.publish(Event("FeaturesExtractedEvent", features))

class FraudPredictionService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        event_bus.subscribe("FeaturesExtractedEvent", self.predict_fraud)

    def predict_fraud(self, event):
        features = event.payload
        transaction_id = features['transaction_id']
        fraud_score = 0
        if features['is_high_value']:
            fraud_score += 0.4
        if features['transaction_velocity'] > 7:
            fraud_score += 0.3
        if features['device_change']:
            fraud_score += 0.2
        
        is_fraud = fraud_score > 0.5

        prediction_result = {
            "transaction_id": transaction_id,
            "user_id": features['user_id'],
            "is_fraud": is_fraud,
            "fraud_score": round(fraud_score, 2)
        }
        print(f"FraudPrediction: Predicted fraud for {transaction_id}: {is_fraud} (Score: {prediction_result['fraud_score']})")
        self.event_bus.publish(Event("FraudPredictionEvent", prediction_result))

class AlertingService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        event_bus.subscribe("FraudPredictionEvent", self.send_alert)

    def send_alert(self, event):
        prediction = event.payload
        transaction_id = prediction['transaction_id']
        if prediction['is_fraud']:
            print(f"Alerting: !!! FRAUD ALERT for transaction {transaction_id} (User: {prediction['user_id']}) with score {prediction['fraud_score']} !!!")
        else:
            print(f"Alerting: Transaction {transaction_id} is clean.")

event_bus = EventBus()

ingestion_service = TransactionIngestionService(event_bus)
feature_extraction_service = FeatureExtractionService(event_bus)
fraud_prediction_service = FraudPredictionService(event_bus)
alerting_service = AlertingService(event_bus)

print("--- Simulating E-commerce Fraud Detection Pipeline ---")
transactions_to_simulate = [
    {"transaction_id": "TXN001", "user_id": "userA", "amount": 50, "location": "NY"},
    {"transaction_id": "TXN002", "user_id": "userB", "amount": 1200, "location": "CA"},
    {"transaction_id": "TXN003", "user_id": "userA", "amount": 75, "location": "NY"},
    {"transaction_id": "TXN004", "user_id": "userC", "amount": 2500, "location": "FL"},
    {"transaction_id": "TXN005", "user_id": "userB", "amount": 80, "location": "CA"},
]

for i, transaction in enumerate(transactions_to_simulate):
    print(f"\n--- Processing Transaction {i+1} ---")
    ingestion_service.ingest_transaction(transaction)
    time.sleep(0.1)
print("\n--- Simulation Complete ---")