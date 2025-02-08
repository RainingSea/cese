import json
import os
from password import Password

class VaultManager:
    def __init__(self) -> None:
        self.vaults = self.load_vaults()

    def create_vault(self, name: str) -> bool:
        if name not in self.vaults:
            self.vaults[name] = []
            self.save_vaults()
            return True
        return False

    def delete_vault(self, name: str) -> bool:
        if name in self.vaults:
            del self.vaults[name]
            self.save_vaults()
            return True
        return False

    def add_password(self, vault_name: str, password_data: dict) -> bool:
        if vault_name in self.vaults:
            password = Password(**password_data)
            self.vaults[vault_name].append(password.encrypt_password())
            self.save_vaults()
            return True
        return False

    def edit_password(self, vault_name: str, password_id: int, new_data: dict) -> bool:
        if vault_name in self.vaults and 0 <= password_id < len(self.vaults[vault_name]):
            password = Password(**new_data)
            self.vaults[vault_name][password_id] = password.encrypt_password()
            self.save_vaults()
            return True
        return False

    def delete_password(self, vault_name: str, password_id: int) -> bool:
        if vault_name in self.vaults and 0 <= password_id < len(self.vaults[vault_name]):
            del self.vaults[vault_name][password_id]
            self.save_vaults()
            return True
        return False

    def search_password(self, vault_name: str, query: str) -> list:
        if vault_name in self.vaults:
            return [pwd for pwd in self.vaults[vault_name] if query in pwd]
        return []

    def analyze_password_strength(self, password: str) -> str:
        if len(password) < 8:
            return "Weak"
        elif len(password) < 12:
            return "Moderate"
        else:
            return "Strong"

    def load_vaults(self) -> dict:
        if os.path.exists('vaults.json'):
            with open('vaults.json', 'r') as file:
                return json.load(file)
        return {}

    def save_vaults(self) -> bool:
        with open('vaults.json', 'w') as file:
            json.dump(self.vaults, file)
        return True