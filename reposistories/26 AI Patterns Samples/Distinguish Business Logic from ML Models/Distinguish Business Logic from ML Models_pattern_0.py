import random
import time

class FraudDetectionModel:
    def __init__(self):
        self._model_loaded = True

    def predict(self, transaction_features: dict) -> float:
        if not self._model_loaded:
            raise RuntimeError("ML model not loaded.")
        
        time.sleep(0.05) 
        
        amount = transaction_features.get("amount", 0)
        num_items = transaction_features.get("num_items", 0)
        user_history_score = transaction_features.get("user_history_score", 0.5)
        
        risk_score = 0.1
        if amount > 1000:
            risk_score += 0.3
        if num_items > 50:
            risk_score += 0.2
        if user_history_score < 0.3:
            risk_score += 0.4
            
        risk_score += random.uniform(-0.05, 0.05)
        return min(max(risk_score, 0.0), 1.0)

class OrderDataStore:
    def get_user_transaction_history(self, user_id: str) -> dict:
        time.sleep(0.02)
        return {
            "total_transactions_last_30_days": random.randint(5, 50),
            "avg_transaction_value_last_30_days": random.uniform(20, 200),
            "user_history_score": random.uniform(0.1, 0.9)
        }

    def get_product_details(self, product_id: str) -> dict:
        time.sleep(0.01)
        return {"name": f"Product_{product_id}", "price": random.uniform(10, 500)}

class OrderProcessingService:
    def __init__(self, fraud_model: FraudDetectionModel, data_store: OrderDataStore):
        self.fraud_model = fraud_model
        self.data_store = data_store
        self.FRAUD_THRESHOLD = 0.7

    def process_order(self, order_details: dict) -> dict:
        user_id = order_details.get("user_id")
        amount = order_details.get("amount")
        num_items = order_details.get("num_items")

        user_history = self.data_store.get_user_transaction_history(user_id)
        
        ml_features = {
            "amount": amount,
            "num_items": num_items,
            "user_history_score": user_history.get("user_history_score", 0.5)
        }

        fraud_risk_score = self.fraud_model.predict(ml_features)

        order_status = "PENDING"
        processing_message = "Order received."

        if fraud_risk_score >= self.FRAUD_THRESHOLD:
            order_status = "FLAGGED_FOR_REVIEW"
            processing_message = f"High fraud risk ({fraud_risk_score:.2f}). Order flagged for manual review."
        elif amount > 5000 and user_history.get("total_transactions_last_30_days", 0) < 3:
            order_status = "FLAGGED_FOR_REVIEW"
            processing_message = "Large order from new user. Order flagged for manual review."
        else:
            order_status = "APPROVED"
            processing_message = "Order successfully processed."

        return {
            "order_id": f"ORD_{random.randint(10000, 99999)}",
            "user_id": user_id,
            "amount": amount,
            "status": order_status,
            "message": processing_message,
            "fraud_risk_score": fraud_risk_score
        }

def main_ecommerce_app():
    fraud_model = FraudDetectionModel()
    data_store = OrderDataStore()
    order_service = OrderProcessingService(fraud_model, data_store)

    orders_to_process = [
        {"user_id": "user_A", "amount": 150.0, "num_items": 2, "product_ids": ["P101"]},
        {"user_id": "user_B", "amount": 1200.0, "num_items": 5, "product_ids": ["P202", "P203"]},
        {"user_id": "user_C", "amount": 7500.0, "num_items": 1, "product_ids": ["P303"]},
        {"user_id": "user_D", "amount": 500.0, "num_items": 100, "product_ids": ["P401", "P402"]},
        {"user_id": "user_E", "amount": 250.0, "num_items": 3, "product_ids": ["P505"]}
    ]

    for order_request in orders_to_process:
        result = order_service.process_order(order_request)
        time.sleep(0.1)

if __name__ == '__main__':
    main_ecommerce_app()