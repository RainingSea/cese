import json
from typing import List, Dict
from password_strength_analyzer import PasswordStrengthAnalyzer

class VaultManager:
    def __init__(self):
        self.vaults = {}
        self.load_vaults()
        self.strength_analyzer = PasswordStrengthAnalyzer()

    def create_vault(self, vault_name: str) -> None:
        if vault_name not in self.vaults:
            self.vaults[vault_name] = []
            self.save_vaults()

    def add_password(self, vault_name: str, password_data: Dict) -> None:
        if vault_name in self.vaults:
            self.vaults[vault_name].append(password_data)
            self.save_vaults()

    def edit_password(self, vault_name: str, password_id: int, new_data: Dict) -> None:
        if vault_name in self.vaults and 0 <= password_id < len(self.vaults[vault_name]):
            self.vaults[vault_name][password_id] = new_data
            self.save_vaults()

    def delete_password(self, vault_name: str, password_id: int) -> None:
        if vault_name in self.vaults and 0 <= password_id < len(self.vaults[vault_name]):
            del self.vaults[vault_name][password_id]
            self.save_vaults()

    def search_passwords(self, vault_name: str, query: str) -> List[Dict]:
        if vault_name in self.vaults:
            return [pwd for pwd in self.vaults[vault_name] if query in pwd['website'] or query in pwd['username']]
        return []

    def load_vaults(self) -> None:
        try:
            with open('vaults.json', 'r') as file:
                self.vaults = json.load(file)
        except FileNotFoundError:
            self.vaults = {}

    def save_vaults(self) -> None:
        with open('vaults.json', 'w') as file:
            json.dump(self.vaults, file, indent=4)