class Order:
    def __init__(self, order_id, initial_status="pending"):
        self.order_id = order_id
        self._status = initial_status
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def update_status(self, new_status):
        if new_status not in ["pending", "processing", "shipped", "delivered"]:
            raise ValueError("Invalid order status")
        self._status = new_status
        print(f"\nOrder {self.order_id}: Status changed to '{self._status}'")
        self.notify()

    def get_status(self):
        return self._status

    def notify(self):
        for observer in self._observers:
            observer.on_status_change(self.order_id, self._status)

class CustomerNotifier:
    def __init__(self, customer_name, contact_method="email"):
        self.customer_name = customer_name
        self.contact_method = contact_method

    def on_status_change(self, order_id, status):
        print(f"Customer Notifier ({self.customer_name} via {self.contact_method}): Order {order_id} is now '{status}'.")

class WarehouseManager:
    def __init__(self, manager_name):
        self.manager_name = manager_name

    def on_status_change(self, order_id, status):
        if status == "processing":
            print(f"Warehouse Manager ({self.manager_name}): Processing order {order_id} for shipment.")
        elif status == "shipped":
            print(f"Warehouse Manager ({self.manager_name}): Order {order_id} has left the warehouse.")

if __name__ == '__main__':
    order123 = Order("ORD123")
    order456 = Order("ORD456", "processing")

    customer_notifier = CustomerNotifier("Alice Smith")
    warehouse_manager = WarehouseManager("Bob Johnson")

    order123.attach(customer_notifier)
    order123.attach(warehouse_manager)
    order456.attach(customer_notifier)

    order123.update_status("processing")
    order123.update_status("shipped")
    order456.update_status("shipped")
    order123.update_status("delivered")
    order123.detach(warehouse_manager)
    order123.update_status("pending")