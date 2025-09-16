class StockMarket:
    def __init__(self):
        self._observers = []
        self._stock_prices = {}

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def set_price(self, stock_name, price):
        self._stock_prices[stock_name] = price
        self.notify(stock_name, price)

    def notify(self, stock_name, price):
        for observer in self._observers:
            observer.update(stock_name, price)

class Investor:
    def __init__(self, name):
        self.name = name

    def update(self, stock_name, price):
        print(f"Investor {self.name}: {stock_name} price changed to ${price}")

if __name__ == '__main__':
    market = StockMarket()
    investor1 = Investor("Alice")
    investor2 = Investor("Bob")

    market.attach(investor1)
    market.attach(investor2)

    market.set_price("GOOG", 1500.50)
    market.set_price("AAPL", 175.20)

    market.detach(investor1)
    market.set_price("GOOG", 1510.00)