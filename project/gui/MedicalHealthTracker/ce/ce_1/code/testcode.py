import unittest
import os
from daily_activities import DailyActivities
from exercise_routines import ExerciseRoutines
from sleep_patterns import SleepPatterns
from nutrition_intake import NutritionIntake
from stress_levels import StressLevels
from visualization import visualize_trends

class TestMedicalHealthTracker(unittest.TestCase):

    def setUp(self):
        # Set up the test environment
        self.daily_activities = DailyActivities()
        self.exercise_routines = ExerciseRoutines()
        self.sleep_patterns = SleepPatterns()
        self.nutrition_intake = NutritionIntake()
        self.stress_levels = StressLevels()

        # Clear the contents of the files before each test
        open(self.daily_activities.file_path, 'w').close()
        open(self.exercise_routines.file_path, 'w').close()
        open(self.sleep_patterns.file_path, 'w').close()
        open(self.nutrition_intake.file_path, 'w').close()
        open(self.stress_levels.file_path, 'w').close()

    def test_input_daily_activities(self):
        # Functionalities 1: Input Daily Activities
        activity = "Walking for 30 minutes"
        self.daily_activities.add_activity(activity)
        activities = self.daily_activities.load_activities()
        self.assertIn(activity, activities)

    def test_record_exercise_routines(self):
        # Functionalities 2: Record Exercise Routines
        routine = "Running for 30 minutes at moderate intensity"
        self.exercise_routines.add_routine(routine)
        routines = self.exercise_routines.load_routines()
        self.assertIn(routine, routines)

    def test_log_sleep_patterns(self):
        # Functionalities 3: Log Sleep Patterns
        pattern = "10:00 PM to 6:00 AM"
        self.sleep_patterns.add_pattern(pattern)
        patterns = self.sleep_patterns.load_patterns()
        self.assertIn(pattern, patterns)

    def test_track_nutrition_intake(self):
        # Functionalities 4: Track Nutrition Intake
        nutrition = "Breakfast: Oatmeal, 150 calories"
        self.nutrition_intake.add_nutrition(nutrition)
        nutrition_log = self.nutrition_intake.load_nutrition()
        self.assertIn(nutrition, nutrition_log)

    def test_monitor_stress_levels(self):
        # Functionalities 5: Monitor Stress Levels
        stress_level = "Stress Level: 5, Feeling anxious"
        self.stress_levels.add_stress(stress_level)
        stress_log = self.stress_levels.load_stress()
        self.assertIn(stress_level, stress_log)

    def test_provide_visualizations_for_health_trends_analysis(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        try:
            visualize_trends()
            self.assertTrue(True)  # If no exception, the test passes
        except Exception as e:
            self.fail(f"Visualization failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
