import unittest
import os
from main import ActivityTracker, ExerciseLogger, SleepLogger, NutritionTracker, StressMonitor

class TestMedicalHealthTracker(unittest.TestCase):

    def setUp(self):
        # Initialize the trackers
        self.activity_tracker = ActivityTracker()
        self.exercise_logger = ExerciseLogger()
        self.sleep_logger = SleepLogger()
        self.nutrition_tracker = NutritionTracker()
        self.stress_monitor = StressMonitor()

    def test_input_daily_activities(self):
        # Functionalities 1: Input Daily Activities
        self.activity_tracker.add_activity("Walking", 30)
        self.activity_tracker.add_activity("Cooking", 45)
        
        # Check if activities are saved correctly
        self.assertEqual(len(self.activity_tracker.activities), 2)
        self.assertIn(("Walking", 30), self.activity_tracker.activities)
        self.assertIn(("Cooking", 45), self.activity_tracker.activities)

    def test_record_exercise_routines(self):
        # Functionalities 2: Record Exercise Routines
        self.exercise_logger.log_exercise("Running", 45)
        self.exercise_logger.log_exercise("Weightlifting", 60)

        # Check if exercises are saved correctly
        self.assertEqual(len(self.exercise_logger.exercises), 2)
        self.assertIn(("Running", 45), self.exercise_logger.exercises)
        self.assertIn(("Weightlifting", 60), self.exercise_logger.exercises)

    def test_log_sleep_patterns(self):
        # Functionalities 3: Log Sleep Patterns
        self.sleep_logger.log_sleep(480)  # 8 hours
        self.sleep_logger.log_sleep(420)  # 7 hours

        # Check if sleep records are saved correctly
        self.assertEqual(len(self.sleep_logger.sleep_records), 2)
        self.assertIn(480, self.sleep_logger.sleep_records)
        self.assertIn(420, self.sleep_logger.sleep_records)

    def test_track_nutrition_intake(self):
        # Functionalities 4: Track Nutrition Intake
        self.nutrition_tracker.track_nutrition("Apple", 95)
        self.nutrition_tracker.track_nutrition("Chicken", 250)

        # Check if nutrition entries are saved correctly
        self.assertEqual(len(self.nutrition_tracker.nutrition_entries), 2)
        self.assertIn(("Apple", 95), self.nutrition_tracker.nutrition_entries)
        self.assertIn(("Chicken", 250), self.nutrition_tracker.nutrition_entries)

    def test_monitor_stress_levels(self):
        # Functionalities 5: Monitor Stress Levels
        self.stress_monitor.monitor_stress(3)
        self.stress_monitor.monitor_stress(5)

        # Check if stress levels are saved correctly
        self.assertEqual(len(self.stress_monitor.stress_levels), 2)
        self.assertIn(3, self.stress_monitor.stress_levels)
        self.assertIn(5, self.stress_monitor.stress_levels)

    def test_provide_visualizations(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        # This functionality is not implemented in the codebase, so we will fail the test
        self.fail("Visualization functionality not implemented.")

if __name__ == '__main__':
    unittest.main()
