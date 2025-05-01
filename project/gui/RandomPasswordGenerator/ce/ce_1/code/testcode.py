import unittest
import os
import subprocess
from main import Main

class TestRandomPasswordGenerator(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = Main()
        self.app.root.withdraw()  # Hide the main window for testing

    def test_password_length(self):
        # Functionality 1: Specify Desired Password Length
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '12')
        self.app.generate_password()
        self.assertEqual(self.app.password_length, 12)

        # Test invalid length
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '-5')
        with self.assertRaises(ValueError):
            self.app.generate_password()

        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '0')
        with self.assertRaises(ValueError):
            self.app.generate_password()

    def test_character_types_selection(self):
        # Functionality 2: Select Inclusion/Exclusion of Character Types
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.symbols_var.set(True)
        self.app.generate_password()
        self.assertIn(self.app.result_label.cget("text"), self.app.result_label.cget("text"))

        # Uncheck all character types
        self.app.uppercase_var.set(False)
        self.app.lowercase_var.set(False)
        self.app.numbers_var.set(False)
        self.app.symbols_var.set(False)
        self.app.generate_password()
        self.assertEqual(self.app.result_label.cget("text"), "No character types selected!")

    def test_exclude_ambiguous_characters(self):
        # Functionality 3: Exclude Ambiguous Characters
        self.app.ambiguous_var.set(True)
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.symbols_var.set(True)
        self.app.generate_password()
        password = self.app.result_label.cget("text")
        self.assertNotIn('l', password)
        self.assertNotIn('1', password)
        self.assertNotIn('O', password)
        self.assertNotIn('0', password)

    def test_generate_random_password(self):
        # Functionality 4: Generate Random Password
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '10')
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.generate_password()
        password = self.app.result_label.cget("text")
        self.assertEqual(len(password), 10)

        # Test with all character types
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '15')
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.symbols_var.set(True)
        self.app.generate_password()
        password = self.app.result_label.cget("text")
        self.assertEqual(len(password), 15)

    def test_save_generated_password(self):
        # Functionality 5: Save Generated Password to Local Text File
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '12')
        self.app.uppercase_var.set(True)
        self.app.lowercase_var.set(True)
        self.app.numbers_var.set(True)
        self.app.symbols_var.set(True)
        self.app.generate_password()
        password = self.app.result_label.cget("text")

        # Save password
        self.app.save_password(password)

        # Check if password is saved in the file
        with open('passwords.txt', 'r') as f:
            saved_passwords = f.readlines()
            self.assertIn(password + '\n', saved_passwords)

    def tearDown(self):
        # Clean up the generated passwords file after tests
        if os.path.exists('passwords.txt'):
            os.remove('passwords.txt')

if __name__ == '__main__':
    unittest.main()
