import unittest
from expense_planner import ExpensePlanner
from expense import Expense

class TestExpensePlanner(unittest.TestCase):

    def setUp(self):
        self.planner = ExpensePlanner()
        self.planner.load_data()

    def test_input_expenses(self):
        # Functionalities 1: Input expenses
        initial_count = len(self.planner.expenses)
        self.planner.add_expense(50.00, "Miscellaneous")
        self.assertEqual(len(self.planner.expenses), initial_count + 1)
        self.assertEqual(self.planner.expenses[-1].amount, 50.00)
        self.assertEqual(self.planner.expenses[-1].category, "Miscellaneous")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize expenses into predefined categories
        self.planner.add_expense(30.00, "Groceries")
        self.assertEqual(self.planner.expenses[-1].category, "Groceries")

    def test_set_budget_goals(self):
        # Functionalities 3: Set budget goals
        self.planner.set_budget_goal("Monthly", 500.00)
        self.assertIn("Monthly", self.planner.budget_goals)
        self.assertEqual(self.planner.budget_goals["Monthly"], 500.00)

    def test_track_spending_against_budget_goals(self):
        # Functionalities 4: Track spending against budget goals
        self.planner.set_budget_goal("General", 500.00)
        self.planner.add_expense(200.00, "General")
        spending_summary = self.planner.track_spending()
        self.assertEqual(spending_summary.get("General", 0), 200.00)
        remaining_budget = self.planner.budget_goals["General"] - spending_summary["General"]
        self.assertEqual(remaining_budget, 300.00)

        # Simulate removing an expense
        self.planner.expenses.pop()
        spending_summary = self.planner.track_spending()
        self.assertEqual(spending_summary.get("General", 0), 0)
        remaining_budget = self.planner.budget_goals["General"] - spending_summary.get("General", 0)
        self.assertEqual(remaining_budget, 500.00)

    def test_visualize_budget(self):
        # Functionalities 5: Provide visual representations of budget breakdowns
        self.planner.add_expense(50.00, "Groceries")
        self.planner.add_expense(30.00, "Transport")
        # Since visualization is a GUI feature, we assume it works if no exceptions are raised
        try:
            self.planner.visualize_budget()
            visualization_successful = True
        except Exception:
            visualization_successful = False
        self.assertTrue(visualization_successful)

    def test_generate_reports(self):
        # Functionalities 6: Generate reports to analyze financial habits
        report = self.planner.generate_report()
        self.assertIn("Expense Report:", report)
        self.assertIn("Food - $50.00", report)
        self.assertIn("Transport - $20.00", report)
        self.assertIn("Entertainment - $30.00", report)

if __name__ == '__main__':
    unittest.main()
