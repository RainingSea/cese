import unittest
import os
from main import PasswordGenerator, GUI

class TestPasswordGenerator(unittest.TestCase):

    def setUp(self):
        # Set up the GUI instance
        self.gui = GUI()
        self.gui.create_widgets()

    def test_specify_password_length(self):
        # Test valid password length
        self.gui.length_entry.insert(0, '12')
        length = int(self.gui.length_entry.get())
        self.assertEqual(length, 12)

        # Test invalid password length
        self.gui.length_entry.delete(0, 'end')
        self.gui.length_entry.insert(0, '-5')
        with self.assertRaises(ValueError):
            length = int(self.gui.length_entry.get())
            if length <= 0:
                raise ValueError("Length must be a positive integer")

    def test_select_inclusion_exclusion_of_character_types(self):
        # Check all character type options
        self.gui.include_upper.set(1)
        self.gui.include_lower.set(1)
        self.gui.include_numbers.set(1)
        self.gui.include_symbols.set(1)
        self.assertTrue(self.gui.include_upper.get())
        self.assertTrue(self.gui.include_lower.get())
        self.assertTrue(self.gui.include_numbers.get())
        self.assertTrue(self.gui.include_symbols.get())

        # Uncheck all character type options
        self.gui.include_upper.set(0)
        self.gui.include_lower.set(0)
        self.gui.include_numbers.set(0)
        self.gui.include_symbols.set(0)
        with self.assertRaises(ValueError):
            if not (self.gui.include_upper.get() or self.gui.include_lower.get() or 
                    self.gui.include_numbers.get() or self.gui.include_symbols.get()):
                raise ValueError("At least one character type must be selected")

    def test_exclude_ambiguous_characters(self):
        # Select the option to exclude ambiguous characters
        self.gui.exclude_ambiguous.set(1)
        self.assertTrue(self.gui.exclude_ambiguous.get())

        # Generate a password and check for ambiguous characters
        password_generator = PasswordGenerator(10, True, True, True, True, True)
        password = password_generator.generate_password()
        ambiguous_characters = 'il1Lo0O'
        for char in ambiguous_characters:
            self.assertNotIn(char, password)

    def test_generate_random_password(self):
        # Specify a password length and character types
        self.gui.length_entry.insert(0, '10')
        self.gui.include_upper.set(1)
        self.gui.include_lower.set(1)
        self.gui.include_numbers.set(1)
        self.gui.include_symbols.set(0)

        # Generate password
        self.gui.generate_button_clicked()
        password = self.gui.output_area.get("1.0", "end-1c")
        self.assertEqual(len(password), 10)

        # Generate a password with all character types
        self.gui.length_entry.delete(0, 'end')
        self.gui.length_entry.insert(0, '15')
        self.gui.include_symbols.set(1)
        self.gui.generate_button_clicked()
        password = self.gui.output_area.get("1.0", "end-1c")
        self.assertEqual(len(password), 15)

    def test_save_generated_password_to_file(self):
        # Generate a password
        self.gui.length_entry.insert(0, '10')
        self.gui.include_upper.set(1)
        self.gui.include_lower.set(1)
        self.gui.include_numbers.set(1)
        self.gui.include_symbols.set(1)
        self.gui.generate_button_clicked()

        # Check if the password is saved to the file
        with open('generated_passwords.txt', 'r') as file:
            lines = file.readlines()
            self.assertGreater(len(lines), 0)
            self.assertIn(self.gui.output_area.get("1.0", "end-1c"), lines[-1])

if __name__ == '__main__':
    unittest.main()
