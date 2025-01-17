from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt_data(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, data: str) -> str:
        return self.cipher.decrypt(data.encode()).decode()