import unittest
from password_generator import PasswordGenerator

class TestPasswordGenerator(unittest.TestCase):

    def setUp(self):
        # Default setup for PasswordGenerator
        self.generator = PasswordGenerator(12, True, True, True, True, False)

    def test_specify_password_length(self):
        # Test valid password length
        self.generator.length = 12
        password = self.generator.generate_password()
        self.assertEqual(len(password), 12)

        # Test invalid password length
        with self.assertRaises(ValueError):
            self.generator.length = -5
            self.generator.generate_password()

        with self.assertRaises(ValueError):
            self.generator.length = 0
            self.generator.generate_password()

    def test_select_inclusion_exclusion_of_character_types(self):
        # Test all character types selected
        self.generator.include_upper = True
        self.generator.include_lower = True
        self.generator.include_numbers = True
        self.generator.include_symbols = True
        password = self.generator.generate_password()
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

        # Test no character types selected
        self.generator.include_upper = False
        self.generator.include_lower = False
        self.generator.include_numbers = False
        self.generator.include_symbols = False
        with self.assertRaises(ValueError):
            self.generator.generate_password()

    def test_exclude_ambiguous_characters(self):
        # Test excluding ambiguous characters
        self.generator.exclude_ambiguous = True
        password = self.generator.generate_password()
        ambiguous_chars = 'il1Lo0O'
        self.assertFalse(any(c in ambiguous_chars for c in password))

    def test_generate_random_password(self):
        # Test generating password with specific criteria
        self.generator.length = 10
        self.generator.include_upper = True
        self.generator.include_lower = True
        self.generator.include_numbers = True
        self.generator.include_symbols = False
        password = self.generator.generate_password()
        self.assertEqual(len(password), 10)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertFalse(any(c in string.punctuation for c in password))

        # Test generating password with all character types
        self.generator.length = 15
        self.generator.include_symbols = True
        password = self.generator.generate_password()
        self.assertEqual(len(password), 15)
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_save_generated_password_to_local_text_file(self):
        # This functionality is not implemented in the codebase
        self.fail("Save generated password to local text file functionality not implemented")

if __name__ == '__main__':
    unittest.main()
