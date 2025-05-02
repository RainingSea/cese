import unittest
from datetime import datetime
from birthdate_manager import BirthdateManager

class TestBirthdateManager(unittest.TestCase):

    def setUp(self):
        self.file_path = "birthdates.txt"
        self.birthdate_manager = BirthdateManager(self.file_path)

    def test_user_input_birthdate(self):
        # Functionality 1: User Input of Birthdate
        valid_birthdate = "1990-05-15"
        invalid_birthdate = "2023-13-01"

        # Test valid input
        self.assertTrue(self.birthdate_manager.validate_birthdate(valid_birthdate), 
                        "Valid birthdate should be accepted.")

        # Test invalid input
        self.assertFalse(self.birthdate_manager.validate_birthdate(invalid_birthdate), 
                         "Invalid birthdate should not be accepted.")

    def test_calculate_and_display_age(self):
        # Functionality 2: Calculate and Display Age
        birthdate = "1990-05-15"
        today = datetime(2023, 10, 5)  # Assuming today's date for testing

        # Calculate age
        years, months, days = self.birthdate_manager.calculate_age(birthdate, today)
        self.assertEqual((years, months, days), (33, 4, 20), 
                         "Age calculation should be correct.")

        # Test age for today
        birthdate_today = "2023-10-05"
        years, months, days = self.birthdate_manager.calculate_age(birthdate_today, today)
        self.assertEqual((years, months, days), (0, 0, 0), 
                         "Age for today should be 0 years, 0 months, and 0 days.")

    def test_calculate_days_until_next_birthday(self):
        # Functionality 3: Calculate Days Until Next Birthday
        birthdate = "1990-05-15"
        today = datetime(2023, 10, 5)  # Assuming today's date for testing

        # Calculate days until next birthday
        days_until_birthday = self.birthdate_manager.days_until_next_birthday(birthdate, today)
        self.assertEqual(days_until_birthday, 223, 
                         "Days until next birthday should be correct.")

        # Test days until birthday for today
        birthdate_today = "2023-10-05"
        days_until_birthday_today = self.birthdate_manager.days_until_next_birthday(birthdate_today, today)
        self.assertEqual(days_until_birthday_today, 365, 
                         "Days until next birthday from today should be 365.")

if __name__ == '__main__':
    unittest.main()
