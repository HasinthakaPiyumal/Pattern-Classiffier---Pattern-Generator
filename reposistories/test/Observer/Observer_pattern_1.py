class Stock:
    def __init__(self, symbol, price):
        self._symbol = symbol
        self._price = price
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._symbol, self._price)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price != self._price:
            self._price = new_price
            self._notify()

class Investor:
    def __init__(self, name):
        self._name = name

    def update(self, symbol, price):
        print(f"{self._name}: Stock {symbol} updated to ${price:.2f}")

if __name__ == "__main__":
    microsoft = Stock("MSFT", 150.00)

    investor1 = Investor("Alice")
    investor2 = Investor("Bob")

    microsoft.attach(investor1)
    microsoft.attach(investor2)

    microsoft.price = 150.50
    microsoft.price = 151.25

    microsoft.detach(investor1)
    microsoft.price = 152.00