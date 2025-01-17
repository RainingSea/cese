import unittest
from expense_manager import ExpensePlanner

class TestExpensePlanner(unittest.TestCase):

    def setUp(self):
        self.expense_planner = ExpensePlanner()

    def test_input_expenses(self):
        # Functionalities 1: Input expenses
        initial_count = len(self.expense_planner.expenses)
        self.expense_planner.add_expense(50.00, "Food", "2023-10-04")
        self.assertEqual(len(self.expense_planner.expenses), initial_count + 1)
        self.assertEqual(self.expense_planner.expenses[-1].amount, 50.00)
        self.assertEqual(self.expense_planner.expenses[-1].category, "Food")
        self.assertEqual(self.expense_planner.expenses[-1].date, "2023-10-04")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize expenses into predefined categories
        self.expense_planner.add_expense(30.00, "Groceries", "2023-10-05")
        self.assertEqual(self.expense_planner.expenses[-1].category, "Groceries")

    def test_set_budget_goals(self):
        # Functionalities 3: Set budget goals
        initial_count = len(self.expense_planner.budget_goals)
        self.expense_planner.set_budget_goal("Monthly", 500.00)
        self.assertEqual(len(self.expense_planner.budget_goals), initial_count + 1)
        self.assertEqual(self.expense_planner.budget_goals[-1].category, "Monthly")
        self.assertEqual(self.expense_planner.budget_goals[-1].amount, 500.00)

    def test_track_spending_against_budget_goals(self):
        # Functionalities 4: Track spending against budget goals
        self.expense_planner.set_budget_goal("Monthly", 500.00)
        self.expense_planner.add_expense(200.00, "Food", "2023-10-06")
        total_spent = sum(exp.amount for exp in self.expense_planner.expenses if exp.category == "Food")
        remaining_budget = 500.00 - total_spent
        self.assertEqual(remaining_budget, 300.00)

        # Remove an expense
        self.expense_planner.expenses.pop()
        total_spent = sum(exp.amount for exp in self.expense_planner.expenses if exp.category == "Food")
        remaining_budget = 500.00 - total_spent
        self.assertEqual(remaining_budget, 500.00)

    def test_provide_visual_representations(self):
        # Functionalities 5: Provide visual representations of budget breakdowns
        self.expense_planner.add_expense(50.00, "Groceries", "2023-10-07")
        self.expense_planner.add_expense(30.00, "Transport", "2023-10-08")
        # Since visualization is not directly testable, we assume the function works if no exceptions are raised
        try:
            self.expense_planner.visualize_budget_breakdown()
        except Exception as e:
            self.fail(f"Visualization failed with exception: {e}")

    def test_generate_reports(self):
        # Functionalities 6: Generate reports to analyze financial habits
        report = self.expense_planner.generate_report()
        self.assertIn("Expense Report:", report)
        self.assertIn("Food", report)
        self.assertIn("Transport", report)
        self.assertIn("Entertainment", report)

if __name__ == '__main__':
    unittest.main()
