import os

class HealthTracker:
    def __init__(self, data_directory: str):
        self.data_directory = data_directory
        self.daily_activities_file = os.path.join(data_directory, 'daily_activities.txt')
        self.exercise_routines_file = os.path.join(data_directory, 'exercise_routines.txt')
        self.sleep_patterns_file = os.path.join(data_directory, 'sleep_patterns.txt')
        self.nutrition_intake_file = os.path.join(data_directory, 'nutrition_intake.txt')
        self.stress_levels_file = os.path.join(data_directory, 'stress_levels.txt')

    def input_daily_activity(self, activity: str) -> None:
        with open(self.daily_activities_file, 'a') as file:
            file.write(activity + '\n')

    def input_exercise_routine(self, exercise: str) -> None:
        with open(self.exercise_routines_file, 'a') as file:
            file.write(exercise + '\n')

    def log_sleep_pattern(self, sleep_data: str) -> None:
        with open(self.sleep_patterns_file, 'a') as file:
            file.write(sleep_data + '\n')

    def track_nutrition(self, nutrition_data: str) -> None:
        with open(self.nutrition_intake_file, 'a') as file:
            file.write(nutrition_data + '\n')

    def monitor_stress_level(self, stress_data: str) -> None:
        with open(self.stress_levels_file, 'a') as file:
            file.write(stress_data + '\n')

    def visualize_health_trends(self) -> None:
        # Placeholder for visualization logic using matplotlib
        print("Visualizing health trends...")