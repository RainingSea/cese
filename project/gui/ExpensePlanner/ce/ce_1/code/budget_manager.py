class BudgetManager:
    def __init__(self):
        self.budget_goal = 0.0

    def set_budget(self, goal: float) -> None:
        self.budget_goal = goal

    def check_budget_status(self) -> str:
        return f"Current budget goal is: {self.budget_goal}"