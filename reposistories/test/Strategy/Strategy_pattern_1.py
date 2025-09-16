import abc

class PaymentStrategy(abc.ABC):
    @abc.abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number):
        self.card_number = card_number
    def pay(self, amount):
        print(f"Paying {amount:.2f} using Credit Card {self.card_number[-4:]}")

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email
    def pay(self, amount):
        print(f"Paying {amount:.2f} using PayPal account {self.email}")

class ShoppingCart:
    def __init__(self, payment_strategy: PaymentStrategy):
        self._payment_strategy = payment_strategy
        self.items = []

    def add_item(self, item_price):
        self.items.append(item_price)

    def calculate_total(self):
        return sum(self.items)

    def checkout(self):
        total = self.calculate_total()
        self._payment_strategy.pay(total)

if __name__ == "__main__":
    cart1 = ShoppingCart(CreditCardPayment("1234-5678-9012-3456"))
    cart1.add_item(1200)
    cart1.add_item(25)
    cart1.checkout()

    cart2 = ShoppingCart(PayPalPayment("user@example.com"))
    cart2.add_item(30)
    cart2.checkout()