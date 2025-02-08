import unittest
import tkinter as tk
from ExpenseSplitter import ExpenseSplitter
from main import ExpenseSplitterApp

class TestExpenseSplitterApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = ExpenseSplitterApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_input_total_amount(self):
        # Test valid total amount
        self.app.amount_entry.insert(0, "100")
        self.app.submit_expense()
        self.assertEqual(self.app.splitter.expenses[-1].total_amount, 100.0)

        # Test invalid total amount (non-numeric)
        self.app.amount_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "abc")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

        # Test invalid total amount (negative number)
        self.app.amount_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "-50")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

    def test_input_names_of_individuals(self):
        # Test valid names
        self.app.participants_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()
        self.assertEqual(self.app.splitter.expenses[-1].participants, ["Alice", "Bob", "Charlie"])

        # Test invalid names (empty string)
        self.app.participants_entry.delete(0, tk.END)
        self.app.participants_entry.insert(0, "")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

        # Test invalid names (special characters)
        self.app.participants_entry.delete(0, tk.END)
        self.app.participants_entry.insert(0, "@@@")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

    def test_calculate_share_of_each_individual(self):
        # Test calculation with $100 and "Alice, Bob, Charlie"
        self.app.amount_entry.insert(0, "100")
        self.app.participants_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()
        shares = self.app.splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 33.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 33.33, places=2)
        self.assertAlmostEqual(shares["Charlie"], 33.33, places=2)

        # Test calculation with $200 and "Alice, Bob"
        self.app.amount_entry.delete(0, tk.END)
        self.app.participants_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "200")
        self.app.participants_entry.insert(0, "Alice, Bob")
        self.app.submit_expense()
        shares = self.app.splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 100.0, places=2)
        self.assertAlmostEqual(shares["Bob"], 100.0, places=2)

    def test_support_multiple_expenses(self):
        # Add first expense
        self.app.amount_entry.insert(0, "100")
        self.app.participants_entry.insert(0, "Alice, Bob")
        self.app.submit_expense()

        # Add second expense
        self.app.amount_entry.delete(0, tk.END)
        self.app.participants_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "150")
        self.app.participants_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()

        # Check if both expenses are recorded
        self.assertEqual(len(self.app.splitter.expenses), 2)
        self.assertEqual(self.app.splitter.expenses[0].total_amount, 100.0)
        self.assertEqual(self.app.splitter.expenses[1].total_amount, 150.0)

if __name__ == '__main__':
    unittest.main()
