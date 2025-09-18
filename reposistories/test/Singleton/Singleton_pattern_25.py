class SingletonBase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class AuthenticationManager(SingletonBase):
    def __init__(self, default_user_role="guest"):
        if not hasattr(self, '_initialized'):
            self.current_user = None
            self.session_token = None
            self.default_user_role = default_user_role
            self._initialized = True

    def login(self, username, password):
        if username == "admin" and password == "securepass":
            self.current_user = username
            self.session_token = f"token_{hash(username+password)}"
            return True
        self.current_user = None
        self.session_token = None
        return False

    def logout(self):
        self.current_user = None
        self.session_token = None

    def get_current_user(self):
        return self.current_user

    def is_authenticated(self):
        return self.current_user is not None

if __name__ == "__main__":
    auth_manager1 = AuthenticationManager("viewer")
    auth_manager2 = AuthenticationManager("editor")

    print(f"Are auth_manager1 and auth_manager2 the same instance? {auth_manager1 is auth_manager2}")
    print(f"Auth Manager 1 default role: {auth_manager1.default_user_role}")
    print(f"Auth Manager 2 default role: {auth_manager2.default_user_role}")

    auth_manager1.login("admin", "securepass")
    print(f"Current user via auth_manager1: {auth_manager1.get_current_user()}")
    print(f"Is auth_manager2 authenticated? {auth_manager2.is_authenticated()}")

    auth_manager2.logout()
    print(f"Current user via auth_manager1 after logout: {auth_manager1.get_current_user()}")