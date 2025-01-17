import unittest
import tkinter as tk
from main import UI
from PasswordGenerator import PasswordGenerator

class TestRandomPasswordGenerator(unittest.TestCase):

    def setUp(self):
        self.app = UI()
        self.app.root.update()

    def tearDown(self):
        self.app.root.destroy()

    def test_specify_desired_password_length(self):
        # Test valid password length
        self.app.length_entry.delete(0, tk.END)
        self.app.length_entry.insert(0, '12')
        self.app.generate_and_display_password()
        self.assertEqual(self.app.password_generator.length, 12)

        # Test invalid password length
        self.app.length_entry.delete(0, tk.END)
        self.app.length_entry.insert(0, '-5')
        with self.assertRaises(ValueError):
            self.app.generate_and_display_password()

        self.app.length_entry.delete(0, tk.END)
        self.app.length_entry.insert(0, '0')
        with self.assertRaises(ValueError):
            self.app.generate_and_display_password()

    def test_select_inclusion_exclusion_of_character_types(self):
        # Check all character type options
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.symbols_var.set(True)
        self.app.generate_and_display_password()
        self.assertTrue(self.app.password_generator.include_uppercase)
        self.assertTrue(self.app.password_generator.include_lowercase)
        self.assertTrue(self.app.password_generator.include_numbers)
        self.assertTrue(self.app.password_generator.include_symbols)

        # Uncheck all character type options
        self.app.uppercase_var.set(False)
        self.app.lowercase_var.set(False)
        self.app.numbers_var.set(False)
        self.app.symbols_var.set(False)
        with self.assertRaises(ValueError):
            self.app.generate_and_display_password()

    def test_exclude_ambiguous_characters(self):
        # Select exclude ambiguous characters
        self.app.exclude_ambiguous_var.set(True)
        self.app.generate_and_display_password()
        password = self.app.password_display.get(1.0, tk.END).strip()
        self.assertNotIn('l', password)
        self.assertNotIn('1', password)
        self.assertNotIn('O', password)
        self.assertNotIn('0', password)

    def test_generate_random_password(self):
        # Generate password with specific criteria
        self.app.length_entry.delete(0, tk.END)
        self.app.length_entry.insert(0, '10')
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.symbols_var.set(False)
        self.app.generate_and_display_password()
        password = self.app.password_display.get(1.0, tk.END).strip()
        self.assertEqual(len(password), 10)

        # Generate password with all character types
        self.app.length_entry.delete(0, tk.END)
        self.app.length_entry.insert(0, '15')
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.symbols_var.set(True)
        self.app.generate_and_display_password()
        password = self.app.password_display.get(1.0, tk.END).strip()
        self.assertEqual(len(password), 15)

    def test_save_generated_password_to_local_text_file(self):
        # Generate and save password
        self.app.generate_and_display_password()
        password = self.app.password_display.get(1.0, tk.END).strip()
        self.app.save_generated_password()

        # Check if password is saved in the file
        with open('generated_passwords.txt', 'r') as f:
            saved_passwords = f.read().strip().split('\n')
            self.assertIn(password, saved_passwords)

if __name__ == '__main__':
    unittest.main()
