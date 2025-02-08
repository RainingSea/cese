import unittest
from datetime import datetime
from age_calculator import AgeCalculator

class TestAgeCalculator(unittest.TestCase):

    def test_user_input_of_birthdate(self):
        # Test valid birthdate input
        try:
            age_calculator = AgeCalculator("1990-05-15")
            self.assertEqual(age_calculator.birthdate.strftime("%Y-%m-%d"), "1990-05-15")
        except ValueError:
            self.fail("Valid birthdate raised ValueError unexpectedly!")

        # Test invalid birthdate input
        with self.assertRaises(ValueError):
            AgeCalculator("2023-13-01")

    def test_calculate_and_display_age(self):
        # Test age calculation for a given birthdate
        age_calculator = AgeCalculator("1990-05-15")
        age_calculator.calculate_age()
        # Assuming the current date is "2023-10-05"
        self.assertEqual(age_calculator.age_years, 33)
        self.assertEqual(age_calculator.age_months, 4)
        self.assertEqual(age_calculator.age_days, 20)

        # Test age calculation for today's birthdate
        today_str = datetime.today().strftime("%Y-%m-%d")
        age_calculator_today = AgeCalculator(today_str)
        age_calculator_today.calculate_age()
        self.assertEqual(age_calculator_today.age_years, 0)
        self.assertEqual(age_calculator_today.age_months, 0)
        self.assertEqual(age_calculator_today.age_days, 0)

    def test_calculate_days_until_next_birthday(self):
        # Test days until next birthday for a given birthdate
        age_calculator = AgeCalculator("1990-05-15")
        age_calculator.days_until_next_birthday()
        # Assuming the current date is "2023-10-05"
        self.assertEqual(age_calculator.days_until_birthday, 223)

        # Test days until next birthday for today's birthdate
        today_str = datetime.today().strftime("%Y-%m-%d")
        age_calculator_today = AgeCalculator(today_str)
        age_calculator_today.days_until_next_birthday()
        self.assertEqual(age_calculator_today.days_until_birthday, 365)

if __name__ == '__main__':
    unittest.main()
