import unittest
from goal_manager import GoalManager, Goal
from investment_manager import InvestmentManager, Investment
from portfolio_manager import PortfolioManager, Portfolio
from report_generator import generate_report
from visualization import visualize_investments
import tkinter as tk
from unittest.mock import patch
import matplotlib.pyplot as plt

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        # Set up the environment for each test
        self.investment_manager = InvestmentManager()
        self.portfolio_manager = PortfolioManager()
        self.goal_manager = GoalManager()

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        investment = Investment("Stock A", "Equity", 1000.0, "2023-01-01")
        self.investment_manager.add_investment(investment)
        self.assertIn(investment, self.investment_manager.investments)

    def test_categorize_investments_into_different_portfolios(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        portfolio_growth = Portfolio("Growth", "Long-term")
        self.portfolio_manager.add_portfolio(portfolio_growth)
        self.assertIn(portfolio_growth, self.portfolio_manager.portfolios)

        portfolio_income = Portfolio("Income", "Short-term")
        portfolio_balanced = Portfolio("Balanced", "Medium-term")
        self.portfolio_manager.add_portfolio(portfolio_income)
        self.portfolio_manager.add_portfolio(portfolio_balanced)
        self.assertIn(portfolio_income, self.portfolio_manager.portfolios)
        self.assertIn(portfolio_balanced, self.portfolio_manager.portfolios)

    @patch('matplotlib.pyplot.show')
    def test_provide_visualizations_showing_investment_performance_over_time(self, mock_show):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        investment = Investment("Stock A", "Equity", 1000.0, "2023-01-01")
        self.investment_manager.add_investment(investment)
        visualize_investments(self.investment_manager.investments)
        mock_show.assert_called_once()

    def test_generate_reports_on_investment_performance(self):
        # Functionalities 4: Generate Reports on Investment Performance
        investment = Investment("Stock A", "Equity", 1000.0, "2023-01-01")
        self.investment_manager.add_investment(investment)
        report = generate_report(self.investment_manager.investments)
        self.assertIn("Total Investment Amount: 1000.0", report)

    def test_set_investment_goals(self):
        # Functionalities 5: Set Investment Goals
        goal = Goal("Save $10,000", 10000.0, "2024-12-31")
        self.goal_manager.add_goal(goal)
        self.assertIn(goal, self.goal_manager.goals)

if __name__ == '__main__':
    unittest.main()
