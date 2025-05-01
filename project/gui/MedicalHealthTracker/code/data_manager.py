import os

class DataManager:
    def __init__(self):
        self.daily_activities_file = 'daily_activities.txt'
        self.exercise_routines_file = 'exercise_routines.txt'
        self.sleep_patterns_file = 'sleep_patterns.txt'
        self.nutrition_intake_file = 'nutrition_intake.txt'
        self.stress_levels_file = 'stress_levels.txt'
        self.daily_activities = []
        self.exercise_routines = []
        self.sleep_patterns = []
        self.nutrition_intake = []
        self.stress_levels = []

    def load_data(self):
        self.daily_activities = self._load_file(self.daily_activities_file)
        self.exercise_routines = self._load_file(self.exercise_routines_file)
        self.sleep_patterns = self._load_file(self.sleep_patterns_file)
        self.nutrition_intake = self._load_file(self.nutrition_intake_file)
        self.stress_levels = self._load_file(self.stress_levels_file)

    def _load_file(self, filename):
        if not os.path.exists(filename):
            open(filename, 'w').close()  # Create the file if it does not exist
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_daily_activity(self, data: str):
        self._save_data(self.daily_activities_file, data)
        self.daily_activities.append(data)

    def save_exercise_routine(self, data: str):
        self._save_data(self.exercise_routines_file, data)
        self.exercise_routines.append(data)

    def save_sleep_pattern(self, data: str):
        self._save_data(self.sleep_patterns_file, data)
        self.sleep_patterns.append(data)

    def save_nutrition_intake(self, data: str):
        self._save_data(self.nutrition_intake_file, data)
        self.nutrition_intake.append(data)

    def save_stress_level(self, data: str):
        self._save_data(self.stress_levels_file, data)
        self.stress_levels.append(data)

    def _save_data(self, filename: str, data: str):
        with open(filename, 'a') as file:
            file.write(data + '\n')