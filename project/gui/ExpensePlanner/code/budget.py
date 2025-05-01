class BudgetManager:
    def __init__(self):
        self.budget_goal = 0.0

    def set_budget_goal(self, goal: float) -> None:
        self.budget_goal = goal

    def track_spending(self, expenses) -> float:
        total_spent = sum(expense.amount for expense in expenses)
        return self.budget_goal - total_spent