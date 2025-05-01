import unittest
import os
from main import ExpenseCategorizer

class TestExpenseCategorizer(unittest.TestCase):

    def setUp(self):
        self.categorizer = ExpenseCategorizer()
        self.categorizer.load_expenses()  # Load existing expenses for testing

    def test_add_expense_valid(self):
        # Functionality 1: Input Expenses
        self.categorizer.add_expense(100.0, "Dinner at restaurant", "Food")
        self.assertEqual(len(self.categorizer.expenses), 1)
        self.assertEqual(self.categorizer.expenses[0].amount, 100.0)
        self.assertEqual(self.categorizer.expenses[0].description, "Dinner at restaurant")
        self.assertEqual(self.categorizer.expenses[0].category, "Food")

    def test_add_expense_invalid(self):
        # Functionality 1: Input Expenses - Invalid amount
        with self.assertRaises(ValueError):
            self.categorizer.add_expense(-50.0, "Invalid expense", "Food")

    def test_create_custom_category(self):
        # Functionality 3: Create and Customize Categories
        self.categorizer.create_custom_category("Health")
        self.assertIn("Health", self.categorizer.categories)

    def test_edit_existing_category(self):
        # Functionality 3: Edit an existing category
        self.categorizer.create_custom_category("Leisure")
        self.categorizer.categories[self.categorizer.categories.index("Entertainment")] = "Leisure"
        self.assertIn("Leisure", self.categorizer.categories)
        self.assertNotIn("Entertainment", self.categorizer.categories)

    def test_get_expense_summary(self):
        # Functionality 5: View Detailed Summaries of Expenses by Category
        self.categorizer.add_expense(50.0, "Groceries", "Food")
        self.categorizer.add_expense(20.0, "Transport", "Travel")
        summary = self.categorizer.get_expense_summary()
        self.assertIn("Food: 50.0", summary)
        self.assertIn("Travel: 20.0", summary)

    def tearDown(self):
        # Clean up the test files
        if os.path.exists('expenses.txt'):
            os.remove('expenses.txt')
        if os.path.exists('categories.txt'):
            os.remove('categories.txt')

if __name__ == '__main__':
    unittest.main()
