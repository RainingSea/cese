import unittest
from unittest.mock import patch
from password_generator import PasswordGenerator
from user_preferences import UserPreferences
import tkinter as tk
from main import GUI

class TestRandomPasswordGenerator(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.gui.root.update()

    def tearDown(self):
        self.gui.root.destroy()

    def test_specify_password_length(self):
        # Test valid password length
        self.gui.length_entry.delete(0, tk.END)
        self.gui.length_entry.insert(0, '12')
        self.assertEqual(self.gui.length_entry.get(), '12')

        # Test invalid password length
        self.gui.length_entry.delete(0, tk.END)
        self.gui.length_entry.insert(0, '-5')
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.gui.on_generate_button_click()
            mock_showerror.assert_called_with("Error", "Length must be a positive integer")

        self.gui.length_entry.delete(0, tk.END)
        self.gui.length_entry.insert(0, '0')
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.gui.on_generate_button_click()
            mock_showerror.assert_called_with("Error", "Length must be a positive integer")

    def test_select_inclusion_exclusion_of_character_types(self):
        # Test selecting all character types
        self.gui.uppercase_var.set(True)
        self.gui.lowercase_var.set(True)
        self.gui.numbers_var.set(True)
        self.gui.symbols_var.set(True)
        self.assertTrue(self.gui.uppercase_var.get())
        self.assertTrue(self.gui.lowercase_var.get())
        self.assertTrue(self.gui.numbers_var.get())
        self.assertTrue(self.gui.symbols_var.get())

        # Test unchecking all character types
        self.gui.uppercase_var.set(False)
        self.gui.lowercase_var.set(False)
        self.gui.numbers_var.set(False)
        self.gui.symbols_var.set(False)
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.gui.on_generate_button_click()
            mock_showerror.assert_called_with("Error", "At least one character type must be selected")

    def test_exclude_ambiguous_characters(self):
        # Test excluding ambiguous characters
        self.gui.ambiguous_var.set(True)
        self.assertTrue(self.gui.ambiguous_var.get())

        # Generate a password and check for ambiguous characters
        self.gui.length_entry.delete(0, tk.END)
        self.gui.length_entry.insert(0, '10')
        self.gui.uppercase_var.set(True)
        self.gui.lowercase_var.set(True)
        self.gui.numbers_var.set(True)
        self.gui.symbols_var.set(True)
        self.gui.on_generate_button_click()
        password = self.gui.password_display.get(1.0, tk.END).strip()
        for char in 'il1Lo0O':
            self.assertNotIn(char, password)

    def test_generate_random_password(self):
        # Test generating a password with specific criteria
        self.gui.length_entry.delete(0, tk.END)
        self.gui.length_entry.insert(0, '10')
        self.gui.uppercase_var.set(True)
        self.gui.lowercase_var.set(True)
        self.gui.numbers_var.set(True)
        self.gui.symbols_var.set(False)
        self.gui.on_generate_button_click()
        password = self.gui.password_display.get(1.0, tk.END).strip()
        self.assertEqual(len(password), 10)

        # Test generating a password with all character types
        self.gui.length_entry.delete(0, tk.END)
        self.gui.length_entry.insert(0, '15')
        self.gui.uppercase_var.set(True)
        self.gui.lowercase_var.set(True)
        self.gui.numbers_var.set(True)
        self.gui.symbols_var.set(True)
        self.gui.on_generate_button_click()
        password = self.gui.password_display.get(1.0, tk.END).strip()
        self.assertEqual(len(password), 15)

    def test_save_generated_password_to_local_text_file(self):
        # Test saving generated password to a file
        self.gui.length_entry.delete(0, tk.END)
        self.gui.length_entry.insert(0, '10')
        self.gui.uppercase_var.set(True)
        self.gui.lowercase_var.set(True)
        self.gui.numbers_var.set(True)
        self.gui.symbols_var.set(False)
        self.gui.on_generate_button_click()
        password = self.gui.password_display.get(1.0, tk.END).strip()

        with open('generated_passwords.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn(password + '\n', lines)

if __name__ == '__main__':
    unittest.main()
