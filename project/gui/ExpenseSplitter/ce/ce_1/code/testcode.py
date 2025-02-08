import unittest
from ExpenseSplitter import ExpenseSplitter

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        self.splitter = ExpenseSplitter()

    def test_input_total_amount(self):
        # Test valid total expense amount
        self.splitter.add_expense(100.0, ["Alice", "Bob"])
        shares = self.splitter.calculate_shares()
        self.assertEqual(shares, {"Alice": 50.0, "Bob": 50.0})

        # Test invalid total expense amount (negative)
        with self.assertRaises(ValueError):
            self.splitter.add_expense(-100.0, ["Alice", "Bob"])

        # Test invalid total expense amount (non-numeric)
        with self.assertRaises(ValueError):
            self.splitter.add_expense("invalid", ["Alice", "Bob"])

    def test_input_names_of_individuals(self):
        # Test valid names
        self.splitter.add_expense(100.0, ["Alice", "Bob", "Charlie"])
        shares = self.splitter.calculate_shares()
        self.assertEqual(shares, {"Alice": 33.33, "Bob": 33.33, "Charlie": 33.33})

        # Test invalid names (empty string)
        with self.assertRaises(ValueError):
            self.splitter.add_expense(100.0, [""])

        # Test invalid names (special characters)
        with self.assertRaises(ValueError):
            self.splitter.add_expense(100.0, ["@#$%"])

    def test_calculate_share_of_each_individual(self):
        # Test calculation for $100 split among Alice, Bob, Charlie
        self.splitter.add_expense(100.0, ["Alice", "Bob", "Charlie"])
        shares = self.splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 33.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 33.33, places=2)
        self.assertAlmostEqual(shares["Charlie"], 33.33, places=2)

        # Test calculation for $200 split among Alice, Bob
        self.splitter.add_expense(200.0, ["Alice", "Bob"])
        shares = self.splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 133.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 133.33, places=2)

    def test_support_multiple_expenses(self):
        # Add first expense
        self.splitter.add_expense(100.0, ["Alice", "Bob"])
        shares = self.splitter.calculate_shares()
        self.assertEqual(shares, {"Alice": 50.0, "Bob": 50.0})

        # Add second expense
        self.splitter.add_expense(150.0, ["Alice", "Bob", "Charlie"])
        shares = self.splitter.calculate_shares()
        self.assertEqual(shares, {"Alice": 125.0, "Bob": 125.0, "Charlie": 50.0})

        # Check if both expenses are retained
        self.assertEqual(len(self.splitter.expenses), 2)

if __name__ == '__main__':
    unittest.main()
