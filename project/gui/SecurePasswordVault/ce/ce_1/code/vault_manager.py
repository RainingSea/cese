import os
import json
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
                self.vaults[vault_name] = Vault(vault_name)

    def create_vault(self, name: str):
        if name not in self.vaults:
            self.vaults[name] = Vault(name)

    def add_password(self, vault_name: str, password: str):
        if vault_name in self.vaults:
            self.vaults[vault_name].add_password(password)

    def edit_password(self, vault_name: str, password_id: int, new_password: str):
        if vault_name in self.vaults:
            self.vaults[vault_name].edit_password(password_id, new_password)

    def delete_password(self, vault_name: str, password_id: int):
        if vault_name in self.vaults:
            self.vaults[vault_name].delete_password(password_id)

    def search_password(self, vault_name: str, query: str):
        if vault_name in self.vaults:
            return self.vaults[vault_name].search_password(query)
        return None

    def analyze_password_strength(self, password: str):
        # Simple password strength analysis
        if len(password) < 8:
            return "Weak"
        elif len(password) < 12:
            return "Moderate"
        else:
            return "Strong"

    def list_vaults(self):
        return list(self.vaults.keys())

class Vault:
    def __init__(self, name: str):
        self.name = name
        self.passwords = []
        self.load_passwords()

    def load_passwords(self):
        file_path = f'vaults/{self.name}.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    self.passwords.append(line.strip())

    def add_password(self, password: str):
        self.passwords.append(password)
        self.save_passwords()

    def edit_password(self, password_id: int, new_password: str):
        if 0 <= password_id < len(self.passwords):
            self.passwords[password_id] = new_password
            self.save_passwords()

    def delete_password(self, password_id: int):
        if 0 <= password_id < len(self.passwords):
            del self.passwords[password_id]
            self.save_passwords()

    def save_passwords(self):
        file_path = f'vaults/{self.name}.txt'
        with open(file_path, 'w') as file:
            for password in self.passwords:
                file.write(password + '\n')

    def search_password(self, query: str):
        return [password for password in self.passwords if query in password]