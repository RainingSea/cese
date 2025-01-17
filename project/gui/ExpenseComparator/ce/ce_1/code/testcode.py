import unittest
from ExpenseComparator import ExpenseComparator
from datetime import datetime

class TestExpenseComparator(unittest.TestCase):

    def setUp(self):
        self.expense_comparator = ExpenseComparator()

    def test_input_expenses(self):
        # Functionalities 1: Input Expenses
        self.expense_comparator.add_expense(50.0, "Groceries", "2024-11-01")
        expenses = self.expense_comparator.get_expenses()
        self.assertTrue(any(expense.amount == 50.0 and expense.category == "Groceries" and expense.date == "2024-11-01" for expense in expenses))

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize Expenses
        self.expense_comparator.add_expense(20.0, "Transportation", "2024-11-01")
        expenses = self.expense_comparator.get_expenses()
        self.assertTrue(any(expense.category == "Transportation" for expense in expenses))

    def test_compare_expenses_across_different_time_periods(self):
        # Functionalities 3: Compare Expenses Across Different Time Periods
        self.expense_comparator.add_expense(100.0, "Food", "2024-01-15")
        self.expense_comparator.add_expense(150.0, "Food", "2024-02-15")
        comparison = self.expense_comparator.compare_expenses("2024-01-01", "2024-01-31")
        self.assertIn("Food", comparison)
        self.assertEqual(comparison["Food"], 100.0)

    def test_visual_representations_of_expenses(self):
        # Functionalities 4: Provide Visual Representations of Expenses Through Charts and Graphs
        self.expense_comparator.add_expense(100.0, "Food", "2024-01-15")
        comparison = self.expense_comparator.compare_expenses("2024-01-01", "2024-01-31")
        try:
            self.expense_comparator.visualize_expenses(comparison)
        except Exception as e:
            self.fail(f"Visualization failed with exception {e}")

    def test_set_custom_date_ranges_for_expense_comparison(self):
        # Functionalities 5: Set Custom Date Ranges for Expense Comparison
        self.expense_comparator.add_expense(100.0, "Food", "2024-10-15")
        comparison = self.expense_comparator.compare_expenses("2024-10-01", "2024-10-31")
        self.assertIn("Food", comparison)
        self.assertEqual(comparison["Food"], 100.0)

    def test_analyze_and_highlight_spending_patterns(self):
        # Functionalities 6: Analyze and Highlight Spending Patterns
        self.fail("not implemented")  # This functionality is not implemented in the codebase

if __name__ == '__main__':
    unittest.main()
