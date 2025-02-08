import unittest
from expense import ExpenseSplitter
from main import ExpenseSplitterApp
import tkinter as tk

class TestExpenseSplitterApp(unittest.TestCase):

    def setUp(self):
        # Set up the application environment
        self.root = tk.Tk()
        self.app = ExpenseSplitterApp(self.root)

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    def test_input_total_amount_valid(self):
        # Test valid total expense amount input
        self.app.amount_entry.insert(0, "100")
        self.app.submit_expense()
        self.assertEqual(self.app.splitter.expenses[-1].amount, 100.0)

    def test_input_total_amount_invalid(self):
        # Test invalid total expense amount input
        self.app.amount_entry.insert(0, "-100")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

        self.app.amount_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "abc")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

    def test_input_names_valid(self):
        # Test valid names input
        self.app.names_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()
        self.assertEqual(self.app.splitter.expenses[-1].names, ["Alice", "Bob", "Charlie"])

    def test_input_names_invalid(self):
        # Test invalid names input
        self.app.names_entry.insert(0, "")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

        self.app.names_entry.delete(0, tk.END)
        self.app.names_entry.insert(0, "@@@")
        with self.assertRaises(ValueError):
            self.app.submit_expense()

    def test_calculate_share(self):
        # Test share calculation
        self.app.amount_entry.insert(0, "100")
        self.app.names_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()
        shares = self.app.splitter.calculate_shares(self.app.splitter.expenses[-1])
        self.assertEqual(shares, {"Alice": 33.33, "Bob": 33.33, "Charlie": 33.33})

        self.app.amount_entry.delete(0, tk.END)
        self.app.names_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "200")
        self.app.names_entry.insert(0, "Alice, Bob")
        self.app.submit_expense()
        shares = self.app.splitter.calculate_shares(self.app.splitter.expenses[-1])
        self.assertEqual(shares, {"Alice": 100.0, "Bob": 100.0})

    def test_multiple_expenses(self):
        # Test managing multiple expenses
        self.app.amount_entry.insert(0, "100")
        self.app.names_entry.insert(0, "Alice, Bob")
        self.app.submit_expense()

        self.app.amount_entry.delete(0, tk.END)
        self.app.names_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "150")
        self.app.names_entry.insert(0, "Alice, Bob, Charlie")
        self.app.submit_expense()

        self.assertEqual(len(self.app.splitter.expenses), 2)
        self.assertEqual(self.app.splitter.expenses[0].amount, 100.0)
        self.assertEqual(self.app.splitter.expenses[1].amount, 150.0)

if __name__ == '__main__':
    unittest.main()
