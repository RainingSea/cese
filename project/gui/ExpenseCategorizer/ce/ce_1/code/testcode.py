import unittest
from main import ExpenseCategorizer

class TestExpenseCategorizer(unittest.TestCase):

    def setUp(self):
        # Initialize the ExpenseCategorizer for testing
        self.categorizer = ExpenseCategorizer()

    def test_input_expenses(self):
        # Test valid expense input
        initial_count = len(self.categorizer.expenses)
        self.categorizer.add_expense(25.00, "Lunch", "Food")
        self.assertEqual(len(self.categorizer.expenses), initial_count + 1)
        self.assertEqual(self.categorizer.expenses[-1].amount, 25.00)
        self.assertEqual(self.categorizer.expenses[-1].description, "Lunch")
        self.assertEqual(self.categorizer.expenses[-1].category, "Food")

        # Test invalid expense input (negative amount)
        with self.assertRaises(ValueError):
            self.categorizer.add_expense(-10.00, "Invalid Expense", "Food")

    def test_automatic_categorization(self):
        # Test automatic categorization (not implemented in codebase)
        self.fail("Automatic categorization not implemented")

    def test_create_and_customize_categories(self):
        # Test creating a new category
        initial_count = len(self.categorizer.categories)
        self.categorizer.categories.append("Health")
        self.categorizer.save_categories()
        self.assertIn("Health", self.categorizer.categories)
        self.assertEqual(len(self.categorizer.categories), initial_count + 1)

        # Test editing an existing category
        if "Entertainment" in self.categorizer.categories:
            index = self.categorizer.categories.index("Entertainment")
            self.categorizer.categories[index] = "Leisure"
            self.categorizer.save_categories()
            self.assertIn("Leisure", self.categorizer.categories)
            self.assertNotIn("Entertainment", self.categorizer.categories)
        else:
            self.fail("Category 'Entertainment' not found for editing")

    def test_display_categorized_expenses(self):
        # Test displaying categorized expenses (not implemented in codebase)
        self.fail("Display categorized expenses not implemented")

    def test_view_detailed_summaries(self):
        # Test viewing detailed summaries
        self.categorizer.add_expense(30.00, "Dinner", "Food")
        self.categorizer.add_expense(15.00, "Taxi", "Transport")
        summary = self.categorizer.get_summary()
        self.assertIn("Food", summary)
        self.assertIn("Transport", summary)
        self.assertEqual(summary["Food"], 30.00)
        self.assertEqual(summary["Transport"], 15.00)

        # Test filtering summary by category (not implemented in codebase)
        self.fail("Filtering summary by category not implemented")

if __name__ == '__main__':
    unittest.main()
