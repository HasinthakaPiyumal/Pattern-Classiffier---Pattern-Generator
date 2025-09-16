class Database:
    def __init__(self, name):
        self._name = name
        self._data = {}
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self, change_type, key, value=None):
        for observer in self._observers:
            observer.update(self._name, change_type, key, value)

    def insert(self, key, value):
        self._data[key] = value
        print(f"DB '{self._name}': Inserted '{key}'='{value}'")
        self._notify("INSERT", key, value)

    def update_record(self, key, new_value):
        if key in self._data:
            self._data[key] = new_value
            print(f"DB '{self._name}': Updated '{key}' to '{new_value}'")
            self._notify("UPDATE", key, new_value)
        else:
            print(f"DB '{self._name}': Key '{key}' not found for update.")

    def delete(self, key):
        if key in self._data:
            del self._data[key]
            print(f"DB '{self._name}': Deleted '{key}'")
            self._notify("DELETE", key)
        else:
            print(f"DB '{self._name}': Key '{key}' not found for deletion.")

class CacheUpdater:
    def update(self, db_name, change_type, key, value=None):
        if change_type == "INSERT" or change_type == "UPDATE":
            print(f"CacheUpdater: Refreshing cache for DB '{db_name}', key '{key}' with value '{value}'.")
        elif change_type == "DELETE":
            print(f"CacheUpdater: Invalidating cache for DB '{db_name}', key '{key}'.")

class Logger:
    def update(self, db_name, change_type, key, value=None):
        if value:
            print(f"Logger: [{db_name}] Data change: Type={change_type}, Key={key}, Value={value}")
        else:
            print(f"Logger: [{db_name}] Data change: Type={change_type}, Key={key}")

if __name__ == "__main__":
    user_db = Database("UserDB")

    cache_updater = CacheUpdater()
    activity_logger = Logger()

    user_db.attach(cache_updater)
    user_db.attach(activity_logger)

    user_db.insert("user:1", {"name": "Alice", "email": "alice@example.com"})
    user_db.update_record("user:1", {"name": "Alice Smith", "email": "alice.s@example.com"})
    user_db.insert("product:101", {"name": "Laptop", "price": 1200})

    user_db.detach(cache_updater)
    user_db.delete("user:1")