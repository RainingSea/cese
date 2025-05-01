import unittest
import json
import os
from tkinter import Tk
from main import Main, ExpenseManager

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        # Create a temporary Tkinter root window for testing
        self.root = Tk()
        self.app = Main(self.root)
        self.expense_manager = ExpenseManager()

    def tearDown(self):
        # Clean up the expenses.json file after tests
        if os.path.exists('expenses.json'):
            os.remove('expenses.json')
        self.root.destroy()

    def test_input_total_amount(self):
        # Functionality 1: Input Total Amount of the Expense
        # Valid input
        self.app.total_entry.insert(0, '100')
        self.assertEqual(self.app.total_entry.get(), '100')

        # Invalid input (non-numeric)
        self.app.total_entry.delete(0, 'end')
        self.app.total_entry.insert(0, 'invalid')
        with self.assertRaises(ValueError):
            float(self.app.total_entry.get())

    def test_input_names(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        # Valid input
        self.app.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.assertEqual(self.app.names_entry.get(), 'Alice, Bob, Charlie')

        # Invalid input (empty string)
        self.app.names_entry.delete(0, 'end')
        self.app.names_entry.insert(0, '')
        self.assertEqual(self.app.names_entry.get(), '')

    def test_calculate_share(self):
        # Functionality 3: Calculate Share of Each Individual
        self.app.total_entry.insert(0, '100')
        self.app.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.app.submit_expense()  # Submit the expense
        self.app.display_shares()   # Calculate shares
        self.assertIn('Alice: 33.33', self.app.shares_display.get(1.0, 'end'))
        self.assertIn('Bob: 33.33', self.app.shares_display.get(1.0, 'end'))
        self.assertIn('Charlie: 33.33', self.app.shares_display.get(1.0, 'end'))

        # Second test case
        self.app.total_entry.delete(0, 'end')
        self.app.names_entry.delete(0, 'end')
        self.app.total_entry.insert(0, '200')
        self.app.names_entry.insert(0, 'Alice, Bob')
        self.app.submit_expense()  # Submit the expense
        self.app.display_shares()   # Calculate shares
        self.assertIn('Alice: 100.00', self.app.shares_display.get(1.0, 'end'))
        self.assertIn('Bob: 100.00', self.app.shares_display.get(1.0, 'end'))

    def test_multiple_expenses(self):
        # Functionality 4: Support Multiple Expenses to Manage and Split Over Time
        self.app.total_entry.insert(0, '100')
        self.app.names_entry.insert(0, 'Alice, Bob')
        self.app.submit_expense()  # Submit the first expense
        self.app.display_shares()   # Calculate shares

        self.app.total_entry.delete(0, 'end')
        self.app.names_entry.delete(0, 'end')
        self.app.total_entry.insert(0, '150')
        self.app.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.app.submit_expense()  # Submit the second expense
        self.app.display_shares()   # Calculate shares

        # Check if both expenses are retained
        self.assertEqual(len(self.expense_manager.expenses), 2)

if __name__ == '__main__':
    unittest.main()
