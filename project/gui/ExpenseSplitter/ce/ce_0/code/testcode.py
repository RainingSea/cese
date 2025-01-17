import unittest
from ExpenseSplitter import ExpenseSplitter

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        self.splitter = ExpenseSplitter()

    def test_input_total_amount_valid(self):
        # Functionality 1: Input Total Amount of the Expense
        try:
            self.splitter.add_expense(100.0, ["Alice", "Bob", "Charlie"])
            self.assertTrue(True)  # If no exception, the test passes
        except ValueError:
            self.fail("add_expense() raised ValueError unexpectedly!")

    def test_input_total_amount_invalid(self):
        # Functionality 1: Input Total Amount of the Expense
        with self.assertRaises(ValueError):
            self.splitter.add_expense(-100.0, ["Alice", "Bob", "Charlie"])

    def test_input_names_valid(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        try:
            self.splitter.add_expense(50.0, ["Alice", "Bob", "Charlie"])
            self.assertTrue(True)  # If no exception, the test passes
        except ValueError:
            self.fail("add_expense() raised ValueError unexpectedly!")

    def test_input_names_invalid(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        with self.assertRaises(ValueError):
            self.splitter.add_expense(50.0, ["", "@@@", "###"])

    def test_calculate_shares(self):
        # Functionality 3: Calculate Share of Each Individual
        self.splitter.add_expense(100.0, ["Alice", "Bob", "Charlie"])
        shares = self.splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 33.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 33.33, places=2)
        self.assertAlmostEqual(shares["Charlie"], 33.33, places=2)

        self.splitter.add_expense(200.0, ["Alice", "Bob"])
        shares = self.splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 100.0, places=2)
        self.assertAlmostEqual(shares["Bob"], 100.0, places=2)

    def test_multiple_expenses(self):
        # Functionality 4: Support Multiple Expenses to Manage and Split Over Time
        self.splitter.add_expense(100.0, ["Alice", "Bob"])
        self.splitter.add_expense(150.0, ["Alice", "Bob", "Charlie"])
        shares = self.splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 83.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 83.33, places=2)
        self.assertAlmostEqual(shares["Charlie"], 50.0, places=2)

if __name__ == '__main__':
    unittest.main()
