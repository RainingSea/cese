import unittest
import os
from datetime import datetime
from main import Main

class TestAgeCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Main()
        self.test_birthdate_valid = "1990-05-15"
        self.test_birthdate_today = datetime.today().strftime("%Y-%m-%d")
        self.test_birthdate_invalid = "2023-13-01"

    def test_user_input_birthdate(self):
        # Functionality 1: User Input of Birthdate
        # Valid input
        self.calculator.birthdate_entry.insert(0, self.test_birthdate_valid)
        self.calculator.main()
        self.assertIn(self.test_birthdate_valid, open("birthdates.txt").read())

        # Invalid input
        self.calculator.birthdate_entry.delete(0, 'end')
        self.calculator.birthdate_entry.insert(0, self.test_birthdate_invalid)
        with self.assertRaises(ValueError):
            self.calculator.main()

    def test_calculate_and_display_age(self):
        # Functionality 2: Calculate and Display Age
        self.calculator.birthdate_entry.insert(0, self.test_birthdate_valid)
        self.calculator.main()
        expected_age = "Age: 33 years, 4 months, 20 days"  # Adjust based on the current date
        self.assertEqual(self.calculator.age_label.cget("text"), expected_age)

        # Test for birthdate that is today
        self.calculator.birthdate_entry.delete(0, 'end')
        self.calculator.birthdate_entry.insert(0, self.test_birthdate_today)
        self.calculator.main()
        expected_age_today = "Age: 0 years, 0 months, 0 days"
        self.assertEqual(self.calculator.age_label.cget("text"), expected_age_today)

    def test_calculate_days_until_next_birthday(self):
        # Functionality 3: Calculate Days Until Next Birthday
        self.calculator.birthdate_entry.insert(0, self.test_birthdate_valid)
        self.calculator.main()
        expected_days_until_birthday = 223  # Adjust based on the current date
        self.assertIn(f"Days until next birthday: {expected_days_until_birthday}", 
                      self.calculator.days_until_birthday_label.cget("text"))

        # Test for birthdate that is today
        self.calculator.birthdate_entry.delete(0, 'end')
        self.calculator.birthdate_entry.insert(0, self.test_birthdate_today)
        self.calculator.main()
        expected_days_until_birthday_today = 365
        self.assertIn(f"Days until next birthday: {expected_days_until_birthday_today}", 
                      self.calculator.days_until_birthday_label.cget("text"))

    def tearDown(self):
        # Clean up the birthdates.txt file after tests
        if os.path.exists("birthdates.txt"):
            os.remove("birthdates.txt")

if __name__ == '__main__':
    unittest.main()
