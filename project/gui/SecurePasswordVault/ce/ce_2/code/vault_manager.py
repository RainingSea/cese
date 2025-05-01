import json
from password import Password

class VaultManager:
    def __init__(self):
        self.vaults = {}

    def create_vault(self, name: str) -> None:
        self.vaults[name] = []

    def add_password(self, vault_name: str, password: Password) -> None:
        if vault_name in self.vaults:
            self.vaults[vault_name].append(password)

    def edit_password(self, vault_name: str, password_id: int, new_password: Password) -> None:
        if vault_name in self.vaults and 0 <= password_id < len(self.vaults[vault_name]):
            self.vaults[vault_name][password_id] = new_password

    def delete_password(self, vault_name: str, password_id: int) -> None:
        if vault_name in self.vaults and 0 <= password_id < len(self.vaults[vault_name]):
            del self.vaults[vault_name][password_id]

    def search_password(self, vault_name: str, query: str) -> list:
        if vault_name in self.vaults:
            return [pwd for pwd in self.vaults[vault_name] if query in pwd.account_name]

    def analyze_password_strength(self, password: str) -> str:
        if len(password) < 6:
            return "Weak"
        elif len(password) < 12:
            return "Moderate"
        else:
            return "Strong"