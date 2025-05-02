import unittest
import os
from datetime import datetime
from main import BirthdateManager, Main
import tkinter as tk

class TestAgeCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary Tkinter root for the GUI
        cls.root = tk.Tk()
        cls.app = Main(cls.root)
        cls.birthdate_manager = cls.app.birthdate_manager

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_user_input_of_birthdate(self):
        # Test valid birthdate input
        valid_birthdate = "1990-05-15"
        self.app.birthdate_entry.insert(0, valid_birthdate)
        self.app.calculate_age()
        self.assertEqual(self.app.result_label.cget("text"), f"Age: {self.birthdate_manager.calculate_age(valid_birthdate, datetime.today())}, Days until next birthday: {self.birthdate_manager.days_until_next_birthday(valid_birthdate, datetime.today())}")
        self.assertEqual(self.app.error_label.cget("text"), "")

        # Test invalid birthdate input
        invalid_birthdate = "2023-13-01"
        self.app.birthdate_entry.delete(0, tk.END)
        self.app.birthdate_entry.insert(0, invalid_birthdate)
        self.app.calculate_age()
        self.assertEqual(self.app.error_label.cget("text"), "Invalid birthdate format. Please use YYYY-MM-DD.")

    def test_calculate_and_display_age(self):
        # Test valid birthdate calculation
        valid_birthdate = "1990-05-15"
        self.app.birthdate_entry.insert(0, valid_birthdate)
        self.app.calculate_age()
        expected_age = self.birthdate_manager.calculate_age(valid_birthdate, datetime.today())
        self.assertIn("years", self.app.result_label.cget("text"))
        self.assertIn("months", self.app.result_label.cget("text"))
        self.assertIn("days", self.app.result_label.cget("text"))

        # Test age calculation for today's date
        today_birthdate = datetime.today().strftime("%Y-%m-%d")
        self.app.birthdate_entry.delete(0, tk.END)
        self.app.birthdate_entry.insert(0, today_birthdate)
        self.app.calculate_age()
        self.assertEqual(self.app.result_label.cget("text"), "Age: 0 years, 0 months, 0 days")

    def test_calculate_days_until_next_birthday(self):
        # Test days until next birthday
        valid_birthdate = "1990-05-15"
        self.app.birthdate_entry.insert(0, valid_birthdate)
        days_until_birthday = self.birthdate_manager.days_until_next_birthday(valid_birthdate, datetime.today())
        self.app.calculate_age()
        self.assertIn(f"Days until next birthday: {days_until_birthday}", self.app.result_label.cget("text"))

        # Test days until next birthday for today's date
        today_birthdate = datetime.today().strftime("%Y-%m-%d")
        self.app.birthdate_entry.delete(0, tk.END)
        self.app.birthdate_entry.insert(0, today_birthdate)
        self.app.calculate_age()
        self.assertIn("365 days", self.app.result_label.cget("text"))

if __name__ == '__main__':
    unittest.main()
