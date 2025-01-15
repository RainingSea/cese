class Preferences:
    def __init__(self, budget: float, activities: list, climate: str):
        self.budget = budget
        self.activities = activities
        self.climate = climate

    def save(self):
        with open('preferences.txt', 'a') as file:
            activities_str = ','.join(self.activities)
            file.write(f"{self.budget}|{activities_str}|{self.climate}\n")