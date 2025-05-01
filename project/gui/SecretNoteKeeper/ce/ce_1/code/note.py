from cryptography.fernet import Fernet

class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_content(self) -> str:
        return self.cipher.encrypt(self.content.encode()).decode()

    def decrypt_content(self) -> str:
        return self.cipher.decrypt(self.content.encode()).decode()