class PaymentGateway:
    def pay(self, amount):
        raise NotImplementedError

class CreditCardGateway(PaymentGateway):
    def pay(self, amount):
        return f"Processing credit card payment of ${amount}."

class PayPalGateway(PaymentGateway):
    def pay(self, amount):
        return f"Processing PayPal payment of ${amount}."

class BankTransferGateway(PaymentGateway):
    def pay(self, amount):
        return f"Processing bank transfer payment of ${amount}."

class PaymentGatewayFactory:
    @staticmethod
    def get_gateway(gateway_type):
        if gateway_type == "creditcard":
            return CreditCardGateway()
        elif gateway_type == "paypal":
            return PayPalGateway()
        elif gateway_type == "banktransfer":
            return BankTransferGateway()
        else:
            raise ValueError("Invalid gateway type")

if __name__ == "__main__":
    cc_gateway = PaymentGatewayFactory.get_gateway("creditcard")
    print(cc_gateway.pay(100.00))
    pp_gateway = PaymentGatewayFactory.get_gateway("paypal")
    print(pp_gateway.pay(50.50))
    bt_gateway = PaymentGatewayFactory.get_gateway("banktransfer")
    print(bt_gateway.pay(200.00))
    try:
        crypto_gateway = PaymentGatewayFactory.get_gateway("crypto")
        print(crypto_gateway.pay(10.00))
    except ValueError as e:
        print(e)