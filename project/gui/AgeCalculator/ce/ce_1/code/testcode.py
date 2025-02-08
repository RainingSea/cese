import unittest
from age_calculator import AgeCalculator
from datetime import datetime

class TestAgeCalculator(unittest.TestCase):

    def setUp(self):
        self.age_calculator = AgeCalculator()

    def test_user_input_of_birthdate(self):
        # Test with a valid birthdate
        valid_birthdate = "1990-05-15"
        try:
            self.age_calculator.set_birthdate(valid_birthdate)
            self.assertEqual(self.age_calculator.birthdate, valid_birthdate)
        except Exception as e:
            self.fail(f"Valid birthdate input failed with exception: {e}")

        # Test with an invalid birthdate
        invalid_birthdate = "2023-13-01"
        with self.assertRaises(ValueError):
            self.age_calculator.set_birthdate(invalid_birthdate)

    def test_calculate_and_display_age(self):
        # Test with a valid birthdate
        self.age_calculator.set_birthdate("1990-05-15")
        expected_age = "You are 33 years old."  # Assuming the current date is 2023-10-05
        self.assertEqual(self.age_calculator.calculate_age(), expected_age)

        # Test with a birthdate that is today
        today = datetime.today().strftime("%Y-%m-%d")
        self.age_calculator.set_birthdate(today)
        expected_age_today = "You are 0 years old."
        self.assertEqual(self.age_calculator.calculate_age(), expected_age_today)

    def test_calculate_days_until_next_birthday(self):
        # Test with a valid birthdate
        self.age_calculator.set_birthdate("1990-05-15")
        expected_days = 223  # Assuming the current date is 2023-10-05
        self.assertEqual(self.age_calculator.days_until_next_birthday(), expected_days)

        # Test with a birthdate that is today
        today = datetime.today().strftime("%Y-%m-%d")
        self.age_calculator.set_birthdate(today)
        expected_days_today = 365
        self.assertEqual(self.age_calculator.days_until_next_birthday(), expected_days_today)

if __name__ == '__main__':
    unittest.main()
