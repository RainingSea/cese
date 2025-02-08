import unittest
from expenses import ExpenseComparator
import os
import json

class TestExpenseComparator(unittest.TestCase):

    def setUp(self):
        # Setup a fresh instance of ExpenseComparator and a temporary expenses file
        self.expense_comparator = ExpenseComparator()
        self.expense_comparator.expenses = []  # Clear any loaded expenses
        self.expenses_file = 'expenses.json'
        if os.path.exists(self.expenses_file):
            os.remove(self.expenses_file)

    def tearDown(self):
        # Clean up the expenses file after each test
        if os.path.exists(self.expenses_file):
            os.remove(self.expenses_file)

    def test_input_expenses(self):
        # Functionalities 1: Input Expenses
        self.expense_comparator.add_expense("2024-11-01", "Groceries", 50.0)
        self.assertEqual(len(self.expense_comparator.expenses), 1)
        self.assertEqual(self.expense_comparator.expenses[0].category, "Groceries")
        self.assertEqual(self.expense_comparator.expenses[0].amount, 50.0)

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize Expenses
        self.expense_comparator.add_expense("2024-11-01", "Transportation", 20.0)
        self.assertEqual(self.expense_comparator.expenses[0].category, "Transportation")

    def test_compare_expenses_across_different_time_periods(self):
        # Functionalities 3: Compare Expenses Across Different Time Periods
        self.expense_comparator.add_expense("2024-01-15", "Food", 100.0)
        self.expense_comparator.add_expense("2024-02-15", "Food", 150.0)
        jan_expenses = self.expense_comparator.compare_expenses("2024-01-01", "2024-01-31")
        feb_expenses = self.expense_comparator.compare_expenses("2024-02-01", "2024-02-28")
        self.assertEqual(jan_expenses.get("Food", 0), 100.0)
        self.assertEqual(feb_expenses.get("Food", 0), 150.0)

    def test_provide_visual_representations_of_expenses(self):
        # Functionalities 4: Provide Visual Representations of Expenses Through Charts and Graphs
        self.expense_comparator.add_expense("2024-01-15", "Food", 100.0)
        data = self.expense_comparator.compare_expenses("2024-01-01", "2024-01-31")
        self.expense_comparator.generate_chart(data)
        # Note: Actual chart display cannot be tested in a unit test; this is a placeholder

    def test_set_custom_date_ranges_for_expense_comparison(self):
        # Functionalities 5: Set Custom Date Ranges for Expense Comparison
        self.expense_comparator.add_expense("2024-10-15", "Utilities", 75.0)
        self.expense_comparator.add_expense("2024-11-15", "Utilities", 100.0)
        oct_expenses = self.expense_comparator.compare_expenses("2024-10-01", "2024-10-31")
        self.assertEqual(oct_expenses.get("Utilities", 0), 75.0)

    def test_analyze_and_highlight_spending_patterns(self):
        # Functionalities 6: Analyze and Highlight Spending Patterns
        self.fail("not implemented")  # Placeholder for spending pattern analysis

if __name__ == '__main__':
    unittest.main()
