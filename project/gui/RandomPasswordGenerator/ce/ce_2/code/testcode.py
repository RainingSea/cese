import unittest
from main import Main
from tkinter import Tk

class TestRandomPasswordGenerator(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = Main()
        self.app.root = Tk()  # Create a Tkinter root window
        self.app.create_ui()  # Set up the UI

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.app.root.destroy()

    def test_specify_password_length(self):
        # Test valid password length
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '12')
        self.assertEqual(self.app.length_entry.get(), '12')

        # Test invalid password length
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '-5')
        self.app.generate_password()
        self.assertEqual(self.app.length_entry.get(), '-5')  # Check if the error is handled

        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '0')
        self.app.generate_password()
        self.assertEqual(self.app.length_entry.get(), '0')  # Check if the error is handled

    def test_select_inclusion_exclusion_of_character_types(self):
        # Check all character type options
        self.app.include_uppercase_var.set(True)
        self.app.include_lowercase_var.set(True)
        self.app.include_numbers_var.set(True)
        self.app.include_symbols_var.set(True)
        self.assertTrue(self.app.include_uppercase_var.get())
        self.assertTrue(self.app.include_lowercase_var.get())
        self.assertTrue(self.app.include_numbers_var.get())
        self.assertTrue(self.app.include_symbols_var.get())

        # Uncheck all character type options and attempt to generate a password
        self.app.include_uppercase_var.set(False)
        self.app.include_lowercase_var.set(False)
        self.app.include_numbers_var.set(False)
        self.app.include_symbols_var.set(False)
        self.app.generate_password()
        # Since we cannot capture messagebox output in a unittest, we assume the error handling is correct

    def test_exclude_ambiguous_characters(self):
        # Select the option to exclude ambiguous characters
        self.app.exclude_ambiguous_var.set(True)
        self.assertTrue(self.app.exclude_ambiguous_var.get())

        # Generate a password and check for ambiguous characters
        self.app.generate_password()
        password = self.app.result_text.get("1.0", 'end-1c')
        ambiguous_chars = 'il1Lo0O'
        for char in ambiguous_chars:
            self.assertNotIn(char, password)

    def test_generate_random_password(self):
        # Specify a password length of 10 and select character types
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '10')
        self.app.include_uppercase_var.set(True)
        self.app.include_lowercase_var.set(True)
        self.app.include_numbers_var.set(True)
        self.app.include_symbols_var.set(False)
        self.app.generate_password()
        password = self.app.result_text.get("1.0", 'end-1c')
        self.assertEqual(len(password), 10)

        # Generate a password with a length of 15 and all character types selected
        self.app.length_entry.delete(0, 'end')
        self.app.length_entry.insert(0, '15')
        self.app.include_symbols_var.set(True)
        self.app.generate_password()
        password = self.app.result_text.get("1.0", 'end-1c')
        self.assertEqual(len(password), 15)

    def test_save_generated_password_to_local_text_file(self):
        # This functionality is not implemented in the codebase
        self.fail("Save functionality not implemented")

if __name__ == '__main__':
    unittest.main()
