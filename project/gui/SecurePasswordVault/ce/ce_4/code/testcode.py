import unittest
from vault_manager import VaultManager
from vault import Vault
import os

class TestSecurePasswordVault(unittest.TestCase):

    def setUp(self):
        # Setup a VaultManager instance for testing
        self.vault_manager = VaultManager()
        self.test_vault_name = "test_vault"
        self.vault_manager.create_vault(self.test_vault_name)
        self.vault = self.vault_manager.load_vault(self.test_vault_name)

    def tearDown(self):
        # Clean up created test vault files
        if os.path.exists(f"{self.test_vault_name}.txt"):
            os.remove(f"{self.test_vault_name}.txt")
        if os.path.exists("vaults.txt"):
            with open("vaults.txt", "r") as file:
                lines = file.readlines()
            with open("vaults.txt", "w") as file:
                for line in lines:
                    if line.strip("\n") != self.test_vault_name:
                        file.write(line)

    def test_store_passwords_securely_with_encryption(self):
        # Functionalities 1: Store passwords securely with encryption
        account = "email"
        password = "secure_password"
        self.vault_manager.add_password(account, password, self.vault)
        self.assertIn(account, self.vault.passwords)
        self.assertNotEqual(self.vault.passwords[account], password)

    def test_create_multiple_password_vaults(self):
        # Functionalities 2: Create multiple password vaults
        new_vault_name = "new_test_vault"
        self.vault_manager.create_vault(new_vault_name)
        self.assertIn(new_vault_name, self.vault_manager.vaults)
        self.assertTrue(os.path.exists(f"{new_vault_name}.txt"))

    def test_categorize_passwords_into_different_vaults(self):
        # Functionalities 3: Categorize passwords into different vaults
        account = "social"
        password = "social_password"
        self.vault_manager.add_password(account, password, self.vault)
        self.assertIn(account, self.vault.passwords)
        # Ensure the password does not appear in another vault
        another_vault = self.vault_manager.load_vault("personal_vault")
        self.assertNotIn(account, another_vault.passwords)

    def test_add_new_passwords_to_a_vault(self):
        # Functionalities 4: Add new passwords to a vault
        account = "bank"
        password = "bank_password"
        self.vault_manager.add_password(account, password, self.vault)
        self.assertIn(account, self.vault.passwords)

    def test_edit_existing_passwords(self):
        # Functionalities 5: Edit existing passwords
        account = "email"
        old_password = "old_password"
        new_password = "new_password"
        self.vault_manager.add_password(account, old_password, self.vault)
        self.vault_manager.edit_password(account, new_password, self.vault)
        self.assertNotEqual(self.vault.passwords[account], old_password)

    def test_delete_passwords_from_a_vault(self):
        # Functionalities 6: Delete passwords from a vault
        account = "email"
        password = "email_password"
        self.vault_manager.add_password(account, password, self.vault)
        self.vault_manager.delete_password(account, self.vault)
        self.assertNotIn(account, self.vault.passwords)

    def test_analyze_password_strength(self):
        # Functionalities 7: Analyze password strength
        weak_password = "123"
        moderate_password = "12345678"
        strong_password = "123456789012"
        self.assertEqual(self.vault_manager.analyze_strength(weak_password), "Weak")
        self.assertEqual(self.vault_manager.analyze_strength(moderate_password), "Moderate")
        self.assertEqual(self.vault_manager.analyze_strength(strong_password), "Strong")

    def test_search_for_passwords_within_a_vault(self):
        # Functionalities 8: Search for passwords within a vault
        account = "email"
        password = "email_password"
        self.vault_manager.add_password(account, password, self.vault)
        result = self.vault_manager.search_password(account, self.vault)
        self.assertNotEqual(result, "Password not found.")

    def test_retrieve_stored_passwords(self):
        # Functionalities 9: Retrieve stored passwords
        account = "email"
        password = "email_password"
        self.vault_manager.add_password(account, password, self.vault)
        retrieved_password = self.vault_manager.search_password(account, self.vault)
        self.assertNotEqual(retrieved_password, "Password not found.")

if __name__ == '__main__':
    unittest.main()
