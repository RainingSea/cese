import unittest
import os
from expense_manager import ExpenseManager

class TestExpenseManager(unittest.TestCase):

    def setUp(self):
        # Create a new instance of ExpenseManager for each test
        self.expense_manager = ExpenseManager()
        # Clear existing expenses for testing
        self.expense_manager.expenses = []
        with open('expenses.txt', 'w') as f:
            f.write("")  # Clear the expenses file

    def test_input_expenses(self):
        # Functionalities 1: Input Expenses
        self.expense_manager.add_expense("2024-11-01", 50.0, "groceries")
        self.assertEqual(len(self.expense_manager.expenses), 1)
        self.assertEqual(self.expense_manager.expenses[0].get_details(), "2024-11-01, 50.0, groceries")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize Expenses
        self.expense_manager.add_expense("2024-11-01", 50.0, "groceries")
        expense = self.expense_manager.expenses[0]
        self.assertEqual(expense.category, "groceries")
        # Change category
        expense.category = "transportation"
        self.assertEqual(expense.category, "transportation")

    def test_compare_expenses(self):
        # Functionalities 3: Compare Expenses Across Different Time Periods
        self.expense_manager.add_expense("2024-01-01", 100.0, "groceries")
        self.expense_manager.add_expense("2024-02-01", 150.0, "groceries")
        expenses_january = self.expense_manager.get_expenses("2024-01-01", "2024-01-31")
        expenses_february = self.expense_manager.get_expenses("2024-02-01", "2024-02-29")
        self.assertEqual(len(expenses_january), 1)
        self.assertEqual(len(expenses_february), 1)

    def test_visualize_expenses(self):
        # Functionalities 4: Provide Visual Representations of Expenses Through Charts and Graphs
        self.expense_manager.add_expense("2024-11-01", 50.0, "groceries")
        self.expense_manager.add_expense("2024-11-02", 30.0, "transportation")
        # Here we would normally check if the visualization works, but we can't assert GUI output
        # So we will just fail this test point as it's not implemented
        self.fail("Visualization functionality is not implemented.")

    def test_custom_date_ranges(self):
        # Functionalities 5: Set Custom Date Ranges for Expense Comparison
        self.expense_manager.add_expense("2024-10-01", 50.0, "groceries")
        self.expense_manager.add_expense("2024-10-15", 30.0, "transportation")
        expenses = self.expense_manager.get_expenses("2024-10-01", "2024-10-31")
        self.assertEqual(len(expenses), 2)

    def test_analyze_spending_patterns(self):
        # Functionalities 6: Analyze and Highlight Spending Patterns
        self.expense_manager.add_expense("2024-10-01", 50.0, "groceries")
        self.expense_manager.add_expense("2024-10-15", 30.0, "groceries")
        # Here we would normally analyze the spending patterns, but we can't assert this without implementation
        self.fail("Spending pattern analysis functionality is not implemented.")

if __name__ == '__main__':
    unittest.main()
