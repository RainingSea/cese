class Preferences:
    def __init__(self, budget: float, activities: list, climate: str):
        self.budget = budget
        self.activities = activities
        self.climate = climate

    def save_preferences(self):
        with open('preferences.txt', 'a') as file:
            activities_str = ','.join(self.activities)
            file.write(f"{self.budget}|{activities_str}|{self.climate}\n")

    @staticmethod
    def load_preferences():
        preferences = []
        try:
            with open('preferences.txt', 'r') as file:
                for line in file:
                    budget, activities_str, climate = line.strip().split('|')
                    activities = activities_str.split(',')
                    preferences.append(Preferences(float(budget), activities, climate))
        except FileNotFoundError:
            pass
        return preferences