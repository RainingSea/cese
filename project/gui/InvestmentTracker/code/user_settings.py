import os

class Goal:
    def __init__(self, description: str, target_amount: float):
        self.description = description
        self.target_amount = target_amount

class UserSettings:
    def __init__(self):
        self.goals = []
        self.load_settings()

    def load_settings(self):
        if os.path.exists('user_settings.txt'):
            with open('user_settings.txt', 'r') as file:
                for line in file:
                    description, target_amount = line.strip().split('|')
                    self.goals.append(Goal(description, float(target_amount)))

    def save_settings(self):
        with open('user_settings.txt', 'w') as file:
            for goal in self.goals:
                file.write(f"{goal.description}|{goal.target_amount}\n")