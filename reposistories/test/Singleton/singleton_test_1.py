class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AppSettings(metaclass=SingletonMeta):
    def __init__(self):
        self.theme = "Light"
        self.language = "en"

    def set_theme(self, theme: str):
        self.theme = theme

    def set_language(self, language: str):
        self.language = language

    def get_settings(self):
        return {"theme": self.theme, "language": self.language}


# Usage
settings1 = AppSettings()
settings2 = AppSettings()

settings1.set_theme("Dark")

print(settings2.get_settings())  # {'theme': 'Dark', 'language': 'en'}
print(settings1 is settings2)   # True, both are the same instance
