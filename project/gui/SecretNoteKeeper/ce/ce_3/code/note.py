from cryptography.fernet import Fernet

class Note:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
        self.encrypted_content = self.encrypt()

    def encrypt(self) -> str:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(self.content.encode())
        return encrypted.decode()

    def decrypt(self) -> str:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        decrypted = cipher.decrypt(self.encrypted_content.encode())
        return decrypted.decode()