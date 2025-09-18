import abc

class PaymentStrategy(abc.ABC):
    @abc.abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number, cvv, expiry_date):
        self._card_number = card_number
        self._cvv = cvv
        self._expiry_date = expiry_date

    def pay(self, amount):
        print(f"Paying ${amount:.2f} using Credit Card {self._card_number[-4:]} (exp: {self._expiry_date})")
        print("Credit card payment processed successfully.")
        return True

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self._email = email

    def pay(self, amount):
        print(f"Paying ${amount:.2f} using PayPal account: {self._email}")
        print("PayPal payment processed successfully.")
        return True

class BitcoinPayment(PaymentStrategy):
    def __init__(self, wallet_address):
        self._wallet_address = wallet_address

    def pay(self, amount):
        print(f"Paying ${amount:.2f} using Bitcoin to wallet: {self._wallet_address[:8]}...")
        print("Bitcoin payment initiated. Waiting for confirmations.")
        return True

class ShoppingCart:
    def __init__(self):
        self._items = []
        self._payment_strategy = None

    def add_item(self, name, price):
        self._items.append({"name": name, "price": price})

    def calculate_total(self):
        return sum(item["price"] for item in self._items)

    def set_payment_strategy(self, strategy):
        if not isinstance(strategy, PaymentStrategy):
            raise ValueError("Provided strategy is not a valid PaymentStrategy.")
        self._payment_strategy = strategy

    def checkout(self):
        if not self._payment_strategy:
            raise RuntimeError("Payment strategy not set.")
        total_amount = self.calculate_total()
        print(f"\n--- Checking out order with total: ${total_amount:.2f} ---")
        if self._payment_strategy.pay(total_amount):
            print("Order successfully placed!")
        else:
            print("Order placement failed.")

if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item("Laptop", 1200.00)
    cart.add_item("Mouse", 25.00)
    cart.add_item("Keyboard", 75.00)

    credit_card_strat = CreditCardPayment("1234-5678-9012-3456", "123", "12/25")
    cart.set_payment_strategy(credit_card_strat)
    cart.checkout()

    paypal_strat = PayPalPayment("john.doe@example.com")
    cart.set_payment_strategy(paypal_strat)
    cart.checkout()

    bitcoin_strat = BitcoinPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    cart.set_payment_strategy(bitcoin_strat)
    cart.checkout()