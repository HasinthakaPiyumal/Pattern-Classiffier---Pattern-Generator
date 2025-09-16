class ShippingStrategy:
    def calculate_cost(self, weight):
        raise NotImplementedError
class StandardShipping(ShippingStrategy):
    def calculate_cost(self, weight):
        return 5.0 + weight * 1.5
class ExpressShipping(ShippingStrategy):
    def calculate_cost(self, weight):
        return 15.0 + weight * 2.5
class InternationalShipping(ShippingStrategy):
    def calculate_cost(self, weight):
        return 25.0 + weight * 3.0
class ShippingCalculator:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def get_shipping_cost(self, weight):
        return self._strategy.calculate_cost(weight)
calculator = ShippingCalculator(StandardShipping())
print(f"Standard shipping for 2kg: ${calculator.get_shipping_cost(2):.2f}")
calculator.set_strategy(ExpressShipping())
print(f"Express shipping for 2kg: ${calculator.get_shipping_cost(2):.2f}")
calculator.set_strategy(InternationalShipping())
print(f"International shipping for 2kg: ${calculator.get_shipping_cost(2):.2f}")