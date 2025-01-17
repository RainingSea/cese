import unittest
from vault_manager import VaultManager
from password import Password

class TestVaultManager(unittest.TestCase):

    def setUp(self):
        self.vault_manager = VaultManager()
        self.vault_manager.vaults = {}  # Start with an empty vault for testing

    def test_store_passwords_securely(self):
        # Functionalities 1: Store passwords securely with encryption
        password_data = {'website': 'example.com', 'username': 'user', 'password': 'pass1234'}
        self.vault_manager.create_vault('TestVault')
        self.vault_manager.add_password('TestVault', password_data)
        
        encrypted_passwords = self.vault_manager.vaults['TestVault']
        self.assertEqual(len(encrypted_passwords), 1)
        self.assertNotEqual(encrypted_passwords[0], 'pass1234')  # Ensure password is encrypted

    def test_create_multiple_password_vaults(self):
        # Functionalities 2: Create multiple password vaults
        self.assertTrue(self.vault_manager.create_vault('Vault1'))
        self.assertTrue(self.vault_manager.create_vault('Vault2'))
        self.assertIn('Vault1', self.vault_manager.vaults)
        self.assertIn('Vault2', self.vault_manager.vaults)

    def test_categorize_passwords_into_different_vaults(self):
        # Functionalities 3: Categorize passwords into different vaults
        password_data1 = {'website': 'example1.com', 'username': 'user1', 'password': 'pass1234'}
        password_data2 = {'website': 'example2.com', 'username': 'user2', 'password': 'pass5678'}
        
        self.vault_manager.create_vault('Vault1')
        self.vault_manager.create_vault('Vault2')
        
        self.vault_manager.add_password('Vault1', password_data1)
        self.vault_manager.add_password('Vault2', password_data2)
        
        self.assertEqual(len(self.vault_manager.vaults['Vault1']), 1)
        self.assertEqual(len(self.vault_manager.vaults['Vault2']), 1)
        self.assertNotEqual(self.vault_manager.vaults['Vault1'], self.vault_manager.vaults['Vault2'])

    def test_add_new_passwords_to_a_vault(self):
        # Functionalities 4: Add new passwords to a vault
        password_data = {'website': 'example.com', 'username': 'user', 'password': 'pass1234'}
        self.vault_manager.create_vault('TestVault')
        self.assertTrue(self.vault_manager.add_password('TestVault', password_data))
        self.assertEqual(len(self.vault_manager.vaults['TestVault']), 1)

    def test_edit_existing_passwords(self):
        # Functionalities 5: Edit existing passwords
        password_data = {'website': 'example.com', 'username': 'user', 'password': 'pass1234'}
        new_data = {'website': 'example.com', 'username': 'user', 'password': 'newpass5678'}
        
        self.vault_manager.create_vault('TestVault')
        self.vault_manager.add_password('TestVault', password_data)
        
        self.assertTrue(self.vault_manager.edit_password('TestVault', 0, new_data))
        encrypted_password = self.vault_manager.vaults['TestVault'][0]
        password = Password(**new_data)
        self.assertEqual(encrypted_password, password.encrypt_password())

    def test_delete_passwords_from_a_vault(self):
        # Functionalities 6: Delete passwords from a vault
        password_data = {'website': 'example.com', 'username': 'user', 'password': 'pass1234'}
        
        self.vault_manager.create_vault('TestVault')
        self.vault_manager.add_password('TestVault', password_data)
        
        self.assertTrue(self.vault_manager.delete_password('TestVault', 0))
        self.assertEqual(len(self.vault_manager.vaults['TestVault']), 0)

    def test_analyze_password_strength(self):
        # Functionalities 7: Analyze password strength
        self.assertEqual(self.vault_manager.analyze_password_strength('short'), 'Weak')
        self.assertEqual(self.vault_manager.analyze_password_strength('moderate1'), 'Moderate')
        self.assertEqual(self.vault_manager.analyze_password_strength('verystrongpassword123'), 'Strong')

    def test_search_for_passwords_within_a_vault(self):
        # Functionalities 8: Search for passwords within a vault
        password_data = {'website': 'example.com', 'username': 'user', 'password': 'pass1234'}
        
        self.vault_manager.create_vault('TestVault')
        self.vault_manager.add_password('TestVault', password_data)
        
        results = self.vault_manager.search_password('TestVault', 'example.com')
        self.assertEqual(len(results), 1)

    def test_retrieve_stored_passwords(self):
        # Functionalities 9: Retrieve stored passwords
        password_data = {'website': 'example.com', 'username': 'user', 'password': 'pass1234'}
        
        self.vault_manager.create_vault('TestVault')
        self.vault_manager.add_password('TestVault', password_data)
        
        encrypted_password = self.vault_manager.vaults['TestVault'][0]
        password = Password(**password_data)
        self.assertEqual(password.decrypt_password(encrypted_password), 'pass1234')

if __name__ == '__main__':
    unittest.main()
