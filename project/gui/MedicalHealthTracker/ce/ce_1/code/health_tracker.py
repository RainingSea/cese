from daily_activities import DailyActivities
from exercise_routines import ExerciseRoutines
from sleep_patterns import SleepPatterns
from nutrition_intake import NutritionIntake
from stress_levels import StressLevels
from visualization import visualize_trends

class HealthTracker:
    def __init__(self):
        self.daily_activities = DailyActivities()
        self.exercise_routines = ExerciseRoutines()
        self.sleep_patterns = SleepPatterns()
        self.nutrition_intake = NutritionIntake()
        self.stress_levels = StressLevels()

    def input_daily_activity(self, activity: str):
        self.daily_activities.add_activity(activity)

    def record_exercise(self, routine: str):
        self.exercise_routines.add_routine(routine)

    def log_sleep_pattern(self, pattern: str):
        self.sleep_patterns.add_pattern(pattern)

    def track_nutrition(self, nutrition: str):
        self.nutrition_intake.add_nutrition(nutrition)

    def monitor_stress(self, level: str):
        self.stress_levels.add_stress(level)

    def visualize_trends(self):
        visualize_trends()