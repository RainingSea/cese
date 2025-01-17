import json
from cryptography.fernet import Fernet
from password import Password

class VaultManager:
    def __init__(self) -> None:
        self.vaults = {}
        self.load_vaults()

    def create_vault(self, vault_name: str) -> None:
        if vault_name not in self.vaults:
            self.vaults[vault_name] = {'passwords': []}
            self.save_vaults()

    def add_password(self, vault_name: str, service: str, username: str, password: str) -> None:
        if vault_name in self.vaults:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted_password = cipher.encrypt(password.encode()).decode()
            new_password = Password(service, username, encrypted_password)
            self.vaults[vault_name]['passwords'].append(new_password.__dict__)
            self.save_vaults()

    def edit_password(self, vault_name: str, service: str, new_username: str, new_password: str) -> None:
        if vault_name in self.vaults:
            for pwd in self.vaults[vault_name]['passwords']:
                if pwd['service'] == service:
                    key = Fernet.generate_key()
                    cipher = Fernet(key)
                    encrypted_password = cipher.encrypt(new_password.encode()).decode()
                    pwd['username'] = new_username
                    pwd['encrypted_password'] = encrypted_password
                    self.save_vaults()
                    break

    def delete_password(self, vault_name: str, service: str) -> None:
        if vault_name in self.vaults:
            self.vaults[vault_name]['passwords'] = [
                pwd for pwd in self.vaults[vault_name]['passwords'] if pwd['service'] != service
            ]
            self.save_vaults()

    def search_password(self, vault_name: str, query: str) -> list:
        if vault_name in self.vaults:
            return [
                pwd for pwd in self.vaults[vault_name]['passwords']
                if query in pwd['service'] or query in pwd['username']
            ]
        return []

    def analyze_password_strength(self, password: str) -> str:
        if len(password) < 6:
            return "Weak"
        elif len(password) < 12:
            return "Moderate"
        else:
            return "Strong"

    def load_vaults(self) -> None:
        try:
            with open('vaults.json', 'r') as file:
                self.vaults = json.load(file)
        except FileNotFoundError:
            self.vaults = {}

    def save_vaults(self) -> None:
        with open('vaults.json', 'w') as file:
            json.dump(self.vaults, file, indent=4)