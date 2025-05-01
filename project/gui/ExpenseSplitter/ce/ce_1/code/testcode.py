import unittest
import os
from tkinter import Tk
from ExpenseSplitter import ExpenseSplitter
from main import Main

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        # Create a temporary Tkinter root window for testing
        self.root = Tk()
        self.app = Main(self.root)
        self.expense_splitter = self.app.expense_splitter

    def tearDown(self):
        # Clean up the expenses file after each test
        if os.path.exists('expenses.txt'):
            os.remove('expenses.txt')
        self.root.destroy()

    def test_input_total_amount(self):
        # Functionality 1: Input Total Amount of the Expense
        # Valid input
        self.app.total_entry.insert(0, "100")
        self.assertEqual(float(self.app.total_entry.get()), 100.0)

        # Invalid input
        self.app.total_entry.delete(0, 'end')
        self.app.total_entry.insert(0, "-50")
        with self.assertRaises(ValueError):
            float(self.app.total_entry.get())

        self.app.total_entry.delete(0, 'end')
        self.app.total_entry.insert(0, "abc")
        with self.assertRaises(ValueError):
            float(self.app.total_entry.get())

    def test_input_names(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        # Valid input
        self.app.names_entry.insert(0, "Alice, Bob, Charlie")
        self.assertEqual(self.app.names_entry.get(), "Alice, Bob, Charlie")

        # Invalid input
        self.app.names_entry.delete(0, 'end')
        self.app.names_entry.insert(0, "")
        self.assertEqual(self.app.names_entry.get(), "")

        self.app.names_entry.delete(0, 'end')
        self.app.names_entry.insert(0, "@#$%")
        self.assertEqual(self.app.names_entry.get(), "@#$%")

    def test_calculate_share(self):
        # Functionality 3: Calculate Share of Each Individual
        self.app.total_entry.insert(0, "100")
        self.app.names_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()  # Simulate clicking the submit button

        self.app.results_text.delete(1.0, 'end')
        self.app.display_results()
        self.assertIn("Alice: 33.33", self.app.results_text.get(1.0, 'end'))
        self.assertIn("Bob: 33.33", self.app.results_text.get(1.0, 'end'))
        self.assertIn("Charlie: 33.33", self.app.results_text.get(1.0, 'end'))

        # Test another expense
        self.app.total_entry.delete(0, 'end')
        self.app.names_entry.delete(0, 'end')
        self.app.total_entry.insert(0, "200")
        self.app.names_entry.insert(0, "Alice, Bob")
        self.app.submit_expense()  # Simulate clicking the submit button

        self.app.results_text.delete(1.0, 'end')
        self.app.display_results()
        self.assertIn("Alice: 100.00", self.app.results_text.get(1.0, 'end'))
        self.assertIn("Bob: 100.00", self.app.results_text.get(1.0, 'end'))

    def test_support_multiple_expenses(self):
        # Functionality 4: Support Multiple Expenses to Manage and Split Over Time
        self.app.total_entry.insert(0, "100")
        self.app.names_entry.insert(0, "Alice, Bob")
        self.app.submit_expense()  # Simulate clicking the submit button

        self.app.total_entry.delete(0, 'end')
        self.app.names_entry.delete(0, 'end')
        self.app.total_entry.insert(0, "150")
        self.app.names_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()  # Simulate clicking the submit button

        self.app.results_text.delete(1.0, 'end')
        self.app.display_results()
        self.assertIn("Alice: 125.00", self.app.results_text.get(1.0, 'end'))
        self.assertIn("Bob: 125.00", self.app.results_text.get(1.0, 'end'))
        self.assertIn("Charlie: 50.00", self.app.results_text.get(1.0, 'end'))

if __name__ == '__main__':
    unittest.main()
