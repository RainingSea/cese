import unittest
from expense_categorizer import ExpenseCategorizer
from expense import Expense

class TestExpenseCategorizer(unittest.TestCase):

    def setUp(self):
        self.categorizer = ExpenseCategorizer()

    def test_input_expenses(self):
        # Test valid expense input
        initial_count = len(self.categorizer.expenses)
        self.categorizer.add_expense(50.0, "Dinner", "Food")
        self.assertEqual(len(self.categorizer.expenses), initial_count + 1)
        self.assertEqual(self.categorizer.expenses[-1].amount, 50.0)
        self.assertEqual(self.categorizer.expenses[-1].description, "Dinner")
        self.assertEqual(self.categorizer.expenses[-1].category, "Food")

        # Test invalid expense input (negative amount)
        with self.assertRaises(ValueError):
            self.categorizer.add_expense(-20.0, "Invalid Expense", "Food")

    def test_automatic_categorization_of_expenses(self):
        # Test automatic categorization with predefined category
        self.categorizer.add_expense(25.0, "Dinner at restaurant", "Food")
        self.assertEqual(self.categorizer.expenses[-1].category, "Food")

        # Test manual categorization prompt (not implemented)
        self.fail("Manual categorization prompt not implemented")

    def test_create_and_customize_categories(self):
        # Test create new category
        self.categorizer.custom_categories.append("Health")
        self.categorizer.save_categories()
        self.assertIn("Health", self.categorizer.custom_categories)

        # Test edit existing category (not implemented)
        self.fail("Edit category functionality not implemented")

    def test_display_categorized_expenses(self):
        # Test display of categorized expenses
        self.categorizer.add_expense(20.0, "Lunch", "Food")
        self.categorizer.add_expense(15.0, "Bus fare", "Travel")
        summary = self.categorizer.get_summary()
        self.assertIn("Food", summary)
        self.assertIn("Travel", summary)

        # Test remove expense from category (not implemented)
        self.fail("Remove expense functionality not implemented")

    def test_view_detailed_summaries_of_expenses_by_category(self):
        # Test detailed summary of expenses
        self.categorizer.add_expense(10.0, "Coffee", "Food")
        self.categorizer.add_expense(5.0, "Taxi", "Travel")
        summary = self.categorizer.get_summary()
        self.assertEqual(summary["Food"], 10.0)
        self.assertEqual(summary["Travel"], 5.0)

        # Test filter summary by category (not implemented)
        self.fail("Filter summary by category functionality not implemented")

if __name__ == '__main__':
    unittest.main()
