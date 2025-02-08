import os

class Goal:
    def __init__(self, description: str, target_amount: float, target_date: str):
        self.description = description
        self.target_amount = target_amount
        self.target_date = target_date

class GoalManager:
    def __init__(self):
        self.goals = []

    def add_goal(self, goal: Goal):
        self.goals.append(goal)
        self.save_goals()

    def load_goals(self):
        if os.path.exists('goals.txt'):
            with open('goals.txt', 'r') as file:
                for line in file:
                    description, target_amount, target_date = line.strip().split('|')
                    self.goals.append(Goal(description, float(target_amount), target_date))

    def save_goals(self):
        with open('goals.txt', 'w') as file:
            for goal in self.goals:
                file.write(f"{goal.description}|{goal.target_amount}|{goal.target_date}\n")