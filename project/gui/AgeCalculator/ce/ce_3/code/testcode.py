import unittest
from tkinter import Tk
from ui import UI

class TestAgeCalculator(unittest.TestCase):

    def setUp(self):
        # Initialize the UI for testing
        self.ui = UI()
        self.ui.root.update()

    def tearDown(self):
        # Destroy the UI after each test
        self.ui.root.destroy()

    def test_user_input_of_birthdate(self):
        # Test valid birthdate input
        self.ui.birthdate_entry.insert(0, "1990-05-15")
        self.ui.calculate_button.invoke()
        self.ui.root.update()
        self.assertIn("Your age:", self.ui.results_label.cget("text"))

        # Test invalid birthdate input
        self.ui.birthdate_entry.delete(0, 'end')
        self.ui.birthdate_entry.insert(0, "2023-13-01")
        self.ui.calculate_button.invoke()
        self.ui.root.update()
        # Check if an error message box is displayed
        # Since we cannot directly capture messagebox output, we assume the test fails if no valid age is displayed
        self.assertNotIn("Your age:", self.ui.results_label.cget("text"))

    def test_calculate_and_display_age(self):
        # Test age calculation for a specific date
        self.ui.birthdate_entry.delete(0, 'end')
        self.ui.birthdate_entry.insert(0, "1990-05-15")
        self.ui.calculate_button.invoke()
        self.ui.root.update()
        self.assertIn("Your age: 33 years", self.ui.results_label.cget("text"))

        # Test age calculation for today's date
        self.ui.birthdate_entry.delete(0, 'end')
        self.ui.birthdate_entry.insert(0, "2023-10-05")
        self.ui.calculate_button.invoke()
        self.ui.root.update()
        self.assertIn("Your age: 0 years", self.ui.results_label.cget("text"))

    def test_calculate_days_until_next_birthday(self):
        # Test days until next birthday for a specific date
        self.ui.birthdate_entry.delete(0, 'end')
        self.ui.birthdate_entry.insert(0, "1990-05-15")
        self.ui.calculate_button.invoke()
        self.ui.root.update()
        self.assertIn("Days until next birthday: 223", self.ui.results_label.cget("text"))

        # Test days until next birthday for today's date
        self.ui.birthdate_entry.delete(0, 'end')
        self.ui.birthdate_entry.insert(0, "2023-10-05")
        self.ui.calculate_button.invoke()
        self.ui.root.update()
        self.assertIn("Days until next birthday: 365", self.ui.results_label.cget("text"))

if __name__ == '__main__':
    unittest.main()
