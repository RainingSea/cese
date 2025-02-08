import os
from cryptography.fernet import Fernet
from vault import Vault

class VaultManager:
    def __init__(self) -> None:
        self.vaults = []
        self.load_vaults()

    def load_vaults(self) -> None:
        if os.path.exists("vaults.txt"):
            with open("vaults.txt", "r") as file:
                self.vaults = [line.strip() for line in file]

    def create_vault(self, vault_name: str) -> None:
        if vault_name not in self.vaults:
            self.vaults.append(vault_name)
            with open("vaults.txt", "a") as file:
                file.write(f"{vault_name}\n")

    def load_vault(self, vault_name: str) -> Vault:
        return Vault(vault_name)

    def add_password(self, account: str, password: str, vault: Vault) -> None:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        vault.passwords[account] = encrypted_password
        vault.save_passwords()

    def edit_password(self, account: str, new_password: str, vault: Vault) -> None:
        if account in vault.passwords:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()
            vault.passwords[account] = encrypted_password
            vault.save_passwords()

    def delete_password(self, account: str, vault: Vault) -> None:
        if account in vault.passwords:
            del vault.passwords[account]
            vault.save_passwords()

    def search_password(self, account: str, vault: Vault) -> str:
        return vault.passwords.get(account, "Password not found.")

    def analyze_strength(self, password: str) -> str:
        if len(password) < 8:
            return "Weak"
        elif len(password) < 12:
            return "Moderate"
        else:
            return "Strong"