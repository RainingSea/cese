import unittest
import os
from main import ExpenseManager

class TestExpenseCategorizer(unittest.TestCase):

    def setUp(self):
        self.manager = ExpenseManager()
        # Clear expenses.txt before each test
        open('expenses.txt', 'w').close()

    def test_input_expenses(self):
        # Functionality 1: Input Expenses
        # Valid expense input
        self.manager.add_expense(100, "Dinner", "Food")
        self.assertEqual(len(self.manager.expenses), 1)
        self.assertEqual(self.manager.expenses[0].amount, 100)
        
        # Invalid expense input (negative amount)
        with self.assertRaises(ValueError):
            self.manager.add_expense(-50, "Invalid Expense", "Food")

    def test_automatic_categorization(self):
        # Functionality 2: Automatic Categorization of Expenses
        # This functionality is not implemented in the codebase
        self.fail("Automatic categorization functionality not implemented.")

    def test_create_and_customize_categories(self):
        # Functionality 3: Create and Customize Categories
        # This functionality is not implemented in the codebase
        self.fail("Category management functionality not implemented.")

    def test_display_categorized_expenses(self):
        # Functionality 4: Display Categorized Expenses
        self.manager.add_expense(100, "Dinner", "Food")
        self.manager.add_expense(50, "Bus Ticket", "Transport")
        self.manager.add_expense(30, "Groceries", "Food")
        
        # Check if expenses are categorized correctly
        summary = self.manager.get_summary()
        self.assertIn("Food: 130", summary)
        self.assertIn("Transport: 50", summary)

    def test_view_detailed_summaries(self):
        # Functionality 5: View Detailed Summaries of Expenses by Category
        self.manager.add_expense(100, "Dinner", "Food")
        self.manager.add_expense(50, "Bus Ticket", "Transport")
        self.manager.add_expense(30, "Groceries", "Food")
        
        summary = self.manager.get_summary()
        self.assertIn("Food: 130", summary)
        self.assertIn("Transport: 50", summary)

if __name__ == '__main__':
    unittest.main()
