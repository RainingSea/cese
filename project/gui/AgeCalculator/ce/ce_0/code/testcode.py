import unittest
from datetime import datetime
from age_calculator import AgeCalculator

class TestAgeCalculator(unittest.TestCase):

    def test_user_input_of_birthdate(self):
        # Test valid birthdate input
        try:
            age_calculator = AgeCalculator("1990-05-15")
            self.assertIsInstance(age_calculator, AgeCalculator)
        except ValueError:
            self.fail("AgeCalculator raised ValueError unexpectedly!")

        # Test invalid birthdate input
        with self.assertRaises(ValueError):
            AgeCalculator("2023-13-01")

    def test_calculate_and_display_age(self):
        # Test age calculation for a given birthdate
        age_calculator = AgeCalculator("1990-05-15")
        expected_age = {'years': 33, 'months': 4, 'days': 20}  # Assuming current date is 2023-10-05
        self.assertEqual(age_calculator.calculate_age(), expected_age)

        # Test age calculation for today's birthdate
        today_str = datetime.today().strftime('%Y-%m-%d')
        age_calculator_today = AgeCalculator(today_str)
        expected_age_today = {'years': 0, 'months': 0, 'days': 0}
        self.assertEqual(age_calculator_today.calculate_age(), expected_age_today)

    def test_calculate_days_until_next_birthday(self):
        # Test days until next birthday for a given birthdate
        age_calculator = AgeCalculator("1990-05-15")
        expected_days = 223  # Assuming current date is 2023-10-05
        self.assertEqual(age_calculator.days_until_next_birthday(), expected_days)

        # Test days until next birthday for today's birthdate
        today_str = datetime.today().strftime('%Y-%m-%d')
        age_calculator_today = AgeCalculator(today_str)
        expected_days_today = 365
        self.assertEqual(age_calculator_today.days_until_next_birthday(), expected_days_today)

if __name__ == '__main__':
    unittest.main()
