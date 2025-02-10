class Preferences:
    def __init__(self, budget: str, activities: list, climate: str):
        self.budget = budget
        self.activities = activities
        self.climate = climate

    def save_preferences(self):
        pass  # Preferences are managed in main.py

    def load_preferences(self, username: str):
        return {'budget': self.budget, 'activities': self.activities, 'climate': self.climate}