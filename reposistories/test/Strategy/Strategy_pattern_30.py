import abc
import hashlib
import os
import binascii

class AuthenticationStrategy(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, username, credentials):
        pass

class PasswordAuthentication(AuthenticationStrategy):
    def __init__(self, user_database):
        self._user_database = user_database

    def _hash_password(self, password, salt):
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return binascii.hexlify(pwdhash).decode('ascii')

    def authenticate(self, username, credentials):
        print(f"--- PASSWORD AUTHENTICATION for {username} ---")
        if username not in self._user_database:
            print(f"Authentication failed: User '{username}' not found.")
            return False

        stored_info = self._user_database[username]
        stored_hash = stored_info["hashed_password"]
        stored_salt = stored_info["salt"]

        provided_password = credentials.get("password")
        if not provided_password:
            print("Authentication failed: Password not provided.")
            return False

        computed_hash = self._hash_password(provided_password, binascii.unhexlify(stored_salt))

        if computed_hash == stored_hash:
            print(f"Authentication successful for '{username}'.")
            return True
        else:
            print(f"Authentication failed: Incorrect password for '{username}'.")
            return False

class TwoFactorAuthentication(AuthenticationStrategy):
    def __init__(self, user_database, sms_service_mock):
        self._user_database = user_database
        self._sms_service_mock = sms_service_mock

    def authenticate(self, username, credentials):
        print(f"--- TWO-FACTOR AUTHENTICATION for {username} ---")
        if username not in self._user_database:
            print(f"Authentication failed: User '{username}' not found.")
            return False

        stored_info = self._user_database[username]
        provided_password = credentials.get("password")
        provided_otp = credentials.get("otp")

        if stored_info["password"] != provided_password:
            print(f"Authentication failed: Incorrect password for '{username}'.")
            return False

        if not provided_otp:
            print(f"Password correct. Sending OTP to {username}'s registered device (simulated).")
            return False

        expected_otp = "123456"
        if provided_otp == expected_otp:
            print(f"Authentication successful for '{username}' with 2FA.")
            return True
        else:
            print(f"Authentication failed: Invalid OTP for '{username}'.")
            return False

class OAuthAuthentication(AuthenticationStrategy):
    def __init__(self, oauth_provider_mock):
        self._oauth_provider_mock = oauth_provider_mock

    def authenticate(self, username, credentials):
        print(f"--- OAUTH AUTHENTICATION for {username} ---")
        access_token = credentials.get("access_token")

        if not access_token:
            print("Authentication failed: OAuth access token not provided.")
            return False

        if self._oauth_provider_mock.validate_token(access_token, username):
            print(f"Authentication successful for '{username}' via OAuth.")
            return True
        else:
            print(f"Authentication failed: Invalid or expired OAuth token for '{username}'.")
            return False

class Authenticator:
    def __init__(self, default_strategy: AuthenticationStrategy):
        self._authentication_strategy = default_strategy

    def set_authentication_strategy(self, strategy: AuthenticationStrategy):
        self._authentication_strategy = strategy

    def login(self, username, credentials):
        print(f"\nAttempting login for '{username}'...")
        return self._authentication_strategy.authenticate(username, credentials)

class SMSMockService:
    def send_otp(self, phone_number, secret):
        print(f"SMS: Sending OTP to {phone_number} (secret: {secret[:4]}...).")

class OAuthProviderMock:
    def validate_token(self, token, expected_username):
        return token == "valid_oauth_token_for_" + expected_username.lower()

if __name__ == "__main__":
    users_pwd = {}
    salt = os.urandom(16)
    hashed_pwd = hashlib.pbkdf2_hmac('sha256', "securepass123".encode('utf-8'), salt, 100000)
    users_pwd["alice"] = {"hashed_password": binascii.hexlify(hashed_pwd).decode('ascii'), "salt": binascii.hexlify(salt).decode('ascii')}

    users_2fa = {
        "bob": {"password": "bob_password", "2fa_secret": "ABCDEF", "phone_number": "555-1234"}
    }
    sms_mock = SMSMockService()

    oauth_mock = OAuthProviderMock()

    pwd_authenticator = Authenticator(PasswordAuthentication(users_pwd))
    pwd_authenticator.login("alice", {"password": "securepass123"})
    pwd_authenticator.login("alice", {"password": "wrong_password"})
    pwd_authenticator.login("charlie", {"password": "any_password"})

    tfa_authenticator = Authenticator(TwoFactorAuthentication(users_2fa, sms_mock))
    tfa_authenticator.login("bob", {"password": "bob_password"})
    tfa_authenticator.login("bob", {"password": "bob_password", "otp": "123456"})
    tfa_authenticator.login("bob", {"password": "bob_password", "otp": "999999"})

    oauth_authenticator = Authenticator(OAuthAuthentication(oauth_mock))
    oauth_authenticator.login("diana", {"access_token": "valid_oauth_token_for_diana"})
    oauth_authenticator.login("diana", {"access_token": "invalid_token"})
    oauth_authenticator.login("diana", {"access_token": "valid_oauth_token_for_charlie"})