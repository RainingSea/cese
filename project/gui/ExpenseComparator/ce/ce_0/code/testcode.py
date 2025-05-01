import unittest
import os
from main import ExpenseManager

class TestExpenseManager(unittest.TestCase):

    def setUp(self):
        self.manager = ExpenseManager()
        # Clear the expenses.txt file before each test
        open('expenses.txt', 'w').close()

    def test_input_expenses(self):
        # Functionalities 1: Input Expenses
        self.manager.add_expense("2024-11-01", "Groceries", 50.00)
        expenses = self.manager.get_expenses("2024-11-01", "2024-11-01")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].category, "Groceries")
        self.assertEqual(expenses[0].amount, 50.00)

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize Expenses
        self.manager.add_expense("2024-11-01", "Transportation", 20.00)
        expenses = self.manager.get_expenses("2024-11-01", "2024-11-01")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].category, "Transportation")

    def test_compare_expenses(self):
        # Functionalities 3: Compare Expenses Across Different Time Periods
        self.manager.add_expense("2024-01-15", "Food", 100.00)
        self.manager.add_expense("2024-02-15", "Food", 150.00)
        january_expenses = self.manager.get_expenses("2024-01-01", "2024-01-31")
        february_expenses = self.manager.get_expenses("2024-02-01", "2024-02-29")
        self.assertEqual(sum(exp.amount for exp in january_expenses), 100.00)
        self.assertEqual(sum(exp.amount for exp in february_expenses), 150.00)

    def test_visualize_expenses(self):
        # Functionalities 4: Provide Visual Representations of Expenses Through Charts and Graphs
        self.manager.add_expense("2024-11-01", "Groceries", 50.00)
        self.manager.add_expense("2024-11-02", "Groceries", 30.00)
        self.manager.visualize_expenses()  # This will show a plot, but we can't assert on visual output

    def test_custom_date_ranges(self):
        # Functionalities 5: Set Custom Date Ranges for Expense Comparison
        self.manager.add_expense("2024-10-01", "Utilities", 100.00)
        self.manager.add_expense("2024-10-15", "Utilities", 150.00)
        expenses = self.manager.get_expenses("2024-10-01", "2024-10-31")
        self.assertEqual(len(expenses), 2)

    def test_analyze_spending_patterns(self):
        # Functionalities 6: Analyze and Highlight Spending Patterns
        self.manager.add_expense("2024-10-01", "Groceries", 100.00)
        self.manager.add_expense("2024-10-15", "Groceries", 110.00)
        # Here we would need to implement a method to analyze spending patterns
        self.fail("Spending pattern analysis not implemented")

if __name__ == '__main__':
    unittest.main()
