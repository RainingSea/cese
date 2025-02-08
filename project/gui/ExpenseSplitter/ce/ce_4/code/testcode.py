import unittest
from tkinter import Tk
from main import ExpenseSplitter, GUI

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        self.splitter = ExpenseSplitter()
        self.gui = GUI(self.splitter)
        self.gui.root.update()

    def tearDown(self):
        self.gui.root.destroy()

    def test_input_total_amount(self):
        # Test valid total expense amount
        self.gui.amount_entry.delete(0, 'end')
        self.gui.amount_entry.insert(0, '100')
        self.assertEqual(self.gui.amount_entry.get(), '100')

        # Test invalid total expense amount (negative number)
        self.gui.amount_entry.delete(0, 'end')
        self.gui.amount_entry.insert(0, '-50')
        self.gui.submit_expense()
        self.assertIn("Input Error", self.gui.root.tk.call('tk', 'messageBox', 'show', 'error'))

        # Test invalid total expense amount (non-numeric value)
        self.gui.amount_entry.delete(0, 'end')
        self.gui.amount_entry.insert(0, 'abc')
        self.gui.submit_expense()
        self.assertIn("Input Error", self.gui.root.tk.call('tk', 'messageBox', 'show', 'error'))

    def test_input_names(self):
        # Test valid names
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.assertEqual(self.gui.names_entry.get(), 'Alice, Bob, Charlie')

        # Test invalid names (empty string)
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, '')
        self.gui.submit_expense()
        self.assertIn("Input Error", self.gui.root.tk.call('tk', 'messageBox', 'show', 'error'))

        # Test invalid names (special characters only)
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, '@#$%')
        self.gui.submit_expense()
        self.assertIn("Input Error", self.gui.root.tk.call('tk', 'messageBox', 'show', 'error'))

    def test_calculate_share(self):
        # Test calculation with $100 and names "Alice, Bob, Charlie"
        self.gui.amount_entry.delete(0, 'end')
        self.gui.amount_entry.insert(0, '100')
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.gui.submit_expense()
        expected_output = "Alice: 33.33\nBob: 33.33\nCharlie: 33.33\n"
        self.assertEqual(self.gui.shares_display.get("1.0", "end-1c"), expected_output)

        # Test calculation with $200 and names "Alice, Bob"
        self.gui.amount_entry.delete(0, 'end')
        self.gui.amount_entry.insert(0, '200')
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, 'Alice, Bob')
        self.gui.submit_expense()
        expected_output = "Alice: 100.00\nBob: 100.00\n"
        self.assertEqual(self.gui.shares_display.get("1.0", "end-1c"), expected_output)

    def test_multiple_expenses(self):
        # Test managing multiple expenses
        self.gui.amount_entry.delete(0, 'end')
        self.gui.amount_entry.insert(0, '100')
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, 'Alice, Bob')
        self.gui.submit_expense()

        self.gui.amount_entry.delete(0, 'end')
        self.gui.amount_entry.insert(0, '150')
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.gui.submit_expense()

        # Check if both expenses are saved correctly
        self.splitter.load_expenses()
        self.assertEqual(len(self.splitter.expenses), 2)
        self.assertIn((100.0, ['Alice', 'Bob']), self.splitter.expenses)
        self.assertIn((150.0, ['Alice', 'Bob', 'Charlie']), self.splitter.expenses)

if __name__ == '__main__':
    unittest.main()
