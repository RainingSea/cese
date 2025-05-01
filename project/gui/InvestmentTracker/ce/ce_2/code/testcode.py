import unittest
import os
from main import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = InvestmentTracker()
        # Clear the investment files before each test
        for filename in ['stocks.txt', 'bonds.txt', 'mutual_funds.txt', 'other_assets.txt']:
            if os.path.exists(filename):
                os.remove(filename)

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        self.tracker.input_investment('stock', 1000, 'Tech')
        self.assertEqual(len(self.tracker.stocks), 1)
        self.assertEqual(self.tracker.stocks[0]['amount'], 1000)
        self.assertEqual(self.tracker.stocks[0]['category'], 'Tech')

    def test_categorize_investments(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        self.tracker.input_investment('bond', 500, 'Government')
        self.tracker.categorize_investment('bond', 'Growth')  # Placeholder, should be implemented
        self.fail("Categorize investment functionality not implemented")

        self.tracker.input_investment('mutual_fund', 2000, 'Equity')
        self.tracker.categorize_investment('mutual_fund', 'Income')  # Placeholder, should be implemented
        self.fail("Categorize investment functionality not implemented")

    def test_visualize_performance(self):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        self.tracker.input_investment('stock', 1000, 'Tech')
        self.tracker.visualize_performance()  # This will show a plot, cannot assert directly
        self.fail("Visualization functionality cannot be tested directly")

    def test_generate_reports(self):
        # Functionalities 4: Generate Reports on Investment Performance
        self.tracker.input_investment('stock', 1000, 'Tech')
        self.tracker.input_investment('bond', 500, 'Government')
        report = self.tracker.generate_report()
        self.assertIn("Investment Report", report)
        self.assertIn("Stocks:", report)
        self.assertIn("Bonds:", report)

    def test_set_investment_goals(self):
        # Functionalities 5: Set Investment Goals
        self.fail("Set investment goals functionality not implemented")

if __name__ == '__main__':
    unittest.main()
