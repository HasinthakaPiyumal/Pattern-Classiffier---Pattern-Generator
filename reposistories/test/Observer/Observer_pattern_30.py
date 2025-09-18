import random

class Order:
    def __init__(self, order_id, initial_status):
        self._order_id = order_id
        self._status = initial_status
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def _notify(self):
        for observer in self._observers:
            observer.update(self._order_id, self._status)

    def set_status(self, new_status):
        print(f"Order {self._order_id}: Status changing from '{self._status}' to '{new_status}'")
        self._status = new_status
        self._notify()

class Customer:
    def __init__(self, customer_id, name):
        self._customer_id = customer_id
        self._name = name

    def update(self, order_id, status):
        print(f"Customer {self._name} ({self._customer_id}): Received update for Order {order_id} - New status is '{status}'.")

class EmailService:
    def __init__(self, service_name):
        self._service_name = service_name

    def update(self, order_id, status):
        print(f"Email Service ({self._service_name}): Preparing email for Order {order_id} - Status: '{status}'.")


order1 = Order("ORD1001", "Pending")
order2 = Order("ORD1002", "Processing")

customer1 = Customer("CUST001", "Alice")
customer2 = Customer("CUST002", "Bob")
customer3 = Customer("CUST003", "Charlie")
email_service = EmailService("Marketing")

print("--- Simulation Start: E-commerce Order Updates ---")

order1.attach(customer1)
order1.attach(customer2)
order1.attach(email_service)

order2.attach(customer2)
order2.attach(customer3)

print("\n--- Order 1 Status Changes ---")
order1.set_status("Shipped")
order1.set_status("Out for Delivery")

print("\n--- Order 2 Status Changes ---")
order2.set_status("Shipped")

print("\n--- Customer 1 unsubscribes from Order 1 ---")
order1.detach(customer1)
order1.set_status("Delivered")

print("\n--- Order 2 Status Changes Again ---")
order2.set_status("Delivered")

print("--- Simulation End ---")