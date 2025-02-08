import unittest
from datetime import datetime
from age_calculator import AgeCalculator

class TestAgeCalculator(unittest.TestCase):

    def setUp(self):
        # Assuming today's date is 2023-10-05 for testing purposes
        self.current_date = datetime(2023, 10, 5)
        self.age_calculator_valid = AgeCalculator("1990-05-15")
        self.age_calculator_today = AgeCalculator("2023-10-05")
        self.age_calculator_invalid = None

    def test_user_input_of_birthdate(self):
        # Functionalities 1: User Input of Birthdate
        # Valid birthdate
        try:
            self.age_calculator_valid = AgeCalculator("1990-05-15")
            valid_birthdate = True
        except ValueError:
            valid_birthdate = False
        self.assertTrue(valid_birthdate, "The application should accept a valid birthdate without errors.")

        # Invalid birthdate
        with self.assertRaises(ValueError):
            self.age_calculator_invalid = AgeCalculator("2023-13-01")

    def test_calculate_and_display_age(self):
        # Functionalities 2: Calculate and Display Age
        # Valid birthdate
        age_years, age_months, age_days = self.age_calculator_valid.calculate_age()
        self.assertEqual((age_years, age_months, age_days), (33, 4, 20), "The application should display the correct age.")

        # Birthdate is today
        age_years, age_months, age_days = self.age_calculator_today.calculate_age()
        self.assertEqual((age_years, age_months, age_days), (0, 0, 0), "The application should display age as 0 years, 0 months, and 0 days.")

    def test_calculate_days_until_next_birthday(self):
        # Functionalities 3: Calculate Days Until Next Birthday
        # Valid birthdate
        days_until_birthday = self.age_calculator_valid.days_until_next_birthday()
        self.assertEqual(days_until_birthday, 223, "The application should display the correct number of days until the next birthday.")

        # Birthdate is today
        days_until_birthday = self.age_calculator_today.days_until_next_birthday()
        self.assertEqual(days_until_birthday, 365, "The application should display 365 days until the next birthday.")

if __name__ == '__main__':
    unittest.main()
