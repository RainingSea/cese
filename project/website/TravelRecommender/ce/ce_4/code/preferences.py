class Preferences:
    def __init__(self, budget: float, activities: list, climate: str):
        self.budget = budget
        self.activities = activities
        self.climate = climate

    def save(self) -> None:
        with open('preferences.txt', 'a') as f:
            activities_str = ','.join(self.activities)
            f.write(f"{self.budget}|{activities_str}|{self.climate}\n")

    @staticmethod
    def load() -> 'Preferences':
        with open('preferences.txt', 'r') as f:
            last_line = f.readlines()[-1].strip()
            budget, activities_str, climate = last_line.split('|')
            activities = activities_str.split(',')
            return Preferences(float(budget), activities, climate)