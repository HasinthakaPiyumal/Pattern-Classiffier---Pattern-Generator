class ConfigurationManager:
    _instance = None
    _config_data = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config_data = {
                "DATABASE_URL": "sqlite:///app.db",
                "API_KEY": "your_secret_api_key",
                "LOG_LEVEL": "INFO"
            }
        return cls._instance

    def get_setting(self, key):
        return self._config_data.get(key)

    def set_setting(self, key, value):
        self._config_data[key] = value

if __name__ == "__main__":
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()

    print(f"Config1 DB URL: {config1.get_setting('DATABASE_URL')}")
    print(f"Config2 API Key: {config2.get_setting('API_KEY')}")

    config1.set_setting("LOG_LEVEL", "DEBUG")
    print(f"Config2 new LOG_LEVEL: {config2.get_setting('LOG_LEVEL')}")

    print(f"Are config1 and config2 the same instance? {config1 is config2}")