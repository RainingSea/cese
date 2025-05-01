import unittest
from expense_manager import ExpenseManager
from data_storage import load_expenses, load_categories

class TestExpenseManager(unittest.TestCase):

    def setUp(self):
        self.expense_manager = ExpenseManager()
        # Load initial expenses for testing
        expenses = load_expenses()
        for expense in expenses:
            self.expense_manager.add_expense(expense['date'], expense['amount'], expense['category'])

    def test_input_expenses(self):
        # Functionalities 1: Input Expenses
        self.expense_manager.add_expense("2024-11-01", 50.0, "Groceries")
        expenses = self.expense_manager.get_expenses("2024-11-01", "2024-11-01")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 50.0)
        self.assertEqual(expenses[0].category, "Groceries")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize Expenses
        self.expense_manager.add_expense("2024-11-01", 100.0, "Transportation")
        expenses = self.expense_manager.get_expenses("2024-11-01", "2024-11-01")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].category, "Transportation")

    def test_compare_expenses(self):
        # Functionalities 3: Compare Expenses Across Different Time Periods
        self.fail("not implemented")  # This functionality is not implemented in the codebase

    def test_visualize_expenses(self):
        # Functionalities 4: Provide Visual Representations of Expenses Through Charts and Graphs
        self.fail("not implemented")  # Visualization functionality is not directly testable without GUI

    def test_custom_date_ranges(self):
        # Functionalities 5: Set Custom Date Ranges for Expense Comparison
        self.expense_manager.add_expense("2024-10-15", 75.0, "Utilities")
        expenses = self.expense_manager.get_expenses("2024-10-01", "2024-10-31")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 75.0)

    def test_analyze_spending_patterns(self):
        # Functionalities 6: Analyze and Highlight Spending Patterns
        self.fail("not implemented")  # This functionality is not implemented in the codebase

if __name__ == '__main__':
    unittest.main()
