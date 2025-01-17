import unittest
from ExpenseSplitter import ExpenseSplitter

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        self.expense_splitter = ExpenseSplitter()

    def test_input_total_amount(self):
        # Test valid total amount
        try:
            self.expense_splitter.add_expense(100.0, ["Alice", "Bob"])
            valid_input = True
        except ValueError:
            valid_input = False
        self.assertTrue(valid_input, "The application should accept valid total amount input.")

        # Test invalid total amount (negative number)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense(-50.0, ["Alice", "Bob"])

        # Test invalid total amount (non-numeric value)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense("invalid", ["Alice", "Bob"])

    def test_input_names(self):
        # Test valid names
        try:
            self.expense_splitter.add_expense(100.0, ["Alice", "Bob", "Charlie"])
            valid_input = True
        except ValueError:
            valid_input = False
        self.assertTrue(valid_input, "The application should accept valid names input.")

        # Test invalid names (empty string)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense(100.0, [""])

        # Test invalid names (special characters only)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense(100.0, ["@#$%"])

    def test_calculate_shares(self):
        # Test share calculation for $100 among Alice, Bob, Charlie
        self.expense_splitter.add_expense(100.0, ["Alice", "Bob", "Charlie"])
        shares = self.expense_splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 33.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 33.33, places=2)
        self.assertAlmostEqual(shares["Charlie"], 33.33, places=2)

        # Test share calculation for $200 among Alice, Bob
        self.expense_splitter = ExpenseSplitter()  # Reset for a new test
        self.expense_splitter.add_expense(200.0, ["Alice", "Bob"])
        shares = self.expense_splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 100.0, places=2)
        self.assertAlmostEqual(shares["Bob"], 100.0, places=2)

    def test_support_multiple_expenses(self):
        # Add multiple expenses and check if they are retained
        self.expense_splitter.add_expense(100.0, ["Alice", "Bob"])
        self.expense_splitter.add_expense(150.0, ["Alice", "Bob", "Charlie"])
        self.assertEqual(len(self.expense_splitter.expenses), 2)

        # Check if the expenses are correctly saved and loaded
        self.expense_splitter.save_data()
        self.expense_splitter = ExpenseSplitter()  # Reload data
        self.assertEqual(len(self.expense_splitter.expenses), 2)
        self.assertEqual(self.expense_splitter.expenses[0], (100.0, ["Alice", "Bob"]))
        self.assertEqual(self.expense_splitter.expenses[1], (150.0, ["Alice", "Bob", "Charlie"]))

if __name__ == '__main__':
    unittest.main()
