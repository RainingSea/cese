import unittest
import os
from ExpensePlanner import ExpensePlanner

class TestExpensePlanner(unittest.TestCase):

    def setUp(self):
        # Set up a fresh instance of ExpensePlanner for each test
        self.planner = ExpensePlanner()
        # Clear any existing data files to ensure a clean test environment
        if os.path.exists('expenses.txt'):
            os.remove('expenses.txt')
        if os.path.exists('budget.txt'):
            os.remove('budget.txt')

    def test_input_expenses(self):
        # Functionalities 1: Input expenses
        self.planner.add_expense(50.00, "Test Expense", "Food")
        self.assertEqual(len(self.planner.expenses), 1)
        self.assertEqual(self.planner.expenses[0].amount, 50.00)
        self.assertEqual(self.planner.expenses[0].description, "Test Expense")
        self.assertEqual(self.planner.expenses[0].category, "Food")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize expenses into predefined categories
        self.planner.add_expense(30.00, "Groceries Shopping", "Groceries")
        self.assertEqual(self.planner.expenses[0].category, "Groceries")

    def test_set_budget_goals(self):
        # Functionalities 3: Set budget goals
        self.planner.set_budget("Monthly", 500.00)
        self.assertIn("Monthly", self.planner.budget_goals)
        self.assertEqual(self.planner.budget_goals["Monthly"], 500.00)

    def test_track_spending_against_budget_goals(self):
        # Functionalities 4: Track spending against budget goals
        self.planner.set_budget("Food", 500.00)
        self.planner.add_expense(200.00, "Dinner", "Food")
        total_expense = sum(exp.amount for exp in self.planner.expenses if exp.category == "Food")
        remaining_budget = self.planner.budget_goals["Food"] - total_expense
        self.assertEqual(remaining_budget, 300.00)

        # Simulate removing an expense (not implemented in codebase)
        # Assuming a method remove_expense exists
        # self.planner.remove_expense(200.00, "Dinner", "Food")
        # total_expense_after_removal = sum(exp.amount for exp in self.planner.expenses if exp.category == "Food")
        # remaining_budget_after_removal = self.planner.budget_goals["Food"] - total_expense_after_removal
        # self.assertEqual(remaining_budget_after_removal, 500.00)
        self.fail("Remove expense functionality not implemented")

    def test_visual_representations(self):
        # Functionalities 5: Provide visual representations of budget breakdowns
        self.planner.add_expense(50.00, "Groceries", "Groceries")
        self.planner.add_expense(30.00, "Bus Fare", "Transport")
        # This functionality typically requires manual or integration testing
        self.fail("Visual representation functionality not implemented")

    def test_generate_reports(self):
        # Functionalities 6: Generate reports to analyze financial habits
        report = self.planner.generate_report()
        self.assertIn("Category: Food", report)
        self.assertIn("Category: Transport", report)
        self.assertIn("Total Expenses", report)

if __name__ == '__main__':
    unittest.main()
