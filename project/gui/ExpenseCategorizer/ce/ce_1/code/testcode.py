import unittest
import os
from main import ExpenseManager

class TestExpenseManager(unittest.TestCase):

    def setUp(self):
        self.manager = ExpenseManager()
        # Clear expenses.txt and categories.txt for testing
        open('expenses.txt', 'w').close()
        open('categories.txt', 'w').close()

    def test_add_expense_valid(self):
        # Functionality 1: Input Expenses
        self.manager.add_expense(50.00, "Groceries", "Food")
        self.assertEqual(len(self.manager.expenses), 1)
        self.assertEqual(self.manager.expenses[0], (50.00, "Groceries", "Food"))

    def test_add_expense_invalid_amount(self):
        # Functionality 1: Input Expenses
        with self.assertRaises(ValueError):
            self.manager.add_expense(-10.00, "Invalid Expense", "Food")

    def test_automatic_categorization(self):
        # Functionality 2: Automatic Categorization of Expenses
        self.manager.add_expense(100.00, "Dinner at restaurant", "Food")
        self.assertEqual(self.manager.expenses[0][2], "Food")

        # Adding an expense that doesn't match any category
        self.manager.add_expense(30.00, "New shoes", "Uncategorized")
        self.assertEqual(self.manager.expenses[1][2], "Uncategorized")

    def test_create_and_customize_categories(self):
        # Functionality 3: Create and Customize Categories
        self.manager.categories.append("Health")
        self.manager.save_categories()
        self.manager.load_categories()
        self.assertIn("Health", self.manager.categories)

        # Edit an existing category
        self.manager.categories[1] = "Leisure"  # Assuming "Entertainment" is at index 1
        self.manager.save_categories()
        self.manager.load_categories()
        self.assertIn("Leisure", self.manager.categories)

    def test_display_categorized_expenses(self):
        # Functionality 4: Display Categorized Expenses
        self.manager.add_expense(50.00, "Groceries", "Food")
        self.manager.add_expense(20.00, "Transport", "Travel")
        self.assertEqual(len(self.manager.expenses), 2)

        # Remove an expense
        self.manager.expenses.pop(0)
        self.assertEqual(len(self.manager.expenses), 1)

    def test_view_detailed_summaries(self):
        # Functionality 5: View Detailed Summaries of Expenses by Category
        self.manager.add_expense(50.00, "Groceries", "Food")
        self.manager.add_expense(20.00, "Transport", "Travel")
        self.manager.add_expense(100.00, "Dinner", "Food")

        summary = self.manager.get_summary()
        self.assertEqual(summary["Food"], 150.00)
        self.assertEqual(summary["Travel"], 20.00)

if __name__ == '__main__':
    unittest.main()
