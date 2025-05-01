import unittest
import os
from main import Main, DateUtils

class TestAgeCalculator(unittest.TestCase):

    def setUp(self):
        self.app = Main()
        self.valid_birthdate = "1990-05-15"
        self.invalid_birthdate = "2023-13-01"
        self.today_birthdate = "2023-10-05"

    def test_user_input_birthdate(self):
        # Functionality 1: User Input of Birthdate
        # Test valid birthdate input
        self.app.birthdate_entry.insert(0, self.valid_birthdate)
        self.app.save_birthdate(self.valid_birthdate)
        with open('birthdates.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn(self.valid_birthdate + '\n', lines)

        # Test invalid birthdate input
        self.app.birthdate_entry.delete(0, tk.END)
        self.app.birthdate_entry.insert(0, self.invalid_birthdate)
        with self.assertRaises(ValueError):
            self.app.calculate_age()  # This should trigger the error message

    def test_calculate_and_display_age(self):
        # Functionality 2: Calculate and Display Age
        self.app.birthdate_entry.insert(0, self.valid_birthdate)
        self.app.calculate_age()
        # Assuming the current date is "2023-10-05"
        self.assertEqual(self.app.age_label.cget("text"), "Age: 33 years, 4 months, 20 days")

        # Test age calculation for today's birthdate
        self.app.birthdate_entry.delete(0, tk.END)
        self.app.birthdate_entry.insert(0, self.today_birthdate)
        self.app.calculate_age()
        self.assertEqual(self.app.age_label.cget("text"), "Age: 0 years, 0 months, 0 days")

    def test_calculate_days_until_next_birthday(self):
        # Functionality 3: Calculate Days Until Next Birthday
        self.app.birthdate_entry.insert(0, self.valid_birthdate)
        days_until_birthday = DateUtils.days_until_next_birthday(self.valid_birthdate)
        self.app.calculate_age()  # This will also calculate days until birthday
        self.assertEqual(self.app.days_until_birthday_label.cget("text"), f"Days until next birthday: {days_until_birthday}")

        # Test days until next birthday for today's birthdate
        self.app.birthdate_entry.delete(0, tk.END)
        self.app.birthdate_entry.insert(0, self.today_birthdate)
        self.app.calculate_age()
        self.assertEqual(self.app.days_until_birthday_label.cget("text"), "Days until next birthday: 365 days")

if __name__ == '__main__':
    unittest.main()
