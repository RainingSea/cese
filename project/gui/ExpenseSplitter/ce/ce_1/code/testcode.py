import unittest
from tkinter import Tk
from GUI import GUI
from ExpenseSplitter import ExpenseSplitter

class TestExpenseSplitterGUI(unittest.TestCase):

    def setUp(self):
        self.splitter = ExpenseSplitter()
        self.gui = GUI(self.splitter)
        self.gui.root.update()  # Ensure the GUI is updated before tests

    def tearDown(self):
        self.gui.root.destroy()

    def test_input_total_amount(self):
        # Test valid total expense amount
        self.gui.total_entry.insert(0, "100")
        self.assertEqual(self.gui.total_entry.get(), "100")

        # Test invalid total expense amount
        self.gui.total_entry.delete(0, 'end')
        self.gui.total_entry.insert(0, "-50")
        self.gui.calculate_button_clicked()
        self.assertIn("Input Error", self.gui.root.tk.call("tk_messageBox", "show", "error", "Input Error", "Please enter valid total and names."))

        self.gui.total_entry.delete(0, 'end')
        self.gui.total_entry.insert(0, "abc")
        self.gui.calculate_button_clicked()
        self.assertIn("Input Error", self.gui.root.tk.call("tk_messageBox", "show", "error", "Input Error", "Please enter valid total and names."))

    def test_input_names(self):
        # Test valid names
        self.gui.names_entry.insert(0, "Alice, Bob, Charlie")
        self.assertEqual(self.gui.names_entry.get(), "Alice, Bob, Charlie")

        # Test invalid names
        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, "")
        self.gui.calculate_button_clicked()
        self.assertIn("Input Error", self.gui.root.tk.call("tk_messageBox", "show", "error", "Input Error", "Please enter valid total and names."))

        self.gui.names_entry.delete(0, 'end')
        self.gui.names_entry.insert(0, "@@@")
        self.gui.calculate_button_clicked()
        self.assertIn("Input Error", self.gui.root.tk.call("tk_messageBox", "show", "error", "Input Error", "Please enter valid total and names."))

    def test_calculate_share(self):
        # Test calculation with $100 and names "Alice, Bob, Charlie"
        self.gui.total_entry.insert(0, "100")
        self.gui.names_entry.insert(0, "Alice, Bob, Charlie")
        self.gui.calculate_button_clicked()
        result = self.gui.result_display.get("1.0", "end-1c")
        expected_result = "Alice: 33.33\nBob: 33.33\nCharlie: 33.33"
        self.assertEqual(result.strip(), expected_result)

        # Test calculation with $200 and names "Alice, Bob"
        self.gui.total_entry.delete(0, 'end')
        self.gui.names_entry.delete(0, 'end')
        self.gui.total_entry.insert(0, "200")
        self.gui.names_entry.insert(0, "Alice, Bob")
        self.gui.calculate_button_clicked()
        result = self.gui.result_display.get("1.0", "end-1c")
        expected_result = "Alice: 100.00\nBob: 100.00"
        self.assertEqual(result.strip(), expected_result)

    def test_support_multiple_expenses(self):
        # Test saving and loading multiple expenses
        self.gui.total_entry.insert(0, "100")
        self.gui.names_entry.insert(0, "Alice, Bob")
        self.gui.calculate_button_clicked()
        self.gui.save_button_clicked()

        self.gui.total_entry.delete(0, 'end')
        self.gui.names_entry.delete(0, 'end')
        self.gui.total_entry.insert(0, "150")
        self.gui.names_entry.insert(0, "Alice, Bob, Charlie")
        self.gui.calculate_button_clicked()
        self.gui.save_button_clicked()

        # Load expenses and check if they are retained
        self.gui.load_button_clicked()
        self.assertEqual(len(self.splitter.expenses), 2)
        self.assertEqual(self.splitter.expenses[0], (100.0, ['Alice', 'Bob']))
        self.assertEqual(self.splitter.expenses[1], (150.0, ['Alice', 'Bob', 'Charlie']))

if __name__ == '__main__':
    unittest.main()
