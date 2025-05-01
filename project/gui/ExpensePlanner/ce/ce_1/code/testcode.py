import unittest
from budget_manager import BudgetManager
from expense_manager import ExpenseManager
from data_storage import DataStorage
from expense import Expense

class TestExpensePlanner(unittest.TestCase):

    def setUp(self):
        self.budget_manager = BudgetManager()
        self.expense_manager = ExpenseManager()
        self.data_storage = DataStorage()

    def test_input_expenses(self):
        # Functionalities 1: Input expenses
        self.expense_manager.add_expense(50.0, "Food")
        expenses = self.expense_manager.get_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 50.0)
        self.assertEqual(expenses[0].category, "Food")

    def test_categorize_expenses(self):
        # Functionalities 2: Categorize expenses into predefined categories
        self.expense_manager.add_expense(30.0, "Groceries")
        expenses = self.expense_manager.get_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 30.0)
        self.assertEqual(expenses[0].category, "Groceries")

    def test_set_budget_goals(self):
        # Functionalities 3: Set budget goals
        self.budget_manager.set_budget(500.0)
        self.assertEqual(self.budget_manager.budget_goal, 500.0)

    def test_track_spending_against_budget_goals(self):
        # Functionalities 4: Track spending against budget goals
        self.budget_manager.set_budget(500.0)
        self.expense_manager.add_expense(200.0, "Utilities")
        total_expenses = sum(exp.amount for exp in self.expense_manager.get_expenses())
        remaining_budget = self.budget_manager.budget_goal - total_expenses
        self.assertEqual(remaining_budget, 300.0)

        # Remove an expense
        self.expense_manager.expenses.pop()  # Simulate removing the last added expense
        total_expenses = sum(exp.amount for exp in self.expense_manager.get_expenses())
        remaining_budget = self.budget_manager.budget_goal - total_expenses
        self.assertEqual(remaining_budget, 500.0)  # Should revert back to the original budget

    def test_generate_reports(self):
        # Functionalities 6: Generate reports to analyze financial habits
        self.expense_manager.add_expense(50.0, "Groceries")
        self.expense_manager.add_expense(30.0, "Transport")
        self.budget_manager.set_budget(500.0)

        report = self.budget_manager.check_budget_status()
        self.assertIn("Current budget goal is:", report)

        total_expenses = sum(exp.amount for exp in self.expense_manager.get_expenses())
        self.assertEqual(total_expenses, 80.0)

if __name__ == '__main__':
    unittest.main()
