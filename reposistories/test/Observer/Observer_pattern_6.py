class Product:
    def __init__(self, name, initial_stock):
        self._name = name
        self._stock_level = initial_stock
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._name, self._stock_level)

    @property
    def stock_level(self):
        return self._stock_level

    @stock_level.setter
    def stock_level(self, new_level):
        if new_level != self._stock_level:
            old_level = self._stock_level
            self._stock_level = new_level
            if (old_level == 0 and new_level > 0) or (old_level > 0 and new_level == 0):
                self._notify()
            elif new_level > 0 and old_level > 0:
                pass
            elif new_level == 0 and old_level > 0:
                self._notify()


class Customer:
    def __init__(self, name):
        self._name = name

    def update(self, product_name, stock_level):
        if stock_level > 0:
            print(f"Customer {self._name}: Good news! '{product_name}' is now in stock ({stock_level} units).")
        else:
            print(f"Customer {self._name}: Oh no! '{product_name}' is now out of stock.")

if __name__ == "__main__":
    laptop = Product("Gaming Laptop", 0)
    headset = Product("Wireless Headset", 5)

    customer_a = Customer("Alice")
    customer_b = Customer("Bob")

    laptop.attach(customer_a)
    headset.attach(customer_b)

    print("--- Initial state ---")
    laptop.stock_level = 0
    headset.stock_level = 5

    print("\n--- Stock changes ---")
    laptop.stock_level = 2
    headset.stock_level = 4
    headset.stock_level = 0
    headset.detach(customer_b)

    print("\n--- More stock changes ---")
    laptop.stock_level = 0