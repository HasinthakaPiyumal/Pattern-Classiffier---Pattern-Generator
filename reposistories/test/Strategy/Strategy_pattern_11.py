class OperationStrategy:
    def execute(self, a, b):
        raise NotImplementedError
class AddStrategy(OperationStrategy):
    def execute(self, a, b):
        return a + b
class SubtractStrategy(OperationStrategy):
    def execute(self, a, b):
        return a - b
class MultiplyStrategy(OperationStrategy):
    def execute(self, a, b):
        return a * b
class Calculator:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def calculate(self, a, b):
        return self._strategy.execute(a, b)
calculator = Calculator(AddStrategy())
print(f"10 + 5 = {calculator.calculate(10, 5)}")
calculator.set_strategy(SubtractStrategy())
print(f"10 - 5 = {calculator.calculate(10, 5)}")
calculator.set_strategy(MultiplyStrategy())
print(f"10 * 5 = {calculator.calculate(10, 5)}")