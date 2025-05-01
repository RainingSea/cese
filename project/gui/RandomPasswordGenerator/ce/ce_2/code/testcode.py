import unittest
import os
from main import PasswordGenerator

class TestPasswordGenerator(unittest.TestCase):

    def setUp(self):
        self.password_generator = PasswordGenerator()
        self.password_generator.length = 12  # Default length
        self.password_generator.include_uppercase = True
        self.password_generator.include_lowercase = True
        self.password_generator.include_numbers = True
        self.password_generator.include_symbols = True
        self.password_generator.exclude_ambiguous = False

    def test_specify_password_length(self):
        # Functionality 1: Specify Desired Password Length
        self.password_generator.length = 12
        self.assertEqual(self.password_generator.length, 12)

        with self.assertRaises(ValueError):
            self.password_generator.length = -5
            self.password_generator.generate_password()

        with self.assertRaises(ValueError):
            self.password_generator.length = 0
            self.password_generator.generate_password()

    def test_select_character_types(self):
        # Functionality 2: Select Inclusion/Exclusion of Character Types
        self.password_generator.include_uppercase = True
        self.password_generator.include_lowercase = True
        self.password_generator.include_numbers = True
        self.password_generator.include_symbols = True

        # Check if all options are selected
        self.assertTrue(self.password_generator.include_uppercase)
        self.assertTrue(self.password_generator.include_lowercase)
        self.assertTrue(self.password_generator.include_numbers)
        self.assertTrue(self.password_generator.include_symbols)

        # Uncheck all character types and attempt to generate a password
        self.password_generator.include_uppercase = False
        self.password_generator.include_lowercase = False
        self.password_generator.include_numbers = False
        self.password_generator.include_symbols = False

        with self.assertRaises(ValueError):
            self.password_generator.generate_password()

    def test_exclude_ambiguous_characters(self):
        # Functionality 3: Exclude Ambiguous Characters
        self.password_generator.exclude_ambiguous = True
        password = self.password_generator.generate_password()
        ambiguous_chars = set('l1O0')
        self.assertFalse(any(char in ambiguous_chars for char in password))

    def test_generate_random_password(self):
        # Functionality 4: Generate Random Password
        self.password_generator.length = 10
        password = self.password_generator.generate_password()
        self.assertEqual(len(password), 10)

        self.password_generator.length = 15
        self.password_generator.include_symbols = True
        password_with_symbols = self.password_generator.generate_password()
        self.assertEqual(len(password_with_symbols), 15)

    def test_save_generated_password(self):
        # Functionality 5: Save Generated Password to Local Text File
        password = self.password_generator.generate_password()
        self.password_generator.save_generated_password(password)

        # Check if the password is saved in the file
        with open('generated_passwords.txt', 'r') as f:
            saved_passwords = f.readlines()
            self.assertIn(password + '\n', saved_passwords)

    def tearDown(self):
        # Clean up the generated passwords file after tests
        if os.path.exists('generated_passwords.txt'):
            os.remove('generated_passwords.txt')

if __name__ == '__main__':
    unittest.main()
