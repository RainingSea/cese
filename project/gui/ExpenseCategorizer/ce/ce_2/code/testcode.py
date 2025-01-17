import unittest
from ExpenseCategorizer import ExpenseCategorizer

class TestExpenseCategorizer(unittest.TestCase):

    def setUp(self):
        self.categorizer = ExpenseCategorizer()

    def test_input_expenses(self):
        # Test valid expense input
        initial_expense_count = len(self.categorizer.expenses)
        self.categorizer.add_expense(100, "Dinner", "Food")
        self.assertEqual(len(self.categorizer.expenses), initial_expense_count + 1)
        self.assertEqual(self.categorizer.expenses[-1]['amount'], 100)
        self.assertEqual(self.categorizer.expenses[-1]['description'], "Dinner")
        self.assertEqual(self.categorizer.expenses[-1]['category'], "Food")

        # Test invalid expense input (negative amount)
        with self.assertRaises(ValueError):
            self.categorizer.add_expense(-50, "Invalid Expense", "Food")

    def test_automatic_categorization(self):
        # Test automatic categorization
        self.categorizer.add_expense(30, "Dinner at restaurant", "Food")
        categorized_expenses = self.categorizer.categorize_expenses()
        self.assertIn("Food", categorized_expenses)
        self.assertEqual(categorized_expenses["Food"][0]['description'], "Dinner at restaurant")

        # Test manual categorization prompt (not implemented in logic)
        self.fail("Manual categorization prompt not implemented in logic")

    def test_create_and_customize_categories(self):
        # Test creating a new category
        self.categorizer.categories.append("Health")
        self.categorizer.save_categories()
        self.assertIn("Health", self.categorizer.categories)

        # Test editing an existing category (not implemented in logic)
        self.fail("Editing categories not implemented in logic")

    def test_display_categorized_expenses(self):
        # Test displaying categorized expenses
        self.categorizer.add_expense(50, "Groceries", "Food")
        self.categorizer.add_expense(20, "Bus fare", "Transport")
        summary = self.categorizer.display_summary()
        self.assertIn("Category: Food", summary)
        self.assertIn("Groceries: $50", summary)
        self.assertIn("Category: Transport", summary)
        self.assertIn("Bus fare: $20", summary)

        # Test removing an expense (not implemented in logic)
        self.fail("Removing expenses not implemented in logic")

    def test_view_detailed_summaries(self):
        # Test viewing detailed summaries
        self.categorizer.add_expense(100, "Electricity bill", "Utilities")
        summary = self.categorizer.display_summary()
        self.assertIn("Category: Utilities", summary)
        self.assertIn("Electricity bill: $100", summary)

        # Test filtering summary by category (not implemented in logic)
        self.fail("Filtering summary by category not implemented in logic")

if __name__ == '__main__':
    unittest.main()
