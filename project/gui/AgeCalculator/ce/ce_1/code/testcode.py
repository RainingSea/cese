import unittest
import os
from datetime import datetime
from main import Main, DateUtils, BirthdateManager

class TestAgeCalculator(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.test_file_path = 'test_birthdates.txt'
        self.birthdate_manager = BirthdateManager(self.test_file_path)
        self.app = Main(None)  # Pass None for master since we are not testing GUI

    def tearDown(self):
        # Remove the test file after tests
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_user_input_birthdate(self):
        # Test valid birthdate input
        valid_birthdate = "1990-05-15"
        self.app.entry.insert(0, valid_birthdate)
        self.app.calculate_age()  # Simulate button click
        self.assertIn(valid_birthdate, self.birthdate_manager.load_birthdates())

        # Test invalid birthdate input
        invalid_birthdate = "2023-13-01"
        self.app.entry.delete(0, tk.END)
        self.app.entry.insert(0, invalid_birthdate)
        with self.assertRaises(ValueError):
            self.app.calculate_age()  # This should raise an error

    def test_calculate_and_display_age(self):
        # Test age calculation for a valid birthdate
        birthdate = "1990-05-15"
        self.app.entry.insert(0, birthdate)
        self.app.calculate_age()  # Simulate button click
        expected_age = DateUtils.calculate_age(birthdate, datetime(2023, 10, 5))
        self.assertEqual(self.app.age_label.cget("text"), f"Age: {expected_age[0]} years, {expected_age[1]} months, {expected_age[2]} days")

        # Test age calculation for today's date
        today_birthdate = "2023-10-05"
        self.app.entry.delete(0, tk.END)
        self.app.entry.insert(0, today_birthdate)
        self.app.calculate_age()  # Simulate button click
        self.assertEqual(self.app.age_label.cget("text"), "Age: 0 years, 0 months, 0 days")

    def test_calculate_days_until_next_birthday(self):
        # Test days until next birthday for a valid birthdate
        birthdate = "1990-05-15"
        self.app.entry.insert(0, birthdate)
        days_until_birthday = DateUtils.days_until_next_birthday(birthdate, datetime(2023, 10, 5))
        self.app.calculate_age()  # Simulate button click
        self.assertEqual(self.app.days_label.cget("text"), f"Days until next birthday: {days_until_birthday}")

        # Test days until next birthday for today's date
        today_birthdate = "2023-10-05"
        self.app.entry.delete(0, tk.END)
        self.app.entry.insert(0, today_birthdate)
        self.app.calculate_age()  # Simulate button click
        self.assertEqual(self.app.days_label.cget("text"), "Days until next birthday: 365")

if __name__ == '__main__':
    unittest.main()
