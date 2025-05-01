import os
from cryptography.fernet import Fernet

class VaultManager:
    def __init__(self):
        self.vaults = {}
        self.load_vaults()

    def load_vaults(self):
        if not os.path.exists('vaults'):
            os.makedirs('vaults')
        for filename in os.listdir('vaults'):
            if filename.endswith('.txt'):
                vault_name = filename[:-4]
                self.vaults[vault_name] = {}
                with open(os.path.join('vaults', filename), 'r') as vault_file:
                    for line in vault_file:
                        password, encrypted = line.strip().split('|')
                        self.vaults[vault_name][password] = encrypted

    def create_vault(self, name: str):
        if name not in self.vaults:
            self.vaults[name] = {}
            with open(os.path.join('vaults', f"{name}.txt"), 'w') as vault_file:
                vault_file.write("")
        else:
            raise ValueError("Vault already exists.")

    def add_password(self, vault_name: str, password: str):
        if vault_name in self.vaults:
            if self.analyze_password_strength(password):
                encrypted_password = self.encrypt_password(password)
                self.vaults[vault_name][password] = encrypted_password
                with open(os.path.join('vaults', f"{vault_name}.txt"), 'a') as vault_file:
                    vault_file.write(f"{password}|{encrypted_password}\n")
            else:
                raise ValueError("Password does not meet strength requirements.")
        else:
            raise ValueError("Vault does not exist.")

    def edit_password(self, vault_name: str, old_password: str, new_password: str):
        if vault_name in self.vaults and old_password in self.vaults[vault_name]:
            self.delete_password(vault_name, old_password)
            self.add_password(vault_name, new_password)
        else:
            raise ValueError("Password does not exist.")

    def delete_password(self, vault_name: str, password: str):
        if vault_name in self.vaults and password in self.vaults[vault_name]:
            del self.vaults[vault_name][password]
            self.save_vault(vault_name)
        else:
            raise ValueError("Password does not exist.")

    def search_password(self, vault_name: str, query: str) -> str:
        if vault_name in self.vaults:
            found_passwords = [password for password in self.vaults[vault_name] if query in password]
            return ', '.join(found_passwords) if found_passwords else "Password not found."
        return "Vault does not exist."

    def encrypt_password(self, password: str) -> str:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password.decode()

    def save_vault(self, vault_name: str):
        with open(os.path.join('vaults', f"{vault_name}.txt"), 'w') as vault_file:
            for password, encrypted in self.vaults[vault_name].items():
                vault_file.write(f"{password}|{encrypted}\n")

    def list_vaults(self):
        return list(self.vaults.keys())

    def analyze_password_strength(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        return True