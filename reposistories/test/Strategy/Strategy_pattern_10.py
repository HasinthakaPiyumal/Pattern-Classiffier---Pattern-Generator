import abc

class DiscountStrategy(abc.ABC):
    @abc.abstractmethod
    def apply_discount(self, total_amount):
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage / 100

    def apply_discount(self, total_amount):
        discount_amount = total_amount * self.percentage
        final_amount = total_amount - discount_amount
        print(f"Applied {self.percentage*100:.0f}% discount. Original: {total_amount:.2f}, Discount: {discount_amount:.2f}, Final: {final_amount:.2f}")
        return final_amount

class FixedAmountDiscount(DiscountStrategy):
    def __init__(self, fixed_amount):
        self.fixed_amount = fixed_amount

    def apply_discount(self, total_amount):
        discount_amount = min(self.fixed_amount, total_amount) # Discount cannot exceed total
        final_amount = total_amount - discount_amount
        print(f"Applied fixed discount of {self.fixed_amount:.2f}. Original: {total_amount:.2f}, Discount: {discount_amount:.2f}, Final: {final_amount:.2f}")
        return final_amount

class Order:
    def __init__(self, total_amount, discount_strategy: DiscountStrategy):
        self._total_amount = total_amount
        self._discount_strategy = discount_strategy

    def set_discount_strategy(self, strategy: DiscountStrategy):
        self._discount_strategy = strategy

    def get_final_amount(self):
        return self._discount_strategy.apply_discount(self._total_amount)

if __name__ == "__main__":
    order1 = Order(100.0, PercentageDiscount(10))
    order1.get_final_amount()

    order2 = Order(250.0, FixedAmountDiscount(50))
    order2.get_final_amount()

    order3 = Order(75.0, PercentageDiscount(20))
    order3.get_final_amount()
    order3.set_discount_strategy(FixedAmountDiscount(10))
    order3.get_final_amount()