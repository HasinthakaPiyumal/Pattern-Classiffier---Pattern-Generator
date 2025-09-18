class _PaymentGateway:
    def __init__(self, api_endpoint="https://api.paymentgateway.com/v1"):
        self.api_endpoint = api_endpoint
        self.api_key = "sk_test_12345"

    def process_payment(self, amount, currency, card_details):
        if card_details.startswith("4"): 
            return {"status": "success", "transaction_id": f"txn_{hash(card_details)}"}
        return {"status": "failed", "error": "Invalid card details"}

    def refund_payment(self, transaction_id, amount):
        return {"status": "success", "refund_id": f"ref_{hash(transaction_id)}"}

payment_gateway_instance = _PaymentGateway()

if __name__ == "__main__":
    pg1 = payment_gateway_instance
    pg2 = payment_gateway_instance

    print(f"Are pg1 and pg2 the same instance? {pg1 is pg2}")
    print(f"PG1 Endpoint: {pg1.api_endpoint}")

    result1 = pg1.process_payment(100.00, "USD", "4111222233334444")
    result2 = pg2.process_payment(50.00, "EUR", "5555666677778888")

    print(f"Payment 1 result: {result1}")
    print(f"Payment 2 result: {result2}")

    refund_result = pg1.refund_payment(result1["transaction_id"], 100.00)
    print(f"Refund result: {refund_result}")