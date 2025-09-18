class DatabaseConnector:
    def connect(self) -> str:
        pass
    def execute_query(self, query: str) -> str:
        pass

class MySQLConnector(DatabaseConnector):
    def connect(self) -> str:
        return "Connecting to MySQL database..."
    def execute_query(self, query: str) -> str:
        return f"Executing MySQL query: '{query}'"

class PostgreSQLConnector(DatabaseConnector):
    def connect(self) -> str:
        return "Connecting to PostgreSQL database..."
    def execute_query(self, query: str) -> str:
        return f"Executing PostgreSQL query: '{query}'"

class SQLiteConnector(DatabaseConnector):
    def connect(self) -> str:
        return "Connecting to SQLite database..."
    def execute_query(self, query: str) -> str:
        return f"Executing SQLite query: '{query}'"

class DBConnectorFactory:
    def get_connector(self, db_type: str) -> DatabaseConnector:
        if db_type == "mysql":
            return MySQLConnector()
        elif db_type == "postgresql":
            return PostgreSQLConnector()
        elif db_type == "sqlite":
            return SQLiteConnector()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

factory = DBConnectorFactory()

mysql_conn = factory.get_connector("mysql")
pg_conn = factory.get_connector("postgresql")
sqlite_conn = factory.get_connector("sqlite")

print(mysql_conn.connect())
print(mysql_conn.execute_query("SELECT * FROM users;"))
print(pg_conn.connect())
print(pg_conn.execute_query("INSERT INTO products (name, price) VALUES ('Widget', 19.99);"))
print(sqlite_conn.connect())
print(sqlite_conn.execute_query("UPDATE settings SET value = 'enabled' WHERE key = 'feature_x';"))

try:
    oracle_conn = factory.get_connector("oracle")
except ValueError as e:
    print(e)