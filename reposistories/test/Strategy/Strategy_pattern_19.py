class DiscountStrategy:
    def calculate_discount(self, price):
        raise NotImplementedError
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage
    def calculate_discount(self, price):
        return price * (self.percentage / 100)
class FixedDiscount(DiscountStrategy):
    def __init__(self, amount):
        self.amount = amount
    def calculate_discount(self, price):
        return min(self.amount, price)
class NoDiscount(DiscountStrategy):
    def calculate_discount(self, price):
        return 0
class ShoppingCart:
    def __init__(self, discount_strategy):
        self._discount_strategy = discount_strategy
    def set_discount_strategy(self, strategy):
        self._discount_strategy = strategy
    def get_final_price(self, original_price):
        discount = self._discount_strategy.calculate_discount(original_price)
        return original_price - discount
cart = ShoppingCart(PercentageDiscount(10))
print(f"Price $100 with 10% off: ${cart.get_final_price(100):.2f}")
cart.set_discount_strategy(FixedDiscount(20))
print(f"Price $100 with $20 off: ${cart.get_final_price(100):.2f}")
cart.set_discount_strategy(NoDiscount())
print(f"Price $100 with no discount: ${cart.get_final_price(100):.2f}")