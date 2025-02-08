import unittest
from expense_splitter import ExpenseSplitter
import os

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        # Setup before each test
        self.expense_splitter = ExpenseSplitter()
        # Ensure the expenses.txt file is empty before each test
        open('expenses.txt', 'w').close()

    def tearDown(self):
        # Clean up after each test
        if os.path.exists('expenses.txt'):
            os.remove('expenses.txt')

    def test_input_total_amount_of_expense(self):
        # Functionality 1: Input Total Amount of the Expense
        # Valid amount
        self.expense_splitter.add_expense(100.00, ["John", "Doe", "Jane"])
        self.assertEqual(self.expense_splitter.expenses[-1][0], 100.00)

        # Invalid amount (non-numeric)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense(float("invalid"), ["John", "Doe", "Jane"])

        # Invalid amount (negative)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense(-100.00, ["John", "Doe", "Jane"])

    def test_input_names_of_individuals_involved_in_the_expense(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        # Valid names
        self.expense_splitter.add_expense(100.00, ["Alice", "Bob", "Charlie"])
        self.assertEqual(self.expense_splitter.expenses[-1][1], ["Alice", "Bob", "Charlie"])

        # Invalid names (empty string)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense(100.00, [""])

        # Invalid names (special characters only)
        with self.assertRaises(ValueError):
            self.expense_splitter.add_expense(100.00, ["@#$%", "^&*()"])

    def test_calculate_share_of_each_individual(self):
        # Functionality 3: Calculate Share of Each Individual
        # Test case 1
        self.expense_splitter.add_expense(100.00, ["Alice", "Bob", "Charlie"])
        shares = self.expense_splitter.calculate_shares()
        expected_shares = {"Alice": 33.33, "Bob": 33.33, "Charlie": 33.33}
        for name, share in shares.items():
            self.assertAlmostEqual(share, expected_shares[name], places=2)

        # Test case 2
        self.expense_splitter.add_expense(200.00, ["Alice", "Bob"])
        shares = self.expense_splitter.calculate_shares()
        expected_shares = {"Alice": 100.00, "Bob": 100.00}
        for name, share in shares.items():
            self.assertAlmostEqual(share, expected_shares[name], places=2)

    def test_support_multiple_expenses_to_manage_and_split_over_time(self):
        # Functionality 4: Support Multiple Expenses to Manage and Split Over Time
        # Add first expense
        self.expense_splitter.add_expense(100.00, ["Alice", "Bob"])
        self.expense_splitter.save_expenses()

        # Add second expense
        self.expense_splitter.add_expense(150.00, ["Alice", "Bob", "Charlie"])
        self.expense_splitter.save_expenses()

        # Load expenses and verify
        self.expense_splitter.load_expenses()
        self.assertEqual(len(self.expense_splitter.expenses), 2)
        self.assertEqual(self.expense_splitter.expenses[0], (100.00, ["Alice", "Bob"]))
        self.assertEqual(self.expense_splitter.expenses[1], (150.00, ["Alice", "Bob", "Charlie"]))

if __name__ == '__main__':
    unittest.main()
