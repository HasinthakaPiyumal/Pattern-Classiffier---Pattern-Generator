import abc

class TaxStrategy(abc.ABC):
    @abc.abstractmethod
    def calculate_tax(self, income):
        pass

class USTaxStrategy(TaxStrategy):
    def calculate_tax(self, income):
        if income < 50000:
            tax = income * 0.10
        elif income < 100000:
            tax = income * 0.15
        else:
            tax = income * 0.20
        print(f"US Tax calculated for income {income}: {tax:.2f}")
        return tax

class EuropeanTaxStrategy(TaxStrategy):
    def calculate_tax(self, income):
        if income < 60000:
            tax = income * 0.20
        else:
            tax = income * 0.25
        print(f"European Tax calculated for income {income}: {tax:.2f}")
        return tax

class TaxCalculator:
    def __init__(self, strategy: TaxStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: TaxStrategy):
        self._strategy = strategy

    def get_tax(self, income):
        return self._strategy.calculate_tax(income)

if __name__ == "__main__":
    calc = TaxCalculator(USTaxStrategy())
    calc.get_tax(45000)
    calc.get_tax(75000)

    calc.set_strategy(EuropeanTaxStrategy())
    calc.get_tax(45000)
    calc.get_tax(75000)