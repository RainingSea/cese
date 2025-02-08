import os

class DataManager:
    def __init__(self, activities_file: str, exercise_file: str, sleep_file: str, nutrition_file: str, stress_file: str) -> None:
        self.activities_file = activities_file
        self.exercise_file = exercise_file
        self.sleep_file = sleep_file
        self.nutrition_file = nutrition_file
        self.stress_file = stress_file

    def save_activity(self, activity: str) -> None:
        with open(self.activities_file, 'a') as file:
            file.write(activity + '\n')

    def save_exercise(self, exercise: str) -> None:
        with open(self.exercise_file, 'a') as file:
            file.write(exercise + '\n')

    def save_sleep(self, sleep: str) -> None:
        with open(self.sleep_file, 'a') as file:
            file.write(sleep + '\n')

    def save_nutrition(self, nutrition: str) -> None:
        with open(self.nutrition_file, 'a') as file:
            file.write(nutrition + '\n')

    def save_stress(self, stress: str) -> None:
        with open(self.stress_file, 'a') as file:
            file.write(stress + '\n')

    def load_activities(self) -> list:
        if not os.path.exists(self.activities_file):
            return []
        with open(self.activities_file, 'r') as file:
            return file.read().strip().split('\n')

    def load_exercises(self) -> list:
        if not os.path.exists(self.exercise_file):
            return []
        with open(self.exercise_file, 'r') as file:
            return file.read().strip().split('\n')

    def load_sleep(self) -> list:
        if not os.path.exists(self.sleep_file):
            return []
        with open(self.sleep_file, 'r') as file:
            return file.read().strip().split('\n')

    def load_nutrition(self) -> list:
        if not os.path.exists(self.nutrition_file):
            return []
        with open(self.nutrition_file, 'r') as file:
            return file.read().strip().split('\n')

    def load_stress(self) -> list:
        if not os.path.exists(self.stress_file):
            return []
        with open(self.stress_file, 'r') as file:
            return file.read().strip().split('\n')