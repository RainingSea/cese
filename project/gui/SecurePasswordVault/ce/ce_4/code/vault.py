import os
from cryptography.fernet import Fernet

class Vault:
    def __init__(self, name: str) -> None:
        self.name = name
        self.passwords = {}
        self.load_passwords()

    def load_passwords(self) -> None:
        if os.path.exists(f"{self.name}.txt"):
            with open(f"{self.name}.txt", "r") as file:
                for line in file:
                    account, encrypted_password = line.strip().split(":")
                    self.passwords[account] = encrypted_password

    def save_passwords(self) -> None:
        with open(f"{self.name}.txt", "w") as file:
            for account, encrypted_password in self.passwords.items():
                file.write(f"{account}:{encrypted_password}\n")