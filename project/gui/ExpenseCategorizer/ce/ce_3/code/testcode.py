import unittest
from ExpenseCategorizer import ExpenseCategorizer

class TestExpenseCategorizer(unittest.TestCase):

    def setUp(self):
        self.categorizer = ExpenseCategorizer()

    def test_input_expenses(self):
        # Test valid expense input
        self.categorizer.add_expense(100.0, "Food", "2023-10-04")
        self.assertEqual(len(self.categorizer.expenses), 4)  # 3 existing + 1 new
        self.assertEqual(self.categorizer.expenses[-1].amount, 100.0)
        self.assertEqual(self.categorizer.expenses[-1].category, "Food")
        self.assertEqual(self.categorizer.expenses[-1].date, "2023-10-04")

        # Test invalid expense input (negative amount)
        with self.assertRaises(ValueError):
            self.categorizer.add_expense(-50.0, "Food", "2023-10-05")

    def test_automatic_categorization_of_expenses(self):
        # This functionality is not implemented in the codebase
        self.fail("Automatic categorization of expenses is not implemented")

    def test_create_and_customize_categories(self):
        # Test creating a new category
        self.categorizer.create_category("Health")
        self.assertIn("Health", [category.name for category in self.categorizer.categories])

        # Test editing an existing category (not implemented in the codebase)
        self.fail("Editing categories is not implemented")

    def test_display_categorized_expenses(self):
        # Test displaying categorized expenses
        summary = self.categorizer.get_summary()
        self.assertIn("Food", summary)
        self.assertIn("Transport", summary)
        self.assertIn("Entertainment", summary)

        # Test removing an expense (not implemented in the codebase)
        self.fail("Removing expenses is not implemented")

    def test_view_detailed_summaries_of_expenses_by_category(self):
        # Test viewing detailed summaries
        summary = self.categorizer.get_summary()
        self.assertEqual(summary["Food"], 50.0)
        self.assertEqual(summary["Transport"], 30.0)
        self.assertEqual(summary["Entertainment"], 20.0)

        # Test filtering summary by category (not implemented in the codebase)
        self.fail("Filtering summary by category is not implemented")

if __name__ == '__main__':
    unittest.main()
