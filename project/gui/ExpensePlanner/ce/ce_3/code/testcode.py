import unittest
from main import ExpensePlanner

class TestExpensePlanner(unittest.TestCase):

    def setUp(self):
        self.planner = ExpensePlanner()

    def test_input_expenses(self):
        # Functionalities 1: Input expenses
        initial_expense_count = len(self.planner.expenses)
        self.planner.add_expense(50.0, "Food", "2023-10-04")
        self.assertEqual(len(self.planner.expenses), initial_expense_count + 1)
        self.assertEqual(self.planner.expenses[-1].amount, 50.0)
        self.assertEqual(self.planner.expenses[-1].category, "Food")
        self.assertEqual(self.planner.expenses[-1].date, "2023-10-04")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize expenses into predefined categories
        self.planner.add_expense(30.0, "Groceries", "2023-10-05")
        self.assertEqual(self.planner.expenses[-1].category, "Groceries")

    def test_set_budget_goals(self):
        # Functionalities 3: Set budget goals
        self.planner.set_budget_goal("Monthly", 500.0)
        self.assertIn("Monthly", self.planner.budget_goals)
        self.assertEqual(self.planner.budget_goals["Monthly"].amount, 500.0)

    def test_track_spending_against_budget_goals(self):
        # Functionalities 4: Track spending against budget goals
        self.planner.set_budget_goal("General", 500.0)
        self.planner.add_expense(200.0, "General", "2023-10-06")
        spending = self.planner.track_spending()
        self.assertEqual(spending.get("General", 0), 200.0)
        self.planner.expenses.pop()  # Simulate removing an expense
        spending = self.planner.track_spending()
        self.assertEqual(spending.get("General", 0), 0.0)

    def test_provide_visual_representations(self):
        # Functionalities 5: Provide visual representations of budget breakdowns
        self.planner.add_expense(50.0, "Groceries", "2023-10-07")
        self.planner.add_expense(30.0, "Transport", "2023-10-08")
        # Assuming a method to generate a pie chart exists
        # This functionality is not implemented in the codebase
        self.fail("Visual representation functionality not implemented")

    def test_generate_reports(self):
        # Functionalities 6: Generate reports to analyze financial habits
        report = self.planner.generate_report()
        self.assertIn("Food", report)
        self.assertIn("Transport", report)
        self.assertIn("Utilities", report)

if __name__ == '__main__':
    unittest.main()
