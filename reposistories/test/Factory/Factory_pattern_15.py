import abc

class PaymentGateway(abc.ABC):
    @abc.abstractmethod
    def process_payment(self, amount: float):
        pass

class CreditCardGateway(PaymentGateway):
    def process_payment(self, amount: float):
        return f"Processing credit card payment of ${amount:.2f}"

class PayPalGateway(PaymentGateway):
    def process_payment(self, amount: float):
        return f"Processing PayPal payment of ${amount:.2f}"

class PaymentGatewayFactory:
    @staticmethod
    def create_gateway(gateway_type: str) -> PaymentGateway:
        if gateway_type == "creditcard":
            return CreditCardGateway()
        elif gateway_type == "paypal":
            return PayPalGateway()
        else:
            raise ValueError("Invalid gateway type")

if __name__ == "__main__":
    cc_gateway = PaymentGatewayFactory.create_gateway("creditcard")
    print(cc_gateway.process_payment(100.50))
    paypal_gateway = PaymentGatewayFactory.create_gateway("paypal")
    print(paypal_gateway.process_payment(25.99))