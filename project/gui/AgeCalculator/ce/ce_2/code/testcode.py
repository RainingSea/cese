import unittest
from birthdate_manager import BirthdateManager
from datetime import datetime
import os

class TestBirthdateManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_path = "birthdates.txt"
        cls.birthdate_manager = BirthdateManager(cls.file_path)

    def setUp(self):
        # Clear the birthdates.txt file before each test
        open(self.file_path, 'w').close()

    def test_user_input_of_birthdate(self):
        # Functionality 1: User Input of Birthdate
        # Valid input
        self.birthdate_manager.save_birthdate("1990-05-15")
        self.assertIn("1990-05-15", self.birthdate_manager.load_birthdates())

        # Invalid input (not tested directly since we don't have GUI)
        with self.assertRaises(ValueError):
            self.birthdate_manager.calculate_age("2023-13-01")

    def test_calculate_and_display_age(self):
        # Functionality 2: Calculate and Display Age
        # Valid input
        self.birthdate_manager.save_birthdate("1990-05-15")
        age = self.birthdate_manager.calculate_age("1990-05-15")
        self.assertEqual(age, (33, 4, 20))  # Assuming today's date is 2023-10-05

        # Input a birthdate that is today
        age_today = self.birthdate_manager.calculate_age(datetime.today().strftime("%Y-%m-%d"))
        self.assertEqual(age_today, (0, 0, 0))

    def test_calculate_days_until_next_birthday(self):
        # Functionality 3: Calculate Days Until Next Birthday
        # Valid input
        self.birthdate_manager.save_birthdate("1990-05-15")
        days_until_birthday = self.birthdate_manager.days_until_next_birthday("1990-05-15")
        self.assertEqual(days_until_birthday, 223)  # Assuming today's date is 2023-10-05

        # Input a birthdate that is today
        days_until_birthday_today = self.birthdate_manager.days_until_next_birthday(datetime.today().strftime("%Y-%m-%d"))
        self.assertEqual(days_until_birthday_today, 365)

    def test_invalid_date_handling(self):
        # Test for invalid date handling
        with self.assertRaises(ValueError):
            self.birthdate_manager.calculate_age("2023-13-01")

if __name__ == '__main__':
    unittest.main()
