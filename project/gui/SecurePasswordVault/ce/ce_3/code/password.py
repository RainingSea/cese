from cryptography.fernet import Fernet

class Password:
    def __init__(self, website: str, username: str, password: str) -> None:
        self.website = website
        self.username = username
        self.password = password
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_password(self) -> str:
        return self.cipher.encrypt(self.password.encode()).decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        return self.cipher.decrypt(encrypted_password.encode()).decode()