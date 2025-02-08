from cryptography.fernet import Fernet

class PasswordEncryption:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, password: str) -> str:
        """Encrypt the password."""
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt(self, encrypted_password: str) -> str:
        """Decrypt the password."""
        return self.cipher.decrypt(encrypted_password.encode()).decode()