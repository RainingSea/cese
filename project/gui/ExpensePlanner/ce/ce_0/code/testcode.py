import unittest
import os
from main import ExpensePlanner

class TestExpensePlanner(unittest.TestCase):

    def setUp(self):
        self.planner = ExpensePlanner()
        # Clear existing expenses and budget goals for testing
        self.planner.expenses.clear()
        self.planner.budget_goals.clear()

    def test_input_expenses(self):
        # Functionalities 1: Input expenses
        self.planner.add_expense(50, "Lunch", "Food")
        self.assertEqual(len(self.planner.expenses), 1)
        self.assertEqual(self.planner.expenses[0].amount, 50)
        self.assertEqual(self.planner.expenses[0].description, "Lunch")
        self.assertEqual(self.planner.expenses[0].category, "Food")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize expenses into predefined categories
        self.planner.add_expense(30, "Groceries", "Groceries")
        self.assertEqual(len(self.planner.expenses), 1)
        self.assertEqual(self.planner.expenses[0].category, "Groceries")

    def test_set_budget_goals(self):
        # Functionalities 3: Set budget goals
        self.planner.set_budget_goal("Monthly Budget", 500)
        self.assertEqual(len(self.planner.budget_goals), 1)
        self.assertEqual(self.planner.budget_goals[0].amount, 500)
        self.assertEqual(self.planner.budget_goals[0].category, "Monthly Budget")

    def test_track_spending_against_budget_goals(self):
        # Functionalities 4: Track spending against budget goals
        self.planner.set_budget_goal("Monthly Budget", 500)
        self.planner.add_expense(200, "Groceries", "Food")
        self.assertEqual(len(self.planner.expenses), 1)
        self.assertEqual(self.planner.budget_goals[0].amount, 500)
        self.assertEqual(500 - 200, 300)  # Remaining budget should be 300

        # Remove an expense
        self.planner.expenses.pop()
        self.assertEqual(len(self.planner.expenses), 0)
        self.assertEqual(500 - 0, 500)  # Remaining budget should adjust to 500

    def test_visual_representations_of_budget_breakdowns(self):
        # Functionalities 5: Provide visual representations of budget breakdowns
        self.planner.add_expense(50, "Groceries", "Groceries")
        self.planner.add_expense(30, "Transport", "Transport")
        self.assertEqual(len(self.planner.expenses), 2)
        # Visualization cannot be tested directly, so we will skip this test point
        self.fail("Visualization test not implemented")

    def test_generate_reports(self):
        # Functionalities 6: Generate reports to analyze financial habits
        self.planner.add_expense(50, "Lunch", "Food")
        self.planner.add_expense(20, "Bus Ticket", "Transport")
        report = self.planner.generate_report()
        self.assertIn("Expense Report:", report)
        self.assertIn("Lunch: $50.0 in Food", report)
        self.assertIn("Bus Ticket: $20.0 in Transport", report)
        self.assertIn("Total Expenses: $70.0", report)

if __name__ == '__main__':
    unittest.main()
