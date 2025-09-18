import abc

class Subject(abc.ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self, subject):
        pass

class Product(Subject):
    def __init__(self, name, initial_stock):
        super().__init__()
        self._name = name
        self._stock = initial_stock
        self._price = 0.0

    @property
    def name(self):
        return self._name

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, new_stock):
        if new_stock != self._stock:
            self._stock = new_stock
            self.notify()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price != self._price:
            self._price = new_price
            self.notify()

class CustomerNotifier(Observer):
    def update(self, product):
        if product.stock > 0 and product.stock <= 5:
            print(f"CUSTOMER NOTIFIER: {product.name} is low in stock ({product.stock} left)! Hurry up!")
        elif product.stock > 5:
            print(f"CUSTOMER NOTIFIER: {product.name} stock updated to {product.stock}.")
        elif product.stock == 0:
            print(f"CUSTOMER NOTIFIER: {product.name} is out of stock.")

class WarehouseManager(Observer):
    def update(self, product):
        if product.stock <= 3:
            print(f"WAREHOUSE MANAGER: Initiating reorder for {product.name}. Current stock: {product.stock}.")
        else:
            print(f"WAREHOUSE MANAGER: Stock level for {product.name} is {product.stock}.")

class MarketingDepartment(Observer):
    def update(self, product):
        if product.stock > 50:
            print(f"MARKETING DEPARTMENT: Consider promotion for {product.name}, high stock ({product.stock}).")
        elif product.price != 0.0:
            print(f"MARKETING DEPARTMENT: Price for {product.name} changed to ${product.price:.2f}.")
        else:
            print(f"MARKETING DEPARTMENT: Stock for {product.name} is {product.stock}. No immediate action.")

if __name__ == "__main__":
    print("--- E-commerce Product Stock Monitoring Simulation ---")
    iphone = Product("iPhone 15 Pro", 100)

    customer_notifier = CustomerNotifier()
    warehouse_manager = WarehouseManager()
    marketing_department = MarketingDepartment()

    iphone.attach(customer_notifier)
    iphone.attach(warehouse_manager)
    iphone.attach(marketing_department)

    print("\n--- Event 1: Initial Price Set ---")
    iphone.price = 999.99

    print("\n--- Event 2: Multiple Sales ---")
    iphone.stock = 90
    iphone.stock = 85
    iphone.stock = 55 # Marketing might react here
    iphone.stock = 10 # Customer & Warehouse might react here

    print("\n--- Event 3: Low Stock Sale ---")
    iphone.stock = 3 # Warehouse reorders, Customer sees low stock

    print("\n--- Event 4: Out of Stock ---")
    iphone.stock = 0

    print("\n--- Event 5: Restock ---")
    iphone.stock = 75 # All observers get update

    print("\n--- Event 6: Detach Marketing and another Sale ---")
    iphone.detach(marketing_department)
    iphone.stock = 70