class PaymentProcessor:
    def process_payment(self, amount: float) -> str:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via Credit Card. Transaction complete."

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via PayPal. Funds transferred."

class BankTransferProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via Bank Transfer. Awaiting confirmation."

class PaymentProcessorFactory:
    def get_processor(self, method: str) -> PaymentProcessor:
        if method == "credit_card":
            return CreditCardProcessor()
        elif method == "paypal":
            return PayPalProcessor()
        elif method == "bank_transfer":
            return BankTransferProcessor()
        else:
            raise ValueError(f"Unsupported payment method: {method}")

factory = PaymentProcessorFactory()

cc_processor = factory.get_processor("credit_card")
pp_processor = factory.get_processor("paypal")
bt_processor = factory.get_processor("bank_transfer")

print(cc_processor.process_payment(150.75))
print(pp_processor.process_payment(49.99))
print(bt_processor.process_payment(1200.00))

try:
    crypto_processor = factory.get_processor("cryptocurrency")
except ValueError as e:
    print(e)