import unittest
from main import ExpensePlanner

class TestExpensePlanner(unittest.TestCase):

    def setUp(self):
        self.planner = ExpensePlanner()

    def test_input_expenses(self):
        # Functionalities 1: Input expenses
        self.planner.add_expense(50.00, "Food")
        self.assertEqual(len(self.planner.expenses), 4)  # 3 existing + 1 new
        self.assertEqual(self.planner.expenses[-1].amount, 50.00)
        self.assertEqual(self.planner.expenses[-1].category, "Food")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize expenses into predefined categories
        self.planner.add_expense(30.00, "Groceries")
        self.assertEqual(self.planner.expenses[-1].category, "Groceries")

    def test_set_budget_goals(self):
        # Functionalities 3: Set budget goals
        self.planner.set_budget("Monthly", 500.00)
        self.assertIn("Monthly", self.planner.budget_goals)
        self.assertEqual(self.planner.budget_goals["Monthly"], 500.00)

    def test_track_spending_against_budget_goals(self):
        # Functionalities 4: Track spending against budget goals
        self.planner.set_budget("General", 500.00)
        self.planner.add_expense(200.00, "General")
        remaining_budget = self.planner.budget_goals["General"] - sum(exp.amount for exp in self.planner.expenses if exp.category == "General")
        self.assertEqual(remaining_budget, 300.00)

        # Remove an expense and check adjustment
        self.planner.expenses.pop()  # Remove last added expense
        remaining_budget = self.planner.budget_goals["General"] - sum(exp.amount for exp in self.planner.expenses if exp.category == "General")
        self.assertEqual(remaining_budget, 500.00)

    def test_visualize_budget(self):
        # Functionalities 5: Provide visual representations of budget breakdowns
        # This functionality involves GUI visualization which is not directly testable via unit tests.
        self.fail("Visualization test not implemented due to GUI limitations")

    def test_generate_reports(self):
        # Functionalities 6: Generate reports to analyze financial habits
        report = self.planner.generate_report()
        self.assertIn("2023-10-01 - Food: $50.00", report)
        self.assertIn("2023-10-02 - Transport: $20.00", report)
        self.assertIn("2023-10-03 - Entertainment: $15.00", report)

if __name__ == '__main__':
    unittest.main()
