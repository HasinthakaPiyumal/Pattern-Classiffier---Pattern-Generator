def singleton(cls):
    _instances = {}
    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance

@singleton
class DatabaseConnectionPool:
    def __init__(self, db_type, max_connections=5):
        self.db_type = db_type
        self.max_connections = max_connections
        self.active_connections = 0
        self.pool = []
        for i in range(max_connections):
            self.pool.append(f"Connection-{i+1}-{db_type}")
            self.active_connections += 1

    def get_connection(self):
        if self.pool:
            conn = self.pool.pop(0)
            return conn
        return None

    def release_connection(self, connection):
        self.pool.append(connection)

if __name__ == "__main__":
    pool1 = DatabaseConnectionPool("PostgreSQL", 10)
    pool2 = DatabaseConnectionPool("MySQL", 5)

    print(f"Are pool1 and pool2 the same instance? {pool1 is pool2}")
    print(f"Pool1 DB Type: {pool1.db_type}, Max Connections: {pool1.max_connections}")
    print(f"Pool2 DB Type: {pool2.db_type}, Max Connections: {pool2.max_connections}")

    conn1 = pool1.get_connection()
    conn2 = pool2.get_connection()
    conn3 = pool1.get_connection()

    print(f"Got connections: {conn1}, {conn2}, {conn3}")

    pool1.release_connection(conn1)
    pool2.release_connection(conn2)