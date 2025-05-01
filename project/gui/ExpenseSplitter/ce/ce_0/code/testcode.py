import unittest
import os
from main import Main

class TestExpenseSplitter(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Main class before each test
        self.app = Main()
        # Clear the expenses.txt file before each test
        if os.path.exists('expenses.txt'):
            os.remove('expenses.txt')

    def test_input_total_amount(self):
        # Functionality 1: Input Total Amount of the Expense
        # Valid input
        self.app.amount_entry.insert(0, '100')
        self.assertEqual(self.app.amount_entry.get(), '100')

        # Invalid input (negative number)
        self.app.amount_entry.delete(0, 'end')
        self.app.amount_entry.insert(0, '-50')
        with self.assertRaises(ValueError):
            self.app.calculate_shares()

        # Invalid input (non-numeric)
        self.app.amount_entry.delete(0, 'end')
        self.app.amount_entry.insert(0, 'abc')
        with self.assertRaises(ValueError):
            self.app.calculate_shares()

    def test_input_names(self):
        # Functionality 2: Input Names of Individuals Involved in the Expense
        # Valid input
        self.app.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.assertEqual(self.app.names_entry.get(), 'Alice, Bob, Charlie')

        # Invalid input (empty string)
        self.app.names_entry.delete(0, 'end')
        self.app.names_entry.insert(0, '')
        with self.assertRaises(ValueError):
            self.app.calculate_shares()

        # Invalid input (special characters only)
        self.app.names_entry.delete(0, 'end')
        self.app.names_entry.insert(0, '@#$%')
        with self.assertRaises(ValueError):
            self.app.calculate_shares()

    def test_calculate_share(self):
        # Functionality 3: Calculate Share of Each Individual
        # Valid calculation
        self.app.amount_entry.insert(0, '100')
        self.app.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.app.calculate_shares()
        self.assertIn("Alice: $33.33", self.app.result_display.get(1.0, 'end'))
        self.assertIn("Bob: $33.33", self.app.result_display.get(1.0, 'end'))
        self.assertIn("Charlie: $33.33", self.app.result_display.get(1.0, 'end'))

        # Another valid calculation
        self.app.amount_entry.delete(0, 'end')
        self.app.amount_entry.insert(0, '200')
        self.app.names_entry.delete(0, 'end')
        self.app.names_entry.insert(0, 'Alice, Bob')
        self.app.calculate_shares()
        self.assertIn("Alice: $100.00", self.app.result_display.get(1.0, 'end'))
        self.assertIn("Bob: $100.00", self.app.result_display.get(1.0, 'end'))

    def test_multiple_expenses(self):
        # Functionality 4: Support Multiple Expenses to Manage and Split Over Time
        # First expense
        self.app.amount_entry.insert(0, '100')
        self.app.names_entry.insert(0, 'Alice, Bob')
        self.app.calculate_shares()

        # Check if the first expense is saved
        self.assertTrue(os.path.exists('expenses.txt'))
        with open('expenses.txt', 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].strip(), '100.0;Alice,Bob')

        # Second expense
        self.app.amount_entry.delete(0, 'end')
        self.app.amount_entry.insert(0, '150')
        self.app.names_entry.delete(0, 'end')
        self.app.names_entry.insert(0, 'Alice, Bob, Charlie')
        self.app.calculate_shares()

        # Check if the second expense is saved
        with open('expenses.txt', 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[1].strip(), '150.0;Alice,Bob,Charlie')

if __name__ == '__main__':
    unittest.main()
