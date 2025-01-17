import unittest
from expense_comparator import ExpenseComparator
from expense import Expense

class TestExpenseComparator(unittest.TestCase):

    def setUp(self):
        self.expense_comparator = ExpenseComparator()

    def test_input_expenses(self):
        # Functionalities 1: Input Expenses
        self.expense_comparator.add_expense("2024-11-01", 50.0, "Groceries")
        self.assertEqual(len(self.expense_comparator.expenses), 1)
        self.assertEqual(self.expense_comparator.expenses[0].amount, 50.0)
        self.assertEqual(self.expense_comparator.expenses[0].category, "Groceries")
        self.assertEqual(self.expense_comparator.expenses[0].date, "2024-11-01")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize Expenses
        self.expense_comparator.add_expense("2024-11-01", 50.0, "Groceries")
        self.expense_comparator.expenses[0].category = "Transportation"
        self.assertEqual(self.expense_comparator.expenses[0].category, "Transportation")

    def test_compare_expenses_across_time_periods(self):
        # Functionalities 3: Compare Expenses Across Different Time Periods
        self.expense_comparator.add_expense("2024-01-15", 100.0, "Food")
        self.expense_comparator.add_expense("2024-02-20", 200.0, "Transport")
        jan_expenses = self.expense_comparator.compare_expenses("2024-01-01", "2024-01-31")
        feb_expenses = self.expense_comparator.compare_expenses("2024-02-01", "2024-02-28")
        self.assertEqual(len(jan_expenses), 1)
        self.assertEqual(len(feb_expenses), 1)

    def test_visualize_expenses(self):
        # Functionalities 4: Provide Visual Representations of Expenses Through Charts and Graphs
        self.expense_comparator.add_expense("2024-01-15", 100.0, "Food")
        self.expense_comparator.add_expense("2024-01-20", 200.0, "Transport")
        expenses = self.expense_comparator.compare_expenses("2024-01-01", "2024-01-31")
        # Assuming visualize_expenses method works correctly if no exception is raised
        try:
            self.expense_comparator.visualize_expenses(expenses)
        except Exception as e:
            self.fail(f"Visualization failed with exception: {e}")

    def test_set_custom_date_ranges(self):
        # Functionalities 5: Set Custom Date Ranges for Expense Comparison
        self.expense_comparator.add_expense("2024-10-15", 100.0, "Food")
        self.expense_comparator.add_expense("2024-11-20", 200.0, "Transport")
        oct_expenses = self.expense_comparator.compare_expenses("2024-10-01", "2024-10-31")
        self.assertEqual(len(oct_expenses), 1)
        self.assertEqual(oct_expenses[0].date, "2024-10-15")

    def test_analyze_and_highlight_spending_patterns(self):
        # Functionalities 6: Analyze and Highlight Spending Patterns
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
