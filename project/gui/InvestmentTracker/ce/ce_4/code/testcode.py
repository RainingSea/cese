import unittest
from investment_tracker import InvestmentTracker
from investment import Investment
import os

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        # Set up a fresh InvestmentTracker instance for each test
        self.tracker = InvestmentTracker()
        # Clear the investments file before each test
        open('investments.txt', 'w').close()
        open('reports.txt', 'w').close()

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        self.tracker.add_investment("Test Stock", "Equity", 1500.0, "2023-04-01", "Growth")
        investments = self.tracker.investments
        self.assertEqual(len(investments), 1)
        self.assertEqual(investments[0].name, "Test Stock")
        self.assertEqual(investments[0].type, "Equity")
        self.assertEqual(investments[0].amount, 1500.0)
        self.assertEqual(investments[0].date, "2023-04-01")
        self.assertEqual(investments[0].category, "Growth")

    def test_categorize_investments(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        self.tracker.add_investment("Growth Stock", "Equity", 2000.0, "2023-05-01", "Growth")
        self.tracker.add_investment("Income Bond", "Fixed Income", 1000.0, "2023-06-01", "Income")
        investments = self.tracker.investments
        self.assertEqual(investments[0].category, "Growth")
        self.assertEqual(investments[1].category, "Income")

    def test_visualize_performance(self):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        self.fail("Visualization functionality not implemented")

    def test_generate_reports(self):
        # Functionalities 4: Generate Reports on Investment Performance
        self.tracker.add_investment("Report Stock", "Equity", 3000.0, "2023-07-01", "Balanced")
        report = self.tracker.generate_report()
        self.assertIn("Report Stock", report)
        self.assertIn("Equity", report)
        self.assertIn("3000.0", report)
        self.assertIn("2023-07-01", report)
        self.assertIn("Balanced", report)

    def test_set_investment_goals(self):
        # Functionalities 5: Set Investment Goals
        self.fail("Investment goals functionality not implemented")

if __name__ == '__main__':
    unittest.main()
