import unittest
import os
from main import Investment, Portfolio, Goal, InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = InvestmentTracker()
        self.tracker.investments.clear()  # Clear existing investments for testing
        self.tracker.goals.clear()         # Clear existing goals for testing
        self.tracker.portfolios.clear()     # Clear existing portfolios for testing

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        investment = Investment("Test Investment", 1000, "Stock")
        self.tracker.add_investment(investment)
        self.assertEqual(len(self.tracker.investments), 1)
        self.assertEqual(self.tracker.investments[0].name, "Test Investment")
        self.assertEqual(self.tracker.investments[0].amount, 1000)
        self.assertEqual(self.tracker.investments[0].type, "Stock")

    def test_categorize_investments(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        portfolio = Portfolio("Growth")
        self.tracker.portfolios.append(portfolio)

        investment1 = Investment("Investment A", 1000, "Stock")
        investment2 = Investment("Investment B", 500, "Bond")
        
        self.tracker.add_investment(investment1)
        self.tracker.add_investment(investment2)

        self.tracker.categorize_investment(investment1, portfolio)
        self.tracker.categorize_investment(investment2, portfolio)

        self.assertIn(investment1, portfolio.investments)
        self.assertIn(investment2, portfolio.investments)

    def test_generate_visualization(self):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        investment = Investment("Investment A", 1000, "Stock")
        self.tracker.add_investment(investment)
        # Visualization cannot be tested directly as it opens a window, so we will just check if it runs without error
        try:
            self.tracker.generate_visualization()
        except Exception as e:
            self.fail(f"Visualization generation failed with exception: {e}")

    def test_generate_report(self):
        # Functionalities 4: Generate Reports on Investment Performance
        investment = Investment("Investment A", 1000, "Stock")
        self.tracker.add_investment(investment)
        # Report generation cannot be tested directly as it shows a message box, so we will just check if it runs without error
        try:
            self.tracker.generate_report()
        except Exception as e:
            self.fail(f"Report generation failed with exception: {e}")

    def test_set_investment_goals(self):
        # Functionalities 5: Set Investment Goals
        goal = Goal("Save for House", 20000)
        self.tracker.set_goal(goal)
        self.assertEqual(len(self.tracker.goals), 1)
        self.assertEqual(self.tracker.goals[0].description, "Save for House")
        self.assertEqual(self.tracker.goals[0].target_amount, 20000)

if __name__ == '__main__':
    unittest.main()
