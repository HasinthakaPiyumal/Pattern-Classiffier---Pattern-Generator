import threading

class InventoryManager:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, warehouse_id="WH_MAIN_01"):
        with self._lock:
            if not self._initialized:
                self.warehouse_id = warehouse_id
                self.inventory = {}
                self._initialized = True

    def add_product(self, product_id, quantity):
        with self._lock:
            self.inventory[product_id] = self.inventory.get(product_id, 0) + quantity
            return self.inventory[product_id]

    def remove_product(self, product_id, quantity):
        with self._lock:
            if self.inventory.get(product_id, 0) >= quantity:
                self.inventory[product_id] -= quantity
                return True
            return False

    def get_stock(self, product_id):
        with self._lock:
            return self.inventory.get(product_id, 0)

if __name__ == "__main__":
    def worker(manager, product, quantity, operation):
        if operation == "add":
            manager.add_product(product, quantity)
        elif operation == "remove":
            manager.remove_product(product, quantity)

    inv_manager1 = InventoryManager("WH_EAST")
    inv_manager2 = InventoryManager("WH_WEST")

    print(f"Are inv_manager1 and inv_manager2 the same instance? {inv_manager1 is inv_manager2}")
    print(f"Inv Manager 1 Warehouse ID: {inv_manager1.warehouse_id}")

    inv_manager1.add_product("SKU123", 100)
    print(f"Initial stock for SKU123: {inv_manager1.get_stock('SKU123')}")

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(inv_manager1, "SKU123", 10, "remove"), name=f"Remover-{i}")
        threads.append(t)
        t = threading.Thread(target=worker, args=(inv_manager1, "SKU123", 5, "add"), name=f"Adder-{i}")
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Final stock for SKU123: {inv_manager1.get_stock('SKU123')}")