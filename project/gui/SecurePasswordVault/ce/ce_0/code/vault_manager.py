import json
import os
from password_encryption import PasswordEncryption

class VaultManager:
    def __init__(self):
        self.vaults = {}
        self.encryption = PasswordEncryption()
        self.load_vaults()

    def create_vault(self, name: str) -> bool:
        """Create a new vault."""
        if name in self.vaults:
            return False
        self.vaults[name] = []
        self.save_vaults()
        return True

    def add_password(self, vault_name: str, website: str, username: str, password: str) -> bool:
        """Add a password to a vault."""
        if vault_name not in self.vaults:
            return False
        encrypted_password = self.encryption.encrypt(password)
        self.vaults[vault_name].append({
            'website': website,
            'username': username,
            'password': encrypted_password
        })
        self.save_vaults()
        return True

    def edit_password(self, vault_name: str, website: str, username: str, new_password: str) -> bool:
        """Edit a password in a vault."""
        if vault_name not in self.vaults:
            return False
        for entry in self.vaults[vault_name]:
            if entry['website'] == website and entry['username'] == username:
                entry['password'] = self.encryption.encrypt(new_password)
                self.save_vaults()
                return True
        return False

    def delete_password(self, vault_name: str, website: str, username: str) -> bool:
        """Delete a password from a vault."""
        if vault_name not in self.vaults:
            return False
        self.vaults[vault_name] = [
            entry for entry in self.vaults[vault_name]
            if not (entry['website'] == website and entry['username'] == username)
        ]
        self.save_vaults()
        return True

    def search_password(self, vault_name: str, query: str) -> list:
        """Search for passwords in a vault."""
        if vault_name not in self.vaults:
            return []
        return [
            entry for entry in self.vaults[vault_name]
            if query.lower() in entry['website'].lower() or query.lower() in entry['username'].lower()
        ]

    def load_vaults(self) -> None:
        """Load vaults from JSON files."""
        if not os.path.exists('vaults'):
            os.makedirs('vaults')
        for filename in os.listdir('vaults'):
            if filename.endswith('.json'):
                with open(os.path.join('vaults', filename), 'r') as file:
                    self.vaults[filename[:-5]] = json.load(file)

    def save_vaults(self) -> None:
        """Save vaults to JSON files."""
        for vault_name, passwords in self.vaults.items():
            with open(os.path.join('vaults', f'{vault_name}.json'), 'w') as file:
                json.dump(passwords, file)