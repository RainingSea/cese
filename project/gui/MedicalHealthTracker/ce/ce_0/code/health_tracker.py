import numpy as np

class HealthTracker:
    def __init__(self):
        self.activities = []
        self.exercise = []
        self.sleep = []
        self.nutrition = []
        self.stress = []
        self.load_data()

    def log_activity(self, activity: str) -> None:
        self.activities.append(activity)
        self.save_data()

    def log_exercise(self, exercise: str) -> None:
        self.exercise.append(exercise)
        self.save_data()

    def log_sleep(self, sleep: str) -> None:
        self.sleep.append(sleep)
        self.save_data()

    def log_nutrition(self, nutrition: str) -> None:
        self.nutrition.append(nutrition)
        self.save_data()

    def log_stress(self, stress: str) -> None:
        self.stress.append(stress)
        self.save_data()

    def visualize_trends(self) -> None:
        # This method would typically create visualizations based on the data.
        # For simplicity, we will just print the data here.
        print("Activities:", self.activities)
        print("Exercise:", self.exercise)
        print("Sleep:", self.sleep)
        print("Nutrition:", self.nutrition)
        print("Stress:", self.stress)

    def load_data(self) -> None:
        try:
            with open('activities.txt', 'r') as f:
                self.activities = f.read().splitlines()
            with open('exercise.txt', 'r') as f:
                self.exercise = f.read().splitlines()
            with open('sleep.txt', 'r') as f:
                self.sleep = f.read().splitlines()
            with open('nutrition.txt', 'r') as f:
                self.nutrition = f.read().splitlines()
            with open('stress.txt', 'r') as f:
                self.stress = f.read().splitlines()
        except FileNotFoundError:
            pass  # If the files do not exist, we start with empty lists

    def save_data(self) -> None:
        with open('activities.txt', 'w') as f:
            f.write('\n'.join(self.activities))
        with open('exercise.txt', 'w') as f:
            f.write('\n'.join(self.exercise))
        with open('sleep.txt', 'w') as f:
            f.write('\n'.join(self.sleep))
        with open('nutrition.txt', 'w') as f:
            f.write('\n'.join(self.nutrition))
        with open('stress.txt', 'w') as f:
            f.write('\n'.join(self.stress))