class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

class Product(Subject):
    def __init__(self, name, price, stock):
        super().__init__()
        self._name = name
        self._price = price
        self._stock = stock
        print(f"Product '{self._name}' created. Price: ${self._price:.2f}, Stock: {self._stock}")

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if self._price != new_price:
            old_price = self._price
            self._price = new_price
            print(f"Product '{self._name}' price changed from ${old_price:.2f} to ${new_price:.2f}.")
            self.notify("price_update", new_price=new_price)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, new_stock):
        if self._stock != new_stock:
            old_stock = self._stock
            self._stock = new_stock
            print(f"Product '{self._name}' stock changed from {old_stock} to {new_stock}.")
            self.notify("stock_update", new_stock=new_stock)

class CustomerNotifier:
    def __init__(self, customer_id, notification_type="email"):
        self.customer_id = customer_id
        self.notification_type = notification_type

    def update(self, subject, event_type, **kwargs):
        if event_type == "price_update":
            print(f"Customer {self.customer_id} ({self.notification_type}): Price alert for '{subject.name}'! New price: ${kwargs['new_price']:.2f}")
        elif event_type == "stock_update" and kwargs['new_stock'] > 0:
            print(f"Customer {self.customer_id} ({self.notification_type}): Stock alert for '{subject.name}'! Now available: {kwargs['new_stock']} units.")

class InventoryDashboard:
    def __init__(self, dashboard_id):
        self.dashboard_id = dashboard_id

    def update(self, subject, event_type, **kwargs):
        if event_type == "price_update":
            print(f"Dashboard {self.dashboard_id}: Product '{subject.name}' price updated to ${kwargs['new_price']:.2f}.")
        elif event_type == "stock_update":
            print(f"Dashboard {self.dashboard_id}: Product '{subject.name}' stock updated to {kwargs['new_stock']} units.")

# Simulation of an E-commerce system
print("--- E-commerce Product Monitoring Simulation ---")
laptop = Product("Gaming Laptop", 1200.00, 5)

customer1 = CustomerNotifier("CUST001", "email")
customer2 = CustomerNotifier("CUST002", "sms")
dashboard = InventoryDashboard("DASH001")

laptop.attach(customer1)
laptop.attach(customer2)
laptop.attach(dashboard)

print("\n--- Scenario 1: Price Drop ---")
laptop.price = 1150.00 

print("\n--- Scenario 2: Stock Depletes and Replenishes ---")
laptop.stock = 0 
laptop.stock = 15 

print("\n--- Scenario 3: Detach an Observer ---")
laptop.detach(customer2)
laptop.price = 1100.00 
