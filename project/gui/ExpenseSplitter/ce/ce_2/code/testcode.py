import unittest
from main import ExpenseSplitter, GUI
import tkinter as tk

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        self.expense_splitter = ExpenseSplitter()
        self.gui = GUI(self.expense_splitter)
        self.gui.root.update()

    def test_input_total_amount(self):
        # Test valid total expense amount
        self.gui.total_expense_entry.insert(0, "100")
        self.gui.submit_expense()
        self.assertEqual(self.expense_splitter.expenses[-1][0], 100.0)

        # Test invalid total expense amount
        self.gui.total_expense_entry.delete(0, tk.END)
        self.gui.total_expense_entry.insert(0, "invalid")
        with self.assertRaises(ValueError):
            self.gui.submit_expense()

    def test_input_names(self):
        # Test valid names
        self.gui.names_entry.insert(0, "Alice, Bob, Charlie")
        self.gui.submit_expense()
        self.assertEqual(self.expense_splitter.expenses[-1][1], ["Alice", "Bob", "Charlie"])

        # Test invalid names (empty string)
        self.gui.names_entry.delete(0, tk.END)
        self.gui.names_entry.insert(0, "")
        self.gui.submit_expense()
        self.assertEqual(self.expense_splitter.expenses[-1][1], [])

    def test_calculate_share(self):
        # Test calculation of shares
        self.expense_splitter.add_expense(100, ["Alice", "Bob", "Charlie"])
        shares = self.expense_splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 33.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 33.33, places=2)
        self.assertAlmostEqual(shares["Charlie"], 33.33, places=2)

        self.expense_splitter.add_expense(200, ["Alice", "Bob"])
        shares = self.expense_splitter.calculate_shares()
        self.assertAlmostEqual(shares["Alice"], 133.33, places=2)
        self.assertAlmostEqual(shares["Bob"], 133.33, places=2)

    def test_support_multiple_expenses(self):
        # Test multiple expenses
        self.expense_splitter.add_expense(100, ["Alice", "Bob"])
        self.expense_splitter.add_expense(150, ["Alice", "Bob", "Charlie"])
        self.assertEqual(len(self.expense_splitter.expenses), 4)  # Including initial expenses from file
        self.assertEqual(self.expense_splitter.expenses[-1], (150, ["Alice", "Bob", "Charlie"]))

if __name__ == '__main__':
    unittest.main()
