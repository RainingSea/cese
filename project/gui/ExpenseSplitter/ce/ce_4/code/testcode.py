import unittest
from main import ExpenseSplitter, GUI
import tkinter as tk

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        self.expense_splitter = ExpenseSplitter()
        self.gui = GUI(self.expense_splitter)
        self.gui.root.update_idletasks()

    def tearDown(self):
        self.gui.root.destroy()

    def test_input_total_amount_valid(self):
        # Functionality 1: Input Total Amount of the Expense
        self.gui.amount_entry.insert(0, "100")
        self.assertEqual(self.gui.amount_entry.get(), "100")

    def test_input_total_amount_invalid(self):
        # Functionality 1: Input Total Amount of the Expense
        self.gui.amount_entry.insert(0, "-100")
        self.gui.calculate()
        self.assertEqual(self.gui.results_label.cget("text"), "")
        
        self.gui.amount_entry.delete(0, tk.END)
        self.gui.amount_entry.insert(0, "abc")
        self.gui.calculate()
        self.assertEqual(self.gui.results_label.cget("text"), "")

    def test_input_names_valid(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        self.gui.names_entry.insert(0, "Alice, Bob, Charlie")
        self.assertEqual(self.gui.names_entry.get(), "Alice, Bob, Charlie")

    def test_input_names_invalid(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        self.gui.names_entry.insert(0, "")
        self.gui.calculate()
        self.assertEqual(self.gui.results_label.cget("text"), "")

        self.gui.names_entry.delete(0, tk.END)
        self.gui.names_entry.insert(0, "@@@")
        self.gui.calculate()
        self.assertEqual(self.gui.results_label.cget("text"), "")

    def test_calculate_share(self):
        # Functionality 3: Calculate Share of Each Individual
        self.gui.amount_entry.insert(0, "100")
        self.gui.names_entry.insert(0, "Alice, Bob, Charlie")
        self.gui.calculate()
        self.assertIn("Alice: $33.33", self.gui.results_label.cget("text"))
        self.assertIn("Bob: $33.33", self.gui.results_label.cget("text"))
        self.assertIn("Charlie: $33.33", self.gui.results_label.cget("text"))

        self.gui.amount_entry.delete(0, tk.END)
        self.gui.names_entry.delete(0, tk.END)
        self.gui.amount_entry.insert(0, "200")
        self.gui.names_entry.insert(0, "Alice, Bob")
        self.gui.calculate()
        self.assertIn("Alice: $100.00", self.gui.results_label.cget("text"))
        self.assertIn("Bob: $100.00", self.gui.results_label.cget("text"))

    def test_manage_multiple_expenses(self):
        # Functionality 4: Support Multiple Expenses to Manage and Split Over Time
        self.gui.amount_entry.insert(0, "100")
        self.gui.names_entry.insert(0, "Alice, Bob")
        self.gui.calculate()
        self.gui.load_previous_expenses()
        self.assertIn("100, Alice, Bob", self.gui.previous_expenses_text.get(1.0, tk.END))

        self.gui.amount_entry.delete(0, tk.END)
        self.gui.names_entry.delete(0, tk.END)
        self.gui.amount_entry.insert(0, "150")
        self.gui.names_entry.insert(0, "Alice, Bob, Charlie")
        self.gui.calculate()
        self.gui.load_previous_expenses()
        self.assertIn("150, Alice, Bob, Charlie", self.gui.previous_expenses_text.get(1.0, tk.END))

if __name__ == '__main__':
    unittest.main()
