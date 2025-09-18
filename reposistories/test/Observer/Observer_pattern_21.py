class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Product(Subject):
    def __init__(self, name, initial_stock):
        super().__init__()
        self.name = name
        self._stock = initial_stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if self._stock != value:
            self._stock = value
            self.notify()

class CustomerNotifier:
    def __init__(self, customer_email):
        self.customer_email = customer_email

    def update(self, product):
        if product.stock < 5:
            print(f"E-commerce: Sending low stock alert to {self.customer_email} for {product.name}. Stock: {product.stock}")
        else:
            print(f"E-commerce: Notifying {self.customer_email} about {product.name} stock update. New Stock: {product.stock}")

class WarehouseManager:
    def update(self, product):
        if product.stock < 10:
            print(f"E-commerce: Warehouse Manager: Initiating reorder for {product.name}. Current stock: {product.stock}")

class AnalyticsService:
    def update(self, product):
        print(f"E-commerce: Analytics Service: Logging stock change for {product.name}. New stock: {product.stock}")

product_a = Product("Laptop", 20)

customer1 = CustomerNotifier("john.doe@example.com")
warehouse_manager = WarehouseManager()
analytics_service = AnalyticsService()

product_a.attach(customer1)
product_a.attach(warehouse_manager)
product_a.attach(analytics_service)

print("--- E-commerce Simulation: Initial Stock ---")
print(f"{product_a.name} stock: {product_a.stock}")

print("\n--- E-commerce Simulation: Stock decreases ---")
product_a.stock = 15
product_a.stock = 7
product_a.stock = 3

print("\n--- E-commerce Simulation: Customer 1 unsubscribes ---")
product_a.detach(customer1)
product_a.stock = 1

print("\n--- E-commerce Simulation: Stock increases ---")
product_a.stock = 25