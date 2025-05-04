import hashlib
import os


class PasswordProps:
    def __init__(self, hashed_password: str, salt: str):
        self.hashed_password = hashed_password
        self.salt = salt


class AuthService:

    def __init__(self):
        pass

    @staticmethod
    def get_hashed_password(string_password: str) -> PasswordProps:
        salt = os.urandom(32)
        return AuthService._get_hashed_password(string_password, salt)

    @staticmethod
    def _get_hashed_password(string_password: str, salt: bytes) -> PasswordProps:
        hash_counter = hashlib.new('sha256')
        hash_counter.update((string_password + salt.decode('utf-8', 'ignore')).encode('utf-8'))
        hashed_password = hash_counter.hexdigest()

        return PasswordProps(
            hashed_password=hashed_password,
            salt=salt.decode('utf-8', 'ignore')
        )

    @staticmethod
    def check_password(string_password: str, password_hash: str, salt: str):
        hashed_input_password = AuthService._get_hashed_password(string_password, salt.encode('utf-8')).hashed_password
        return hashed_input_password == password_hash
