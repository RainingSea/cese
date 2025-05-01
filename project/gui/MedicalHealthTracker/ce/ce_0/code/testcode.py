import unittest
import os

# Assuming the HealthTracker class is imported from main.py
from main import HealthTracker

class TestHealthTracker(unittest.TestCase):

    def setUp(self):
        self.health_tracker = HealthTracker()
        # Clear the log files before each test
        self.clear_log_files()

    def clear_log_files(self):
        log_files = [
            "daily_activities.txt",
            "exercise_routines.txt",
            "sleep_patterns.txt",
            "nutrition_intake.txt",
            "stress_levels.txt"
        ]
        for log_file in log_files:
            if os.path.exists(log_file):
                os.remove(log_file)

    def test_log_activity(self):
        # Functionalities 1: Input Daily Activities
        self.health_tracker.log_activity("Walked for 30 minutes")
        self.health_tracker.log_activity("Read a book for 1 hour")
        
        with open("daily_activities.txt", "r") as file:
            activities = file.readlines()
        
        self.assertIn("Walked for 30 minutes\n", activities)
        self.assertIn("Read a book for 1 hour\n", activities)

    def test_log_exercise(self):
        # Functionalities 2: Record Exercise Routines
        self.health_tracker.log_exercise("Jogged for 30 minutes")
        self.health_tracker.log_exercise("Lifted weights for 45 minutes")
        
        with open("exercise_routines.txt", "r") as file:
            exercises = file.readlines()
        
        self.assertIn("Jogged for 30 minutes\n", exercises)
        self.assertIn("Lifted weights for 45 minutes\n", exercises)

    def test_log_sleep(self):
        # Functionalities 3: Log Sleep Patterns
        self.health_tracker.log_sleep("Slept for 8 hours")
        self.health_tracker.log_sleep("Slept for 7 hours")
        
        with open("sleep_patterns.txt", "r") as file:
            sleep_patterns = file.readlines()
        
        self.assertIn("Slept for 8 hours\n", sleep_patterns)
        self.assertIn("Slept for 7 hours\n", sleep_patterns)

    def test_log_nutrition(self):
        # Functionalities 4: Track Nutrition Intake
        self.health_tracker.log_nutrition("Ate a salad for lunch")
        self.health_tracker.log_nutrition("Had oatmeal for breakfast")
        
        with open("nutrition_intake.txt", "r") as file:
            nutrition_entries = file.readlines()
        
        self.assertIn("Ate a salad for lunch\n", nutrition_entries)
        self.assertIn("Had oatmeal for breakfast\n", nutrition_entries)

    def test_log_stress(self):
        # Functionalities 5: Monitor Stress Levels
        self.health_tracker.log_stress("Stress level: 4")
        self.health_tracker.log_stress("Stress level: 6")
        
        with open("stress_levels.txt", "r") as file:
            stress_levels = file.readlines()
        
        self.assertIn("Stress level: 4\n", stress_levels)
        self.assertIn("Stress level: 6\n", stress_levels)

    def test_generate_visualizations(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        # This test will not check the actual visualization but will ensure no errors occur
        try:
            self.health_tracker.generate_visualizations()
        except Exception as e:
            self.fail(f"generate_visualizations raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
